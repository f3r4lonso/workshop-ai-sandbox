# workshop-ai-sandbox — project rules

Shared rules for every AI client in this repository. The workspace rules in the shared infrastructure
(`%USERPROFILE%\workshop\infra\AGENTS.md`) apply too; its security and privacy rules always win.

- **Purpose:** `csvsummary`, a small CSV statistics CLI. It exists only to pilot Workshop AI: three tasks, each run
  once as a plain client session and once with the `wai` tool.
- **Stage:** local POC (sandbox).
- **Commands:** run `python -m csvsummary data/sample.csv`; tests `python -m unittest discover -s tests`.
- **Constraints:**
  - Python 3 standard library only.
  - Do not edit `pilot/` or `pilot-results/` during a pilot run; they hold the fixed task definitions and results.
  - Work only on the task you were given; do not fix other known issues on the way.
- The user is a trader: report outcomes, not code explanations; reply in English.
