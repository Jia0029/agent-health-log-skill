# Real-World Workflow

This document summarizes the intended real-world workflow without publishing full chat logs or private user records.

## Common User Inputs

Users usually send short natural language messages:

- "早餐一杯拿铁、两个鸡蛋、一片吐司。"
- "晚上吃了火锅，帮我粗略记一下。"
- "今天练背，硬拉 80kg 5x5。"
- "午饭吃了鸡胸肉饭，晚上练胸，卧推 60kg 4 组 8 次。"
- "帮我看看最近硬拉有没有进步。"
- "帮我生成这周饮食和训练周报。"
- "昨晚睡了 6 小时，今天精神一般。"

## Agent Processing Flow

```text
classify
↓
parse
↓
normalize
↓
validate
↓
write or read
↓
confirm
```

## Intent Rules

- `meal`: meals, snacks, drinks, food quantity, rough nutrition.
- `workout`: exercises, training sessions, weight, reps, sets, RPE, cardio.
- `mixed`: one input includes both meal and workout content.
- `body_metrics`: sleep, energy, soreness, non-public body state.
- `query`: asks about history, progress, trend, or lookup.
- `weekly_review`: asks for a weekly summary.
- `safety_boundary`: mentions pain, injury, disease, medication, extreme dieting, eating disorder risk, or urgent symptoms.

Writable records are `meal_log`, `workout_log`, `mixed_log`, `body_metrics_log`, and `safety_boundary`. Request intents are `query` and `weekly_review_request`; they should not be written to CSV.

## When To Record Directly

Record directly when the input contains enough information to preserve a useful fact and maps to a writable record:

- Food name but unclear quantity: record item, use `null` nutrition fields, confidence `low`.
- Workout movement and some performance detail: record known fields, leave missing fields as `null`.
- Rough social meal: record as one low-confidence meal.
- Missing RPE: do not ask unless the user requested high-detail tracking.

## When To Ask Follow-Up

Ask follow-up only when no useful structured record can be formed:

- "今天吃得挺多" needs at least meal or food names.
- "帮我记一下训练" needs exercise or session details.
- "状态不太好" may be a body note, but ask if the user wants it tied to sleep, training, pain, or mood.

Do not ask follow-up merely because a request intent is not writable. For example, "帮我看看最近硬拉有没有进步" should trigger a local data query.

## When To Record Only A Note

Record only a note when the message is useful but not structured enough for food or exercise rows:

- "今天训练状态一般。"
- "这周比较忙，没怎么记饮食。"
- "睡眠有点少。"

Do not store `query` or `weekly_review_request` as notes. Use them to read local files and generate an answer or Markdown report.

## When To Trigger `safety_boundary`

Trigger `safety_boundary` for:

- Pain or discomfort that may indicate injury.
- Disease, medication, or treatment questions.
- Extreme dieting or disordered eating risk.
- Fainting, chest pain, breathing difficulty, or urgent symptoms.

The agent can record the user's description and suggest professional help. It must not diagnose or create injury rehabilitation plans.

## Typical Ambiguous Cases

### Unclear Food Portion

Input: "晚上吃了火锅，帮我粗略记一下。"

Action: Record one dinner item `hot_pot`, quantity `1餐`, confidence `low`, nutrition fields `null`.

### Missing Workout Sets Or Reps

Input: "今天练腿，深蹲做了几组，状态一般。"

Action: Record squat as an incomplete workout with null weight, reps, and set count. Preserve the note.

### Meal And Workout In One Message

Input: "午饭吃了鸡胸肉饭，晚上练胸，卧推 60kg 4 组 8 次。"

Action: Produce `mixed_log`, then write meal rows and workout rows separately.

### Too Vague To Parse

Input: "记一下，今天吃得挺多。"

Action: Ask concise follow-up questions. If the user declines, store the raw text as a note only.

### Pain Or Discomfort

Input: "我最近膝盖疼，还能不能继续深蹲？"

Action: Trigger `safety_boundary`. Record the note, avoid diagnosis, and suggest consulting a professional.
