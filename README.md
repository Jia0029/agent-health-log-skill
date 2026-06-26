# Agent Health Log Skill

[English](README.md) | [简体中文](README.zh-CN.md)

> Status: v0.1 experimental MVP. This project is an early local-first skill package for LLM agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Local First](https://img.shields.io/badge/local--first-yes-brightgreen)
![Agent Skill](https://img.shields.io/badge/agent--skill-experimental-blue)
![Languages](https://img.shields.io/badge/languages-English%20%7C%20Chinese-lightgrey)

Agent Health Log Skill is a local-first health logging skill for OpenAI Codex, Claude Code, VS Code Agent Mode, and other Agent Skills-compatible tools.

It lets users record meals, workouts, body metrics, sleep, soreness, weekly health reviews, and exercise progress queries in natural language. Agents parse the input into structured JSON, preserve `raw_text`, and use local scripts to write CSV / Markdown records.

This is not a traditional fitness app. It is not a medical tool. It does not provide diagnosis, treatment, injury rehabilitation plans, medication advice, or extreme dieting guidance.

## Quick Start

### Universal Agent Skill install, recommended

For OpenAI Codex, VS Code Agent Mode, and other Agent Skills-compatible tools:

```bash
git clone https://github.com/Jia0029/agent-health-log-skill.git
cd agent-health-log-skill

python scripts/install_skill.py --target agents-user
python ~/.agents/skills/agent-health-log/scripts/healthlog.py init
```

Then ask your agent:

```text
Use agent-health-log to record: breakfast was two eggs and a latte. Today I trained back, deadlift 80kg 5x5.
```

In Codex, use `/skills` to check availability, or mention `$agent-health-log` explicitly when you want to force the skill.

### Claude Code install

```bash
git clone https://github.com/Jia0029/agent-health-log-skill.git
cd agent-health-log-skill

python scripts/install_skill.py --target claude-personal
python ~/.claude/skills/agent-health-log/scripts/healthlog.py init
```

Then in Claude Code:

```text
/agent-health-log Breakfast was two eggs and a latte. Today I trained back, deadlift 80kg 5x5.
```

### Developer / CLI mode

Use this mode to test schemas, scripts, and local write behavior:

```bash
python skills/agent-health-log/scripts/healthlog.py init
python skills/agent-health-log/scripts/healthlog.py write-stdin
python skills/agent-health-log/scripts/healthlog.py report weekly
```

By default, real local health data is stored under:

```text
~/.agent-health-log/
```

Override it with:

```bash
python skills/agent-health-log/scripts/healthlog.py --data-dir ./private-health-log init
```

## What It Logs

- Meals and drinks
- Workouts, exercises, sets, reps, weight, RPE, and notes
- Sleep and body metrics
- Soreness and general body-state notes
- Mixed meal + workout inputs
- Exercise history queries
- Weekly health reviews
- Safety-boundary notes for medical or injury-adjacent input

## What You Get After Logging

The value is not just storing rows. Once meals, workouts, sleep, and body-state notes accumulate locally, an agent can turn them into:

- Weekly review summaries
- Exercise progress snapshots
- Meal logging coverage
- Rough calorie and protein trends
- Sleep and energy context
- CSV data ready for charts or dashboards
- Markdown reports that can be kept in Obsidian, Git, or any local notes workflow

See [Outcome Showcase](examples/outcome-showcase.md) and [Demo](docs/demo.md) for sanitized examples of weekly reviews, trend tables, and visualization-ready data.

## Repository Layout

```text
skills/agent-health-log/     # Installable skill package
scripts/install_skill.py     # Installer for common agent skill paths
scripts/                     # Developer/debug scripts
schemas/                     # JSON Schema Draft 2020-12
references/                  # Food basics, exercise aliases, safety rules
examples/                    # Sanitized examples
tests/                       # Parser test cases
docs/                        # English and Simplified Chinese docs
```

## Documentation

- [Installation](docs/install.md)
- [Compatibility](docs/compatibility.md)
- [Demo](docs/demo.md)
- [Outcome Showcase](examples/outcome-showcase.md)
- [Promotion Guide](docs/promotion.md)
- [Privacy](PRIVACY.md)
- [Safety](SAFETY.md)

## Developer / Debug Mode

Initialize local files in the repository working directory:

```bash
python scripts/init_health_log.py
```

Write a structured meal record:

```bash
echo '{"type":"meal_log","date":"today","meals":[{"meal_time":"breakfast","items":[{"name":"egg","display_name":"Egg","quantity":"2","nutrition_estimate":{"calories_kcal":140,"protein_g":12,"carbs_g":1,"fat_g":10,"confidence":"medium"}}]}],"raw_text":"breakfast was two eggs","needs_follow_up":false}' | python scripts/write_record.py --timezone Asia/Tokyo
```

Generate a weekly report:

```bash
python scripts/generate_weekly_report.py --timezone Asia/Tokyo
```

Validate parser test cases:

```bash
python scripts/validate_test_cases.py
```

## Privacy

Agent Health Log Skill is local-first. Do not commit real meal logs, workout logs, body weight, sleep records, injury notes, medical details, or full chat logs to GitHub.

The repository `.gitignore` excludes common private data paths such as `data/`, `daily/`, `reports/`, `private/`, `personal/`, `*.sqlite`, and `*.db`.

## Safety

This project is for logging and reflection only. If the user mentions pain, injury, disease, medication, extreme dieting, eating disorder risk, fainting, chest pain, breathing difficulty, or other urgent symptoms, agents should trigger `safety_boundary`, record only factual notes, and suggest consulting a qualified professional.

## Roadmap

- v0.1: Installable skill package, bilingual docs, CSV/Markdown storage, schemas, examples, parser tests
- v0.2: Better exercise and food normalization, query helpers
- v0.3: SQLite and import/export
- v0.4: Local dashboard and charts
- Future: Photo-based meal estimation, wearable integration, more agent integrations, multi-language docs

## License

MIT License. See [LICENSE](LICENSE).
