from typing import Dict, Any, Optional
from src.client import BqClient
from src.sql_generator import SqlGenerator


class BqForecaster:
    """Manages BigQuery AI.FORECAST and AI.DETECT_ANOMALIES workflows."""

    def __init__(self, client: Optional[BqClient] = None):
        self.client = client or BqClient()

    def generate_forecast_sql(
        self,
        table_id: str,
        time_col: str,
        data_col: str,
        horizon: int = 30,
        confidence_level: float = 0.95
    ) -> str:
        return SqlGenerator.build_forecast_query(
            table_id=table_id,
            time_col=time_col,
            data_col=data_col,
            horizon=horizon,
            confidence_level=confidence_level
        )

    def generate_anomaly_sql(
        self,
        table_id: str,
        time_col: str,
        data_col: str,
        contamination: float = 0.05
    ) -> str:
        return SqlGenerator.build_anomaly_query(
            table_id=table_id,
            time_col=time_col,
            data_col=data_col,
            contamination=contamination
        )

    def run_forecast(
        self,
        table_id: str,
        time_col: str,
        data_col: str,
        horizon: int = 30,
        dry_run: bool = True
    ) -> Dict[str, Any]:
        sql = self.generate_forecast_sql(table_id, time_col, data_col, horizon)
        if dry_run:
            dry_res = self.client.dry_run(sql)
            return {"sql": sql, "dry_run": dry_res}
        headers, rows = self.client.execute_query(sql)
        return {"sql": sql, "headers": headers, "rows": rows}
