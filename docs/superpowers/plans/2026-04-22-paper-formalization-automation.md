# Paper Formalization Automation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/loop 10m` automation that pulls `gaia-papers`, formalizes one new paper from `inbox/` per tick, and commits + tags + pushes the resulting Gaia package.

**Architecture:** Most per-tick orchestration lives in a carefully-written loop prompt. The only deterministic logic extracted into a script is slug derivation, which must be stable across ticks. Everything else (git, file moves, gaia CLI invocation) is shell commands the model issues from the prompt.

**Tech Stack:** Python 3 (stdlib only for the slug helper), git, gaia-lang CLI (already installed in `/Users/risoliao/Code/gaia-lb/venv`), Claude Code `/loop` skill.

**Spec:** `docs/superpowers/specs/2026-04-22-paper-formalization-automation-design.md`

**Working directory for all tasks:** `/Users/risoliao/Code/gaia-lb/papers`

---

## File Structure

- Create: `scripts/derive_slug.py` — pure-Python slug derivation, stdlib only.
- Create: `scripts/test_derive_slug.py` — unittest covering slug rules.
- Create: `scripts/loop-prompt.md` — the full per-tick prompt that `/loop 10m` fires.
- Create: `README.md` — one-page ops doc: layout, how to start/stop the loop.
- Modify: `.gitignore` — add `_failed/`.

No other files change. No dependencies added.

---

### Task 1: Ignore failure logs

**Files:**
- Modify: `/Users/risoliao/Code/gaia-lb/papers/.gitignore`

- [ ] **Step 1: Append the `_failed/` rule**

Open `.gitignore` and append exactly one new line at the end (after the existing last line `.venv/`):

```
_failed/
```

- [ ] **Step 2: Verify the file contents**

Run:
```bash
cat /Users/risoliao/Code/gaia-lb/papers/.gitignore
```

Expected output (exact):
```
__pycache__/
*.pyc
*.pyo
.gaia-cache/
.github-output/
.DS_Store
venv/
.venv/
_failed/
```

- [ ] **Step 3: Commit**

```bash
cd /Users/risoliao/Code/gaia-lb/papers
git add .gitignore
git commit -m "chore: ignore _failed/ (loop failure logs)"
```

---

### Task 2: Slug derivation — failing test

**Files:**
- Create: `/Users/risoliao/Code/gaia-lb/papers/scripts/test_derive_slug.py`

- [ ] **Step 1: Create `scripts/` directory**

```bash
mkdir -p /Users/risoliao/Code/gaia-lb/papers/scripts
```

- [ ] **Step 2: Write the failing test**

Create `scripts/test_derive_slug.py` with this exact content:

```python
import unittest

from derive_slug import derive_slug


class DeriveSlugTests(unittest.TestCase):
    def test_simple_pdf(self):
        self.assertEqual(derive_slug("attention.pdf"), "attention")

    def test_spaces_and_capitals(self):
        self.assertEqual(
            derive_slug("Attention Is All You Need.pdf"),
            "attention-is-all-you-need",
        )

    def test_runs_of_non_alnum_collapse(self):
        self.assertEqual(
            derive_slug("Foo  ---  Bar__baz.md"),
            "foo-bar-baz",
        )

    def test_leading_and_trailing_separators_trimmed(self):
        self.assertEqual(derive_slug("---hello---.txt"), "hello")

    def test_unicode_letters_preserved_lowercase(self):
        # Unicode letters are kept (lowercased); non-letters collapse.
        self.assertEqual(derive_slug("Café Noir.pdf"), "café-noir")

    def test_numbers_preserved(self):
        self.assertEqual(derive_slug("GPT-4 Technical Report.pdf"), "gpt-4-technical-report")

    def test_multiple_extensions_only_final_stripped(self):
        # We only strip the final suffix; intermediate dots collapse like any non-alnum.
        self.assertEqual(derive_slug("paper.v2.final.pdf"), "paper-v2-final")

    def test_html_and_txt_extensions(self):
        self.assertEqual(derive_slug("arxiv-2401.00001.html"), "arxiv-2401-00001")
        self.assertEqual(derive_slug("link.txt"), "link")

    def test_empty_stem_raises(self):
        with self.assertRaises(ValueError):
            derive_slug("---.pdf")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the test — expect failure (module not found)**

```bash
cd /Users/risoliao/Code/gaia-lb/papers/scripts
python3 -m unittest test_derive_slug.py -v
```

Expected: `ModuleNotFoundError: No module named 'derive_slug'`. This confirms the test runs and the module is genuinely missing.

---

### Task 3: Slug derivation — implementation

**Files:**
- Create: `/Users/risoliao/Code/gaia-lb/papers/scripts/derive_slug.py`

- [ ] **Step 1: Write the minimal implementation**

Create `scripts/derive_slug.py` with this exact content:

```python
"""Derive a stable kebab-case slug from a paper filename.

Rules (see spec § "Per-Tick Workflow" step 4):
  - Strip the final extension.
  - Lowercase.
  - Replace runs of non-letter/non-digit characters with a single '-'.
  - Trim leading and trailing '-'.
  - Raise ValueError if the result is empty.
"""

