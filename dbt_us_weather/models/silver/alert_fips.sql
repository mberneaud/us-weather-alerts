select
    id as alert_id,
    unnest(fips) as fips_id
from {{ source('us_weather_alerts_bronze', 'alerts') }}
