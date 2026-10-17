# Pilot tasks

Fixed before any run (2026-10-18). Do not change them during the pilot. Every run starts from the tag `pilot-base`
in its own folder (see [user-script.md](user-script.md)). Paste the **Objective** and **Acceptance criteria** of a
task as they are: into the first message of a baseline session, or into `task.md` for a run with the tool.

A run is **done** when every criterion is met or the user stops it.

## T1 `t1-column-option` — small feature

**Objective:** add a `--column <name>` option to `csvsummary` that prints the statistics of that one column only.

**Acceptance criteria:**
- [ ] (a) `python -m csvsummary data/sample.csv --column price` prints only the `price` line.
- [ ] (b) an unknown column prints a clear message naming the column and exits with code 2.
- [ ] (c) new tests cover (a) and (b).
- [ ] (d) `python -m unittest discover -s tests` passes.
- [ ] (e) `README.md` documents the option.
- [ ] (f) no files changed outside `csvsummary/`, `tests/` and `README.md`.

**Context files (tool run):** `csvsummary/__main__.py`, `csvsummary/stats.py`, `tests/test_stats.py`, `README.md`.

## T2 `t2-empty-csv` — bug fix

**Objective:** `csvsummary` must not crash on a CSV that has a header row but no data rows.

**Acceptance criteria:**
- [ ] (a) a regression test fails on `pilot-base` and passes after the fix.
- [ ] (b) a header-only CSV prints `no data rows` and exits with code 0.
- [ ] (c) output for non-empty files is unchanged: the existing tests are untouched and pass.

**Context files (tool run):** `csvsummary/stats.py`, `csvsummary/__main__.py`, `tests/test_stats.py`.

## T3 `t3-validation` — two sessions plus handoff

**Objective:** handle malformed rows (a row with the wrong number of fields, or text in a column that is otherwise
numeric) with a clear, consistent behaviour instead of silently dropping or miscounting data.

Session 1 **only designs**: it decides and records at least two decisions — the error message format, and what
happens on a malformed row (stop, or skip and report) — then stops without changing code. Session 2 starts fresh,
in a new Claude Code session, and implements.

**Acceptance criteria:**
- [ ] (a) session 2, before coding, states the recorded decisions and next step correctly (tool run: from the
  handoff package only; baseline: from whatever the user pasted from session 1).
- [ ] (b) the implementation follows the recorded decisions.
- [ ] (c) tests for a malformed row pass, and `python -m unittest discover -s tests` passes.
- [ ] (d) tool run only: the package was scanned clean and approved, and holds only `handoff.md`, `manifest.json` and
  the selected files under `context/`.

**Context files (tool run):** `csvsummary/stats.py`, `csvsummary/__main__.py`, `tests/test_stats.py`.

## Baseline first message (plain session)

> Task: <paste Objective>. Acceptance criteria: <paste criteria>. Work in this folder. Tell me when every criterion
> is met.
