# Installation

[English](install.md) | [简体中文](install.zh-CN.md)

This guide explains how to install Agent Health Log Skill for common Agent Skills-compatible tools.

## Universal Agent Skills Install

For OpenAI Codex, VS Code Agent Mode, and other tools that read `~/.agents/skills/`:

```bash
git clone https://github.com/Jia0029/agent-health-log-skill.git
cd agent-health-log-skill

python scripts/install_skill.py --target agents-user
python ~/.agents/skills/agent-health-log/scripts/healthlog.py init
```

## OpenAI Codex User-Level Install

```bash
python scripts/install_skill.py --target agents-user
```

Installed path:

```text
~/.agents/skills/agent-health-log/
```

In Codex, use `/skills` to check availability. You can explicitly mention `$agent-health-log` to force the skill.

## OpenAI Codex Project-Level Install

From your project root:

```bash
python /path/to/agent-health-log-skill/scripts/install_skill.py --target agents-project
```

Installed path:

```text
.agents/skills/agent-health-log/
```

## Claude Code Personal Install

```bash
python scripts/install_skill.py --target claude-personal
python ~/.claude/skills/agent-health-log/scripts/healthlog.py init
```

Installed path:

```text
~/.claude/skills/agent-health-log/
```

## Claude Code Project-Level Install

From your project root:

```bash
python /path/to/agent-health-log-skill/scripts/install_skill.py --target claude-project
```

Installed path:

```text
.claude/skills/agent-health-log/
```

## VS Code Agent Mode Project Install

From your project root:

```bash
python /path/to/agent-health-log-skill/scripts/install_skill.py --target vscode-project
```

Installed path:

```text
.agents/skills/agent-health-log/
```

## Confirm Availability

- Codex: run `/skills` and look for `agent-health-log`.
- Claude Code: use `/agent-health-log` explicitly.
- Generic agents: check the configured skill directory.

## Manual Trigger

```text
Use agent-health-log to record: breakfast was two eggs and a latte.
```

Codex explicit trigger:

```text
$agent-health-log record: today I trained back, deadlift 80kg 5x5.
```

Claude Code explicit trigger:

```text
/agent-health-log breakfast was two eggs and a latte.
```

## Automatic Trigger

Implicit invocation depends on the host agent and model. It usually works best after the skill has been indexed and the user mentions meals, workouts, sleep, soreness, weekly review, or exercise history.

## Uninstall

Remove the installed skill directory:

```bash
rm -rf ~/.agents/skills/agent-health-log
rm -rf ~/.claude/skills/agent-health-log
```

For project-level installs, remove:

```bash
rm -rf .agents/skills/agent-health-log
rm -rf .claude/skills/agent-health-log
```

## Data Location

Real health data is stored outside the skill package by default:

```text
~/.agent-health-log/
```

## Change Data Directory

```bash
python ~/.agents/skills/agent-health-log/scripts/healthlog.py --data-dir /path/to/private-health-log init
```

## FAQ

### Should I commit `~/.agent-health-log/`?

No. Keep real health records private.

### Does this provide medical advice?

No. It logs and summarizes. Medical or injury-adjacent input should trigger `safety_boundary`.

### Can I use it without Codex?

Yes. Any agent that can read a skill folder and run local scripts can use it.

