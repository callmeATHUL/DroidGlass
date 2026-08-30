import os
import sys
from typing import Optional, Dict, Any, Tuple

try:
    from google.cloud import bigquery
    from google.api_core.exceptions import GoogleAPIError
except ImportError:
    bigquery = None
    GoogleAPIError = Exception


class BqClient:
    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        self.location = location or os.getenv("BIGQUERY_LOCATION", "US")
        self._client = None

    @property
    def client(self):
        if bigquery is None:
            raise RuntimeError(
                "google-cloud-bigquery package not installed. Run: pip install -r requirements.txt"
            )
        if self._client is None:
            self._client = bigquery.Client(project=self.project_id, location=self.location)
        return self._client

    def dry_run(self, query: str) -> Dict[str, Any]:
        """Perform dry run to validate SQL syntax and estimate bytes scanned."""
        if bigquery is None:
            return {
                "valid": False,
                "bytes_scanned": 0,
                "mb_scanned": 0,
                "gb_scanned": 0,
                "error": "google-cloud-bigquery not installed (pip install -r requirements.txt)",
            }
        try:
            job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
            query_job = self.client.query(query, job_config=job_config)
            bytes_scanned = query_job.total_bytes_processed or 0
            mb_scanned = bytes_scanned / (1024 * 1024)
            gb_scanned = bytes_scanned / (1024 * 1024 * 1024)
            return {
                "valid": True,
                "bytes_scanned": bytes_scanned,
                "mb_scanned": round(mb_scanned, 2),
                "gb_scanned": round(gb_scanned, 4),
                "error": None,
            }
        except Exception as e:
            return {
                "valid": False,
                "bytes_scanned": 0,
                "mb_scanned": 0,
                "gb_scanned": 0,
                "error": str(e),
            }

    def execute_query(self, query: str, max_results: int = 50) -> Tuple[list, list]:
        """Execute query and return (headers, rows)."""
        if bigquery is None:
            raise RuntimeError("google-cloud-bigquery not installed")
        query_job = self.client.query(query)
        results = query_job.result(max_results=max_results)
        headers = [field.name for field in results.schema] if results.schema else []
        rows = [list(row.values()) for row in results]
        return headers, rows
