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
| `life` | life.odootools.com (single version, not moved by `env-serie`) |
| `system` | System modules |
| `odoo` / `enterprise` / `others` | Read-only reference unless explicitly asked |
| `odoo-apps-addons` | Independent apps-addons (own in-repo rules) |

## Active Odoo serie

Serie is the branch of the tree a target mounts, not the shared checkout. `env-up` mounts the shared checkout when it is already on that branch, otherwise the worktree that has the branch checked out (usually `_worktrees/<repo>-<branch>`; a detached one does not count). It does not check out the hub. A missing required tree stops the launch. There is no fallback to another serie.

```bash
cd /home/feelwhy/Odoo/faotools_env && ./local/env-serie.sh 18.0
```

That command prints each tree and moves nothing. **Never assume the shared `tools` checkout is 19.0.** “Change version” and “pull” are the skill `01-hub-serie`. Launch and test commands are `ai_rules` `30-command-vocabulary`.

Do not move single-version repos: `life`, `support`, `ai_rules`, `ai_rules_fao`, `faotools_env`. `odoo-apps-addons` has no `16.0`. `others` has no `20.0`. A missing tree is an error. Do not mount the copy baked into the image.

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

# Repo analysis priority

The hub holds many checkouts, but a task almost always lives in one of them. Resolve the
context first (from the chat, the mentioned module/URL, or the MCP server in use), then read
and search the repos **in the listed order**. Repos that are not listed are **out of scope**
unless the user names them.

| Task context | Analyze in this order |
|--------------|-----------------------|
| Public apps-store modules | `tools` > `system` |
| faotools.com public site / support / `faotools_env` deploy | `support` > `faotools_env` > `system` > `tools` |
| life.odootools.com | `life` > `system` > `tools` |
| MCP module (`ai_mcp_server`) | `odoo-apps-addons` |
| faOtools app release | owning repo (`tools` or `odoo-apps-addons`) |

## Rules

- Stop as soon as the listed repos answer the question — do not keep widening the search.
- **Never** pull unrelated repos into the analysis: a `tools` task does not need `support`, and even less `life`.
- `odoo` and `enterprise` are **read-only reference in every context**: read them for core API / view truth, never edit (see `02-repo-boundaries`).
- `others` is read-only reference too, and only relevant when a third-party addon is actually part of the task.
- If the context is genuinely ambiguous, ask which product/repo is meant instead of grepping the whole hub.
- This rule is about **where to look**; permission to write still follows `02-repo-boundaries`.

# Manifest Version

- **Never** modify the `version` field in any `__manifest__.py` under `tools/`.
- When editing manifests (dependencies, assets, data, metadata), leave `version` exactly as it is.
- Bump `version` only when the user explicitly asks for a version increase or release bump.
- **Port exception (19 → 20 only):** during the saas-19.4 stand-in (`Gx.3`), drop the
  serie prefix (`19.0.1.3.33` → `1.3.33`) so `check_version` does not set
  `installable=False` on `saas~19.4`. At `Fx` / phase 8, on real 20.0, write
  `20.0.` + that same tail. Do not invent a fourth number. See `ai_rules`
  `22-migrate-v19-to-v20` **Manifest version**.
- If a task would normally imply a version change, do not bump automatically — ask the user first.
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
- This is the reference implementation for the pattern: `[knowsystem/models/knowsystem_article.py](knowsystem/models/knowsystem_article.py)` (`action_check_option`, ~L791-802).
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

- Local Odoo runs **only in Docker** via `faotools_env/local/` — never a host Python virtualenv or host `odoo-bin`.
- Launch a target (restores + neutralizes on first run):

```bash
cd /home/feelwhy/Odoo/faotools_env
./local/env-up.sh demo19          # community all-apps 19 → http://localhost:18190
./local/env-up.sh demo19e         # enterprise all-apps 19 → http://localhost:18191
./local/env-up.sh support         # faotools.com (neutralized) → http://localhost:18100
```

- Prefer Odoo ORM via the container shell:

```bash
./local/env-shell.sh demo19       # odoo shell
./local/env-shell.sh demo19 psql  # SQL against the local Postgres (host port 15432)
```

- Several targets (and Febado) can run at once — each Odoo has its own HTTP port
  (`support` 18100, `life` 18110, `demo19` 18190, …); shared Mailpit is on **18025**.
  See `faotools_env/local/README.md`.
- Keep images/DBs fresh: `./local/env-sync.sh` (or `./local/env-sync.sh --check`).
- Never store local database credentials, tokens, or connection strings in repository files.
- Details: `faotools_env/local/README.md`.

## Lifecycle: leave nothing behind

