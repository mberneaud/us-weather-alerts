""""
Functions for accessing the National Weather Service API
Created: 19.03.204
Author: Malte Berneaud
"""

import pandas as pd
import requests
#TODO: make asynchronous
from datetime import datetime, timezone
from typing import List, Dict, LiteralString


def scrape_alerts(start_datetime: LiteralString, end_datetime: LiteralString, status: LiteralString, output_file:LiteralString, limit: int = 500) -> list:
    """Scrapes alerts for the specified timeframe and status and saves them to an output CSV file
    datetime format: "%Y-%m-%dT%H:%M:%SZ"
    """
    base_url = "https://api.weather.gov/alerts"
    params = {"limit": limit,
          "start": start_datetime,
          "end": end_datetime,
          "status": status}

    features = []

    response = requests.get(base_url, params=params).json()
    if response["features"] == []:
        raise KeyError("No alerts found for the specified properties. Try a longer time span.")
    features.append(response["features"])

    while True:
        try:
            next = response["pagination"]["next"]
            print(f"Sending follow-up request to {next}")
            response = requests.get(next).json()

            # TODO: parse the response to keep only important data inside

            features.append(response["features"])
        except:
            print("No further pagination URL found")
            break

    return features

def parse_features(features: list) -> pd.DataFrame:
    pass

def upload_to_gcp(dataframe: pd.DataFrame):
    pass

if __name__ == "__main__":
    # Creating request paramenters
    LIMIT = 500
    dt_format = "%Y-%m-%dT%H:%M:%SZ"
    start_datetime = datetime(2023, 1, 1, 1, 0, 0, 1).astimezone(timezone.utc).strftime(dt_format)
    # end_datetime = datetime(2023, 1, 1, 5, 0, 0, 1).astimezone(timezone.utc).strftime(dt_format)


    end_datetime = datetime.now().astimezone(timezone.utc).strftime(dt_format)
    scrape_alerts(start_datetime, end_datetime, "actual", "test.csv", LIMIT)