from __future__ import annotations

import os
import re
import sys


_NON_ALNUM_RUN = re.compile(r"[^0-9a-zÀ-ɏͰ-῿Ⰰ-퟿]+", re.UNICODE)


def derive_slug(filename: str) -> str:
    stem, _ext = os.path.splitext(filename)
    lowered = stem.lower()
    replaced = _NON_ALNUM_RUN.sub("-", lowered)
    trimmed = replaced.strip("-")
    if not trimmed:
        raise ValueError(f"cannot derive slug from filename: {filename!r}")
    return trimmed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: derive_slug.py <filename>", file=sys.stderr)
        sys.exit(2)
    print(derive_slug(sys.argv[1]))
```

- [ ] **Step 2: Run the test — expect pass**

```bash
cd /Users/risoliao/Code/gaia-lb/papers/scripts
python3 -m unittest test_derive_slug.py -v
```

Expected: all 9 tests pass, exit code 0.

- [ ] **Step 3: Smoke-check the CLI entry point**

```bash
cd /Users/risoliao/Code/gaia-lb/papers/scripts
python3 derive_slug.py "Attention Is All You Need.pdf"
```

Expected output (exact): `attention-is-all-you-need`

- [ ] **Step 4: Commit**

```bash
cd /Users/risoliao/Code/gaia-lb/papers
git add scripts/derive_slug.py scripts/test_derive_slug.py
git commit -m "feat(scripts): add derive_slug helper with tests"
```

---

### Task 4: Write the loop prompt

**Files:**
- Create: `/Users/risoliao/Code/gaia-lb/papers/scripts/loop-prompt.md`

This is the prompt text that `/loop 10m "<paste contents>"` fires every 10 minutes. The model reads it each tick and executes the workflow. It's a prose artifact; no unit test applies. Correctness is verified by the end-to-end validation task.

- [ ] **Step 1: Create the file**

Create `scripts/loop-prompt.md` with this exact content:

````markdown
# Paper Formalization Loop — Per-Tick Prompt

You are running one tick of the paper-formalization loop. The authoritative
spec is:

  /Users/risoliao/Code/gaia-lb/papers/docs/superpowers/specs/2026-04-22-paper-formalization-automation-design.md

**Hard constraints for this tick:**
- Do NOT ask clarifying questions. If `/gaia:formalization` would normally ask
  a disambiguation, pick the best-guess answer silently and continue.
- Process exactly ONE paper this tick, then stop. Never process two papers in
  one tick.
- Never commit broken packages. On any failure, execute the failure branch
  exactly as described below.
- Never use destructive git operations (`push --force`, `reset --hard`,
  `clean -f`). A normal failure branch is all you need.
- All paths below are absolute. Use them as-is.

## Step 1 — Pull

```bash
cd /Users/risoliao/Code/gaia-lb/papers
git pull --rebase --autostash origin main
```

If the pull fails (conflict, non-zero exit), stop this tick. Do not try to
resolve. The next tick will retry.

## Step 2 — Find the next paper

List eligible files in `inbox/`:

```bash
cd /Users/risoliao/Code/gaia-lb/papers
ls -1 inbox/ | grep -Ei '\.(pdf|md|txt|html)$' | sort
```

If the list is empty, **stop this tick**.

Otherwise take the FIRST entry. Call it `<file>`. Note: `<file>` may contain
spaces or other shell-special characters; **always wrap it in double quotes**
in every command below.

## Step 3 — Derive slug

```bash
cd /Users/risoliao/Code/gaia-lb/papers
SLUG=$(python3 scripts/derive_slug.py "<file>")
echo "$SLUG"
```

Record `<slug>` as the value of `$SLUG`. Slugs by construction contain no
shell-special characters, so they do not need quoting, but filenames always
do.

## Step 4 — Collision guard

Check whether the target package already exists:

```bash
cd /Users/risoliao/Code/gaia-lb/papers
test -d "formalized/$SLUG-gaia" && echo COLLISION || echo OK
```

If the output is `COLLISION`, append one line to the collision log and
**stop this tick**:

```bash
cd /Users/risoliao/Code/gaia-lb/papers
mkdir -p _failed
printf '%s collision: formalized/%s-gaia/ already exists, skipping inbox/%s\n' \
  "$(date -u +%FT%TZ)" "$SLUG" "<file>" \
  >> "_failed/$SLUG-collision.log"
