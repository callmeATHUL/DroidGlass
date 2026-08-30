-- BigQuery AI.DETECT_ANOMALIES Template
-- Detects statistical and seasonal anomalies in historical time series data.

SELECT *
FROM AI.DETECT_ANOMALIES(
  TABLE `{{ project_id }}.{{ dataset_id }}.{{ table_name }}`,
  data_col => '{{ target_metric }}',
  time_col => '{{ timestamp_col }}',
  contamination => {{ contamination | default(0.05) }}
)
WHERE is_anomaly = TRUE
ORDER BY {{ timestamp_col }} DESC;
