FROM python:3.8.14

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED 1

ENV AIRFLOW_HOME=/app/airflow

# DBT
ENV DBT_DIR=$AIRFLOW_HOME/dbt_us_weather
ENV DBT_TARGET_DIR=$DBT_DIR/target
ENV DBT_PROFILES_DIR=$DBT_DIR
ENV DBT_VERSION=1.1.1
#GCP
ENV SERVICE_ACCOUNT_KEYFILE=$AIRFLOW_HOME/.gcp_keys/us-weather-alert.json
ENV GCP_PROJECT_ID="le-wagon-328012"
ENV BRONZE_DATASET="us_weather_alerts_bronze"
ENV SILVER_DATASET="us_weather_alerts_silver"
ENV GOLD_DATASET="us_weather_alerts_gold"
ENV US_WEATHER_AlERTS_BUCKET="us_weather_alerts_storage"

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts/entrypoint.sh

COPY pyproject.toml poetry.lock ./

RUN pip3 install --upgrade --no-cache-dir pip \
    && pip3 install poetry \
    && poetry install --only main
