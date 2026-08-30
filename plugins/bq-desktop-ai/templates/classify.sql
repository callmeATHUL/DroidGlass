-- BigQuery AI.CLASSIFY Template
-- Zero-shot text classification over BigQuery columns using remote LLMs.

SELECT
  {{ text_col }},
  AI.CLASSIFY(
    {{ text_col }},
    ['{{ category_1 }}', '{{ category_2 }}', '{{ category_3 }}']
  ) AS classification_payload
FROM `{{ project_id }}.{{ dataset_id }}.{{ table_name }}`
LIMIT 100;
