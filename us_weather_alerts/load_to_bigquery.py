from google.cloud import bigquery
import json
import os
from google.oauth2 import service_account
from datetime import datetime, timezone
from google.cloud import storage

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def gcs_recent_file(key_file_path, bucket_name):

    folder_path = "us_weather_alerts"

    # Create credentials from service account key file
    credentials = service_account.Credentials.from_service_account_file(key_file_path)

    # Create storage client with provided credentials
    storage_client = storage.Client(credentials=credentials)

    # List objects in the specified folder in the bucket
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)

    most_recent_file = None
    most_recent_timestamp = datetime.min

    for blob in blobs:
        file_name = os.path.basename(blob.name)
        timestamp = datetime.strptime(file_name, "%Y-%m-%d_%H-%M-%S")

        if timestamp > most_recent_timestamp:
            print(most_recent_timestamp)
            most_recent_timestamp = timestamp
            most_recent_file = blob.name

    return most_recent_file


def load_to_bigquery(bucket_name , most_recent_file , gcp_project_id ,keyfile_path):

 credentials = service_account.Credentials.from_service_account_file(keyfile_path)

 client = bigquery.Client(credentials=credentials)

 table_id = f"{gcp_project_id}.{os.environ['BRONZE_DATASET']}.alerts"

 # Read schema from JSON file
 with open(f"{CURRENT_DIR}/schemas/alerts.json") as f:
    schema_json = json.load(f)

 # Define BigQuery table schema
 schema = []
 for field in schema_json:
    schema.append(bigquery.SchemaField(field['name'], field['type'],field['mode']))

 job_config = bigquery.LoadJobConfig(
    schema=schema,
    skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.CSV
 )

 uri = f"gs://{bucket_name}/{most_recent_file}"

 load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
 )

 load_job.result()

 destination_table = client.get_table(table_id)
 print("Loaded {} rows.".format(destination_table.num_rows))


if __name__ == "__main__":

    # GCP upload parameters
    keyfile_path = os.environ["SERVICE_ACCOUNT_KEYFILE"]

    #GCS parameters
    bucket_name = os.environ["US_WEATHER_AlERTS_BUCKET"]

    #Bigquery
    table_id = f"{os.environ['BRONZE_DATASET']}.alerts"

    gcp_project_id = os.environ["GCP_PROJECT_ID"]

    most_recent_file = gcs_recent_file(keyfile_path, bucket_name)

    load_to_bigquery(bucket_name, most_recent_file ,gcp_project_id ,keyfile_path)
