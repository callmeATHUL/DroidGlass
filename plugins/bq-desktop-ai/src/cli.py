import argparse
import sys
import os
import subprocess
from typing import List

from src.client import BqClient
from src.sql_generator import SqlGenerator
from src.forecaster import BqForecaster
from src.classifier import BqClassifier
from src.vector_search import BqVectorSearch


def format_table(headers: List[str], rows: List[list]) -> str:
    try:
        from tabulate import tabulate
        return tabulate(rows, headers=headers, tablefmt="fancy_grid")
    except ImportError:
        header_str = " | ".join(headers)
        divider = "-" * len(header_str)
        row_strs = [" | ".join(str(val) for val in r) for r in rows]
        return f"{header_str}\n{divider}\n" + "\n".join(row_strs)


def notify_desktop(title: str, message: str):
    try:
        subprocess.run(["notify-send", "-a", "BigQuery AI", title, message], check=False)
    except Exception:
        pass


def get_clipboard_text() -> str:
    try:
        res = subprocess.run(["wl-paste"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    try:
        res = subprocess.run(["xclip", "-o", "-selection", "clipboard"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return ""


def set_clipboard_text(text: str):
    try:
        p = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE, text=True)
        p.communicate(input=text)
        return
    except Exception:
        pass
    try:
        p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE, text=True)
        p.communicate(input=text)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(
        prog="bq-ai",
        description="BigQuery AI/ML Assistant & SQL Companion for Omarchy Desktop"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # SQL subcommand
    sql_parser = subparsers.add_parser("sql", help="Generate or dry-run BigQuery SQL from natural language")
    sql_parser.add_argument("prompt", help="Natural language prompt or query")
    sql_parser.add_argument("--execute", action="store_true", help="Execute the generated query")
    sql_parser.add_argument("--model", default="gemini-1.5-pro", help="Vertex AI model name")

    # Explain subcommand
    explain_parser = subparsers.add_parser("explain", help="Explain, audit, and optimize a SQL query")
    explain_parser.add_argument("query", nargs="?", help="SQL query to explain (or reads stdin/clipboard)")

    # Forecast subcommand
    forecast_parser = subparsers.add_parser("forecast", help="Generate AI.FORECAST pipeline query")
    forecast_parser.add_argument("--table", required=True, help="Full table ID (project.dataset.table)")
    forecast_parser.add_argument("--time-col", required=True, help="Timestamp/Date column name")
    forecast_parser.add_argument("--data-col", required=True, help="Target metric column name")
    forecast_parser.add_argument("--horizon", type=int, default=30, help="Forecast horizon intervals")
    forecast_parser.add_argument("--execute", action="store_true", help="Execute query instead of dry-run")

    # Anomaly subcommand
    anomaly_parser = subparsers.add_parser("anomaly", help="Generate AI.DETECT_ANOMALIES query")
    anomaly_parser.add_argument("--table", required=True, help="Full table ID")
    anomaly_parser.add_argument("--time-col", required=True, help="Timestamp column")
    anomaly_parser.add_argument("--data-col", required=True, help="Metric column")
    anomaly_parser.add_argument("--contamination", type=float, default=0.05, help="Anomaly rate (0 to 0.5)")

    # Classify subcommand
    classify_parser = subparsers.add_parser("classify", help="Generate AI.CLASSIFY query")
    classify_parser.add_argument("--table", required=True, help="Full table ID")
    classify_parser.add_argument("--text-col", required=True, help="Text column to classify")
    classify_parser.add_argument("--categories", nargs="+", required=True, help="List of target categories")

    # Search subcommand
    search_parser = subparsers.add_parser("search", help="Generate VECTOR_SEARCH query")
    search_parser.add_argument("--table", required=True, help="Embedded base table ID")
    search_parser.add_argument("--query", required=True, help="Search prompt/query string")

    # Clipboard subcommand
    clip_parser = subparsers.add_parser("clip", help="Analyze or format SQL directly from Wayland clipboard")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    client = BqClient()

    if args.command == "sql":
        generated_sql = SqlGenerator.generate_ai_query(args.prompt, model_name=args.model)
        print("Generated BigQuery AI SQL:\n")
        print(generated_sql)
        print("\n--- Dry Run Validation ---")
        dry = client.dry_run(generated_sql)
        if dry["valid"]:
            print(f"Status: VALID | Estimated data scanned: {dry['mb_scanned']} MB ({dry['gb_scanned']} GB)")
            if args.execute:
                print("\nExecuting query...")
                headers, rows = client.execute_query(generated_sql)
                print(format_table(headers, rows))
        else:
            print(f"Status: INVALID | Error: {dry['error']}")

    elif args.command == "explain":
        query_text = args.query or get_clipboard_text()
        if not query_text:
            print("Error: No SQL query provided and clipboard is empty.", file=sys.stderr)
            sys.exit(1)
        prompt = SqlGenerator.build_explain_prompt(query_text)
        print("--- Query Optimization & Explanation Plan ---")
        print(prompt)

    elif args.command == "forecast":
        fc = BqForecaster(client)
        sql = fc.generate_forecast_sql(args.table, args.time_col, args.data_col, args.horizon)
        print(sql)
        dry = client.dry_run(sql)
        print(f"\n[Dry Run] Valid: {dry['valid']} | Scanned: {dry['mb_scanned']} MB")
        if not dry["valid"] and dry["error"]:
            print(f"Note: {dry['error']}")

    elif args.command == "anomaly":
        fc = BqForecaster(client)
        sql = fc.generate_anomaly_sql(args.table, args.time_col, args.data_col, args.contamination)
        print(sql)

    elif args.command == "classify":
        clf = BqClassifier(client)
        sql = clf.generate_sql(args.table, args.text_col, args.categories)
        print(sql)

    elif args.command == "search":
        sql = BqVectorSearch.build_vector_search_query(args.table, args.query)
        print(sql)

    elif args.command == "clip":
        clip_text = get_clipboard_text()
        if not clip_text:
            notify_desktop("BigQuery AI", "Clipboard is empty")
            print("Clipboard is empty.")
            sys.exit(1)
        notify_desktop("BigQuery AI", f"Analyzing: {clip_text[:40]}...")
        print(f"Clipboard Content:\n{clip_text}\n")
        dry = client.dry_run(clip_text)
        if dry["valid"]:
            msg = f"Valid SQL! Estimated scan: {dry['mb_scanned']} MB"
            print(f"✓ {msg}")
            notify_desktop("BigQuery AI - Valid", msg)
        else:
            print(f"✗ Validation: {dry['error']}")
            notify_desktop("BigQuery AI - Issue", str(dry['error'])[:80])


if __name__ == "__main__":
    main()
