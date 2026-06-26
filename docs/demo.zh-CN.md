# Demo 示例

[English](demo.md) | [简体中文](demo.zh-CN.md)

所有示例都是脱敏样例，不包含真实个人健康数据。

## 1. 饮食记录 Demo

用户输入：

```text
早餐两个鸡蛋，一杯拿铁。
```

Agent 应生成的结构化 JSON：

```json
{
  "type": "meal_log",
  "date": "today",
  "meals": [
    {
      "meal_time": "breakfast",
      "items": [
        {
          "name": "egg",
          "display_name": "鸡蛋",
          "quantity": "2个",
          "nutrition_estimate": {
            "calories_kcal": 140,
            "protein_g": 12,
            "carbs_g": 1,
            "fat_g": 10,
            "confidence": "medium"
          }
        },
        {
          "name": "latte",
          "display_name": "拿铁",
          "quantity": "1杯",
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
  ],
  "raw_text": "早餐两个鸡蛋，一杯拿铁。",
  "needs_follow_up": false
}
```

写入 CSV / Markdown 的效果：向 `nutrition.csv` 追加两行。

面向用户的简短确认：

```text
已记录早餐：两个鸡蛋和一杯拿铁。拿铁的营养估算标记为低置信度。
```

## 2. 训练记录 Demo

用户输入：

```text
今天练背，硬拉 80kg 5x5。
```

Agent 应生成的结构化 JSON：

```json
{
  "type": "workout_log",
  "date": "today",
  "session_type": "pull",
  "focus": "背",
  "exercises": [
    {
      "exercise_id": "deadlift",
      "display_name": "硬拉",
      "sets": [
        {
          "weight_kg": 80,
          "reps": 5,
          "set_count": 5
        }
      ],
      "rpe": null,
      "notes": null
    }
  ],
  "raw_text": "今天练背，硬拉 80kg 5x5。",
  "needs_follow_up": false
}
```

写入 CSV / Markdown 的效果：向 `training.csv` 追加一行。

面向用户的简短确认：

```text
已记录硬拉：80kg，5 组，每组 5 次。
```

## 3. 饮食 + 训练混合输入 Demo

用户输入：

```text
午饭吃了鸡胸肉饭，晚上练胸，卧推 60kg 4 组 8 次。
```

Agent 应生成的结构化 JSON：

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

写入 CSV / Markdown 的效果：饮食写入 `nutrition.csv`，训练写入 `training.csv`。

面向用户的简短确认：

```text
已同时记录午饭和卧推训练。
```

## 4. 睡眠 / 身体状态 Demo

用户输入：

```text
昨晚睡了 6 小时，今天精神一般。
```

Agent 应生成的结构化 JSON：

```json
{
  "type": "body_metrics_log",
  "date": "today",
  "metrics": {
    "sleep_hours": 6,
    "energy_level": "一般"
  },
  "raw_text": "昨晚睡了 6 小时，今天精神一般。",
  "needs_follow_up": false
}
```

写入 CSV / Markdown 的效果：向 `body_metrics.csv` 追加睡眠和精力状态两行。

面向用户的简短确认：

```text
已记录睡眠时长和今天的精神状态。
```

## 5. 训练历史查询 Demo

用户输入：

```text
最近硬拉有没有进步？
```

Agent 应生成的结构化 JSON：

```json
{
  "type": "query",
  "query_kind": "exercise_progress",
  "exercise_id": "deadlift",
  "display_name": "硬拉",
  "time_range": {
    "preset": "recent",
    "days": null
  },
  "metrics": ["top_weight", "volume", "recent_sessions"],
  "raw_text": "最近硬拉有没有进步？",
  "needs_follow_up": false
}
```

写入 CSV / Markdown 的效果：不写入 CSV。Agent 应读取本地训练记录后回答。

面向用户的简短确认：

```text
我会读取本地硬拉记录，并总结最近趋势。
```

## 6. 周报生成 Demo

用户输入：

```text
帮我生成这周饮食和训练周报。
```

Agent 应生成的结构化 JSON：

```json
{
  "type": "weekly_review_request",
  "date_anchor": "today",
  "period": {
    "preset": "current_week"
  },
  "sections": ["training_frequency", "meal_logging_coverage", "nutrition_estimate_summary", "next_week_suggestions"],
  "raw_text": "帮我生成这周饮食和训练周报。",
  "needs_follow_up": false
}
```

写入 CSV / Markdown 的效果：读取 CSV，并生成 `reports/YYYY-WXX.md`。

面向用户的简短确认：

```text
已生成本周健康记录周报。
```

## 7. 安全边界 Demo

用户输入：

```text
我膝盖疼，还能不能继续深蹲？
```

Agent 应生成的结构化 JSON：

```json
{
  "type": "safety_boundary",
  "category": "medical_or_injury_advice",
  "related_exercise_id": "squat",
  "should_log_as_note": true,
  "note": {
    "date": "today",
    "text": "用户提到膝盖疼，询问是否继续深蹲。"
  },
  "response_policy": {
    "do_not_provide_diagnosis": true,
    "do_not_prescribe_training_plan": true,
    "suggest_professional_help": true,
    "allowed_response": "可以记录疼痛和训练状态，但不要替代医生或物理治疗师判断。若疼痛持续、加重或影响动作，应停止相关动作并咨询专业人士。"
  },
  "raw_text": "我膝盖疼，还能不能继续深蹲？",
  "needs_follow_up": false
}
```

写入 CSV / Markdown 的效果：可以把安全边界备注写入 `body_metrics.csv`。

面向用户的简短确认：

```text
已记录膝盖疼痛备注。我不能诊断原因或制定康复计划；如果疼痛持续、加重或影响动作，请停止相关动作并咨询专业人士。
```

