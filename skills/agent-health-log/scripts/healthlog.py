#!/usr/bin/env python3
"""Local-first health log CLI used by the Agent Health Log Skill."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import mean
from typing import Any

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore[assignment]

    class ZoneInfoNotFoundError(Exception):
        """Fallback when zoneinfo is unavailable."""


NUTRITION_HEADER = ["date", "meal_time", "item", "display_name", "quantity", "calories_kcal", "protein_g", "carbs_g", "fat_g", "confidence", "tags", "raw_text"]
TRAINING_HEADER = ["date", "session_type", "focus", "exercise_id", "display_name", "weight_kg", "reps", "set_count", "rpe", "notes", "raw_text"]
BODY_METRICS_HEADER = ["date", "metric_name", "value", "unit", "notes", "raw_text"]


class HealthLogError(ValueError):
    """Raised when a health log operation cannot continue."""


def default_data_dir() -> Path:
    return Path.home() / ".agent-health-log"


def blank(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise HealthLogError(f"Invalid date: {value}. Expected YYYY-MM-DD.") from exc


def current_date(timezone_name: str | None) -> date:
    if not timezone_name:
        return date.today()
    if ZoneInfo is None:
        raise HealthLogError("Timezone support requires Python 3.9+ zoneinfo.")
    try:
        return datetime.now(ZoneInfo(timezone_name)).date()
    except ZoneInfoNotFoundError as exc:
        raise HealthLogError(f"Unknown timezone: {timezone_name}") from exc


def resolve_date(value: str | None, anchor: date) -> str:
    if not value or value == "today":
        return anchor.isoformat()
    if value == "yesterday":
        return (anchor - timedelta(days=1)).isoformat()
    return value


def init_data_dir(root: Path) -> None:
    data_dir = root / "data"
    daily_dir = root / "daily"
    reports_dir = root / "reports"
    for directory in (data_dir, daily_dir, reports_dir):
        directory.mkdir(parents=True, exist_ok=True)
    create_csv_if_missing(data_dir / "nutrition.csv", NUTRITION_HEADER)
    create_csv_if_missing(data_dir / "training.csv", TRAINING_HEADER)
    create_csv_if_missing(data_dir / "body_metrics.csv", BODY_METRICS_HEADER)
    print(f"Initialized Agent Health Log data directory: {root}")


def create_csv_if_missing(path: Path, header: list[str]) -> None:
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow(header)


def require_data_files(root: Path) -> dict[str, Path]:
    data_dir = root / "data"
    files = {
        "nutrition": data_dir / "nutrition.csv",
        "training": data_dir / "training.csv",
        "body_metrics": data_dir / "body_metrics.csv",
    }
    missing = [str(path) for path in files.values() if not path.exists()]
    if missing:
        raise HealthLogError("Missing data files. Run `healthlog.py init` first. Missing: " + ", ".join(missing))
    return files


def append_rows(path: Path, header: list[str], rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        for row in rows:
            writer.writerow({key: blank(row.get(key)) for key in header})
    return len(rows)


def meal_rows(record: dict[str, Any], date_value: str, raw_text: str) -> list[dict[str, Any]]:
    rows = []
    for meal in record.get("meals", []):
        for item in meal.get("items", []):
            estimate = item.get("nutrition_estimate", {})
            rows.append({
                "date": date_value,
                "meal_time": meal.get("meal_time", "unknown"),
                "item": item.get("name"),
                "display_name": item.get("display_name"),
                "quantity": item.get("quantity"),
                "calories_kcal": estimate.get("calories_kcal"),
                "protein_g": estimate.get("protein_g"),
                "carbs_g": estimate.get("carbs_g"),
                "fat_g": estimate.get("fat_g"),
                "confidence": estimate.get("confidence"),
                "tags": ";".join(item.get("tags", [])),
                "raw_text": raw_text,
            })
    return rows


def workout_rows(record: dict[str, Any], date_value: str, raw_text: str) -> list[dict[str, Any]]:
    rows = []
    for exercise in record.get("exercises", []):
        for set_info in exercise.get("sets") or [{}]:
            rows.append({
                "date": date_value,
                "session_type": record.get("session_type", "unknown"),
                "focus": record.get("focus"),
                "exercise_id": exercise.get("exercise_id"),
                "display_name": exercise.get("display_name"),
                "weight_kg": set_info.get("weight_kg"),
                "reps": set_info.get("reps"),
                "set_count": set_info.get("set_count"),
                "rpe": exercise.get("rpe"),
                "notes": exercise.get("notes"),
                "raw_text": raw_text,
            })
    return rows


def body_metric_rows(record: dict[str, Any], date_value: str, raw_text: str) -> list[dict[str, Any]]:
    return [
        {
            "date": date_value,
            "metric_name": metric_name,
            "value": value,
            "unit": "",
            "notes": record.get("notes"),
            "raw_text": raw_text,
        }
        for metric_name, value in record.get("metrics", {}).items()
    ]


def safety_boundary_rows(record: dict[str, Any], date_value: str, raw_text: str, anchor: date) -> list[dict[str, Any]]:
    note = record.get("note") or {}
    return [{
        "date": resolve_date(note.get("date") or date_value, anchor),
        "metric_name": "safety_boundary",
        "value": record.get("category"),
        "unit": "",
        "notes": note.get("text"),
        "raw_text": raw_text,
    }]


def write_record(root: Path, record: dict[str, Any], anchor: date) -> None:
    files = require_data_files(root)
    record_type = record.get("type")
    raw_text = record.get("raw_text", "")
    date_value = resolve_date(record.get("date") or record.get("date_anchor"), anchor)
    counts = {"nutrition": 0, "training": 0, "body_metrics": 0}

    if record_type == "meal_log":
        counts["nutrition"] = append_rows(files["nutrition"], NUTRITION_HEADER, meal_rows(record, date_value, raw_text))
    elif record_type == "workout_log":
        counts["training"] = append_rows(files["training"], TRAINING_HEADER, workout_rows(record, date_value, raw_text))
    elif record_type == "mixed_log":
        counts["nutrition"] = append_rows(files["nutrition"], NUTRITION_HEADER, meal_rows(record.get("meal_log", {}), date_value, raw_text))
        counts["training"] = append_rows(files["training"], TRAINING_HEADER, workout_rows(record.get("workout_log", {}), date_value, raw_text))
    elif record_type == "body_metrics_log":
        counts["body_metrics"] = append_rows(files["body_metrics"], BODY_METRICS_HEADER, body_metric_rows(record, date_value, raw_text))
    elif record_type == "safety_boundary":
        counts["body_metrics"] = append_rows(files["body_metrics"], BODY_METRICS_HEADER, safety_boundary_rows(record, date_value, raw_text, anchor))
    elif record_type in {"query", "weekly_review_request"}:
        raise HealthLogError("This is a request intent, not a writable record. Use query handling or `report weekly` instead.")
    else:
        raise HealthLogError(f"Unsupported record type: {record_type}")

    print("Record written.")
    for name, count in counts.items():
        if count:
            print(f"- {name}: {count} row(s)")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_row_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def week_range(anchor: date) -> tuple[date, date]:
    start = anchor - timedelta(days=anchor.weekday())
    return start, start + timedelta(days=6)


def filter_week(rows: list[dict[str, str]], start: date, end: date) -> list[dict[str, str]]:
    return [row for row in rows if (row_date := parse_row_date(row.get("date", ""))) and start <= row_date <= end]


def daily_totals(rows: list[dict[str, str]], field: str) -> dict[str, float]:
    totals: dict[str, float] = {}
    for row in rows:
        row_date = row.get("date", "")
        raw = row.get(field, "")
        if not row_date or raw == "":
            continue
        try:
            totals[row_date] = totals.get(row_date, 0.0) + float(raw)
        except ValueError:
            continue
    return totals


def average_daily(totals: dict[str, float], meal_days: list[str], unit: str) -> str:
    if not meal_days or len(totals) < len(meal_days):
        return "Not enough nutrition data for a reliable average."
    return f"{mean(totals[day] for day in meal_days):.1f} {unit} per logged meal day (rough estimate)"


def weekly_report(root: Path, anchor: date) -> Path:
    files = require_data_files(root)
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    start, end = week_range(anchor)
    iso_year, iso_week, _ = anchor.isocalendar()

    nutrition = filter_week(read_csv(files["nutrition"]), start, end)
    training = filter_week(read_csv(files["training"]), start, end)
    body_metrics = filter_week(read_csv(files["body_metrics"]), start, end)
    meal_days = sorted({row.get("date") for row in nutrition if row.get("date")})
    session_counts = Counter(row.get("session_type") or "unknown" for row in training)
    metric_counts = Counter(row.get("metric_name") or "unknown" for row in body_metrics)
    session_lines = "\n".join(f"- {name}: {count}" for name, count in sorted(session_counts.items())) or "- No training rows recorded."
    metric_lines = "\n".join(f"- {name}: {count}" for name, count in sorted(metric_counts.items())) or "- No body metric rows recorded."

    report = f"""# {iso_year}-W{iso_week:02d} Weekly Health Log

