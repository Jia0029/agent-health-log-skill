# Sample Scenarios

These examples are anonymized and intended for open-source parser behavior, documentation, and tests. They do not contain real names, contact details, addresses, body weight, medical records, or full chat logs.

Each sample includes:

- `user_input`
- `intent`
- `expected_structured_json`
- `notes`
- `confidence`

## 1. Simple Meal Record

```yaml
user_input: "早餐一杯拿铁、两个鸡蛋、一片吐司。"
intent: meal
expected_structured_json:
  type: meal_log
  date: today
  meals:
    - meal_time: breakfast
      items:
        - name: latte
          display_name: 拿铁
          quantity: 1杯
          nutrition_estimate:
            calories_kcal: null
            protein_g: null
            carbs_g: null
            fat_g: null
            confidence: low
        - name: egg
          display_name: 鸡蛋
          quantity: 2个
          nutrition_estimate:
            calories_kcal: 140
            protein_g: 12
            carbs_g: 1
            fat_g: 10
            confidence: medium
        - name: toast
          display_name: 吐司
          quantity: 1片
          nutrition_estimate:
            calories_kcal: null
            protein_g: null
            carbs_g: null
            fat_g: null
            confidence: low
  raw_text: "早餐一杯拿铁、两个鸡蛋、一片吐司。"
  needs_follow_up: false
notes: "A simple breakfast record. Unknown drink and toast details can remain null."
confidence: high
```

## 2. Fuzzy Meal Record

```yaml
user_input: "晚上吃了火锅，帮我粗略记一下。"
intent: meal
expected_structured_json:
  type: meal_log
  date: today
  meals:
    - meal_time: dinner
      items:
        - name: hot_pot
          display_name: 火锅
          quantity: 1餐
          nutrition_estimate:
            calories_kcal: null
            protein_g: null
            carbs_g: null
            fat_g: null
            confidence: low
          tags:
            - restaurant_or_social_meal
            - rough_estimate
  raw_text: "晚上吃了火锅，帮我粗略记一下。"
  needs_follow_up: false
notes: "Record as a low-confidence dinner without forcing exact macros."
confidence: medium
```

## 3. Simple Workout Record

```yaml
user_input: "今天练背，硬拉 80kg 5x5。"
intent: workout
expected_structured_json:
  type: workout_log
  date: today
  session_type: pull
  focus: 背
  exercises:
    - exercise_id: deadlift
      display_name: 硬拉
      sets:
        - weight_kg: 80
          reps: 5
          set_count: 5
      rpe: null
      notes: null
  raw_text: "今天练背，硬拉 80kg 5x5。"
  needs_follow_up: false
notes: "Interpret 5x5 as 5 sets of 5 reps. Do not require RPE."
confidence: high
```

## 4. Complex Workout Record

```yaml
user_input: "今天练背，硬拉 80kg 5x5，引体向上 4 组，每组 8 个，坐姿划船 45kg 3 组 12 次。"
intent: workout
expected_structured_json:
  type: workout_log
  date: today
  session_type: pull
  focus: 背
  exercises:
    - exercise_id: deadlift
      display_name: 硬拉
      sets:
        - weight_kg: 80
          reps: 5
          set_count: 5
      rpe: null
      notes: null
    - exercise_id: pull_up
      display_name: 引体向上
      sets:
        - weight_kg: null
          reps: 8
          set_count: 4
      rpe: null
      notes: bodyweight
    - exercise_id: seated_row
      display_name: 坐姿划船
      sets:
        - weight_kg: 45
          reps: 12
          set_count: 3
      rpe: null
      notes: null
  raw_text: "今天练背，硬拉 80kg 5x5，引体向上 4 组，每组 8 个，坐姿划船 45kg 3 组 12 次。"
  needs_follow_up: false
notes: "Split multiple exercises into separate normalized records."
confidence: high
```

## 5. Mixed Meal And Workout Input

```yaml
user_input: "午饭吃了鸡胸肉饭，晚上练胸，卧推 60kg 4 组 8 次。"
intent: mixed
expected_structured_json:
  type: mixed_log
  date: today
  meal_log:
    meals:
      - meal_time: lunch
        items:
          - name: chicken_rice_bowl
            display_name: 鸡胸肉饭
            quantity: 1份
            nutrition_estimate:
              calories_kcal: null
              protein_g: null
              carbs_g: null
              fat_g: null
              confidence: low
  workout_log:
    session_type: push
    focus: 胸
    exercises:
      - exercise_id: bench_press
        display_name: 杠铃卧推
        aliases_seen:
          - 卧推
        sets:
          - weight_kg: 60
            reps: 8
            set_count: 4
        rpe: null
        notes: null
  raw_text: "午饭吃了鸡胸肉饭，晚上练胸，卧推 60kg 4 组 8 次。"
  needs_follow_up: false
notes: "Mixed input produces both meal and workout sections."
confidence: high
```

