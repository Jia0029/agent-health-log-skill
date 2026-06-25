# Integrations

Agent Health Log Skill is entry-point agnostic. It does not require a specific chat app, IDE, or agent vendor.

## Generic Agent Usage

Any agent can use this project if it can:

1. Receive natural language from the user.
2. Produce structured JSON.
3. Read and write local files.
4. Run local scripts when needed.

## Codex Usage

Codex can read `SKILL.md`, parse user input, write local records with `scripts/write_record.py`, and generate weekly reports with `scripts/generate_weekly_report.py`.

## CodexBridge Usage

CodexBridge can forward messages from a chat entry point to Codex or another local agent. The agent then uses this repository as the local logging layer.

## DeepSeek / Claude Code / Cursor Usage

DeepSeek, Claude Code, Cursor, or similar coding agents can use the same schemas and scripts. They do not need Codex-specific features as long as they can operate on local files.

## Feishu Bot Idea

A Feishu bot can receive messages such as "午饭吃了鸡胸肉饭" and pass them to an agent. The agent writes local files and returns a short confirmation.

## WeChat Bot Idea

A WeChat bot can provide a low-friction mobile input surface. The repository still stores data locally; the bot only acts as an input bridge.

## Obsidian / Markdown Workflow

Users who prefer Obsidian can keep `daily/` and `reports/` as Markdown folders. Structured CSV files can remain in `data/` for analysis and report generation.

## Implementation Boundary

This repository does not provide full implementations for every platform. Integrations only need to connect user messages to an agent that can read and write this local project.

