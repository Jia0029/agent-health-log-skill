---
name: agent-health-log
description: Use this skill when the user wants to record meals, workouts, body metrics, or generate health log summaries from natural language. This skill is local-first and agent-agnostic. It stores structured records in Markdown, CSV, or SQLite-compatible formats while preserving raw user input and uncertainty.
---

# Agent Health Log

## Purpose

Use this skill to turn natural language health logs into local, structured records. Focus on low-friction meal logging, workout logging, body metrics, queries, weekly reviews, and safety boundaries.

## When To Use This Skill

Use this skill when the user wants to:

- Record meals, snacks, drinks, or rough nutrition.
- Record workouts, exercises, sets, reps, weights, RPE, cardio, or training notes.
- Record body metrics such as sleep, energy, soreness, pain notes, or other status.
- Parse mixed meal and workout input from one message.
- Query exercise history or nutrition trends from local records.
- Generate weekly or monthly reviews from local records.
- Handle injury, pain, disease, medication, extreme dieting, or other medical-adjacent messages safely.

## When Not To Use This Skill

Do not use this skill to:

- Diagnose disease or injury.
- Provide medical treatment decisions.
- Replace a doctor, dietitian, physical therapist, or rehabilitation professional.
- Create injury rehabilitation plans.
- Recommend extreme diets or unsafe weight-loss behavior.
- Upload real personal health records to public repositories.

## Core Principles

- Log with minimal friction.
- Record first; ask follow-up only when necessary.
- Preserve `raw_text` for every record.
- Keep data local-first and user-owned.
- Mark uncertainty and confidence.
- Allow incomplete but useful records.
- Do not provide medical diagnosis.
- Treat public examples and tests as sanitized data only.

## Intent Classification Rules

Classify each message into one primary intent:

- `meal`: food, drink, meal time, rough nutrition.
- `workout`: exercise, training session, sets, reps, weight, RPE, cardio.
- `mixed`: one message contains both meal and workout information.
- `body_metrics`: sleep, energy, soreness, body state, non-public body metrics.
- `query`: asks for history, progress, trend, or lookup.
- `weekly_review`: asks for a weekly summary or review.
- `safety_boundary`: mentions pain, injury, disease, medication, extreme dieting, eating disorder risk, fainting, chest pain, breathing difficulty, or other high-risk health issues.

If a message includes both normal logging and safety-boundary content, include a safety boundary response and log only safe factual notes.

## Writable And Request Intents

Treat these as writable records:

- `meal_log`
- `workout_log`
- `mixed_log`
- `body_metrics_log`
- `safety_boundary`

Treat these as request intents:

- `query`
- `weekly_review_request`

Do not write `query` or `weekly_review_request` to CSV. Use them to read local data and generate a response or report.

## Meal Logging Workflow

1. Determine `date`; convert `today` / `yesterday` before storage.
2. Infer `meal_time` when possible: breakfast, lunch, dinner, snack, unknown.
3. Extract food and drink items.
4. Extract quantities if present.
5. Estimate rough nutrition only when reasonable.
6. Use `null` for uncertain nutrition values.
7. Set confidence: `high`, `medium`, or `low`.
8. Preserve `raw_text`.
9. Write to local CSV only after generating structured JSON.

For restaurants, social meals, hot pot, vague meals, or unclear portions, prefer `confidence: low` and avoid forced macro estimates.

## Workout Logging Workflow

1. Determine `date`.
2. Infer `session_type`: push, pull, legs, cardio, core, full_body, mobility, unknown.
3. Normalize exercise names with `references/exercise-aliases.json` when available.
4. Parse weight, reps, set count, RPE, and notes.
5. Allow missing weight, reps, set count, and RPE to be `null`.
6. Preserve `raw_text`.
7. Write one CSV row per exercise/set pattern.

Do not ask for RPE or exact rest time if the record is already useful.

## Mixed Input Workflow

If the same message includes meals and training, produce:

- `type: mixed_log`
- `meal_log`
- `workout_log`
- shared `date`
- shared `raw_text`

Write the meal rows and workout rows separately after validation.

## Body Metrics Workflow

Body metrics can include sleep, energy, soreness, mood, pain notes, or private measurements. In public examples, do not include real body weight, sensitive medical details, or identifying information.

Use `body_metrics_log` for simple factual records. Use `safety_boundary` for pain, injury, disease, medication, extreme dieting, eating disorder risk, or dangerous symptoms.

## Query Workflow

When the user asks about history or progress:

1. Produce a structured query object.
2. Treat it as a request intent, not a writable record.
3. Read local data before answering.
4. Do not answer from memory.
5. State uncertainty if records are sparse or missing.

Example query targets: exercise progress, recent sessions, training frequency, nutrition trend, meal logging coverage.

## Weekly Review Workflow

1. Treat `weekly_review_request` as a request intent, not a writable record.
2. Resolve the week date range.
3. Read local `nutrition.csv`, `training.csv`, and `body_metrics.csv`.
4. Summarize training frequency.
5. Summarize muscle/session-type distribution.
6. Summarize key exercise trends when enough data exists.
7. Summarize meal logging coverage.
8. Summarize rough nutrition only when data is sufficient.
9. Add safety-aware notes and next-week suggestions.

Keep suggestions conservative and habit-focused.

## Follow-Up Question Policy

Record without follow-up when the message contains a useful record:

- "硬拉 80kg 5x5" is useful without RPE.
- "晚上吃了火锅，粗略记一下" is useful as a low-confidence meal.
- "今天练腿，深蹲做了几组，状态一般" is useful as an incomplete workout note.

Ask follow-up only when no useful structured record can be formed:

- "今天吃得挺多" should ask which meal and what main foods.
- "帮我记一下训练" should ask what exercise or session was done.

## Safety And Medical Boundary

Trigger `safety_boundary` for:

- Pain
- Injury
- Disease
- Medication
- Extreme dieting
- Eating disorder risk
- High-risk weight loss by minors
- Fainting
- Chest pain
- Breathing difficulty
- Any urgent or dangerous symptom

Allowed:

- Record the user's description.
- Suggest stopping an obviously pain-triggering movement.
- Suggest consulting a doctor, dietitian, physical therapist, or qualified professional.
- Encourage safe, moderate, long-term logging habits.

Not allowed:

- Diagnose injury or disease.
- Prescribe medication or treatment.
- Create injury rehabilitation plans.
- Tell the user to train through pain.
- Give extreme diet plans.

## Storage Rules

- Convert `today` / `yesterday` to `YYYY-MM-DD` before storage.
- Preserve `raw_text` in every record.
- Write incomplete but useful records.
- Store unknown numeric values as `null` in JSON and empty strings in CSV.
- Join tags with `;` in CSV.
- Do not commit real health data to GitHub.

## Output Format

1. Generate structured JSON.
2. Validate against the relevant schema if available.
3. For writable records, write to local files.
4. For request intents, read local files and answer or generate a report.
5. Confirm briefly to the user.

## Examples

Use `examples/sample-scenarios.md` and `tests/parser-test-cases.json` for representative sanitized examples:

- Simple meal
- Fuzzy meal
- Simple workout
- Complex workout
- Mixed meal and workout
- Exercise progress query
- Weekly review
- Missing fields but recordable
- Needs follow-up
- Safety boundary
- Body metrics
