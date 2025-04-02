import json
import os

import numpy as np
import pandas as pd
import redis
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.log.logging_mixin import LoggingMixin
from sqlalchemy import text
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

conf = {
    'host': Variable.get("HOST", default_var=None),
    'port': Variable.get("PORT", default_var=None),
    'database': Variable.get("DB", default_var=None),
    'user': Variable.get("USER", default_var=None),
    'password': Variable.get("PASSWORD", default_var=None)
}

logger = LoggingMixin().log

def extract_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'resources', 'sample_data.json')
    file = pd.read_json(file_path)
    logger.info("File successfully read")
    return file

def load_to_redis(data):
    conn = BaseHook.get_connection("redis")

    try:
        pool = redis.ConnectionPool(
            host=conn.host, port=conn.port,
            decode_responses=True,
            password=Variable.get("REDIS_PASSWORD"),
            username="default"
        )

        r = redis.Redis(connection_pool=pool)

        with r.pipeline() as pipe:
            for indx, row in data.iterrows():
                for key, value in row.items():
                    if isinstance(value, np.ndarray):
                        row[key] = value.tolist()
                row = row.to_dict()
                key = f"sk:{row['job_title']}"
                if r.get(key):
                    continue
                pipe.set(key, json.dumps(row))
            pipe.execute()
    except Exception as e:
        logger.error(f"Something went wrong with redis: {e}", exc_info=True)
    finally:
        pool.close()


def load_to_postgres():
    try:
        logger.info("Connecting to postgres")
        # Redis connection
        conn = BaseHook.get_connection("redis")
        pool = redis.ConnectionPool(
            host=conn.host,
            port=conn.port,
            decode_responses=True,
            password=Variable.get("REDIS_PASSWORD"),
            username="default"
        )
        r = redis.Redis(connection_pool=pool)

        # Postgres connection
        postgres_hook = PostgresHook(postgres_conn_id="POSTGRES_CONN_ID")
        pg_conn = postgres_hook.get_conn()
        cursor = pg_conn.cursor()
        logger.info("Connection successful")

        # Prefetch job titles to avoid duplicates
        cursor.execute("SELECT id, job_title FROM job_titles;")
        rows = cursor.fetchall()
        existing_jobs = {row[1]: row[0] for row in rows} if rows else {}

        # Prepare to collect new jobs and skills
        new_jobs = set()
        skill_records = []

        # Process Redis data
        for key in r.scan_iter(match="sk:*"):
            row = json.loads(r.get(key))

            # Extract job title and skills from Redis data
            job_title = row.get("job_title", "").strip()
            skills = row.get("skills", [])

            if job_title and job_title not in existing_jobs:
                new_jobs.add(job_title)

        # Insert new jobs
        logger.info(f"Inserting {len(new_jobs)} new jobs")
        if new_jobs:
            for job in new_jobs:
                cursor.execute(
                    "INSERT INTO job_titles (job_title) VALUES (%s) "
                    "ON CONFLICT (job_title) DO NOTHING RETURNING id, job_title;",
                    (job,)
                )
                # Store new job title IDs
                if cursor.description is not None:
                    inserted_row = cursor.fetchone()
                    if inserted_row:
                        existing_jobs[inserted_row[1]] = inserted_row[0]

        # Process skills after jobs are inserted
        logger.info("Preparing skill insert")
        for key in r.scan_iter(match="sk:*"):
            row = json.loads(r.get(key))

            job_title = row.get("job_title", "").strip()
            skills = row.get("skills", [])

            job_title_id = existing_jobs.get(job_title)
            if not job_title_id:
                continue

            for skill in skills:
                skill_records.append((job_title_id, skill))

        # Insert skills in batches
        if skill_records:
            batch_size = 1000
            for i in range(0, len(skill_records), batch_size):
                batch = skill_records[i:i + batch_size]
                cursor.executemany(
                    "INSERT INTO job_skills (job_title_id, skill) VALUES (%s, %s) "
                    "ON CONFLICT ON CONSTRAINT unique_job_skill DO NOTHING;",
                    batch
                )
                logger.info(f"Inserted batch of {len(batch)} skills")

        pg_conn.commit()
        logger.info(f"Successfully inserted {len(skill_records)} skill records")

    except Exception as e:
        logger.error(f"Failed to load data into postgres\nTraceback: {e}")
        if 'pg_conn' in locals():
            pg_conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'pg_conn' in locals():
            pg_conn.close()
        if 'r' in locals():
            r.close()
        logger.info("Data loading operation complete")


def load_with_xcom(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids="extract_data")

    if transformed_data is None:
        raise ValueError("No transformed data found in XCom.")

    load_to_redis(transformed_data)