#!/usr/bin/env python3
"""Write structured Agent Health Log records to local CSV files."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover - Python < 3.9 fallback path.
    ZoneInfo = None  # type: ignore[assignment]

    class ZoneInfoNotFoundError(Exception):
        """Fallback exception when zoneinfo is unavailable."""


NUTRITION_HEADER = [
    "date",
    "meal_time",
    "item",
    "display_name",
    "quantity",
    "calories_kcal",
    "protein_g",
    "carbs_g",
    "fat_g",
    "confidence",
    "tags",
    "raw_text",
]

TRAINING_HEADER = [
    "date",
    "session_type",
    "focus",
    "exercise_id",
    "display_name",
    "weight_kg",
    "reps",
    "set_count",
    "rpe",
    "notes",
    "raw_text",
]

BODY_METRICS_HEADER = [
    "date",
    "metric_name",
    "value",
    "unit",
    "notes",
    "raw_text",
]


class RecordError(ValueError):
    """Raised when a structured record cannot be written safely."""


def blank(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def parse_override_date(value: str | None) -> date | None:
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise RecordError(f"Invalid --date value: {value}. Expected YYYY-MM-DD.") from exc


def current_date(timezone_name: str | None) -> date:
    if not timezone_name:
        return date.today()
    if ZoneInfo is None:
        raise RecordError("Timezone support requires Python 3.9+ zoneinfo.")
    try:
        return datetime.now(ZoneInfo(timezone_name)).date()
    except ZoneInfoNotFoundError as exc:
        raise RecordError(f"Unknown timezone: {timezone_name}") from exc


def resolve_date(value: str | None, anchor: date) -> str:
    if not value or value == "today":
        return anchor.isoformat()
    if value == "yesterday":
        return (anchor - timedelta(days=1)).isoformat()
    return value


def ensure_inside_root(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    root_resolved = root.resolve()
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise RecordError(f"Refusing to read outside repository root: {path}")
    return resolved


def read_record(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    if args.json_file:
        input_path = ensure_inside_root(Path(args.json_file), root)
        with input_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    raw = sys.stdin.read().strip()
    if not raw:
        raise RecordError("No JSON received. Pipe a JSON object to stdin or pass a JSON file path.")
    return json.loads(raw)


def require_data_files(root: Path) -> dict[str, Path]:
    data_dir = root / "data"
    if not data_dir.is_dir():
        raise RecordError("data/ does not exist. Run scripts/init_health_log.py first.")

    files = {
        "nutrition": data_dir / "nutrition.csv",
        "training": data_dir / "training.csv",
        "body_metrics": data_dir / "body_metrics.csv",
    }
    missing = [str(path) for path in files.values() if not path.exists()]
    if missing:
        raise RecordError("Missing CSV files. Run scripts/init_health_log.py first. Missing: " + ", ".join(missing))
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
    rows: list[dict[str, Any]] = []
    for meal in record.get("meals", []):
        meal_time = meal.get("meal_time", "unknown")
        for item in meal.get("items", []):
            estimate = item.get("nutrition_estimate", {})
            rows.append(
                {
                    "date": date_value,
                    "meal_time": meal_time,
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
                }
            )
    return rows


def workout_rows(record: dict[str, Any], date_value: str, raw_text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    session_type = record.get("session_type", "unknown")
    focus = record.get("focus")
    for exercise in record.get("exercises", []):
        sets = exercise.get("sets") or [{}]
        for set_info in sets:
            rows.append(
                {
                    "date": date_value,
                    "session_type": session_type,
                    "focus": focus,
                    "exercise_id": exercise.get("exercise_id"),
                    "display_name": exercise.get("display_name"),
                    "weight_kg": set_info.get("weight_kg"),
                    "reps": set_info.get("reps"),
                    "set_count": set_info.get("set_count"),
                    "rpe": exercise.get("rpe"),
                    "notes": exercise.get("notes"),
                    "raw_text": raw_text,
                }
            )
    return rows


def body_metric_rows(record: dict[str, Any], date_value: str, raw_text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    notes = record.get("notes")
    for metric_name, value in record.get("metrics", {}).items():
        rows.append(
            {
                "date": date_value,
                "metric_name": metric_name,
                "value": value,
                "unit": "",
                "notes": notes,
                "raw_text": raw_text,
            }
        )
    return rows


def safety_boundary_rows(record: dict[str, Any], date_value: str, raw_text: str, anchor: date) -> list[dict[str, Any]]:
    note = record.get("note") or {}
    note_date = resolve_date(note.get("date") or date_value, anchor)
    return [
        {
            "date": note_date,
            "metric_name": "safety_boundary",
            "value": record.get("category"),
            "unit": "",
            "notes": note.get("text"),
            "raw_text": raw_text,
        }
    ]


def write_record(record: dict[str, Any], files: dict[str, Path], anchor: date) -> dict[str, int]:
    record_type = record.get("type")
    raw_text = record.get("raw_text", "")
    date_value = resolve_date(record.get("date") or record.get("date_anchor"), anchor)

    counts = {"nutrition": 0, "training": 0, "body_metrics": 0}

    if record_type == "meal_log":
        counts["nutrition"] = append_rows(files["nutrition"], NUTRITION_HEADER, meal_rows(record, date_value, raw_text))
    elif record_type == "workout_log":
        counts["training"] = append_rows(files["training"], TRAINING_HEADER, workout_rows(record, date_value, raw_text))
    elif record_type == "mixed_log":
        meal_record = record.get("meal_log", {})
        workout_record = record.get("workout_log", {})
        counts["nutrition"] = append_rows(files["nutrition"], NUTRITION_HEADER, meal_rows(meal_record, date_value, raw_text))
        counts["training"] = append_rows(files["training"], TRAINING_HEADER, workout_rows(workout_record, date_value, raw_text))
    elif record_type == "body_metrics_log":
        counts["body_metrics"] = append_rows(files["body_metrics"], BODY_METRICS_HEADER, body_metric_rows(record, date_value, raw_text))
    elif record_type == "safety_boundary":
        counts["body_metrics"] = append_rows(files["body_metrics"], BODY_METRICS_HEADER, safety_boundary_rows(record, date_value, raw_text, anchor))
    elif record_type in {"query", "weekly_review_request"}:
        raise RecordError("This is a request intent, not a writable record. Use query or report scripts instead.")
    else:
        raise RecordError(f"Unsupported record type: {record_type}")

    return counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a structured health log record to local CSV files.")
    parser.add_argument("--date", help="Override parser-relative today with YYYY-MM-DD.")
    parser.add_argument("--timezone", help="IANA timezone used to resolve today/yesterday, for example Asia/Tokyo.")
    parser.add_argument("json_file", nargs="?", help="Optional JSON file path inside the repository root. Defaults to stdin.")
    return parser.parse_args()


def main() -> int:
    root = Path.cwd()
    args = parse_args()

    try:
        record = read_record(args, root)
        if record.get("type") in {"query", "weekly_review_request"}:
            raise RecordError("This is a request intent, not a writable record. Use query or report scripts instead.")
        anchor = parse_override_date(args.date) or current_date(args.timezone)
        files = require_data_files(root)
        counts = write_record(record, files, anchor)
    except (OSError, json.JSONDecodeError, RecordError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("Record written.")
    for name, count in counts.items():
        if count:
            print(f"- {name}: {count} row(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
