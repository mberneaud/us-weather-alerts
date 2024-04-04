{{
  config(
    materialized='view',
  )
}}

SELECT
  alert_id AS AlertID,
  fips_id AS FIPS,
  state_name_abbr AS State,
  county_name AS County,
  zone_name AS Zone,
  event AS Event,
  event_start AS Start,
  event_end AS Ends,
  alert_severity AS Severity,
  alert_urgency AS Urgency,
  alert_certainty AS Certainty,
  recommended_action_type AS RecommendedAction,
  recommended_action_description AS RecommendedActionDescription

FROM {{ ref('gold_active_alerts_zone') }}
