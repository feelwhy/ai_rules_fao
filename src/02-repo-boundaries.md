---
id: 02-repo-boundaries
description: Which hub repos are editable vs read-only reference
apply: always
---

# Repository editing boundaries (faOtools hub)

- By default, ONLY create/modify/delete files under the **task’s target repo** (`tools/`, `support/`, `life/`, `system/`, `faotools_env/`, …).
- Which repos to **read / search** for a given task context: see `03-repo-priority`.
- Treat `odoo/`, `enterprise/`, and usually `others/` as **read-only reference**. If a fix seems to require editing core, implement an override in the custom module, or ask for explicit permission.
- Do **not** change another workspace root unless the user explicitly names that repo/module or clearly requests editing outside the current target.
- A general feature request (“change how X behaves”) does **not** grant permission to edit sibling repos — prefer inheritance, JS `patch`, view inheritance, or an override inside the owning module.
- Preserve production / apps-store compatibility: model names, fields, XML IDs, config params, crons, mail templates, routes, and portal URLs stay stable unless the task changes them.

## Commit / push scope (no repo named)

“commit”, “commit A/B…”, “push” **without a named repo** covers **every non-read-only hub checkout**.
Check them all and handle each one that has changes:

`tools`, `system`, `support`, `life`, `faotools_env`, `odoo-apps-addons`, `ai_rules`, `ai_rules_fao`

- This is the one case where **all** repos are inspected regardless of task context — it overrides the
 narrow read scope of `03-repo-priority`.
- **Never commit or push** `odoo`, `enterprise`, `others`. If they show changes, report them and ask —
 do not commit, do not revert (`ai_rules` never-discard-WIP).
- `git status -sb` per repo first; commit only paths belonging to this task. Foreign or unknown WIP →
 stop and ask before committing anything anywhere.
- One command may produce several commits (one per repo). **Report per repo**: repo, branch, short
 SHA, and pushed-or-not — plus the repos that had nothing to commit.
- Mode semantics (A / A1 / B / B1 / B2, tests, review) come from `ai_rules` `16-commit-workflow` and
 apply to **each** repo in scope.
- If the user names a repo (“commit tools”), only that repo. `febado` is never part of the hub commit
 scope — it follows its own in-repo push / MR rules.
