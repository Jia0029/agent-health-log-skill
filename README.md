# Agent Health Log Skill

> Status: v0.1 experimental MVP. This project is an early local-first skill package for LLM agents.

A local-first health logging skill for LLM agents.

Agent Health Log Skill is not a traditional fitness app. It is an agent-agnostic local health logging skill for Codex, DeepSeek, Claude Code, Cursor, CodexBridge, Feishu bots, WeChat bots, or any AI agent that can read and write local files.

The goal is simple: let users record meals, workouts, and body state in natural language, then let the agent classify intent, produce structured JSON, preserve `raw_text`, write local Markdown / CSV files, and support weekly or monthly review. Future versions can upgrade the same data model to SQLite.

This version is an experimental MVP. It is mainly for local logging and review. It does not provide medical advice, does not aim for precise nutrition estimation, and does not include a full app, cloud sync, or photo-based meal recognition.

## Why This Project

Traditional meal and workout apps often require too many taps, forms, and manual corrections. This project turns logging into a sentence:

```text
早餐一杯拿铁、两个鸡蛋、一片吐司。
今天练背，硬拉 80kg 5x5。
```

The agent handles structure, uncertainty, local storage, and review. The project is about low-friction logging, local data ownership, and periodic reflection. It is not about replacing coaches, doctors, dietitians, or physical therapists.

## Core Features

- Natural language meal logging
- Natural language workout logging
- Body metrics logging
- Mixed meal + workout input
- Local Markdown / CSV storage
- Weekly review
- Exercise history query
- Rough nutrition estimate with confidence
- Safety boundary for medical / injury cases

## MVP Scope

v0.1 experimental focuses on:

- Markdown / CSV storage
- JSON Schema Draft 2020-12
- Local Python scripts
- An agent-facing `SKILL.md`
- Sanitized examples
- Parser test cases

## Out of Scope for v0.1

- Precise nutrition database
- Medical advice
- Injury diagnosis
- Complete mobile app
- Automatic photo-based meal recognition
- Cloud sync

## Repository Structure

```text
agent-health-log-skill/
  README.md
  SKILL.md
  LICENSE
  .gitignore
  PRIVACY.md
  SAFETY.md
  docs/
  schemas/
  references/
  examples/
  tests/
  scripts/
```

## Quick Start

Initialize local private data files:

```bash
python scripts/init_health_log.py
```

Write a meal record:

```bash
echo '{"type":"meal_log","date":"today","meals":[{"meal_time":"breakfast","items":[{"name":"egg","display_name":"鸡蛋","quantity":"2个","nutrition_estimate":{"calories_kcal":140,"protein_g":12,"carbs_g":1,"fat_g":10,"confidence":"medium"}}]}],"raw_text":"早餐两个鸡蛋","needs_follow_up":false}' | python scripts/write_record.py --timezone Asia/Tokyo
```

Write a workout record:

```bash
echo '{"type":"workout_log","date":"today","session_type":"pull","focus":"背","exercises":[{"exercise_id":"deadlift","display_name":"硬拉","sets":[{"weight_kg":80,"reps":5,"set_count":5}],"rpe":null,"notes":null}],"raw_text":"今天练背，硬拉80kg 5x5","needs_follow_up":false}' | python scripts/write_record.py --timezone Asia/Tokyo
```

Generate the current weekly report:

```bash
python scripts/generate_weekly_report.py --timezone Asia/Tokyo
```

Run parser test validation:

```bash
python scripts/validate_test_cases.py
```

Use `--date YYYY-MM-DD` to anchor `today` / `yesterday` for reproducible tests, or `--timezone Area/City` to resolve the current date in a specific IANA timezone.

## Intent Types

Writable record intents:

- `meal_log`
- `workout_log`
- `mixed_log`
- `body_metrics_log`
- `safety_boundary`

Request intents:

- `query`
- `weekly_review_request`

`query` and `weekly_review_request` should not be written to CSV. They should trigger local data reads and produce an answer or report. `scripts/write_record.py` rejects request intents with a clear message.

## Example Inputs and Outputs

Input:

```text
午饭吃了鸡胸肉饭，晚上练胸，卧推 60kg 4 组 8 次。
```

Structured output:

```json
{
  "type": "mixed_log",
  "date": "today",
  "meal_log": {
    "meals": [
      {
        "meal_time": "lunch",
        "items": [
          {
            "name": "chicken_rice_bowl",
            "display_name": "鸡胸肉饭",
            "quantity": "1份",
            "nutrition_estimate": {
              "calories_kcal": null,
              "protein_g": null,
              "carbs_g": null,
              "fat_g": null,
              "confidence": "low"
            }
          }
        ]
      }
    ]
  },
  "workout_log": {
    "session_type": "push",
    "focus": "胸",
    "exercises": [
      {
        "exercise_id": "bench_press",
        "display_name": "杠铃卧推",
        "sets": [
          {
            "weight_kg": 60,
            "reps": 8,
            "set_count": 4
          }
        ],
        "rpe": null,
        "notes": null
      }
    ]
  },
  "raw_text": "午饭吃了鸡胸肉饭，晚上练胸，卧推 60kg 4 组 8 次。",
  "needs_follow_up": false
}
```

See [examples/sample-scenarios.md](examples/sample-scenarios.md) and [tests/parser-test-cases.json](tests/parser-test-cases.json) for more cases.

## Privacy Notice

This project is local-first. Real personal health data should stay in private local directories such as `data/`, `daily/`, `reports/`, `private/`, or `personal/`. These paths are ignored by default.

Do not commit real health records, body weight, injury details, medical information, addresses, contact details, or full chat logs to GitHub.

## Safety Disclaimer

This project is a logging and review tool. It does not provide medical diagnosis, disease treatment, injury rehabilitation plans, medication advice, or extreme dieting guidance. For pain, injury, disease, medication, fainting, chest pain, breathing difficulty, or eating disorder risk, trigger `safety_boundary` and recommend professional help.

## Roadmap

- v0.1: Skill instructions, schemas, CSV storage, examples, parser tests, minimal scripts
- v0.2: Better food basics, exercise aliases, weekly report generator, exercise history query
- v0.3: SQLite, stronger validation, import/export
- v0.4: Local dashboard and charts
- Future: Photo-based meal estimation, wearable integration, bot examples, Obsidian/Notion sync, multi-language support

## License

MIT License. See [LICENSE](LICENSE).
