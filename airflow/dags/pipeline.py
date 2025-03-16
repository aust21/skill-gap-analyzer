import json, requests, os
from airflow import DAG
from airflow.decorators import task
from airflow.exceptions import AirflowException
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import pandas as pd
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from pendulum import duration

import tasks

logger = LoggingMixin().log

default_args = {
    "owner" : "skill-gap",
    "start_date" : days_ago(1),
    "retries": 3,
    "retry_delay": duration(seconds=2),
    "retry_exponential_backoff": True,
    "max_retry_delay": duration(hours=2),
}

# POSTGRES_CONN_ID = Variable.get("POSTGRES_CONN_ID")

with DAG(
    dag_id="skill_gap_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False
) as dag:

    task_1 = PythonOperator(
        task_id="extract_data",
        python_callable=tasks.extract_data,
        provide_context=True
    )

    task_2 = PythonOperator(
        task_id="load_to_redis",
        python_callable=tasks.load_with_xcom,
        provide_context=True
    )

    task_3 = PythonOperator(
        task_id="load_to_postgres",
        python_callable=tasks.load_to_postgres,
    )

    task_1 >> task_2 >> task_3