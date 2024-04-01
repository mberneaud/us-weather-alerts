import os

from airflow import DAG

import pendulum
from airflow.operators.bash import BashOperator


from us_weather_alerts import api , load_to_bigquery


def fetch_and_push_alerts_to_gcs():
    """
    Fetches alerts data and pushes it to Google Cloud Storage (GCS).
    """
    # Your code to fetch alerts data and push to GCS goes here
    pass


def load_most_recent_file_from_gcs_to_bigquery():
    """
    Loads the most recent file from Google Cloud Storage (GCS) to BigQuery alerts table.
    """
    # Your code to load the most recent file from GCS to BigQuery bronze table goes here
    pass
