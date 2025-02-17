import json, requests, os
from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import pandas as pd

default_args = {
    "owner" : "skill-gap",
    "start_date" : days_ago(1)
}

POSTGRES_CONN_ID = "postgres_default"
API_CONN_ID = "open_meteo_api"

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
        return file

    sample_data = extract_data()