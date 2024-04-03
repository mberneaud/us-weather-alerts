SELECT
    id AS alert_id,
    UNNEST(RIGHT(same, 5)) AS fips_id
FROM {{ source('us_weather_alerts_bronze', 'alerts') }}
