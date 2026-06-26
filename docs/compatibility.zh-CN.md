# 兼容性说明

[English](compatibility.md) | [简体中文](compatibility.zh-CN.md)

本项目遵循 Agent Skills 风格的目录结构。

## 可安装 Skill 包

真正可安装的 Skill 包位于：

```text
skills/agent-health-log/
```

这个目录包含：

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/healthlog.py`
- `references/`
- `schemas/`

## 推荐路径

OpenAI Codex 推荐路径：

```text
~/.agents/skills/agent-health-log/
.agents/skills/agent-health-log/
```

Claude Code 推荐路径：

```text
~/.claude/skills/agent-health-log/
.claude/skills/agent-health-log/
```

VS Code Agent Mode 推荐项目路径：

```text
.agents/skills/agent-health-log/
```

## 隐式自动调用

隐式自动调用取决于具体 Agent 和模型。有些工具需要刷新 skill index，或者第一次使用时需要显式提到 Skill。

第一次使用时建议显式调用：

- Codex: `$agent-health-log`
- Claude Code: `/agent-health-log`
- 通用 Agent: `Use agent-health-log to ...`

## 本地数据

Skill 安装目录和真实健康数据目录是分开的。真实健康数据默认保存在：

```text
~/.agent-health-log/
```

不要把个人健康数据写进 Skill 安装目录，也不要提交到 GitHub。

