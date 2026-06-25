# Architecture

Agent Health Log Skill uses a local-first pipeline. The agent converts natural language into structured JSON, validates it, writes local files for writable records, and reads local files for request intents.

## High-Level Flow

```text
User message
  ↓
Agent / LLM
  ↓
Intent classification
  ↓
Structured JSON
  ↓
JSON Schema validation
  ↓
Writable record → local storage
Request intent → local read
  ↓
Query / Weekly report
```

## Components

### Natural Language Input

Users write short natural language messages. Inputs can be precise, fuzzy, or mixed:

- Meal only
- Workout only
- Body metrics
- Meal + workout
- Query
- Weekly review request
- Safety-boundary case

### Intent Classification

The agent assigns one intent before parsing. This keeps output predictable and lets downstream scripts decide whether to update CSV files or read local data.

### Structured JSON Parser

The parser produces one of:

- `meal_log`
- `workout_log`
- `mixed_log`
- `body_metrics_log`
- `query`
- `weekly_review_request`
- `safety_boundary`

All objects preserve `raw_text` and `needs_follow_up`.

Writable records:

- `meal_log`
- `workout_log`
- `mixed_log`
- `body_metrics_log`
- `safety_boundary`

Request intents:

- `query`
- `weekly_review_request`

Request intents are not written to CSV. `query` should read local data and answer. `weekly_review_request` should read local data and generate a report.

### JSON Schema Validation

Schemas in `schemas/` use JSON Schema Draft 2020-12. Validation should run before writing to local files when the host agent or integration has a schema validator available.

### Local Storage

MVP storage uses:

- Markdown for daily notes and weekly reports
- CSV for structured records
- Future SQLite-compatible shapes for more reliable queries

CSV files:

- `data/nutrition.csv`
- `data/training.csv`
- `data/body_metrics.csv`

### Reference Data

References improve normalization without requiring cloud services:

- `references/exercise-aliases.json`
- `references/food-basics.json`
- `references/nutrition-estimation-rules.md`
- `references/safety-boundaries.md`

### Weekly Report Generator

The weekly report script reads CSV data and produces a Markdown report with training frequency, session distribution, meal coverage, rough nutrition averages, body metrics notes, and next-week suggestions.

### Future Dashboard

A future local dashboard can read the same CSV or SQLite data and show:

- Calendar coverage
- Nutrition trends
- Exercise history
- Training frequency
- Weekly and monthly reviews

### Integration Layer

This project does not bind to one agent entry point. It can be used with:

- Codex
- CodexBridge
- DeepSeek
- Claude Code
- Cursor
- Feishu
- WeChat
- Generic local Agent

The integration only needs two capabilities:

1. Send user natural language to an agent.
2. Let the agent read and write local files or run local scripts.
