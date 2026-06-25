#!/usr/bin/env python3
"""Generate a Markdown weekly report from local Agent Health Log CSV files."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import mean

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover - Python < 3.9 fallback path.
    ZoneInfo = None  # type: ignore[assignment]

    class ZoneInfoNotFoundError(Exception):
        """Fallback exception when zoneinfo is unavailable."""


class ReportError(ValueError):
    """Raised when report options cannot be resolved."""


def current_week_range(anchor: date) -> tuple[date, date]:
    start = anchor - timedelta(days=anchor.weekday())
    end = start + timedelta(days=6)
    return start, end


def parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def filter_week(rows: list[dict[str, str]], start: date, end: date) -> list[dict[str, str]]:
    filtered = []
    for row in rows:
        row_date = parse_date(row.get("date", ""))
        if row_date and start <= row_date <= end:
            filtered.append(row)
    return filtered


def parse_anchor_date(value: str | None, timezone_name: str | None) -> date:
    if value:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ReportError(f"Invalid --date value: {value}. Expected YYYY-MM-DD.") from exc
    if not timezone_name:
        return date.today()
    if ZoneInfo is None:
        raise ReportError("Timezone support requires Python 3.9+ zoneinfo.")
    try:
        return datetime.now(ZoneInfo(timezone_name)).date()
    except ZoneInfoNotFoundError as exc:
        raise ReportError(f"Unknown timezone: {timezone_name}") from exc


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


def format_daily_average(totals: dict[str, float], meal_days: list[str], unit: str) -> str:
    if not meal_days or len(totals) < len(meal_days):
        return "Not enough nutrition data for a reliable average."
    values = [totals[day] for day in meal_days]
    return f"{mean(values):.1f} {unit} per logged meal day (rough estimate)"


def generate_report(root: Path, anchor: date) -> Path:
    data_dir = root / "data"
    reports_dir = root / "reports"
    reports_dir.mkdir(exist_ok=True)

    start, end = current_week_range(anchor)
    iso_year, iso_week, _ = anchor.isocalendar()

    nutrition = filter_week(read_csv(data_dir / "nutrition.csv"), start, end)
    training = filter_week(read_csv(data_dir / "training.csv"), start, end)
    body_metrics = filter_week(read_csv(data_dir / "body_metrics.csv"), start, end)

    training_sessions = {(row.get("date"), row.get("session_type"), row.get("raw_text")) for row in training}
    session_counts = Counter(row.get("session_type") or "unknown" for row in training)
    meal_days = sorted({row.get("date") for row in nutrition if row.get("date")})
    calories_by_day = daily_totals(nutrition, "calories_kcal")
    protein_by_day = daily_totals(nutrition, "protein_g")
    body_metric_names = Counter(row.get("metric_name") or "unknown" for row in body_metrics)

    session_lines = "\n".join(f"- {name}: {count}" for name, count in sorted(session_counts.items())) or "- No training rows recorded."
    metric_lines = "\n".join(f"- {name}: {count}" for name, count in sorted(body_metric_names.items())) or "- No body metric rows recorded."

    report = f"""# {iso_year}-W{iso_week:02d} Weekly Health Log

Period: {start.isoformat()} to {end.isoformat()}

## Overview

- Training sessions: {len(training_sessions)}
- Training exercise rows: {len(training)}
- Meal logging days: {len(meal_days)}
- Nutrition rows: {len(nutrition)}
- Body metrics rows: {len(body_metrics)}

## Training

Session type distribution:

{session_lines}

## Nutrition

- Average daily calories across logged meal days: {format_daily_average(calories_by_day, meal_days, "kcal")}
- Average daily protein across logged meal days: {format_daily_average(protein_by_day, meal_days, "g")}
- Note: rough or missing estimates are expected in MVP.

## Body Status

{metric_lines}

## Notes

- Treat nutrition estimates as rough.
- Missing workout fields can still be useful when raw text is preserved.
- Pain, injury, disease, medication, extreme dieting, or urgent symptoms should trigger `safety_boundary`.

## Next Week Suggestions

- Keep logging in short natural language messages.
- For key lifts, include weight, reps, and set count when convenient.
- For meals, include rough quantity when easy.
- Review trends only when enough local data exists.

## Disclaimer

This report is for logging and reflection only. It is not medical advice, diagnosis, treatment, or injury rehabilitation guidance.
"""

    output_path = reports_dir / f"{iso_year}-W{iso_week:02d}.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a weekly health log report.")
    parser.add_argument("--date", help="Generate the report for the week containing YYYY-MM-DD.")
    parser.add_argument("--timezone", help="IANA timezone used to resolve the current date, for example Asia/Tokyo.")
    return parser.parse_args()


def main() -> int:
    root = Path.cwd()
    args = parse_args()
    try:
        anchor = parse_anchor_date(args.date, args.timezone)
        output_path = generate_report(root, anchor)
    except (OSError, ReportError) as exc:
        print(f"Error: {exc}")
        return 1
    print(f"Weekly report written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
