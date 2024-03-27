from google.cloud import bigquery
import json
import os
from google.oauth2 import service_account

def load_to_bigquery():

 keyfile_path = os.environ["SERVICE_ACCOUNT_KEYFILE"]

 credentials = service_account.Credentials.from_service_account_file(keyfile_path)

 client = bigquery.Client(credentials=credentials)

 # TODO(developer): Set table_id to the ID of the table to create.
 # table_id = "your-project.your_dataset.your_table_name"
 table_id = f"{os.environ['BRONZE_DATASET']}.alerts"

 # Read schema from JSON file
 with open('schemas/alerts.json') as f:
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
 uri = "gs://us_weather_alerts/us_weather_alerts/2024_03_26"

 load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
 )

 load_job.result()

 destination_table = client.get_table(table_id)
 print("Loaded {} rows.".format(destination_table.num_rows))
