SELECT
  fips AS fips_id,
  zone AS zone_id,
  state AS state_name_abbr,
  county AS county_name,
  name AS zone_name
FROM {{ source('us_weather_alerts_bronze', 'zone_county') }}
