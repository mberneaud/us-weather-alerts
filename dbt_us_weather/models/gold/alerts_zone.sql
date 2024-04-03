SELECT
  a.alert_id,
  zc.fips_id,
  zc.state_name_abbr,
  zc.county_name,
  zc.zone_name,
  a.event,
  a.event_start,
  a.event_end,
  a.alert_severity,
  a.alert_urgency,
  a.alert_certainty,
  a.recommended_action_type,
  a.recommended_action_description
  
FROM {{ source('us_weather_alerts_silver', 'alerts') }} a
LEFT JOIN {{ source('us_weather_alerts_silver', 'alert_fips') }} af ON a.alert_id = af.alert_id
LEFT JOIN {{ source('us_weather_alerts_silver', 'zone_county') }} zc ON af.fips_id = zc.fips_id
WHERE a.event_start <= CURRENT_DATETIME()
  AND (a.event_end >= CURRENT_DATETIME() OR a.event_end IS NULL)
  AND a.alert_status = 'Actual'
