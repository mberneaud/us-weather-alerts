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

'''
    dbt_run_operator = DbtRunOperator(
    task_id='dbt_run_silver_model',
    dir=DBT_DIR,  # Path to your dbt project directory
    profiles_dir=None,  # Path to your dbt profiles directory, if needed
    profiles=None,  # Profile name from profiles.yml to use, if needed
    target='silver',  # Target name to use, if needed
    select='silver',  # Name of the selection in your dbt project
    dag=dag,
)
'''
dbt_run_silver_model
