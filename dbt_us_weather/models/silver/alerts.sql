SELECT DISTINCT
  id AS alert_id,
  event,
  CASE WHEN onset <> 'None' THEN PARSE_TIMESTAMP('%FT%T%Ez', onset) ELSE NULL END AS event_start,
  CASE WHEN ends <> 'None' THEN PARSE_TIMESTAMP('%FT%T%Ez', ends) ELSE NULL END AS event_end,
  CASE WHEN effective <> 'None' THEN PARSE_TIMESTAMP('%FT%T%Ez', effective) ELSE NULL END AS information_start,
  CASE WHEN expires <> 'None' THEN PARSE_TIMESTAMP('%FT%T%Ez', expires) ELSE NULL END AS information_end,
  CASE WHEN sent <> 'None' THEN PARSE_TIMESTAMP('%FT%T%Ez', sent) ELSE NULL END AS information_sent,
  status AS alert_status,
  type AS alert_message_type,
  severity AS alert_severity,
  certainty AS alert_certainty,
  urgency AS alert_urgency,
  response AS recommended_action_type,
  instruction AS recommended_action_description

FROM {{ source('us_weather_alerts_bronze', 'alerts') }}