```

If the output is `OK`, proceed to Step 5.

## Step 5 — Scaffold and stage the source

```bash
cd /Users/risoliao/Code/gaia-lb/papers/formalized
source /Users/risoliao/Code/gaia-lb/venv/bin/activate
gaia init "$SLUG-gaia"
cd /Users/risoliao/Code/gaia-lb/papers
mkdir -p "formalized/$SLUG-gaia/artifacts"
mv "inbox/<file>" "formalized/$SLUG-gaia/artifacts/<file>"
```

## Step 6 — Formalize

Invoke the `/gaia:formalization` skill against
`/Users/risoliao/Code/gaia-lb/papers/formalized/$SLUG-gaia/artifacts/<file>`,
fully autonomous. No questions to the operator. If the skill would branch on
a disambiguation, choose the option it marks as default (or, failing that,
the first option listed) and proceed.

If the skill completes successfully, continue to Step 7. If it raises an
error or produces no DSL output, execute the **Failure Branch** below.

## Step 7 — Compile and check

```bash
cd "/Users/risoliao/Code/gaia-lb/papers/formalized/$SLUG-gaia"
source /Users/risoliao/Code/gaia-lb/venv/bin/activate
gaia compile .
gaia check .
```

If either command exits non-zero, execute the **Failure Branch** below.

## Step 8 — Commit, tag, push

```bash
cd /Users/risoliao/Code/gaia-lb/papers
git add "formalized/$SLUG-gaia/"
git commit -m "Formalize: <Original Paper Title>

Autogenerated by the 10-min formalization loop.
Source: <file>
Package: formalized/$SLUG-gaia/"
git tag "formalized/$SLUG"
git push origin main
git push origin "formalized/$SLUG"
```

`<Original Paper Title>` is the source filename stem with original
capitalization (i.e., `<file>` with its extension removed, spaces preserved).

If `git push` fails, do NOT retry in this tick — leave the commit + tag
local. The next tick's `git pull --rebase` will reconcile and re-push.

**Stop this tick.**

## Failure Branch

When Step 6 or Step 7 fails:

```bash
cd /Users/risoliao/Code/gaia-lb/papers
mkdir -p _failed
TS=$(date -u +%FT%TZ)
{
  echo "timestamp: $TS"
  echo "slug: $SLUG"
  echo "source: inbox/<file>"
  echo "phase: <which step failed>"
  echo "error:"
  echo "<paste the last 50 lines of stderr / skill output here>"
} >> "_failed/$SLUG-$TS.log"

