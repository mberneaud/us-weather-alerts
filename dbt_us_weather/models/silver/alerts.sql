SELECT
  id AS alert_id,
  event,
  onset AS event_start,
  ends AS event_end,
  effective AS information_start,
  expires AS information_end,
  status AS alert_status,
  messageType AS alert_message_type,
  severity AS alert_severity,
  certainty AS alert_certainty,
  urgency AS alert_urgency,
  response AS recommended_action_type,
  instruction AS recommended_action_description

FROM {{ source('us_weather_alerts_bronze', 'alerts') }}
