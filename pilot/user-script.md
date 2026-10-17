# Pilot script (you run this; the agent checks the files afterwards)

Use **PowerShell in a normal terminal**, not inside an AI session: the tool's approvals only work there.
Keep `pilot-results\results.md` (in this folder) open in an editor and fill one row per run as you go.
Task texts: [tasks.md](tasks.md). Order: T1 baseline → T1 tool → T2 tool → T2 baseline → T3 baseline → T3 tool.
You can stop after any run; tell the agent which runs you did.

## A. Once per terminal

```powershell
Set-Alias wai "$env:USERPROFILE\workshop\applications\workshop-ai\wai.cmd"
$sandbox = "$env:USERPROFILE\workshop\applications\workshop-ai-sandbox"
$runs    = "$env:USERPROFILE\workshop\applications\workshop-ai-sandbox-runs"
$shared  = "$env:USERPROFILE\workshop\infra\clients"
```

Each run gets its own folder made from the fixed starting point (no commits needed):

```powershell
cd $sandbox; git worktree add --detach "$runs\<run>" pilot-base; cd "$runs\<run>"
```

## B. A baseline run (plain Claude Code), e.g. `t1-base`

1. Make the run folder (above) with `<run>` = `t1-base`.
2. Write the start time. `claude --add-dir $shared`
3. Paste the baseline first message from tasks.md with the task's Objective and criteria.
4. Answer the session as needed. Count every message you type after the first one.
5. When every criterion is met (or you stop): write the accepted time, then type `/context` and `/cost` and copy
   both outputs into the results file. `/exit`.

## C. A run with the tool, e.g. `t2-tool` (also the resume and handoff checks)

1. Make the run folder with `<run>` = `t2-tool`.
2. `wai init` → `wai resources agents` (a list should appear).
3. `wai task new t2-empty-csv --client claude` → Notepad opens: paste the T2 Objective under `## Objective` and the
   criteria under `## Acceptance criteria`; under the `revision: 0` line add `verify: python -m unittest discover -s tests`
   → save, close.
4. `wai context add t2-empty-csv csvsummary/stats.py csvsummary/__main__.py tests/test_stats.py`
5. Write the start time. `wai start t2-empty-csv` → read what it shows → `y`.
   Work in the session until every criterion is met. Count your messages after the first.
   Write the accepted time; `/context`, `/cost` → copy to the results file → `/exit`.
6. `wai checkpoint t2-empty-csv` → `y` to run the tests → read the changes → `y` to save.
7. **Resume check:** `wai resume t2-empty-csv` → `y` → when it has answered, ask
   "What decisions are recorded for this task?" → copy the answer to the results file → `/exit`.
8. **Handoff:** `wai handoff create t2-empty-csv --to codex` → open
   `.workshop-ai\handoffs\t2-empty-csv-1\` and read every file → `wai handoff approve t2-empty-csv-1` → type
   `reviewed` → `y` → `wai handoff show t2-empty-csv-1`. Do part D now.

For **T1 with the tool** use the same steps with `t1-tool`, task id `t1-column-option` and the T1 context files;
skip steps 7–8.

## D. Codex check (Gate C) — after C step 8

1. `codex login status` → it must show **your own** account; if not signed in, `codex login` and follow the
   browser sign-in. Copy the method shown (not the e-mail) to the results file.
2. Optional, the shared-infrastructure check: in `$env:USERPROFILE\workshop\infra\clients`, run `codex`, then the
   steps in the infrastructure's `clients\codex-cli\README.md` section 5; note pass/fail per step. `/exit`.
3. `cd "$runs\t2-tool"` → `codex --sandbox read-only` (Codex can read but not change files) → paste:
   `Read .workshop-ai/handoffs/t2-empty-csv-1/handoff.md. Using only that package, state the recorded decisions and the next action. Do not change any file.`
4. Copy its answer to the results file (Codex check). `/exit`.

## E. T3 with the tool (`t3-tool`), two sessions

1. Make the run folder; `wai init`; `wai task new t3-validation --client claude` (paste T3 text; add the same
   `verify:` line); `wai context add t3-validation csvsummary/stats.py csvsummary/__main__.py tests/test_stats.py`.
2. Session 1: `wai start t3-validation` → `y` → say "Design only: record the decisions and next action in the task
   file, then stop. Do not change code." → `/context`, `/cost` → `/exit`.
3. `wai checkpoint t3-validation` → `n` to the tests (nothing to test yet) → `y` to save.
4. `wai handoff create t3-validation --to claude` → read the package files → `wai handoff approve t3-validation-1`
   → `reviewed` → `y` → `wai handoff show t3-validation-1` → run the `claude …` command it prints.
5. Session 2: it should first state the decisions and next action (criterion a). Then let it implement.
   `/context`, `/cost` → `/exit`. `wai checkpoint t3-validation` → `y` → `y`.

For **T3 baseline** (`t3-base`): session 1 in plain Claude Code with the design-only instruction; copy whatever you
think session 2 needs; `/exit`; start a new `claude --add-dir $shared` and paste it with the task text.

## F. When you are done

Tell the agent which runs you completed. Leave the run folders as they are: the agent checks them, then proposes
how to remove them (`git worktree remove`) at the end.
