from typing import Dict, Any, Optional
from src.client import BqClient


class BqVectorSearch:
    """Helper for generating BigQuery Vector Search and Embeddings SQL."""

    def __init__(self, client: Optional[BqClient] = None):
        self.client = client or BqClient()

    @staticmethod
    def build_embedding_query(
        table_id: str,
        content_col: str,
        model_name: str = "us.text-embedding-004"
    ) -> str:
        """Generate AI.GENERATE_EMBEDDING / ML.GENERATE_EMBEDDING SQL."""
        return f"""-- BigQuery Vector Embedding Generation
SELECT *
FROM ML.GENERATE_EMBEDDING(
  MODEL `{model_name}`,
  TABLE `{table_id}`,
  STRUCT(TRUE AS flatten_json_output)
);"""

    @staticmethod
    def build_vector_search_query(
        base_table: str,
        query_text: str,
        embedding_model: str = "us.text-embedding-004",
        top_k: int = 5,
        distance_type: str = "COSINE"
    ) -> str:
        """Generate VECTOR_SEARCH query against embedded table."""
        escaped_query = query_text.replace("'", "\\'")
        return f"""-- BigQuery VECTOR_SEARCH with Real-time Query Embedding
SELECT
  query.query_text,
  base.*,
  distance
FROM VECTOR_SEARCH(
  TABLE `{base_table}`,
  'ml_generate_embedding_result',
  (
    SELECT
      ml_generate_embedding_result,
      content AS query_text
    FROM ML.GENERATE_EMBEDDING(
      MODEL `{embedding_model}`,
      (SELECT '{escaped_query}' AS content)
    )
  ),
  top_k => {top_k},
  distance_type => '{distance_type}'
);"""
