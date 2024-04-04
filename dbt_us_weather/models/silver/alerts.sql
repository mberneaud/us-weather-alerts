SELECT
  id AS alert_id,
  event,
  PARSE_TIMESTAMP('%FT%T%Ez', onset) AS event_start,
  PARSE_TIMESTAMP('%FT%T%Ez', ends) AS event_end,
  PARSE_TIMESTAMP('%FT%T%Ez', effective) AS information_start,
  PARSE_TIMESTAMP('%FT%T%Ez', expires) AS information_end,
  status AS alert_status,
  messageType AS alert_message_type,
  severity AS alert_severity,
  certainty AS alert_certainty,
  urgency AS alert_urgency,
  response AS recommended_action_type,
  instruction AS recommended_action_description

FROM {{ source('us_weather_alerts_bronze', 'alerts') }}
