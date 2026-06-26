# Demo

[English](demo.md) | [简体中文](demo.zh-CN.md)

All examples are sanitized and do not contain real personal health data.

## 1. Meal Logging Demo

User input:

```text
Breakfast was two eggs and a latte.
```

Structured JSON:

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
          "display_name": "Egg",
          "quantity": "2",
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
          "display_name": "Latte",
          "quantity": "1 cup",
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
  "raw_text": "Breakfast was two eggs and a latte.",
  "needs_follow_up": false
}
```

CSV effect: append two rows to `nutrition.csv`.

User confirmation:

```text
Logged breakfast with two eggs and one latte. Latte nutrition is marked low confidence.
```

## 2. Workout Logging Demo

User input:

```text
Today I trained back: deadlift 80kg 5x5.
```

Structured JSON:

```json
{
  "type": "workout_log",
  "date": "today",
  "session_type": "pull",
  "focus": "back",
  "exercises": [
    {
      "exercise_id": "deadlift",
      "display_name": "Deadlift",
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
  "raw_text": "Today I trained back: deadlift 80kg 5x5.",
  "needs_follow_up": false
}
```

CSV effect: append one row to `training.csv`.

User confirmation:

```text
Logged deadlift: 80kg, 5 sets of 5 reps.
```

## 3. Mixed Meal + Workout Demo

User input:

```text
Lunch was a chicken rice bowl. Tonight I benched 60kg for 4 sets of 8.
```

Structured JSON:

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
            "display_name": "Chicken rice bowl",
            "quantity": "1 serving",
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
    "focus": "chest",
    "exercises": [
      {
        "exercise_id": "bench_press",
        "display_name": "Bench press",
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
  "raw_text": "Lunch was a chicken rice bowl. Tonight I benched 60kg for 4 sets of 8.",
  "needs_follow_up": false
}
```

CSV effect: append meal rows to `nutrition.csv` and workout rows to `training.csv`.

User confirmation:

```text
Logged lunch and bench press in one entry.
```

## 4. Sleep / Body Metrics Demo

User input:

```text
I slept 6 hours last night and feel low energy today.
```

Structured JSON:

```json
{
  "type": "body_metrics_log",
  "date": "today",
  "metrics": {
    "sleep_hours": 6,
    "energy_level": "low"
  },
  "raw_text": "I slept 6 hours last night and feel low energy today.",
  "needs_follow_up": false
}
```

CSV effect: append two rows to `body_metrics.csv`.

User confirmation:

```text
Logged sleep and energy level.
```

## 5. Exercise History Query Demo

User input:

```text
Has my deadlift improved recently?
```

Structured JSON:

```json
{
  "type": "query",
  "query_kind": "exercise_progress",
  "exercise_id": "deadlift",
  "display_name": "Deadlift",
  "time_range": {
    "preset": "recent",
    "days": null
  },
  "metrics": ["top_weight", "volume", "recent_sessions"],
  "raw_text": "Has my deadlift improved recently?",
  "needs_follow_up": false
}
```

CSV / Markdown effect: no write. The agent should read local training data.

User confirmation:

```text
I will check your local deadlift records and summarize recent progress.
```

## 6. Weekly Review Demo

User input:

```text
Generate this week's meal and workout review.
```

Structured JSON:

```json
{
  "type": "weekly_review_request",
  "date_anchor": "today",
  "period": {
    "preset": "current_week"
  },
  "sections": ["training_frequency", "meal_logging_coverage", "nutrition_estimate_summary", "next_week_suggestions"],
  "raw_text": "Generate this week's meal and workout review.",
  "needs_follow_up": false
}
```

CSV / Markdown effect: read CSV files and write `reports/YYYY-WXX.md`.

User confirmation:

```text
Generated this week's local health log report.
```

## 7. Safety Boundary Demo

User input:

```text
My knee hurts. Can I keep squatting?
```

Structured JSON:

```json
{
  "type": "safety_boundary",
  "category": "medical_or_injury_advice",
  "related_exercise_id": "squat",
  "should_log_as_note": true,
  "note": {
    "date": "today",
    "text": "User reported knee pain and asked whether to continue squatting."
  },
  "response_policy": {
    "do_not_provide_diagnosis": true,
    "do_not_prescribe_training_plan": true,
    "suggest_professional_help": true,
    "allowed_response": "I can record this note, but I cannot diagnose the cause or create an injury rehab plan. Stop movements that cause pain and consult a qualified professional if symptoms persist or worsen."
  },
  "raw_text": "My knee hurts. Can I keep squatting?",
  "needs_follow_up": false
}
```

CSV effect: append a safety note to `body_metrics.csv`.

User confirmation:

```text
Logged the knee pain note. I cannot diagnose it; please stop painful movement and consult a qualified professional if it persists or worsens.
```

