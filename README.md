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
git add formalized/ inbox/
git commit -m "Re-queue <slug> for formalization"
```

### Prerequisites

- `gaia-lang` installed in `/Users/risoliao/Code/gaia-lb/venv`.
- SSH access to `git@github.com:liaoruoxue/gaia-papers.git`.
- A Claude Code session with the `gaia` plugin installed.
