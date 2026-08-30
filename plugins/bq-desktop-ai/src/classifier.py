from typing import List, Dict, Any, Optional
from src.client import BqClient
from src.sql_generator import SqlGenerator


class BqClassifier:
    """Manages BigQuery AI.CLASSIFY and AI.SCORE analytical tasks."""

    def __init__(self, client: Optional[BqClient] = None):
        self.client = client or BqClient()

    def generate_sql(self, table_id: str, text_col: str, categories: List[str]) -> str:
        return SqlGenerator.build_classify_query(table_id, text_col, categories)

    def classify_table(self, table_id: str, text_col: str, categories: List[str], dry_run: bool = True) -> Dict[str, Any]:
        sql = self.generate_sql(table_id, text_col, categories)
        if dry_run:
            dry_res = self.client.dry_run(sql)
            return {"sql": sql, "dry_run": dry_res}
        headers, rows = self.client.execute_query(sql)
        return {"sql": sql, "headers": headers, "rows": rows}
