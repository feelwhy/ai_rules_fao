# ai_rules_fao

Generated from `src/*.md` by `tools/sync_rules.py`. Do not edit by hand.
Always-on rules only. Procedures are skills in `.claude/skills/`.

# faOtools hub repo map

## Hub root

`/home/feelwhy/Odoo` — one shared checkout per repo, plus `_worktrees/<repo>-<branch>` for the other branches. No live `OdooNN/` trees, no `tools-ports/`. Ignore `_archive/`.

## Workspace folders (typical faotools.code-workspace)

| Folder | Role |
|--------|------|
| `ai_rules` | Universal Cursor rules (generated) |
| `ai_rules_fao` | faOtools-specific rules (this repo) |
| `faotools_env` | Local Docker toolkit + master/worker deploy |
| `tools` | Apps-store modules (editable). The serie is the branch of the tree you edit |
| `support` | faotools.com / helpdesk DB custom addons |
| `system` | System modules |
| `odoo` / `enterprise` / `others` | Read-only reference unless explicitly asked |
| `odoo-apps-addons` | Independent apps-addons (own in-repo rules) |

## Active Odoo serie

Serie is the branch of the tree a target mounts, not the shared checkout. `env-up` mounts the shared checkout when it is already on that branch, otherwise the worktree that has the branch checked out (usually `_worktrees/<repo>-<branch>`; a detached one does not count). It does not check out the hub. A missing required tree stops the launch. There is no fallback to another serie.

```bash
cd /home/feelwhy/Odoo/faotools_env && ./local/env-serie.sh 18.0
```

That command prints each tree and moves nothing. **Never assume the shared `tools` checkout is 19.0.** “Change version” and “pull” are the skill `01-hub-serie`. Launch and test commands are `ai_rules` `30-command-vocabulary`.

Do not move single-version repos: `support`, `ai_rules`, `ai_rules_fao`, `faotools_env`. `odoo-apps-addons` has no `16.0`. `others` has no `20.0`. A missing tree is an error. Do not mount the copy baked into the image.

Edit the tree `env-serie.sh` prints. A fix in another checkout does not reach the container. Pull is `--ff-only` on the tree already on that branch. Dirty or diverged: stop, do not stash.

## Manifest version policy (hub)

- **tools**: `11-manifest-version`.
- **faotools_env** `env_master`: bump when shipping a live upgrade.
- **febado**: follow febado in-repo rules (not this repo).
- **odoo-apps-addons**: follow its in-repo rules.

## Who owns rules

- Universal coding / process → `ai_rules`
- Hub map, boundaries, packaging, local Docker, MCP, prepublishment, app releases → `ai_rules_fao`
- Stays in-repo: support SEO/MCP description/index/support-database/v19-migration/translations; tools email-suite / jstree; faotools_env deploy rules; febado committed `.mdc`
- Translations: bans in `17-translation-gates`, glossary and loader steps in the skill `17-translations`. Icon HTML is `ai_rules` `18-xml-translate-html`.
- Demo data: skill `34-demo-data`. KnowSystem articles: skill `35-knowsystem-demo`.
- A major port of the `tools` apps is not done when the last module group is green. The rest is the skill `36-major-version-port`.
- App releases: bans in `33-release-gates`, sequence in the skill `33-faotools-release`.
- LinkedIn company-page posts: skill `37-linkedin-publications`. The owner publishes.

# Repository editing boundaries (faOtools hub)

- By default, ONLY create/modify/delete files under the **task’s target repo** (`tools/`, `support/`, `system/`, `faotools_env/`, …).
- Which repos to **read / search** for a given task context: see `03-repo-priority`.
- Treat `odoo/`, `enterprise/`, and usually `others/` as **read-only reference**. If a fix seems to require editing core, implement an override in the custom module, or ask for explicit permission.
- `life/` is a separate project (life.odootools.com). Do not read, edit, or commit it from this project.
- Do **not** change another workspace root unless the user explicitly names that repo/module or clearly requests editing outside the current target.
- A general feature request (“change how X behaves”) does **not** grant permission to edit sibling repos — prefer inheritance, JS `patch`, view inheritance, or an override inside the owning module.
- Preserve production / apps-store compatibility: model names, fields, XML IDs, config params, crons, mail templates, routes, and portal URLs stay stable unless the task changes them.

## Commit / push scope (no repo named)

“commit”, “commit A/B…”, “push” **without a named repo** covers **every non-read-only hub checkout**.
Check them all and handle each one that has changes:

`tools`, `system`, `support`, `faotools_env`, `odoo-apps-addons`, `ai_rules`, `ai_rules_fao`

This is the one case where **all** repos are inspected regardless of task context — it overrides the narrow read scope of `03-repo-priority`.

**Never commit or push** `odoo`, `enterprise`, `others`. If they show changes, report them and ask — do not commit, do not revert (`ai_rules` `03-never-discard-wip`).

