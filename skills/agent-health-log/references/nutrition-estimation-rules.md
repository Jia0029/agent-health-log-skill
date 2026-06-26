# Nutrition Estimation Rules

## MVP Philosophy

v0.1 does not try to be precise. The goal is useful long-term logging, not medical nutrition therapy or exact macro tracking.

## Preserve Raw Input

Always preserve `raw_text`. The raw user message is often more valuable than a guessed macro estimate, because the user can correct it later.

## Use Rough Estimates For Common Foods

For common foods such as eggs, rice, milk, chicken breast, protein powder, or toast, the agent may use rough values from `references/food-basics.json`.

## Use Low Confidence For Unclear Meals

Use `confidence: low` for:

- Restaurant meals
- Social meals
- Hot pot
- Buffets
- Unknown portions
- Mixed dishes with unknown ingredients
- User-requested rough logging

## Do Not Force Unknown Macros

If calories, protein, carbs, or fat are uncertain, use `null`. Avoid inventing exact-looking numbers for vague meals.

## Let Users Correct Later

Users can later clarify:

- Portion size
- Ingredients
- Cooking method
- Brand or product
- Corrected nutrition values

The logging system should allow updates without losing `raw_text`.

## Not Nutrition Prescription

Nutrition estimates are for logging and reflection only. They are not medical advice, nutrition prescription, disease treatment, or weight-loss treatment.

