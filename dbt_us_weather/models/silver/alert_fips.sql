SELECT 
    af.alert_id, 
    RIGHT(REPLACE(f, '"', ''),5) AS fips_id
FROM (
    SELECT 
        id AS alert_id, 
        JSON_EXTRACT_ARRAY(fips) AS fips_id
    FROM {{ source('us_weather_alerts_bronze', 'alerts') }}
) af
, UNNEST(af.fips_id) f
