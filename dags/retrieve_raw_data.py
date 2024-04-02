import os
from airflow import DAG
import pendulum
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from us_weather_alerts import api , load_to_bigquery

KEYFILE_PATH = os.getenv("SERVICE_ACCOUNT_KEYFILE")
ALERTS_BRONZE_TABLE_ID = f"{os.getenv('BRONZE_DATASET')}.alerts"
BUCKET_NAME = os.getenv("US_WEATHER_AlERTS_BUCKET")

def fetch_and_push_alerts_to_gcs():
    """
    Fetches alerts data and pushes it to Google Cloud Storage (GCS).
    """
    # API request parameters
    LIMIT = 500
    start_datetime = datetime(2024, 1, 1, 1, 0, 0, 1)
    features = api.scrape_alerts(
        status="actual", region_type="land", start_datetime=start_datetime, limit=LIMIT
    )
    df = api.parse_features(features)
    api.upload_to_gcs_from_memory(df, BUCKET_NAME, KEYFILE_PATH)



def load_most_recent_file_from_gcs_to_bigquery():
    """
    Loads the most recent file from Google Cloud Storage (GCS) to BigQuery alerts table.
    """
    load_to_bigquery.transfer_recent_file_to_bigquery(
        BUCKET_NAME, ALERTS_BRONZE_TABLE_ID, KEYFILE_PATH
    )

default_args = {
    'depends_on_past': True,
    'start_date': pendulum.today("UTC").add(days=-1)
}

with DAG('load_alerts_data_bronze_dataset',
         default_args=default_args,
         catchup=False,
         schedule_interval="@hourly") as dag:

    fetch_and_push_alerts_to_gcs = PythonOperator(
        task_id='fetch_and_push_alerts_to_gcs',
        python_callable=fetch_and_push_alerts_to_gcs
    )

    load_most_recent_file_from_gcs_to_bigquery = PythonOperator(
        task_id='load_most_recent_file_from_gcs_to_bigquery',
        python_callable=load_most_recent_file_from_gcs_to_bigquery
    )

fetch_and_push_alerts_to_gcs >> load_most_recent_file_from_gcs_to_bigquery
