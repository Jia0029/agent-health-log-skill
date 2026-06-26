# Outcome Showcase / 效果展示

All examples in this file are sanitized. They are not real personal health records.

本文件展示“记录这些东西有什么用”：自然语言记录会沉淀成本地结构化数据，之后可以用于周报、趋势分析和可视化。

## 1. From Natural Language To Local Records

User inputs:

```text
早餐两个鸡蛋，一杯拿铁。
今天练背，硬拉 80kg 5x5。
昨晚睡了 6 小时，今天精神一般。
```

Agent output:

- Append meal rows to `nutrition.csv`
- Append workout rows to `training.csv`
- Append sleep and energy rows to `body_metrics.csv`
- Preserve the original text as `raw_text`

Why it matters:

- Users do not need to open a complex app.
- Agents can still keep structured data.
- Future reviews can inspect both parsed fields and the original context.

## 2. Weekly Review Example

Generated from sanitized sample records:

```markdown
# 2026-W26 Weekly Health Log

## Overview

- Training days: 3
- Meal logging days: 5
- Body status notes: 4
- Key lift tracked: deadlift

## Training

- Pull: 2 sessions
- Push: 1 session
- Deadlift top set: 80kg x 5
- Bench press top set: 60kg x 8

## Nutrition

- Logged protein average: 92g/day, rough estimate
- Logged calories average: 2,050 kcal/day, rough estimate
- Meal coverage: 5/7 days
- Confidence: mixed, because restaurant meals are low-confidence estimates

## Recovery Context

- Sleep average: 6.6 hours on logged days
- Low-energy notes appeared after shorter sleep days

## Next Review Questions

- Did low-sleep days overlap with weaker training sessions?
- Is protein logging consistent enough for trend analysis?
- Which lift should be tracked as the next benchmark?
```

## 3. Trend Table Example

```markdown
| Date | Exercise | Top Set | Volume Estimate | Note |
| --- | --- | ---: | ---: | --- |
| 2026-06-10 | Deadlift | 75kg x 5 | 1,875kg | Baseline |
| 2026-06-17 | Deadlift | 80kg x 5 | 2,000kg | Improved |
| 2026-06-24 | Deadlift | 80kg x 5 | 2,000kg | Maintained |
```

What this tells the user:

- The lift improved once, then stabilized.
- The next review can focus on whether sleep, food, or training volume explains the plateau.

## 4. Visualization-Ready Data

The project does not need a dashboard in v0.1, but the CSV format is easy to feed into one later.

Line chart example:

```json
{
  "chart_type": "line",
  "title": "Deadlift Top Set",
  "x": ["2026-06-10", "2026-06-17", "2026-06-24"],
  "y": [75, 80, 80],
  "unit": "kg"
}
```

Bar chart example:

```json
{
  "chart_type": "bar",
  "title": "Meal Logging Coverage",
  "x": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  "y": [1, 1, 0, 1, 1, 1, 0],
  "unit": "logged_day"
}
```

Stacked summary example:

```json
{
  "chart_type": "stacked_bar",
  "title": "Training Session Distribution",
  "series": {
    "pull": [1],
    "push": [1],
    "legs": [1],
    "cardio": [0]
  },
  "x": ["2026-W26"]
}
```

## 5. User-Facing Value

For the user, the benefit is:

- Record in one sentence.
- Keep data local.
- Review weekly patterns.
- Spot missing logs.
- Track key exercise progress.
- Prepare data for charts without building a full app first.

中文总结：

- 用一句话记录饮食、训练、睡眠和身体状态。
- 数据默认保存在本地。
- 周报可以看到训练频率、饮食记录覆盖率、动作趋势和恢复线索。
- 后续要做 dashboard 或图表时，CSV 已经是可用的数据基础。

