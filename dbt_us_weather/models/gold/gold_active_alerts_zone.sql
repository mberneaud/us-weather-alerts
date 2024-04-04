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

FROM {{ ref('silver_alerts') }} a
LEFT JOIN {{ ref('silver_alert_fips') }} af ON a.alert_id = af.alert_id
JOIN {{ ref('silver_zone_county') }} zc ON af.fips_id = zc.fips_id
WHERE a.event_start <= CURRENT_TIMESTAMP()
  AND (a.event_end >= CURRENT_TIMESTAMP() OR a.event_end IS NULL)
  AND a.alert_status = 'Actual'
