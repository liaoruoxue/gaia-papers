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

`inbox/` supports two layouts:
- **Direct file:** `inbox/<file>.{pdf,md,txt,html}` — slug derived from the
  filename.
- **Subdirectory:** `inbox/<slug>/` containing a `source.*` file (or a PDF /
  markdown / etc.) — the subdir name *is* the slug. This is the preferred
  layout because it lets the operator pre-specify the slug.

List eligible entries (both direct files and subdirs) and sort:

```bash
cd /Users/risoliao/Code/gaia-lb/papers
{
  find inbox -mindepth 1 -maxdepth 1 -type d -not -name '.*' -exec basename {} \;
  find inbox -mindepth 1 -maxdepth 1 -type f \
    \( -iname '*.pdf' -o -iname '*.md' -o -iname '*.txt' -o -iname '*.html' \) \
    -not -name '.*' -exec basename {} \;
} | sort
```

If the list is empty, **stop this tick**.

Otherwise take the FIRST entry. Call it `<entry>`. An entry is a "subdir
entry" if `test -d inbox/<entry>` is true; otherwise it is a "direct file
entry". Record which branch you are on. Filenames may contain spaces —
**always wrap them in double quotes** in every command below.

## Step 3 — Derive slug

**Subdir entry:** the slug is the entry name itself.
```bash
SLUG="<entry>"
echo "$SLUG"
```

**Direct file entry:** derive slug via the helper.
```bash
cd /Users/risoliao/Code/gaia-lb/papers
SLUG=$(python3 scripts/derive_slug.py "<entry>")
echo "$SLUG"
```

Slugs by construction contain no shell-special characters, so they do not
need quoting, but filenames always do.

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
```

**Subdir entry:** move the contents of `inbox/$SLUG/` into `artifacts/` and
remove the empty subdir.
```bash
mv "inbox/$SLUG"/* "formalized/$SLUG-gaia/artifacts/"
rmdir "inbox/$SLUG"
```

**Direct file entry:** move the file.
```bash
mv "inbox/<entry>" "formalized/$SLUG-gaia/artifacts/<entry>"
```

## Step 6 — Formalize

Invoke the `/gaia:formalization` skill against
`/Users/risoliao/Code/gaia-lb/papers/formalized/$SLUG-gaia/artifacts/<file>`,
fully autonomous. No questions to the operator. If the skill would branch on
a disambiguation, choose the option it marks as default (or, failing that,
the first option listed) and proceed.

**Run the entire six-pass process to completion, including the Critical
Analysis pass.** The required deliverables after this step are:

1. Gaia DSL modules under `src/<pkg>/`
2. `priors.py` at the package root
3. `ANALYSIS.md` at the package root (see SKILL.md § "Critical Analysis" for
   the six required sections: statistics, summary, weak points, evidence gaps,
   contradictions, confidence tiers)

If the skill completes successfully, continue to Step 7. If it raises an
error or produces no DSL output, execute the **Failure Branch** below.

## Step 7 — Compile, check, and verify deliverables

```bash
cd "/Users/risoliao/Code/gaia-lb/papers/formalized/$SLUG-gaia"
source /Users/risoliao/Code/gaia-lb/venv/bin/activate
gaia compile .
gaia check .
test -f ANALYSIS.md || { echo "MISSING ANALYSIS.md"; exit 1; }
```

If any command exits non-zero — including the `ANALYSIS.md` guard — execute
the **Failure Branch** below. Do NOT proceed to Step 8 without ANALYSIS.md.

## Step 8 — Commit, tag, push

```bash
cd /Users/risoliao/Code/gaia-lb/papers
# Stage the new package AND the `mv`-induced inbox deletion(s) in one commit.
# Adding inbox/ picks up deletions from either a moved file or a moved subdir.
git add "formalized/$SLUG-gaia/" inbox/
git commit -m "Formalize: <Original Paper Title>

Autogenerated by the 10-min formalization loop.
Source: inbox/<entry>
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

When Step 5, Step 6, or Step 7 fails (scaffold error, formalization error,
or compile/check failure):

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
# For subdir entries: recreate inbox/$SLUG/ and move the artifacts back.
# For direct file entries: move the file back.
if [ -d "formalized/$SLUG-gaia/artifacts" ]; then
  mkdir -p "inbox/$SLUG"
  mv "formalized/$SLUG-gaia/artifacts"/* "inbox/$SLUG/" 2>/dev/null || true
  # If the inbox/$SLUG dir ended up empty (e.g., no artifacts), remove it.
  rmdir "inbox/$SLUG" 2>/dev/null || true
fi
rm -rf "formalized/$SLUG-gaia/"
```

Note: this failure branch always restores under `inbox/$SLUG/` even if the
original entry was a direct file. Operator can rename/flatten if desired;
the next tick will pick up whichever layout is present.

No git commit, no push. **Stop this tick.**
