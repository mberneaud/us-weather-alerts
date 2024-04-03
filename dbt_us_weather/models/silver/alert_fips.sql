select
    id as alert_id,
    unnest(right(fips, 5)) as fips_id
from {{ source('us_weather_alerts_bronze', 'alerts') }}
