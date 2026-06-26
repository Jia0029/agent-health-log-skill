# Agent Health Log Skill

[English](README.md) | [简体中文](README.zh-CN.md)

> 状态：v0.1 experimental MVP。这是一个早期的、本地优先的 LLM Agent Skill 包。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Local First](https://img.shields.io/badge/local--first-yes-brightgreen)
![Agent Skill](https://img.shields.io/badge/agent--skill-experimental-blue)
![Languages](https://img.shields.io/badge/languages-English%20%7C%20Chinese-lightgrey)

一个给 OpenAI Codex、Claude Code、VS Code Agent Mode 和其他兼容 Agent Skills 的本地优先健康记录 Skill。

它不是传统健身 App，而是给 AI Agent 使用的本地健康记录能力。用户安装后，可以用自然语言记录饮食、训练、睡眠、身体状态、酸痛、训练历史查询和每周健康复盘。Agent 负责把自然语言解析成结构化 JSON，保留 `raw_text`，再通过本地脚本写入 CSV / Markdown。

本项目不是医疗工具，不提供医疗诊断、治疗方案、伤病康复计划、用药建议或极端饮食方案。

## 快速开始

### 方式一：通用 Agent Skill 安装，推荐

适用于 OpenAI Codex、VS Code Agent Mode 以及其他兼容 Agent Skills 的工具。

```bash
git clone https://github.com/Jia0029/agent-health-log-skill.git
cd agent-health-log-skill

python scripts/install_skill.py --target agents-user
python ~/.agents/skills/agent-health-log/scripts/healthlog.py init
```

然后在 Agent 中输入：

```text
Use agent-health-log to record: 早餐两个鸡蛋，一杯拿铁。今天练背，硬拉 80kg 5x5。
```

在 Codex 中，可以用 `/skills` 检查 Skill 是否可用，也可以用 `$agent-health-log` 显式提到这个 Skill。

### 方式二：Claude Code 安装

```bash
git clone https://github.com/Jia0029/agent-health-log-skill.git
cd agent-health-log-skill

python scripts/install_skill.py --target claude-personal
python ~/.claude/skills/agent-health-log/scripts/healthlog.py init
```

然后在 Claude Code 中输入：

```text
/agent-health-log 早餐两个鸡蛋，一杯拿铁。今天练背，硬拉 80kg 5x5。
```

### 方式三：开发者 / CLI 模式

适合测试 schema、脚本和本地写入逻辑。

```bash
python skills/agent-health-log/scripts/healthlog.py init
python skills/agent-health-log/scripts/healthlog.py write-stdin
python skills/agent-health-log/scripts/healthlog.py report weekly
```

真实健康数据默认保存在：

```text
~/.agent-health-log/
```

如果想改数据目录，可以使用：

```bash
python skills/agent-health-log/scripts/healthlog.py --data-dir ./private-health-log init
```

## 可以记录什么

- 饮食和饮品
- 训练动作、重量、组数、次数、RPE 和备注
- 睡眠和身体状态
- 酸痛和恢复感受
- 一句话里同时包含饮食和训练的混合输入
- 某个动作的历史查询
- 每周健康复盘
- 涉及伤病或医疗风险时的安全边界备注

## 记录之后有什么用

这个项目的价值不只是“把数据存下来”。当饮食、训练、睡眠和身体状态持续沉淀在本地后，Agent 可以把它们整理成：

- 每周复盘总结
- 关键训练动作进步趋势
- 饮食记录覆盖率
- 粗略热量和蛋白质趋势
- 睡眠、精力和训练状态的关联线索
- 可视化面板可直接读取的 CSV 数据
- 可以放进 Obsidian、Git 或本地笔记系统的 Markdown 周报

可以查看 [效果展示](examples/outcome-showcase.md) 和 [Demo 示例](docs/demo.zh-CN.md)，里面有脱敏的周报、趋势表和可视化数据样例。

## 仓库结构

```text
skills/agent-health-log/     # 真正可安装的 Skill 包
scripts/install_skill.py     # 安装到常见 Agent Skill 路径
scripts/                     # 开发者 / 调试脚本
schemas/                     # JSON Schema Draft 2020-12
references/                  # 食物基础估算、动作别名、安全边界
examples/                    # 脱敏示例
tests/                       # parser 测试用例
docs/                        # 中英文文档
```

## 文档

- [安装说明](docs/install.zh-CN.md)
- [兼容性说明](docs/compatibility.zh-CN.md)
- [Demo 示例](docs/demo.zh-CN.md)
- [效果展示](examples/outcome-showcase.md)
- [宣传指南](docs/promotion.zh-CN.md)
- [隐私说明](PRIVACY.md)
- [安全边界](SAFETY.md)

## 开发者 / 调试模式

在仓库工作目录中初始化本地文件：

```bash
python scripts/init_health_log.py
```

写入一条结构化饮食记录：

```bash
echo '{"type":"meal_log","date":"today","meals":[{"meal_time":"breakfast","items":[{"name":"egg","display_name":"鸡蛋","quantity":"2个","nutrition_estimate":{"calories_kcal":140,"protein_g":12,"carbs_g":1,"fat_g":10,"confidence":"medium"}}]}],"raw_text":"早餐两个鸡蛋","needs_follow_up":false}' | python scripts/write_record.py --timezone Asia/Tokyo
```

生成周报：

```bash
python scripts/generate_weekly_report.py --timezone Asia/Tokyo
```

运行 parser 测试：

```bash
python scripts/validate_test_cases.py
```

## 隐私

Agent Health Log Skill 默认本地优先。不要把真实饮食、训练、体重、睡眠、伤病、医疗信息或完整聊天记录提交到 GitHub。

仓库默认 `.gitignore` 会忽略 `data/`、`daily/`、`reports/`、`private/`、`personal/`、`*.sqlite`、`*.db` 等常见私有数据路径。

## 安全边界

本项目只用于记录和复盘。如果用户提到疼痛、伤病、疾病、药物、极端节食、进食障碍风险、晕厥、胸痛、呼吸困难等情况，Agent 应触发 `safety_boundary`，只记录事实描述，并建议咨询专业人士。

## 路线图

- v0.1：可安装 Skill 包、中英双语文档、CSV / Markdown 存储、schema、示例和 parser 测试
- v0.2：改进动作和食物标准化，补充查询辅助能力
- v0.3：SQLite、导入 / 导出
- v0.4：本地 dashboard 和图表
- Future：图片饮食估算、可穿戴设备集成、更多 Agent 入口、多语言文档

## License

MIT License. See [LICENSE](LICENSE).