If the user names a repo (“commit tools”), only that repo. `febado` is never part of the hub commit scope — it follows its own in-repo push / MR rules.

Report each repo: branch, short SHA, pushed or not, and the repos with nothing to commit.

How to commit, test, and report is `ai_rules` `16-commit-workflow`.

# Repo analysis priority

The hub holds many checkouts, but a task almost always lives in one of them. Resolve the
context first (from the chat, the mentioned module/URL, or the MCP server in use), then read
and search the repos **in the listed order**. Repos that are not listed are **out of scope**
unless the user names them. `odoo` and `enterprise` are the exception: read them for core API and view truth.

| Task context | Analyze in this order |
|--------------|-----------------------|
| Public apps-store modules | `tools` > `system` |
| faotools.com public site / support / `faotools_env` deploy | `support` > `faotools_env` > `system` > `tools` |
| MCP module (`ai_mcp_server`) | `odoo-apps-addons` |
| faOtools app release | owning repo (`tools` or `odoo-apps-addons`) |

## Rules

- Stop as soon as the listed repos answer the question — do not keep widening the search.
- **Never** pull unrelated repos into the analysis: a `tools` task does not need `support`.
- Search `others` only when a third-party addon is part of the task.
- If the context is genuinely ambiguous, ask which product/repo is meant instead of grepping the whole hub.
- Where to write, and which repos are read-only, is `02-repo-boundaries`.

# Manifest Version

- **Never** modify the `version` field in any `__manifest__.py` under `tools/` unless the user explicitly asks. Editing dependencies, assets, data, or metadata is not that ask.
- **Port exception (19 → 20 only):** during the saas-19.4 stand-in (`Gx.3`), drop the
  serie prefix (`19.0.1.3.33` → `1.3.33`) so `check_version` does not set
  `installable=False` on `saas~19.4`. At `Fx` / phase 8, on real 20.0, write
  `20.0.` + that same tail. Do not invent a fourth number. See `ai_rules`
  `22-migrate-v19-to-v20` **Manifest version**.
- “Make / publish a release” bumps `module.description.exact_version` on faotools.com (`33-faotools-release`). Do not bump the local `__manifest__.py` unless the user also asks for that.

# Boolean Settings Convention

- Every module setting is either `True` (turned on) or `False` (turned off, including "never selected"). No tri-state, no `None`-as-a-third-state handling.
- Boolean settings backed by `ir.config_parameter` must be declared as plain `fields.Boolean(config_parameter="...")` with **no `default=True`**. An unset/never-saved parameter must read as `False`.
- Read these parameters as real booleans with `safe_eval`, never by string-comparing to `"True"`/`"False"`:

```python
from odoo.tools.safe_eval import safe_eval

icp = self.env["ir.config_parameter"].sudo()
enabled = safe_eval(icp.get_param("my_module.some_flag", "False"))
if enabled:
    ...
```

- Forbidden patterns anywhere in `tools/` modules:
  - `get_param(key) == "True"` / `!= "True"`
  - `get_param(key) == "False"` / `!= "False"`
  - `if param is None: return True` (or similar tri-state fallback for a boolean)
  - `default=True` on a `fields.Boolean(config_parameter=...)`
- This is the reference implementation for the pattern: `knowsystem` `action_check_option` in `knowsystem/models/knowsystem_article.py`.
- Apply this convention consistently to every module in this workspace, not just the one currently being edited.

# Translation gates

A translation file in git is not a translation on the site. The glossary, paths, YAML keys, pic steps, and scripts are the skill `17-translations`. Read it when the task changes copy, `.po`, or `module.description`.

- Done means the live page or the live field no longer shows the English sentence. A loader return code and a report of “MISSING: 0” are not that proof.
- Screenshot titles are a separate apply. Translating the guideline body leaves `/ru/` captions English (Google Drive, 2026-09-01, `Open the Google Auth Platform`). `module.pic.name` and `alt_name` are translated. The PNG stays English. Prove the live `ru_RU` value differs from `en_US`.
- Changing English in a template leaves the new term empty on an existing database (Appointments `Any` / `Select`, 2026-09-09). The empty-term fill is part of the same change.
- YAML written in this checkout is not applied by the prepublication hook. That hook reads the copy already on the Functional container. The live apply is still required.
- Store HTML, GitHub manifests, and support mail templates stay `en_US`. KnowSystem article records and `/docs` stay English.
- A 19.0+ release changelog follows `33-release-gates`. Filling the app `.po` is not that translation (Appointments `1.3.33`, 2026-09-10).

# Local Database Access

Local Odoo runs **only** through `faotools_env/local/env-up.sh` and `env-shell.sh`. Never a host Python virtualenv or host `odoo-bin`. Commands, ports, and Mailpit are the skill `20-local-commands`.

Never store local database credentials, tokens, or connection strings in repository files.

## Lifecycle: leave nothing behind