WSL shares one VM (and 18 GB) between Cursor and every container, and its disk
files never shrink on their own. Incident 2026-09-28: 22 Odoo containers booted
together with Docker Desktop, 167 databases (152 agent leftovers), 62 orphaned
~1.2 GB volumes; the two VHDX files had reached ~400 GB.

- **Stop what you started.** When this chat is done with a target it launched,
  `./local/env-down.sh <target>`. Odoo containers are `restart: "no"`; nothing but
  Postgres, Mailpit and the registry proxy boots with Docker.
- **No hand-made stacks or databases.** Anything outside the target table (review
  DB, install-matrix DB, probe) is created by a script or registered at once:
  `./local/env-review.sh keep <db> --hours N`. Unregistered, it is removed by
  `env-gc.sh` after 12h.
- **The creator drops it.** A batch that creates databases (install matrix,
  coverage, builds) drops them in the same batch; `env-up.sh --test` already drops
  its `test_*` clone. `./local/env-review.sh down <db>` removes a stack completely.
- **Remove containers with their volume.** `env-down.sh --remove`,
  `env-review.sh down` or `docker rm -f -v`. Never `docker compose down` / `rm -v`
  alone: a container started with `--no-bind`, or an older container, can still
  leave the baked-addons volume behind. A normal launch does not create one.
- **Cleanup = `./local/env-gc.sh`** (dry run) then `--apply`. `env-sync.sh` runs it
  at the end. Never `docker system prune` / `volume prune --all`: they also delete Febado's
  stopped containers and named volumes.
- After a large cleanup, tell the user to run `local/windows/compact-wsl-disks.ps1`
  from an elevated PowerShell (it shuts WSL down, so an agent cannot run it).


## Serie + bind mounts

- `env-up` mounts the shared checkout when it is already on the serie branch, otherwise the worktree that has the branch checked out (usually `_worktrees/<repo>-<branch>`; a detached one does not count). It does not check out the hub. A missing required tree stops the launch, names the repo and the branch, and prints the `git worktree add` command (`01-hub-serie` rule 3).
- `./local/env-serie.sh <serie>` prints those paths and moves nothing.
- The official image declares `VOLUME /mnt/extra-addons`. A normal launch bind-mounts `faotools_env/addons/runtime` over that path, so Docker does not copy the baked addon tree. `env_dbfilter_header` comes from that directory. `--no-bind` still gets the copy.
- Clean serie trees are fast-forwarded by nightly `env-git-daily` (05:00). Launch does not fetch. The launch log says whether each tree matches that last fetch.
- **Same target again** (already running, or last launched in this chat): only
  `./local/env-up.sh <target> --restart`. No serie switch, prepare, sync, or
  other edits — see `ai_rules` `30-command-vocabulary`.
- See `faotools_env/local/README.md` for full port matrix and sync behavior.

# Live faOtools MCP

- The real live support database may be reachable through the enabled faOtools MCP server (`user-faotools`).
- Use it when a task needs production truth that cannot be reliably inferred from code, such as current `ir.ui.view` contents, live website metadata, config parameters, cron state, or app/module records.
- Prefer read-only MCP checks unless the user explicitly asks to update live data.
- Before calling any MCP tool, inspect that tool's descriptor/schema and use the documented parameters.
- Treat live data as production data: do not expose secrets, tokens, customer-private details, or raw sensitive payloads in chat.
- If code and live behavior disagree, consider whether the module has not been upgraded, a view was customized in the database, or cached/generated content is stale.
- App releases (`module.release`): follow `33-faotools-release`. Do not invent a parallel publish path.

# Release gates

These bans apply even when the user did not say “publish a release”. The sequence, HTML samples, notes, YAML, and the MCP payload recipe are the skill `33-faotools-release`. Read that skill before any `module.release` write.

- Scope is `tools` and `odoo-apps-addons` only. Refuse `support`, `life`, `system`, `faotools_env`. Do not write a row with `prepublish=True`. Do not bump `__manifest__.py` (`11-manifest-version`).
- A new serie: the changelog is published while the page is still hidden, then the page is made public. A public page with an empty changelog is a failed release.
- Bump only the last number of `exact_version`. Across a major serie, keep the same tail. Do not invent an extra number.
- Do not call Quick GitHub Update (`action_update_in_github_quick` / `action_update_in_github`) through MCP. That call commits per module and aborts the MCP transaction.
- “Published” is allowed only after the live page for every shipped language has no new English sentence. A filled `.po` is not that (Appointments `1.3.33`, 2026-09-10, `/ru/` stayed English). A loader return code is not that. An MCP or encoding error means rewrite the payload and apply again (2026-09-28). Stop only when the user explicitly says to skip translations.
- A changelog icon has a space inside the tag, `<i class="fa ..."> </i>`. An empty `<i></i>` becomes `<i/>` and swallows the page (2026-08-23). The full rule is `18-xml-translate-html`.
