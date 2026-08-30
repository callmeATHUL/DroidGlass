import os
from typing import Dict, Any


class SqlGenerator:
    """Generates and optimizes SQL using BigQuery AI & ML syntax patterns."""

    @staticmethod
    def generate_ai_query(
        prompt: str,
        connection: str = "us.vertex-ai-conn",
        model_name: str = "gemini-1.5-pro",
        table_context: str = ""
    ) -> str:
        """Generate a BigQuery AI.GENERATE query for analytical questions."""
        escaped_prompt = prompt.replace("'", "\\'")
        context_str = f"Context: {table_context}\\n\\n" if table_context else ""
        sql = f"""SELECT ml_generate_text_llm_result AS ai_response
FROM ML.GENERATE_TEXT(
  MODEL `{connection}.{model_name}`,
  (
    SELECT '{context_str}Task: {escaped_prompt}' AS prompt
  ),
  STRUCT(
    0.2 AS temperature,
    1024 AS max_output_tokens,
    0.8 AS top_p
  )
);"""
        return sql

    @staticmethod
    def build_forecast_query(
        table_id: str,
        time_col: str,
        data_col: str,
        horizon: int = 30,
        confidence_level: float = 0.95
    ) -> str:
        """Builds an AI.FORECAST query structure."""
        return f"""-- BigQuery AI.FORECAST Pipeline
SELECT *
FROM AI.FORECAST(
  TABLE `{table_id}`,
  data_col => '{data_col}',
  time_col => '{time_col}',
  horizon => {horizon},
  confidence_level => {confidence_level}
);"""

    @staticmethod
    def build_anomaly_query(
        table_id: str,
        time_col: str,
        data_col: str,
        contamination: float = 0.05
    ) -> str:
        """Builds an AI.DETECT_ANOMALIES query."""
        return f"""-- BigQuery AI.DETECT_ANOMALIES Pipeline
SELECT *
FROM AI.DETECT_ANOMALIES(
  TABLE `{table_id}`,
  data_col => '{data_col}',
  time_col => '{time_col}',
  contamination => {contamination}
);"""

    @staticmethod
    def build_classify_query(
        table_id: str,
        text_col: str,
        categories: list
    ) -> str:
        """Builds an AI.CLASSIFY query."""
        cat_array = ", ".join([f"'{c}'" for c in categories])
        return f"""-- BigQuery AI.CLASSIFY Pipeline
SELECT
  {text_col},
  AI.CLASSIFY({text_col}, [{cat_array}]) AS classification_result
FROM `{table_id}`;"""

    @staticmethod
    def build_explain_prompt(sql_query: str) -> str:
        """Creates a prompt to explain and optimize SQL."""
        return (
            f"Analyze this BigQuery SQL query for correctness, performance, and cost optimization:\n\n"
            f"```sql\n{sql_query}\n```\n\n"
            f"Provide:\n"
            f"1. A concise explanation of what the query does.\n"
            f"2. Potential partition/cluster filter recommendations to minimize bytes scanned.\n"
            f"3. Any anti-patterns (e.g. SELECT *, cross joins, unindexed regex) and optimized SQL snippet."
        )
