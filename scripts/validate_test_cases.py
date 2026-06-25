#!/usr/bin/env python3
"""Validate parser test cases against available schemas when possible."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:  # Optional dependency for v0.1.
    Draft202012Validator = None  # type: ignore[assignment]
    ValidationError = Exception  # type: ignore[assignment]


TYPE_TO_SCHEMA = {
    "meal_log": "meal-log.schema.json",
    "workout_log": "workout-log.schema.json",
    "mixed_log": "mixed-log.schema.json",
    "query": "query.schema.json",
    "weekly_review_request": "query.schema.json",
    "body_metrics_log": "body-metrics.schema.json",
    "safety_boundary": "safety-boundary.schema.json",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    root = Path.cwd()
    tests_path = root / "tests" / "parser-test-cases.json"
    schemas_dir = root / "schemas"

    try:
        test_cases = load_json(tests_path)
        schemas = {path.name: load_json(path) for path in sorted(schemas_dir.glob("*.schema.json"))}
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Failed to load test cases or schemas: {exc}", file=sys.stderr)
        return 1

    if Draft202012Validator is None:
        print("Optional dependency missing: jsonschema. Install with: pip install jsonschema")
        print("Running basic JSON and type mapping checks only.")

    total = len(test_cases)
    passed = 0
    failed = 0

    for case in test_cases:
        case_id = case.get("id", "<missing id>")
        expected = case.get("expected_structured_json")
        record_type = expected.get("type") if isinstance(expected, dict) else None
        schema_name = TYPE_TO_SCHEMA.get(record_type)

        if not schema_name:
            print(f"FAIL {case_id}: unknown or missing expected_structured_json.type: {record_type}")
            failed += 1
            continue

        schema = schemas.get(schema_name)
        if schema is None:
            print(f"FAIL {case_id}: missing schema file: {schema_name}")
            failed += 1
            continue

        if Draft202012Validator is not None:
            try:
                Draft202012Validator(schema).validate(expected)
            except ValidationError as exc:
                print(f"FAIL {case_id}: schema validation failed: {exc.message}")
                failed += 1
                continue

        print(f"PASS {case_id}: {record_type} -> {schema_name}")
        passed += 1

    print("")
    print("Summary")
    print(f"- total: {total}")
    print(f"- passed: {passed}")
    print(f"- failed: {failed}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

