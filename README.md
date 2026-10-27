# DataCamp — Associate AI Engineer for Developers

A structured learning repository for my DataCamp AI engineering journey.

## Goal

Build practical AI engineering skills by combining DataCamp's lessons with independent implementations, notes, tests, and small deliverables. The emphasis is on being able to explain and build things independently—not just completing interactive exercises.

## Learning window

- **Current course:** DataCamp — Associate AI Engineer for Developers
- **Target learning period:** October 2026–January 2027
- **Weekly rhythm:** short learning sessions on weekdays, hands-on implementation on Saturday, and review on Sunday.

## Working principles

1. Keep one primary learning track at a time.
2. After a lesson, reimplement the key concept without copying the exercise.
3. Write brief notes in my own words; avoid copying course material.
4. Add tests and realistic failure cases as exercises become more complex.
5. Keep unrelated ideas in a parking lot until they support the current milestone.
6. Never commit API keys, passwords, tokens, or local secret files.

## Repository structure

```text
.
├── notes/          # Short explanations and lessons learned
├── exercises/      # Independent practice based on course concepts
├── projects/       # Larger, integrated exercises
└── tests/          # Automated tests as code grows
```

Folders will be added when needed; keep the repository lightweight at the beginning.

## Local setup

Use Python and `uv` for Python exercises unless a course exercise requires a different environment.

Install the OpenAI SDK when beginning local API exercises:

```bash
uv init
uv add openai
```

Set `OPENAI_API_KEY` in your shell or a local environment configuration that is excluded from Git. The OpenAI API may incur charges separately from a ChatGPT or DataCamp subscription; check API billing and available credits before sending requests.

For PowerShell, a session-only variable can be set with:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

Then create the client without embedding the secret in source code:

```python
from openai import OpenAI

client = OpenAI()
```

## Progress log

Update this table during weekly reviews.

| Period | Focus | Status | Evidence / notes |
|---|---|---|---|
| October 2026 | OpenAI API foundations | In progress | Completed the introductory chapter of *Working with the OpenAI API* |
| November 2026 | Continue the developer AI-engineering track | Not started | To be planned from the actual course curriculum |
| December 2026 | Apply course concepts in a practical feature | Not started | Scope after reviewing course progress |
| January 2027 | Consolidate learning and assess next steps | Not started | Review skills, course progress, and subscription value |

## Parking lot

Ideas worth revisiting later, without interrupting the current milestone:

- Explore advanced agent frameworks when core API and tool-calling concepts are clear.
- Compare vector databases when implementing retrieval requires a decision.
- Explore additional LLM providers when a concrete use case warrants it.

## Learning notes

For each lesson or topic, try to capture:

- **Concept:** What is it?
- **Why it matters:** What problem does it solve?
- **Independent implementation:** What did I build without filling in tutorial blanks?
- **Failure case:** What can go wrong, and how does the code handle it?
- **Open questions:** What should be revisited?

## Security

- Never commit secrets or real API keys.
- Keep `.env` files and local configuration out of version control.
- If a secret is accidentally committed, revoke/rotate it immediately; deleting it from the latest commit alone is not sufficient.
- Use small API requests and monitor billing when experimenting.