- **Stop what you started.** When this chat is done with a target it launched, `./local/env-down.sh <target>`. Odoo containers are `restart: "no"`; nothing but Postgres, Mailpit and the registry proxy boots with Docker.
- **No hand-made stacks or databases.** Anything outside the target table is created by a script or registered at once: `./local/env-review.sh keep <db> --hours N`. Unregistered, `env-gc.sh` removes it after 12h.
- **The creator drops it.** A batch that creates databases drops them in the same batch. `env-up.sh --test` already drops its `test_*` clone. `./local/env-review.sh down <db>` removes a stack completely.
- **Remove containers with their volume.** `env-down.sh --remove`, `env-review.sh down`, or `docker rm -f -v`. Never `docker compose down` / `rm -v` alone: a container started with `--no-bind`, or an older container, can still leave the baked-addons volume behind. A normal launch does not create one.
- **Cleanup = `./local/env-gc.sh`** (dry run) then `--apply`. Never `docker system prune` / `volume prune --all`: they also delete Febado's stopped containers and named volumes.

## Serie + bind mounts

`env-up` mounts the shared checkout when it is already on the serie branch, otherwise the worktree that has the branch checked out (usually `_worktrees/<repo>-<branch>`; a detached one does not count). It does not check out the hub. A missing required tree stops the launch. There is no fallback to another serie. `./local/env-serie.sh <serie>` prints those paths and moves nothing.

A normal launch bind-mounts `faotools_env/addons/runtime` over the image's `/mnt/extra-addons`, so Docker does not copy the baked addon tree. `--no-bind` still gets the copy. Launch does not fetch. Nightly `env-git-daily` (05:00) fast-forwards clean serie trees.

The same target again: only `./local/env-up.sh <target> --restart`. The rest of that case is `ai_rules` `30-command-vocabulary`.

# Live faOtools MCP

- The real live support database may be reachable through the enabled faOtools MCP server (`user-faotools`).
- Use it when a task needs production truth that cannot be reliably inferred from code, such as current `ir.ui.view` contents, live website metadata, config parameters, cron state, or app/module records.
- Prefer read-only MCP checks unless the user explicitly asks to update live data.
- Before calling any MCP tool, inspect that tool's descriptor/schema and use the documented parameters.
- Treat live data as production data: do not expose secrets, tokens, customer-private details, or raw sensitive payloads in chat.
- If code and live behavior disagree, consider whether the module has not been upgraded, a view was customized in the database, or cached/generated content is stale.
- App releases (`module.release`): follow `33-faotools-release`. Do not invent a parallel publish path.

## Files: upload them yourself

The agent uploads every file itself. Never hand a PDF or image to the owner to attach (`linkedin.post` 6 and 7, 2026-11).

- Under ~40 KB: `odoo_attachments_upload_inline`.
- Larger: `odoo_attachments_upload_prepare` (pass `sha256`), then `curl -X PUT -H "X-MCP-Upload-Ticket: <upload_ticket>" -H "Content-Type: <mime>" --data-binary @<file> <upload_url_base>` (expect `204`), then `odoo_attachments_upload_commit`.
- A binary field (`attachment=True`, e.g. `linkedin.post.presentation`): pass `res_model` / `res_id` to prepare, then write the committed `ir.attachment` with `res_field` = the field name and `name` = the field name. Read back: exactly one attachment with that `res_field`, and its `file_size` equals the file.
- This works because `ai_mcp_server.upload_presigned_enabled` is `True` on faotools.com and master.odootools.com (set 2026-11-24). If prepare returns `requires_bearer_token: true`, the setting was turned off: say so and ask the owner to tick Settings → MCP Server → Allow Pre-signed Uploads. Do not fall back to the upload page.

# Release gates

These bans apply even when the user did not say “publish a release”. The sequence, HTML samples, notes, YAML, and the MCP payload recipe are the skill `33-faotools-release`. Read that skill before any `module.release` write.

- Scope is `tools` and `odoo-apps-addons` only. Refuse `support`, `life`, `system`, `faotools_env`. Do not write a row with `prepublish=True`. Do not bump `__manifest__.py` (`11-manifest-version`).
- A new serie: the changelog is published while the page is still hidden, then the page is made public. A public page with an empty changelog is a failed release.
- Bump only the last number of `exact_version`. Across a major serie, keep the same tail. Do not invent an extra number.
- Do not call Quick GitHub Update (`action_update_in_github_quick` / `action_update_in_github`) through MCP. That call commits per module and aborts the MCP transaction.
- “Published” is allowed only after the live page for every shipped language has no new English sentence. A filled `.po` is not that (Appointments `1.3.33`, 2026-09-10, `/ru/` stayed English). A loader return code is not that. An MCP or encoding error means rewrite the payload and apply again (2026-09-28). Stop only when the user explicitly says to skip translations.
- A changelog icon has a space inside the tag, `<i class="fa ..."> </i>`. An empty `<i></i>` becomes `<i/>` and swallows the page (2026-08-23). The full rule is `18-xml-translate-html`.
