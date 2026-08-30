-- BigQuery VECTOR_SEARCH & Embeddings Template
-- Real-time vector search across embedded catalog/documents using Cosine/Euclidean distance.

SELECT
  query.query_text,
  base.doc_id,
  base.title,
  base.content,
  distance
FROM VECTOR_SEARCH(
  TABLE `{{ project_id }}.{{ dataset_id }}.{{ base_table }}`,
  'ml_generate_embedding_result',
  (
    SELECT
      ml_generate_embedding_result,
      content AS query_text
    FROM ML.GENERATE_EMBEDDING(
      MODEL `{{ project_id }}.{{ dataset_id }}.{{ embedding_model }}`,
      (SELECT '{{ user_query }}' AS content)
    )
  ),
  top_k => 5,
  distance_type => 'COSINE'
);