# Restore the source to inbox so the next tick (or the operator) can retry.
mv "formalized/$SLUG-gaia/artifacts/<file>" "inbox/<file>"
rm -rf "formalized/$SLUG-gaia/"
```

No git commit, no push. **Stop this tick.**
````

- [ ] **Step 2: Verify the file saved**

```bash
wc -l /Users/risoliao/Code/gaia-lb/papers/scripts/loop-prompt.md
```

Expected: line count roughly 120–140. (Sanity check the file is not empty.)

- [ ] **Step 3: Commit**

```bash
cd /Users/risoliao/Code/gaia-lb/papers
git add scripts/loop-prompt.md
git commit -m "feat(scripts): add per-tick loop prompt for formalization automation"
```

---

### Task 5: Ops README

**Files:**
- Create: `/Users/risoliao/Code/gaia-lb/papers/README.md`

- [ ] **Step 1: Write the README**

Create `README.md` with this exact content:

````markdown
# gaia-papers

Staging and output for automated Gaia formalization.

## Layout

- `inbox/` — drop source papers here (PDF, Markdown, TXT with a URL, or HTML).
  This directory is the queue of work pending formalization.
- `formalized/` — one subdirectory per successfully formalized paper, each a
  Gaia package (`<slug>-gaia/`) containing the original source under
  `artifacts/`, the DSL modules, `priors.py`, and compiled artifacts.
- `scripts/` — automation helpers (slug derivation, loop prompt).
- `docs/superpowers/` — specs and plans.
- `_failed/` — local-only failure logs from the automation loop (gitignored).

## Running the automation loop

The loop runs in a Claude Code session. Start it once:

```
/loop 10m "$(cat /Users/risoliao/Code/gaia-lb/papers/scripts/loop-prompt.md)"
```

Every 10 minutes the assistant will: pull the repo, pick the first eligible
file from `inbox/`, derive a slug, scaffold a Gaia package, formalize, run
`gaia compile` + `gaia check`, commit + tag + push on success, or restore the
source and log under `_failed/` on failure. See
`docs/superpowers/specs/2026-04-22-paper-formalization-automation-design.md`
for the full contract.

### Stopping the loop

Type `/loop` in the same session to toggle it off, or close the session.

### Re-formalizing a paper

Delete both the package dir and the tag, then move the source back into
`inbox/`:

```bash
cd /Users/risoliao/Code/gaia-lb/papers
mv formalized/<slug>-gaia/artifacts/<file> inbox/<file>
rm -rf formalized/<slug>-gaia/
git tag -d formalized/<slug>
git push origin :refs/tags/formalized/<slug>
git add -A && git commit -m "Re-queue <slug> for formalization"
```

### Prerequisites

- `gaia-lang` installed in `/Users/risoliao/Code/gaia-lb/venv`.
- SSH access to `git@github.com:liaoruoxue/gaia-papers.git`.
- A Claude Code session with the `gaia` plugin installed.
````

- [ ] **Step 2: Commit**

```bash
cd /Users/risoliao/Code/gaia-lb/papers
git add README.md
git commit -m "docs: add README describing layout and loop operation"
```

---

### Task 6: Push all implementation commits

**Files:** none (git only)

- [ ] **Step 1: Verify branch state**

```bash
cd /Users/risoliao/Code/gaia-lb/papers
git status
git log --oneline origin/main..HEAD
```

Expected: clean working tree; five commits ahead of `origin/main`
(gitignore, slug+tests, loop prompt, README, plus the existing spec commit
if not already pushed). Exact count depends on earlier pushes.

- [ ] **Step 2: Push**

```bash
cd /Users/risoliao/Code/gaia-lb/papers
git push origin main
```

Expected: fast-forward push; exit code 0.

---

### Task 7: End-to-end smoke validation

**Files:** test fixture dropped in `inbox/`, observed outputs only.

This task is not TDD — it verifies the contract in the spec's "Success
Criteria" section by actually running one tick manually.

- [ ] **Step 1: Create a minimal test input**

Use a short markdown paper so the formalization skill can complete quickly:

```bash
cat > /Users/risoliao/Code/gaia-lb/papers/inbox/smoke-test-note.md <<'EOF'
# Smoke Test Note