## 6. Query Exercise History

```yaml
user_input: "帮我看看最近硬拉有没有进步。"
intent: query
expected_structured_json:
  type: query
  query_kind: exercise_progress
  exercise_id: deadlift
  display_name: 硬拉
  time_range:
    preset: recent
    days: null
  metrics:
    - top_weight
    - volume
    - estimated_1rm
    - recent_sessions
  raw_text: "帮我看看最近硬拉有没有进步。"
  needs_follow_up: false
notes: "The agent should read local training records instead of answering from memory."
confidence: high
```

## 7. Weekly Review

```yaml
user_input: "帮我生成这周饮食和训练周报。"
intent: weekly_review
expected_structured_json:
  type: weekly_review_request
  date_anchor: today
  period:
    preset: current_week
  sections:
    - training_frequency
    - muscle_group_distribution
    - key_lift_trends
    - meal_logging_coverage
    - nutrition_estimate_summary
    - next_week_suggestions
  raw_text: "帮我生成这周饮食和训练周报。"
  needs_follow_up: false
notes: "Create a report request, then load current-week records from local storage."
confidence: high
```

## 8. Missing Information But Still Recordable

```yaml
user_input: "今天练腿，深蹲做了几组，状态一般。"
intent: workout
expected_structured_json:
  type: workout_log
  date: today
  session_type: legs
  focus: 腿
  exercises:
    - exercise_id: squat
      display_name: 深蹲
      sets:
        - weight_kg: null
          reps: null
          set_count: null
      rpe: null
      notes: "状态一般；组数、次数、重量未提供"
  raw_text: "今天练腿，深蹲做了几组，状态一般。"
  needs_follow_up: false
notes: "Incomplete workout data can still be useful when raw_text is preserved."
confidence: medium
```

## 9. Needs Follow-Up

```yaml
user_input: "记一下，今天吃得挺多。"
intent: meal
expected_structured_json:
  type: meal_log
  date: today
  meals: []
  raw_text: "记一下，今天吃得挺多。"
  needs_follow_up: true
  follow_up_questions:
    - "大概是哪一餐？"
    - "能列一下主要吃了哪些东西吗？"
notes: "Too vague to create food rows. Ask a short follow-up."
confidence: low
```

## 10. Medical Boundary Case

```yaml
user_input: "我最近膝盖疼，还能不能继续深蹲？帮我安排一下。"
intent: query
expected_structured_json:
  type: safety_boundary
  category: medical_or_injury_advice
  related_exercise_id: squat
  should_log_as_note: true
  note:
    date: today
    text: "用户提到膝盖疼，询问是否继续深蹲。"
  response_policy:
    do_not_provide_diagnosis: true
    do_not_prescribe_training_plan: true
    suggest_professional_help: true
    allowed_response: "可以记录疼痛和训练状态，但不要替代医生或物理治疗师判断。若疼痛持续、加重或影响动作，应停止相关动作并咨询专业人士。"
  raw_text: "我最近膝盖疼，还能不能继续深蹲？帮我安排一下。"
  needs_follow_up: false
notes: "Boundary case: log the note, avoid diagnosis or injury-specific programming."
confidence: high
```

## 11. Body Metrics Record

```yaml
user_input: "昨晚睡了 6 小时，今天精神一般。"
intent: body_metrics
expected_structured_json:
  type: body_metrics_log
  date: today
  metrics:
    sleep_hours: 6
    energy_level: 一般
  raw_text: "昨晚睡了 6 小时，今天精神一般。"
  needs_follow_up: false
notes: "Body metrics example intentionally excludes body weight and sensitive health information."
confidence: high
```

## 12. Outcome Showcase Request

```yaml
user_input: "这些记录有什么用？帮我生成一份本周复盘和可视化数据样例。"
intent: weekly_review
expected_structured_json:
  type: weekly_review_request
  date_anchor: today
  period:
    preset: current_week
  sections:
    - training_frequency
    - exercise_progress
    - meal_logging_coverage
    - nutrition_estimate_summary
    - sleep_energy_context
    - visualization_ready_data
    - next_week_suggestions
  raw_text: "这些记录有什么用？帮我生成一份本周复盘和可视化数据样例。"
  needs_follow_up: false
notes: "This request should read local records and generate a review plus chart-ready data. It should not write a normal CSV record."
confidence: high
```

Expected user-facing result:

```text
## 本周复盘

- 训练天数：3 天
- 饮食记录覆盖：5/7 天
- 重点动作：硬拉最高工作组 80kg x 5
- 睡眠记录：4 天，平均 6.6 小时

## 可视化数据样例

{
  "chart_type": "line",
  "title": "硬拉最高工作组",
  "x": ["2026-06-10", "2026-06-17", "2026-06-24"],
  "y": [75, 80, 80],
  "unit": "kg"
}
```
