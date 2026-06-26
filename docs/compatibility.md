# Compatibility

[English](compatibility.md) | [简体中文](compatibility.zh-CN.md)

Agent Health Log Skill follows an Agent Skills-style folder layout.

## Installable Skill Package

The installable skill package lives at:

```text
skills/agent-health-log/
```

This package includes:

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/healthlog.py`
- `references/`
- `schemas/`

## Recommended Paths

OpenAI Codex:

```text
~/.agents/skills/agent-health-log/
.agents/skills/agent-health-log/
```

Claude Code:

```text
~/.claude/skills/agent-health-log/
.claude/skills/agent-health-log/
```

VS Code Agent Mode project path:

```text
.agents/skills/agent-health-log/
```

## Implicit Invocation

Implicit invocation depends on the host agent and model. Some tools require explicit naming until the skill index is refreshed.

Recommended first-use triggers:

- Codex: `$agent-health-log`
- Claude Code: `/agent-health-log`
- Generic agents: `Use agent-health-log to ...`

## Local Data

Skill installation and personal data are separate. Real health data defaults to:

```text
~/.agent-health-log/
```

Do not store personal data inside the installed skill package.

