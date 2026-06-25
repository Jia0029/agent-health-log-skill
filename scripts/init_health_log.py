#!/usr/bin/env python3
"""Initialize local private health log files for Agent Health Log Skill."""

from __future__ import annotations

import csv
from pathlib import Path


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


def create_csv_if_missing(path: Path, header: list[str]) -> bool:
    """Create a CSV with a header if it does not already exist."""
    if path.exists():
        return False

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
    return True


def main() -> None:
    root = Path.cwd()

    data_dir = root / "data"
    daily_dir = root / "daily"
    reports_dir = root / "reports"

    for directory in (data_dir, daily_dir, reports_dir):
        directory.mkdir(exist_ok=True)

    created = {
        "nutrition": create_csv_if_missing(data_dir / "nutrition.csv", NUTRITION_HEADER),
        "training": create_csv_if_missing(data_dir / "training.csv", TRAINING_HEADER),
        "body_metrics": create_csv_if_missing(data_dir / "body_metrics.csv", BODY_METRICS_HEADER),
    }

    print("Initialized Agent Health Log local files.")
    for name, was_created in created.items():
        status = "created" if was_created else "already exists"
        print(f"- {name}: {status}")


if __name__ == "__main__":
    main()

