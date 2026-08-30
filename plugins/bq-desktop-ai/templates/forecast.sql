-- BigQuery AI.FORECAST Template
-- Forecasts future time series steps using ARIMA_PLUS / Vertex AI backends directly in SQL.

SELECT *
FROM AI.FORECAST(
  TABLE `{{ project_id }}.{{ dataset_id }}.{{ table_name }}`,
  data_col => '{{ target_metric }}',
  time_col => '{{ timestamp_col }}',
  horizon => {{ horizon | default(30) }},
  confidence_level => {{ confidence_level | default(0.95) }}
);