Period: {start.isoformat()} to {end.isoformat()}

## Overview

- Training exercise rows: {len(training)}
- Meal logging days: {len(meal_days)}
- Nutrition rows: {len(nutrition)}
- Body metrics rows: {len(body_metrics)}

## Training

{session_lines}

## Nutrition

- Average daily calories: {average_daily(daily_totals(nutrition, "calories_kcal"), meal_days, "kcal")}
- Average daily protein: {average_daily(daily_totals(nutrition, "protein_g"), meal_days, "g")}

## Body Status

{metric_lines}

## Notes

- Treat nutrition estimates as rough.
- Pain, injury, disease, medication, extreme dieting, or urgent symptoms should trigger `safety_boundary`.

## Disclaimer

This report is for logging and reflection only. It is not medical advice, diagnosis, treatment, or injury rehabilitation guidance.
"""
    output = reports_dir / f"{iso_year}-W{iso_week:02d}.md"
    output.write_text(report, encoding="utf-8")
    print(f"Weekly report written: {output}")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agent Health Log local CLI.")
    parser.add_argument("--data-dir", default=str(default_data_dir()), help="Private health log data directory. Defaults to ~/.agent-health-log.")
    parser.add_argument("--date", help="Anchor today/yesterday or weekly report to YYYY-MM-DD.")
    parser.add_argument("--timezone", help="IANA timezone used to resolve the current date, for example Asia/Tokyo.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="Initialize local private health log files.")
    subparsers.add_parser("write-stdin", help="Read a structured JSON record from stdin and write local CSV rows.")
    report_parser = subparsers.add_parser("report", help="Generate reports.")
    report_parser.add_argument("period", choices=["weekly"], help="Report period.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.data_dir).expanduser()
    try:
        anchor = parse_iso_date(args.date) or current_date(args.timezone)
        if args.command == "init":
            init_data_dir(root)
        elif args.command == "write-stdin":
            raw = sys.stdin.read().strip()
            if not raw:
                raise HealthLogError("No JSON received on stdin.")
            write_record(root, json.loads(raw), anchor)
        elif args.command == "report" and args.period == "weekly":
            weekly_report(root, anchor)
        else:
            raise HealthLogError(f"Unsupported command: {args.command}")
    except (OSError, json.JSONDecodeError, HealthLogError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

