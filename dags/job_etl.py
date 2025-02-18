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

default_args = {
    "owner" : "skill-gap",
    "start_date" : days_ago(1)
}

POSTGRES_CONN_ID = Variable.get("POSTGRES_CONN_ID")

with DAG(
    dag_id="skill_gap_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    @task
    def extract_data():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'resources', 'sample_data.json')
        file = pd.read_json(file_path)
        logger.info("File successfully read")
        return file

    @task
    def load(data):
        try:
            logger.info("Connecting to postgres")
            postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
            conn = postgres_hook.get_conn()
            cursor = conn.cursor()

            logger.info("Connection successful")
            logger.info("Loading data to postgres")
            for record in data.to_dict(orient="records"):
                job_title = record['job_title'].strip()
                skills = record['skills']

                # Insert job title
                cursor.execute("""
                    INSERT INTO job_titles (job_title)
                    VALUES (%s)
                    ON CONFLICT (job_title) DO NOTHING
                    RETURNING id;
                """, (job_title,))

                result = cursor.fetchone()
                if result:
                    job_title_id = result[0]
                else:
                    # If there was a conflict (job title already exists), get its ID
                    cursor.execute("""
                        SELECT id FROM job_titles WHERE job_title = %s;
                    """, (job_title,))
                    job_title_id = cursor.fetchone()[0]

                # Insert skills with explicit reference to the unique constraint
                for skill in skills:
                    cursor.execute("""
                        INSERT INTO skills (job_title_id, skill)
                        VALUES (%s, %s)
                        ON CONFLICT ON CONSTRAINT unique_job_skill DO NOTHING;
                    """, (job_title_id, skill))
                conn.commit()
                logger.info("Data loaded to postgres")
        except Exception as e:
            logger.error(f"Failed to load data into postgres\nTraceback: {e}")

    sample_data = extract_data()
    load(sample_data)