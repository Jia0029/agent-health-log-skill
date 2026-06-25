# Privacy

Agent Health Log Skill is local-first by design. The user owns their data and controls where it is stored.

## Local-First By Design

The default workflow writes records to local Markdown, CSV, or future SQLite files. The project does not require cloud sync, external accounts, or remote databases.

## Do Not Commit Real Health Data

Do not commit real personal health records to GitHub. Avoid publishing:

- Real meal records
- Body weight or private body measurements
- Injury details
- Sleep records
- Medical information
- Medication information
- Full chat logs
- Names, addresses, contact details, or account identifiers

## Examples Must Be Sanitized

All `examples/` and `tests/` files should use anonymous sample data. They should demonstrate parser behavior without exposing real people or private health history.

## Ignored Private Paths

The default `.gitignore` excludes private runtime data:

- `data/*.csv`
- `daily/*.md`
- `reports/*.md`
- `*.sqlite`
- `*.db`
- `private/`
- `personal/`
- `.env`

Keep real logs in ignored locations or outside the repository.

