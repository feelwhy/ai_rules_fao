---
id: 02-repo-boundaries
description: Which hub repos are editable vs read-only reference
apply: always
---

# Repository editing boundaries (faOtools hub)

- By default, ONLY create/modify/delete files under the **task’s target repo** (`tools/`, `support/`, `system/`, `faotools_env/`, …).
- Which repos to **read / search** for a given task context: see `03-repo-priority`.
- Treat `odoo/`, `enterprise/`, and usually `others/` as **read-only reference**. If a fix seems to require editing core, implement an override in the custom module, or ask for explicit permission.
- `life/` is a separate project (life.odootools.com). Do not read, edit, or commit it from this project.
- Do **not** change another workspace root unless the user explicitly names that repo/module or clearly requests editing outside the current target.
- A general feature request (“change how X behaves”) does **not** grant permission to edit sibling repos — prefer inheritance, JS `patch`, view inheritance, or an override inside the owning module.
- Preserve production / apps-store compatibility: model names, fields, XML IDs, config params, crons, mail templates, routes, and portal URLs stay stable unless the task changes them.

## odoo-apps-addons is read-only (hard ban)

We do not change `odoo-apps-addons`. Its developer does. Incident 2026-11-21: a chat pushed `cbaf767` (expired MCP session) straight to `19.0` without a PR and copied it onto master and faotools.com by hand. It never reached `17.0`, `18.0`, or `20.0`, and the developer did not know it existed.

- Do not edit, commit, push, revert, cherry-pick, branch, or open a PR in it. Any serie, any worktree, any file, `.po` included.
- Do not copy its files onto master, the worker, or a container by hand (`rsync`, `docker cp`, editing a volume).
- Reading is allowed: diagnose, cite `path:line`, run its tests in local Docker.
- A fix that seems to need it: write the task for the developer (symptom, how to reproduce, proposed change, series) and hand it to the owner. Stop there.
- The developer does not bump a module `version`. We do, through the release (`33-faotools-release`). New stored fields with no version bump are normal: not a developer mistake and not a task for them. A live update runs `-u` for every module whose files changed, not by version (`faotools_env` `redeploy-verify-live.mdc`).
- This outranks any other rule that lists `odoo-apps-addons` as editable or in a commit scope. A `module.release` on faotools.com is a live record, not a repo edit, and stays under `33-release-gates`.

## Commit / push scope (no repo named)

“commit”, “commit A/B…”, “push” **without a named repo** covers **every non-read-only hub checkout**.
Check them all and handle each one that has changes:

`tools`, `system`, `support`, `faotools_env`, `ai_rules`, `ai_rules_fao`

This is the one case where **all** repos are inspected regardless of task context — it overrides the narrow read scope of `03-repo-priority`.

**Never commit or push** `odoo`, `enterprise`, `others`, `odoo-apps-addons`. If they show changes, report them and ask — do not commit, do not revert (`ai_rules` `03-never-discard-wip`).

If the user names a repo (“commit tools”), only that repo. `febado` is never part of the hub commit scope — it follows its own in-repo push / MR rules.

Report each repo: branch, short SHA, pushed or not, and the repos with nothing to commit.

How to commit, test, and report is `ai_rules` `16-commit-workflow`.
