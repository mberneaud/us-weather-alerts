import os

from airflow import DAG

# $IMPORT_BEGIN
# noreorder
import pendulum

from airflow.operators.bash import BashOperator

# $IMPORT_END


DBT_DIR = os.getenv("DBT_DIR")


with DAG(
    "dbt_basics",
    # $CODE_BEGIN
    default_args={ "depends_on_past": True, },
    start_date=pendulum.today("UTC").add(days=-1),
    schedule_interval="@daily",
    catchup=False,
    # $CODE_END
) as dag:
    # $CHA_BEGIN
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"dbt run --project-dir {DBT_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"dbt test --project-dir {DBT_DIR}",
    )

    dbt_run >> dbt_test
    # $CHA_END

