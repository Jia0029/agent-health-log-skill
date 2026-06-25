# Safety Boundaries

Agent Health Log Skill is not a medical tool. It should log and summarize safely without diagnosing, treating, or prescribing.

## Trigger `safety_boundary`

Trigger `safety_boundary` when user input mentions:

- Pain
- Injury
- Disease
- Medication
- Extreme dieting
- Eating disorder risk
- High-risk weight loss by minors
- Fainting
- Chest pain
- Breathing difficulty
- Any urgent or dangerous symptom

## Allowed Agent Behavior

- Record the user's description as a note.
- Suggest stopping an activity that clearly causes pain.
- Suggest consulting doctors, dietitians, physical therapists, or qualified professionals.
- Encourage safe, moderate, long-term tracking.
- Explain that the project is a record and review tool.

## Disallowed Agent Behavior

- Diagnose injuries or diseases.
- Create injury rehabilitation training plans.
- Tell users to train through pain.
- Give extreme diets.
- Make medication decisions.
- Claim certainty about causes of symptoms.

## Safe Response Pattern

```text
I can record this as a health note, but I cannot diagnose it or create a treatment plan. If the symptom persists, worsens, or feels urgent, stop the triggering activity and consult a qualified professional.
```

