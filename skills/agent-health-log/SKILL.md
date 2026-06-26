---
name: agent-health-log
description: Log meals, workouts, body metrics, sleep, soreness, exercise progress, and weekly health reviews from natural language, including English and Chinese inputs. Use when the user says they ate, drank, trained, lifted, ran, slept, 记录饮食, 记录训练, 睡眠, 身体状态, 周报, or asks about workout history. Local-first. Does not provide medical diagnosis, treatment, injury rehab, medication advice, or extreme dieting guidance.
---

# Agent Health Log

## Purpose

Use this skill to turn natural-language health notes into local structured records. Support low-friction logging for meals, workouts, body metrics, sleep, soreness, exercise progress queries, and weekly reviews.

Default private data directory: `~/.agent-health-log/`.

## Core Principles

- Record first; ask follow-up only when a useful record cannot be formed.
- Preserve `raw_text` in every structured record.
- Keep real health data local and out of Git.
- Mark uncertainty and confidence.
- Allow incomplete but useful records.
- Treat nutrition estimates as rough.
- Do not provide diagnosis, treatment, injury rehabilitation plans, medication advice, or extreme dieting guidance.

## Intent Types

Writable records:

- `meal_log`
- `workout_log`
- `mixed_log`
- `body_metrics_log`
- `safety_boundary`

Request intents:

- `query`
- `weekly_review_request`

Do not write `query` or `weekly_review_request` to CSV. Read local records and answer, or generate a report.

## Workflow

1. Classify the user input.
2. Parse structured JSON with `raw_text`.
3. Normalize foods, exercises, dates, and uncertainty where possible.
4. For writable records, call `scripts/healthlog.py write-stdin` with the JSON on stdin.
5. For weekly reviews, call `scripts/healthlog.py report weekly`.
6. Confirm briefly to the user.

## Meal Logging

Extract meal time, food names, quantity, rough nutrition, confidence, and tags. Use `null` for uncertain nutrition fields. For restaurant meals, social meals, hot pot, or unclear portions, use low confidence.

## Workout Logging

Extract session type, focus, exercise names, weight, reps, set count, RPE, notes, and raw text. Normalize exercise IDs with `references/exercise-aliases.json` when helpful. Missing weight, reps, set count, and RPE may be `null`.

## Body Metrics

Record sleep, energy, soreness, and body-state notes as body metrics. Do not include real sensitive health data in public examples.

## Safety Boundary

Trigger `safety_boundary` for pain, injury, disease, medication, extreme dieting, eating disorder risk, fainting, chest pain, breathing difficulty, or other urgent symptoms.

Allowed:

- Record the user's description as a note.
- Suggest stopping obviously pain-triggering activity.
- Suggest consulting a qualified professional.

Not allowed:

- Diagnose.
- Prescribe treatment or medication.
- Create injury rehabilitation plans.
- Encourage training through pain.
- Give extreme dieting plans.

## Chinese Trigger Examples

Use this skill for Chinese inputs such as:

- "早餐两个鸡蛋，一杯拿铁。"
- "今天练背，硬拉 80kg 5x5。"
- "昨晚睡了 6 小时，今天精神一般。"
- "帮我生成这周饮食和训练周报。"
- "最近卧推有没有进步？"
- "我膝盖疼，还能不能继续深蹲？" should trigger `safety_boundary`.

## CLI

Initialize local files:

```bash
python scripts/healthlog.py init
```

Write a structured JSON record from stdin:

```bash
python scripts/healthlog.py write-stdin
```

Generate a weekly report:

```bash
python scripts/healthlog.py report weekly
```

Use `--data-dir PATH` before the subcommand to override `~/.agent-health-log/`.