Claim: The sum of the first n positive integers equals n(n+1)/2.
Justification: Pair the terms 1+n, 2+(n-1), ... — each pair sums to n+1,
and there are n/2 such pairs. Therefore the total is n(n+1)/2.
EOF
```

- [ ] **Step 2: Fire ONE tick manually**

In the Claude Code session, paste the loop prompt literally (not via `/loop`
— we want a one-shot):

```
/compact
```
then paste the full contents of `scripts/loop-prompt.md` as the next user
message. The assistant should execute the workflow once.

- [ ] **Step 3: Verify success path**

Within a few minutes:

```bash
cd /Users/risoliao/Code/gaia-lb/papers
ls inbox/                                    # should NOT contain smoke-test-note.md
ls formalized/smoke-test-note-gaia/artifacts # should contain smoke-test-note.md
git log --oneline -1                         # should be "Formalize: smoke-test-note"
git tag --list 'formalized/*'                # should include formalized/smoke-test-note
git ls-remote --tags origin | grep smoke     # should show the tag on origin
```

- [ ] **Step 4: Verify failure path by inspection**

Forcing a real formalization failure on a carefully-chosen fixture is
unreliable (the skill often produces *something* even on weak input). Instead,
read the Failure Branch in `scripts/loop-prompt.md` and manually trace the
commands against a hypothetical failure at Step 7 (`gaia check .` exits
non-zero). Confirm by eye that the branch:

  1. Writes a log under `_failed/` (gitignored → won't pollute the repo).
  2. Moves the source back to `inbox/`.
  3. Removes the half-baked package dir.
  4. Makes no git commit and no push.

If any of these four is missing or wrong, fix the prompt and commit a patch
before proceeding.

- [ ] **Step 5: Clean up test fixtures**

```bash
cd /Users/risoliao/Code/gaia-lb/papers
rm -rf formalized/smoke-test-note-gaia/
git tag -d formalized/smoke-test-note 2>/dev/null || true
git push origin :refs/tags/formalized/smoke-test-note 2>/dev/null || true
git add -A
git status                        # confirm removal
git commit -m "test: remove smoke-test fixtures" || echo "nothing to commit"
git push origin main
```

- [ ] **Step 6: Start the real loop**

```
/loop 10m "$(cat /Users/risoliao/Code/gaia-lb/papers/scripts/loop-prompt.md)"
```

Confirm the harness accepts it. The first tick fires immediately; subsequent
ticks fire every 10 minutes.

---

## Self-Review Notes

- Spec § Runtime & Cadence → Task 4 (prompt) + Task 5 (README) + Task 7 (start).
- Spec § Per-Tick Workflow steps 1–11 → all mirrored in `loop-prompt.md`.
- Spec § Detection Rule → inbox listing + collision guard in loop prompt.
- Spec § Supported Input Types → `grep -Ei '\.(pdf|md|txt|html)$'` filter.
- Spec § Commit Message Template → inlined in loop prompt Step 8.
- Spec § Tag Format → `git tag formalized/<slug>` in loop prompt Step 8.
- Spec § Error Handling Summary → Failure Branch in loop prompt.
- Spec § Gitignore Additions → Task 1.
- Spec § Success Criteria → Task 7 success and failure smoke tests.
- Spec § Appendix A → superseded by the actual loop prompt in Task 4.
