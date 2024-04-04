""""
Functions for accessing the National Weather Service API
Created: 19.03.204
Author: Malte Berneaud
"""

import pandas as pd
import requests
from google.oauth2 import service_account
import pandas_gbq
import os
#TODO: make asynchronous
from datetime import datetime, timezone
from typing import List, Dict
from google.cloud import storage



def scrape_alerts(status: str, region_type: str, start_datetime: datetime, end_datetime: datetime = datetime.now(), limit: int = 500) -> List[Dict]:
    """Scrapes alerts for the specified timeframe and status and returns a list of dictionaries, where each dictionary represents
    an alert (called Feature in the API response)

    datetime needs to be parsed as a datetime.datetime object.
    """
    # Format for parsing datetime
    dt_format = "%Y-%m-%dT%H:%M:%SZ"
    start = start_datetime.astimezone(timezone.utc).strftime(dt_format)
    end = end_datetime.astimezone(timezone.utc).strftime(dt_format)

    base_url = "https://api.weather.gov/alerts"
    params = {"limit": limit,
          "start": start,
          "end": end,
          "status": status,
          "region_type": region_type}

    features = []

    response = requests.get(base_url, params=params).json()
    if response["features"] == []:
        raise KeyError("No alerts found for the specified parameters. Try a longer time span, a different status or changing other parameters.")

    features.append(response["features"][0])

    while True:
        try:
            next = response["pagination"]["next"]
            print(f"Sending follow-up request to {next}")
            response = requests.get(next).json()

            # TODO: parse the response to keep only important data inside

            features.append(response["features"][0])
        except:
            print("No further pagination URL found")
            break

    return features

def parse_features(features: List[Dict]) -> pd.DataFrame:
    """Takes the list of dictionaries returned from the scrape_api function and
    parses only relevant features, which are then returned as a Pandas data frame"""

    out_list = []
    for feature in features:
        parsed_features = {
            "id": feature["id"],
            "geocode": feature["properties"]["geocode"]["SAME"],
            # Note sure what SAME stands for, but can be mapped to FIPS
            # in the zone county correlation file.
            "type": feature["properties"]["messageType"],
            "sent": feature["properties"]["sent"],
            "effective": feature["properties"]["effective"],
            "expires": feature["properties"]["expires"],
            "status": feature["properties"]["status"],
            "category": feature["properties"]["category"],
            "severity": feature["properties"]["severity"],
            "certainty": feature["properties"]["certainty"],
            "urgency": feature["properties"]["urgency"],
            "event": feature["properties"]["event"],
            "headline": feature["properties"]["headline"],
            "description": feature["properties"]["description"],
            "instruction": feature["properties"]["instruction"]

        }
        out_list.append(parsed_features)

    # converting list of dicts to dataframe and returning
    df = pd.DataFrame(out_list)
    df = df.astype(str)

    return df


def upload_to_gcp(dataframe: pd.DataFrame, project_id: str, table_id, keyfile_path: str) -> None:
    """Uploads the dataframe to a Google Cloud Platform BigQuery table.

    Set project_id to your Google Cloud Platform project ID.
    project_id = "my-project
    Set table_id to the full destination table ID (including the dataset ID).
    table_id = 'my_dataset.my_table'

    Credentials are read from a service account keyfile, which should be stored
    in the same place as your Le Wagon Keyfile and referenced with it's absolute path.
    Put the path to the keyfile in the .env file
    """
    credentials = service_account.Credentials.from_service_account_file(keyfile_path)

    pandas_gbq.to_gbq(dataframe, table_id, project_id=project_id, if_exists="append", credentials=credentials)


def upload_to_gcs_from_memory(dataframe: pd.DataFrame ,bucket_name : str,key_file_path: str):
    """Uploads a file to the bucket."""

    # Convert DataFrame to string representation
    contents = dataframe.to_csv(index=False)

    timestamp_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    blob_path = f"{timestamp_string}.csv"

    # Create credentials from service account key file
    credentials = service_account.Credentials.from_service_account_file(key_file_path)

    # Create storage client with provided credentials
    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(blob_path)
    blob.upload_from_string(contents , 'text/csv')

    print(f"{blob_path} uploaded to {bucket_name}.")


if __name__ == "__main__":
    # API request parameters
    LIMIT = 500
    start_datetime = datetime(2024, 1, 1, 1, 0, 0, 1)

    # GCP upload parameters
    keyfile_path = os.environ["SERVICE_ACCOUNT_KEYFILE"]
    gcp_project_id = os.environ["GCP_PROJECT_ID"]
    # table_id = f"{os.environ['BRONZE_DATASET']}.alerts"

    #GCS upload parameters
    bucket_name = os.environ["US_WEATHER_AlERTS_BUCKET"]

    features = scrape_alerts(status="actual", region_type="land", start_datetime=start_datetime, limit=LIMIT)
    df = parse_features(features)
    #upload_to_gcp(df, gcp_project_id, table_id, keyfile_path)
    upload_to_gcs_from_memory(df, bucket_name , keyfile_path)
