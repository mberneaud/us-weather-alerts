import os

from airflow import DAG


import pendulum

from airflow.operators.bash import BashOperator


DBT_DIR = os.getenv("DBT_DIR")


with DAG(
    "dbt_basics",
    default_args={ "depends_on_past": False, },
    start_date=pendulum.today("UTC").add(days=-1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    dbt_run_silver_model = BashOperator(
        task_id="dbt_run_silver_model",
        bash_command= f"cd /app/airflow && poetry install --no-root &&  poetry run dbt run --project-dir {DBT_DIR} --models silver --target silver",
    )
dbt_run_silver_model
