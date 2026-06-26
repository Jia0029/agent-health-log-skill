# 安装说明

[English](install.md) | [简体中文](install.zh-CN.md)

本文说明如何把 Agent Health Log Skill 安装到常见的 Agent Skills 兼容工具中。

## 通用 Agent Skills 安装

适用于 OpenAI Codex、VS Code Agent Mode，以及其他读取 `~/.agents/skills/` 的工具：

```bash
git clone https://github.com/Jia0029/agent-health-log-skill.git
cd agent-health-log-skill

python scripts/install_skill.py --target agents-user
python ~/.agents/skills/agent-health-log/scripts/healthlog.py init
```

## OpenAI Codex 用户级安装

```bash
python scripts/install_skill.py --target agents-user
```

安装位置：

```text
~/.agents/skills/agent-health-log/
```

在 Codex 中，可以用 `/skills` 检查 Skill 是否可用。第一次使用时，建议用 `$agent-health-log` 显式触发。

## OpenAI Codex 项目级安装

在你的项目根目录执行：

```bash
python /path/to/agent-health-log-skill/scripts/install_skill.py --target agents-project
```

安装位置：

```text
.agents/skills/agent-health-log/
```

项目级安装适合只在某个项目里启用这个 Skill。

## Claude Code 个人级安装

```bash
python scripts/install_skill.py --target claude-personal
python ~/.claude/skills/agent-health-log/scripts/healthlog.py init
```

安装位置：

```text
~/.claude/skills/agent-health-log/
```

## Claude Code 项目级安装

在你的项目根目录执行：

```bash
python /path/to/agent-health-log-skill/scripts/install_skill.py --target claude-project
```

安装位置：

```text
.claude/skills/agent-health-log/
```

## VS Code Agent Mode 项目级安装

在你的项目根目录执行：

```bash
python /path/to/agent-health-log-skill/scripts/install_skill.py --target vscode-project
```

安装位置：

```text
.agents/skills/agent-health-log/
```

## 如何确认 Skill 是否可用

- Codex：运行 `/skills`，查看是否有 `agent-health-log`。
- Claude Code：尝试输入 `/agent-health-log`。
- 其他 Agent：检查对应的 skills 目录是否包含 `agent-health-log`。

## 如何手动触发 Skill

Codex：

```text
$agent-health-log 记录：早餐两个鸡蛋，一杯拿铁。
```

Claude Code：

```text
/agent-health-log 早餐两个鸡蛋，一杯拿铁。
```

通用写法：

```text
Use agent-health-log to record: 早餐两个鸡蛋，一杯拿铁。
```

## 如何让 Agent 自动触发 Skill

隐式自动调用取决于具体 Agent 和模型。一般来说，当用户提到饮食、训练、睡眠、身体状态、周报、动作历史查询时，Agent 更容易自动选择这个 Skill。

第一次使用时建议显式触发，确认工作流稳定后再依赖自动触发。

## 如何卸载

删除对应安装目录即可：

```bash
rm -rf ~/.agents/skills/agent-health-log
rm -rf ~/.claude/skills/agent-health-log
```

项目级安装则删除：

```bash
rm -rf .agents/skills/agent-health-log
rm -rf .claude/skills/agent-health-log
```

## 本地健康数据保存在哪里

真实健康数据默认保存在：

```text
~/.agent-health-log/
```

这个目录不在 Skill 安装包里，也不应该提交到 GitHub。

## 如何修改数据目录

可以通过 `--data-dir` 指定私有数据目录：

```bash
python ~/.agents/skills/agent-health-log/scripts/healthlog.py --data-dir /path/to/private-health-log init
```

之后写入和生成报告时也使用同一个 `--data-dir`。

## 常见问题

### 要不要把 `~/.agent-health-log/` 提交到 GitHub？

不要。这里保存的是真实健康记录，应该只留在本地。

### 这个项目会给医疗建议吗？

不会。它只做记录和复盘。涉及疼痛、伤病、疾病、药物、极端节食等情况时，应触发 `safety_boundary`。

### 不用 Codex 可以吗？

可以。只要你的 Agent 能读取 Skill 目录并执行本地脚本，就可以使用。

