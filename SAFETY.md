# Safety

Agent Health Log Skill is a logging and review tool. It is not a medical tool.

## Not Medical Advice

This project does not provide:

- Disease diagnosis
- Injury diagnosis
- Treatment decisions
- Medication advice
- Injury rehabilitation plans
- Medical nutrition therapy
- Extreme dieting guidance

It does not replace doctors, dietitians, physical therapists, rehabilitation professionals, or emergency services.

## Trigger `safety_boundary`

Trigger `safety_boundary` when the user mentions:

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
- Other urgent or dangerous symptoms

## What The Agent Can Do

- Record the user's description as a factual note.
- Suggest stopping an activity that clearly causes pain.
- Suggest consulting a qualified professional.
- Encourage safe, moderate, long-term record keeping.
- Explain that the project is for logging and review only.

## What The Agent Must Not Do

- Diagnose a condition.
- Decide whether a disease or injury is present.
- Create an injury rehabilitation training plan.
- Tell users to train through pain.
- Provide extreme diet plans.
- Make medication or treatment judgments.

## Example Boundary Response

```text
I can record that you felt knee pain during squats, but I cannot diagnose the cause or create an injury rehab plan. If pain persists, worsens, or affects movement, stop the painful exercise and consult a qualified medical or rehabilitation professional.
```

