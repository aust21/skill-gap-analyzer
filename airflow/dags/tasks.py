import json, requests, os
from airflow import DAG
from airflow.decorators import task
from airflow.exceptions import AirflowException
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.models import Variable

logger = LoggingMixin().log

def extract_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'resources', 'sample_data.json')
    file = pd.read_json(file_path)
    logger.info("File successfully read")
    return file

def load_to_redis(data):
    pass

def load(data):
    try:
        logger.info("Connecting to postgres")
        postgres_hook = PostgresHook(postgres_conn_id="POSTGRES_CONN_ID")
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        logger.info("Connection successful")

        # prefetch job titles to avoid duplicates
        cursor.execute("SELECT id, job_title FROM job_titles;")

        # Get all rows
        rows = cursor.fetchall()
        existing_jobs = {row[1]: row[0] for row in rows} if rows else {}

        # prepare to insert new jobs
        new_jobs = [job.strip() for job in data["job_title"] if job
                    not in
                    existing_jobs]

        logger.info("Inserting new jobs")
        if new_jobs:
            cursor.executemany(
                "INSERT INTO job_titles (job_title) VALUES (%s) "
                "ON CONFLICT (job_title) DO NOTHING RETURNING id, "
                "job_title;", [(job,) for job in new_jobs]
            )

            # Store new job title IDs
            inserted_rows = []
            if cursor.description is not None:
                inserted_rows = cursor.fetchall()

            for row in inserted_rows:
                existing_jobs[row[1]] = row[0]

        logger.info("Preparing skill insert")
        # prepare skill insert
        skill_record = []
        for record in data.to_dict(orient="records"):
            title = record["job_title"]
            job_title_id = existing_jobs.get(title.strip())
            if not job_title_id:
                continue
            skill_record.extend([(job_title_id, skill) for skill in
                                 record["skills"]])
        if skill_record:
            cursor.executemany(
                "INSERT INTO job_skills (job_title_id, skill) VALUES (%s, "
                "%s) "
                "ON CONFLICT ON CONSTRAINT unique_job_skill DO NOTHING;", skill_record
            )
        conn.commit()

    except Exception as e:
        logger.error(f"Failed to load data into postgres\nTraceback: {e}")
    finally:
        logger.info("Data loading operation complete")


def load_with_xcom(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids="extract_data")

    if transformed_data is None:
        raise ValueError("No transformed data found in XCom.")

    load_to_redis(transformed_data)