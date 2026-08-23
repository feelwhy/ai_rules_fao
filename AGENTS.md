# ai_rules_fao

Generated from `src/*.md` by `tools/sync_rules.py`. Do not edit by hand.

## 00-repo-map

_Flat hub repo map, serie resolution, and who owns which rules_

# faOtools hub repo map

## Hub root

`/home/feelwhy/Odoo` — one checkout per repo (flat). No live `OdooNN/` trees, no `tools-ports/`. Ignore `_archive/`.

## Workspace folders (typical faotools.code-workspace)

| Folder | Role |
|--------|------|
| `ai_rules` | Universal Cursor rules (generated) |
| `ai_rules_fao` | faOtools-specific rules (this repo) |
| `faotools_env` | Local Docker toolkit + master/worker deploy |
| `tools` | Apps-store modules (editable); **git branch = serie** |
| `support` | faotools.com / helpdesk DB custom addons |
| `life` | life.odootools.com (not switched by `env-serie`) |
| `system` | System modules |
| `odoo` / `enterprise` / `others` | Read-only reference unless explicitly asked |
| `odoo-apps-addons` | Independent apps-addons (own in-repo rules) |

## Active Odoo serie

Serie is **not** in the path. It is the current git branch on bind-mounted repos:

```bash
git -C /home/feelwhy/Odoo/tools rev-parse --abbrev-ref HEAD
# or switch:
cd /home/feelwhy/Odoo/faotools_env && ./local/env-serie.sh 18.0
```

`env-serie.sh` / `env-up` switch tools, odoo, enterprise, support, others, system, odoo-apps-addons, OpenUpgrade, febado*, … — **skips** `life` and `faotools_env`. Missing branch → fallback `LATEST_SERIE` (19.0). **Never assume tools is 19.0.** For a “change version to \<serie\>” request use the explicit repo list in `01-hub-serie` (`env-serie.sh` moves `support` too and aborts on `febado`).

## Test / run (Docker only)

| Intent | Command |
|--------|---------|
| community demo serie N | `faotools_env/local/env-up.sh demoN --test <module>` |
| enterprise demo serie N | `… demoNe --test <module>` |
| support / faotools.com | `… support` or `bash support/devops/run_tests.sh "<m>" 19 docker` |
| life | `… life` |
| shell / logs | `env-shell.sh <target>`; `docker compose -f local/run/<target>/compose.yml logs -f` |
| switch hub serie | `faotools_env/local/env-serie.sh <serie>` |

## Manifest version policy (hub)

- **tools**: never bump `__manifest__.py` `version` unless the user asks (see `11-manifest-version`).
- **faotools_env** `env_master`: bump when shipping a live upgrade.
- **febado**: follow febado in-repo rules (not this repo).
- **odoo-apps-addons**: follow its in-repo rules.

## Who owns rules

- Universal coding / process → `ai_rules`
- Hub map, boundaries, packaging, local Docker, MCP, prepublishment, app releases → `ai_rules_fao`
- Stays in-repo: support SEO/MCP description/index/support-database/v19-migration/translations; tools email-suite / jstree; faotools_env deploy rules; febado committed `.mdc`
- Translations (glossary, TM, loader): `support/support_translations/` — hub rule `17-translations` is always-on
- App store releases (`module.release` on faotools.com): `33-faotools-release` (`tools` / `odoo-apps-addons` only). 19.0+ public `description` is TM-first (`17-translations`).

## 01-hub-serie

_Hub serie discipline — shared checkout branch, switch-branch and pull-changes commands_

# Hub serie discipline

The flat hub uses **one working tree per repo**. Checking out another serie changes what every Cursor session and every bind-mounted Docker target sees.

## Rules

1. Before `env-serie.sh`, `git checkout`, or `env-up` that switches branches: `git status -sb` on affected repos; respect `ai_rules` never-discard-WIP.
2. Do **not** assume `tools` / `odoo` are on 19.0 — read the branch or ask.
3. Switch the hub **consistently** — move all serie repos together (see the change-version command below), never a random subset. `env-serie.sh <serie>` is the right tool only when you *want* its wider repo list (`support`, `OpenUpgrade`, `febado*`) touched too.
4. `life`, `support`, `ai_rules`, `ai_rules_fao` and `faotools_env` ship in a **single version**; do not “fix” them onto 17.0/18.0 (they may still carry ad-hoc feature branches the user created).
5. After a serie switch, warn that running containers may still be on the previous image/DB until recreated with `env-up`.
6. Do not create parallel `tools-ports/` or `OdooNN/` checkouts for day-to-day work — serie = branch.

## Command: “change version / switch branch to \<serie\>”

“change version to 16.0”, “change branch to 16.0”, “switch branch to 18.0”, “switch to 19”,
“let’s work on 17.0” are all the **same command** — version, serie and branch mean the same thing
here. A bare major number means `\<major\>.0` (“switch to 19” → `19.0`).

With no repo named it means: put the **serie-switched repos** on that branch:

`tools`, `system`, `odoo`, `enterprise`, `others`, `odoo-apps-addons`

- Branch name **is** the serie (`16.0`, `17.0`, …). Check out exactly those repos, falling back to
 `LATEST_SERIE` when the serie branch does not exist:

```bash
for r in tools system odoo enterprise others odoo-apps-addons; do
 p="/home/feelwhy/Odoo/$r"
 git -C "$p" checkout 16.0 2>/dev/null \
 || { git -C "$p" fetch -q origin 16.0 2>/dev/null; git -C "$p" checkout 16.0 2>/dev/null; } \
 || git -C "$p" checkout 19.0
done
```

- Do **not** use `env-serie.sh <serie>` for this command: it also switches `support` (which has old
 serie branches, e.g. `15.0`, and must stay on its single version) and it **dies** on `febado`,
 whose only branch is a feature branch — leaving the hub half-switched.
- **Missing branch → latest serie** (`LATEST_SERIE`, currently `19.0`). Never create the branch,
 never leave a repo detached. A remote-only serie branch is fine: plain `git checkout <serie>`
 creates the local tracking branch, so fetch only if that fails.
- **Report the resulting branch per repo** and call out every fallback explicitly: e.g. `odoo` /
 `enterprise` have no `16.0`, so a “version 16.0” request leaves core on 19.0 — say so, because
 16.0 addons against 19.0 core will not load.
- **If the user names repos** (“change tools to 16.0”, “only system on 18.0”), switch **only**
 those and leave the rest of the hub alone.
- Single-version repos (rule 4) are never included unless the user explicitly asks for them.
- **Always pull after switching** (see next section) so the new branch is up to date, and report the
 per-repo result of both steps.
- Rules 1 and 5 still apply: check `git status -sb` first and stop on foreign WIP; afterwards
 remind that containers keep the old image/DB until `env-up` recreates them.

## Command: “pull changes”

“pull changes”, “pull”, “update the repos” means: fast-forward each repo’s **current branch** from
its upstream.

- **No repo named → every hub checkout**, including the single-version ones (`support`, `life`,
 `ai_rules`, `ai_rules_fao`, `faotools_env`) and `odoo` / `enterprise`. Pulling only updates a
 read-only reference; it does not make it editable.
- **Repo named** (“pull tools”) → only that repo. **Branch named** (“pull 18.0”, “pull tools 18.0”)
 → switch that repo/the serie repos to the branch first, then pull it.

```bash
git -C "/home/feelwhy/Odoo/$r" pull --ff-only
```

- **`--ff-only`, always.** Never `merge`, `rebase`, `pull --rebase`, `reset --hard`, or force
 anything to make a pull land.
- **Skip and report, do not fix**, when a repo is dirty, detached, has no upstream, or has diverged
 (local commits the remote does not have — e.g. `tools` sitting “ahead 1”). Ask the user what to do
 with those; never stash or drop their commits (`ai_rules` never-discard-WIP).
- `git fetch` first when the upstream ref may be stale, or when the branch was just created locally
 from a remote serie branch.
- **Report per repo**: updated (with commit count / new HEAD), already up to date, or skipped with
 the reason.
- After pulling repos that Docker bind-mounts, remind that running containers keep the old code
 until restarted (`env-up`), and that a `-u <module>` upgrade may be needed for XML/asset changes.

## Intentional shared checkout

If the user is browsing or testing on a branch, keep **this chat’s work on that same shared checkout** unless they ask for a side worktree. Parking work only in a disconnected worktree while the shared tree stays elsewhere breaks live Docker bind-mounts and SCM visibility.

## 02-repo-boundaries

_Which hub repos are editable vs read-only reference_

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

## 03-repo-priority

_Which hub repos to read and search first for each task context_

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

## 10-apps-store-packaging

_Apps-store packaging, metadata, and installability expectations for tools modules_

# Apps Store Metadata
- Keep manifests valid Python dictionaries accepted by Odoo 19.
- Preserve `name`, `summary`, `description`, `author`, `website`, `license`, `price`, `currency`, `images`, and `live_test_url` unless explicitly changing listing metadata.
- Version format is `19.0.x.y.z`; never change `version` unless the user explicitly requests a bump (see `manifest-version` rule).

# Module Independence
- A top-level add-on must install with only its manifest dependencies and standard Odoo/Enterprise modules.
- Shared product-family behavior belongs in an explicit base module dependency, not in implicit imports or undeclared XML references.
- Do not make a module depend on a sibling app only to reuse a tiny helper; duplicate small app-local glue when that preserves product independence.

# Static Description
- Keep `static/description/index.html` and manifest `images` in sync.
- Do not remove screenshots, icons, or marketing HTML during code-only tasks.
- Generated/minified listing assets are packaging artifacts; edit source files when available.
- For faOtools prepublishment copy (MCP `module.description` / features / perfect-for), follow `prepublishment-descriptions.mdc`.

# Licensing
- Preserve proprietary licensing text and `LICENSE` files.
- Do not introduce third-party code or vendored libraries without confirming license compatibility.

## 11-manifest-version

_Never change tools module manifest version unless the user explicitly requests it_

# Manifest Version

- **Never** modify the `version` field in any `__manifest__.py` under `tools/`.
- When editing manifests (dependencies, assets, data, metadata), leave `version` exactly as it is.
- Bump `version` only when the user explicitly asks for a version increase or release bump.
- If a task would normally imply a version change, do not bump automatically — ask the user first.
- “Make / publish a release” bumps `module.description.exact_version` on faotools.com (`33-faotools-release`). Do not bump the local `__manifest__.py` unless the user also asks for that.

## 12-boolean-settings

_Store and read config_parameter boolean settings as real Python booleans_

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

## 13-search-views

_Search views for new list/form actions (fields, group-by, archived filter)_

# Search Views for New Models

Whenever a new model gets a list/form action (or an existing action is missing one), add a dedicated `<search>` view and wire it via `search_view_id` on the `ir.actions.act_window`.

## Search fields

- Add `<field name="...">` entries for the model's key user-facing fields: the main identifying `Char`/`text` fields and the important `Many2one` relations (e.g. the fields shown in the list view). Many2one fields in a search already let users type free text and match via `name_search`, so no extra `filter_domain` is needed unless you must search a related sub-field (e.g. `('partner_id.email', 'ilike', self)`).
- Prefer 3-6 search fields: enough to cover real lookups, not every field on the model.

## Group By

- Add a `<group>` block with one `<filter ... context="{'group_by': '<field>'}"/>` per Many2one/Selection field users would plausibly want to group by (status, category, owning record, assigned user, etc).
- Name each filter `group_by_<field>` (or a short readable `name`) and give it a clear `string`.

## Archived filter

- If the model has an `active` field (the default unless explicitly non-archivable), always add:

```xml
<filter string="Archived" name="inactive" domain="[('active', '=', False)]"/>
```

- Place it as its own line (optionally after a `<separator/>`) before the `group_by` block.

## Wiring

- Reference the search view from the action: `<field name="search_view_id" ref="<module>.<search_view_id>"/>`.
- Follow existing XML ID and file-naming conventions (`<record id="..._view_search">`, `<field name="name"><model>.search</field>`).

See `email_from_rule_views.xml` / `email_from_address_views.xml` in `odoo_email_from` for a concrete example (search by key relations, archived filter, group by the same relations).

## 17-translations

_Hub wiring for faOtools translations (support_translations TM, tools .po, no store leak)_

# faOtools hub translations

Companion to `ai_rules` `17-translations`. Read both when the task changes copy, i18n, or `module.description`.

## Where files live

| Surface | Repo / path |
|---------|-------------|
| Glossary, do-not-translate, TM, loader, validators | `support/support_translations/` |
| App UI `.pot` / `.po` | `tools/<module>/i18n/` and `odoo-apps-addons/ai_mcp_server/i18n/` |
| Website QWeb code templates | `support/*/i18n/` plus loader YAML for website-builder (COW) views |
| Cursor rules | `ai_rules` `src/17-translations.md`, this file, `support/.cursor/rules/translations.mdc` |

Do not add a parallel glossary in `tools/` or `life/`.

## Loader vs `.po`

- **`.po`**: exportable strings in Python / XML / JS (`_()`, `string=`, `_t()`).
- **Loader** (`support.translations`): `module.description` and children (including public `module.release.description` on 19.0+ pages), `ticket.type`, `promo.action`, `ir.ui.view` arch terms on COW views. Term-level `update_field_translations`. Description children are unstable across publish; releases are stable. Keys are `tech_name` + `version` + field + source-text hash; releases also key by `module_version` + `exact_version`.

## Leak paths (must stay `en_US`)

- `modules_website` `_prepare_description` (resulted / static / promo index)
- `module.description.get_short_summary` when pushing a GitHub manifest (`with_context(lang="en_US")`)
- Any cron that prepares store HTML
- Support-owned `mail.template` (`lang=en_US`, empty `.po` terms). `check_mail_templates.py` enforces this.

`short_summary` itself is website-translatable (`translate=True`, TM dump). Only the store/GitHub callers stay pinned.

Regression: `modules_website` `test_en_us_store_leak` (includes the now-translated `short_summary`).

## Bind future work

- Editing a tools module that has `i18n/` → update `.po` (or regenerate from TM) in the same task.
- Editing a faotools.com page or 19.0 description → update TM YAML, then loader.
- Publishing a **19.0+** `module.release` → TM-first translate `description` (not `notes`) in the same task; `33-faotools-release` step 8. Older-serie rows shown on that 19.0 page are in scope too.
- `action_apply_prepublishment` re-applies translations in code; do not skip the hook.
- After `git pull` / serie switch of `odoo` / `enterprise`, run the glossary-vs-core drift check before adding new translations.
- Permanent gate: `support/support_translations/scripts/check_translation_coverage.py` (wired into `devops/run_tests.sh` on Odoo 19). `--live` crawls en vs each language.

## Out of scope until asked

KnowSystem article bodies and `/docs` content stay English. Screenshot **files** stay English; `module.pic.name` and `alt_name` are translated. Country variants and the extended set are shipped (same list as `ai_rules` `17-translations`); production URL prefixes are Phase 11 activation. Seed from the root locale and analyze each string separately (translations may differ — not a copy, not an SEO-only event).

## 20-local-docker

_faotools_env local Docker: env-up, env-serie, env-shell, ports, Mailpit_

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


## Serie + bind mounts

- Custom addons bind from `/home/feelwhy/Odoo/<repo>`; tools serie = git branch.
- `./local/env-serie.sh <serie>` before cross-serie work; `env-up` also ensures the target serie.
- **Same target again** (already running, or last launched in this chat): only
  `./local/env-up.sh <target> --restart`. No serie switch, prepare, sync, or
  other edits — see `ai_rules` `30-command-vocabulary`.
- See `faotools_env/local/README.md` for full port matrix and sync behavior.

## 21-faotools-mcp

_Live faOtools MCP usage for production truth on faotools.com_

# Live faOtools MCP

- The real live support database may be reachable through the enabled faOtools MCP server (`user-faotools`).
- Use it when a task needs production truth that cannot be reliably inferred from code, such as current `ir.ui.view` contents, live website metadata, config parameters, cron state, or app/module records.
- Prefer read-only MCP checks unless the user explicitly asks to update live data.
- Before calling any MCP tool, inspect that tool's descriptor/schema and use the documented parameters.
- Treat live data as production data: do not expose secrets, tokens, customer-private details, or raw sensitive payloads in chat.
- If code and live behavior disagree, consider whether the module has not been upgraded, a view was customized in the database, or cached/generated content is stale.
- App releases (`module.release`): follow `33-faotools-release`. Do not invent a parallel publish path.

## 30-prepublishment-descriptions

_Rewrite/adapt faOtools apps-store module descriptions before publishment_

# Prepublishment module descriptions (faOtools MCP)

Canonical extended rule (same logic): `/home/feelwhy/Odoo/Odoo19/support/.cursor/rules/module-description-mcp-adaptation.mdc`.
Screenshots: `prepublishment-screenshots.mdc`. Packaging metadata: `apps-store-packaging.mdc`.

All edits go through the `user-faotools` MCP. Inspect each tool schema before calling; writes use `odoo_records_write` then `odoo_operations_confirm`.

## Golden rule: edit the prepublishment, never the published description

- Work ONLY on `module.description` records with `prepublish = True`.
- The live record is referenced by `pre_publish_origin_id`. NEVER write to it.
- If no prepublishment exists, run `action_make_prepublish` on the origin.
- Child records (`module.feature`, `module.pic`, `module.extra.note`, `optional.app`, `module.conf`) must belong to the prepublishment (`description_id` -> prepublish record).

## What you may change vs must not

Editable (rephrase freely; keep facts truthful):
- `module.feature.name`, `subheader`, `body` for every feature.
- `module.description.summary` and `module.description.perfect_for`.
- `module.description.summary_key_words` — **extend only**; never remove existing keywords.

Hard do-not-touch:
- `module.description.short_summary` — leave exactly as-is.
- Prepublishments are **English-only**. Do not author translations on the draft; the `support_translations` loader re-applies them after publish.
- The **first** feature in `feature_ids` (overview block) has no title — never add `name`/`subheader`; only improve its `body`.
- Never invent capabilities.

## Goals

- Sell the outcome: which customer pain each capability removes.
- Modern, professional copy; AI/SEO-friendly keywords (extend, do not replace).
- Research first: module source in `tools/` (correct branch from `version` + `tech_name`), release notes, and docs before rewriting.

## Section structure and logical grouping

Order features so the page reads top-to-bottom like a product story:

1. **Overview (first feature, no title)** — 6-card key-benefits grid mapping the whole app at a glance. Use multiples of 3 for `col-lg-4` rows.
2. **Native / suite-owned capabilities** — group related features (composer, sending safety, message actions, metadata) into named sections with plain-text `name` + `subheader`.
3. **Bundled dependency apps (suite modules only)** — one dedicated section per dependency, titled with the **published product name** (e.g. "Lost Messages Routing", "Private Thread", "Odoo Email From"). Explain what the dependency delivers and how the suite extends or integrates it. Do **not** merge several dependencies into one section or dump a dependency list block.
4. **Administration / configuration** — unified settings, allowed models, presets, manager workflows.
5. **Bridge modules** (e.g. `email_suite_accounting`) — one focused section on the integration surface, not a repeat of the parent suite.

Standalone modules skip step 3. Optional extensions must match real rows in `optional_app_ids`.

## Styling: cloud_base / 1043 pattern

Style reference: `module.description` **1031** (`cloud_base`) and **1043** on faOtools.

- Bootstrap grid + FontAwesome only. No `<style>`, `<script>`, JS handlers, or custom CSS beyond approved inline card styles.
- Brand green `#017e84`, card border `#e7f0ee`, radius `16px`, padding `20px`, white background, shadow `0 6px 24px rgba(0,0,0,0.06)`.
- **Overview cards:** `row justify-content-center mx-0`, cols `col-lg-4 col-md-6 col-sm-12 mt8 mb16 d-flex`, inner `h-100 w-100` + green `<h4 style="color:#017e84;font-weight:700;">` with inline FA icon.
- **Detail sections:** `row mx-0`, cols `col-lg-6 col-md-6 col-sm-12 mt8 mb16 d-flex`, same card shell, bullet lists with `<ul class="list-unstyled" style="padding-left:0;list-style:none;">` and `<i class="fa fa-check-square-o" style="color:#017e84;"> </i>`.
- **Perfect For:** `row text-left mx-0`, `col-lg-4 col-md-6 col-sm-12 mt8 mb16 d-flex`, green `<h3 style="color:#017e84;font-weight:700;"><i class="fa ..."> </i> ...</h3>`.
- Feature `name` / `subheader`: plain text (or existing optional-extension icon markup). Do not wrap in green spans.
- Use `<b>` for visible bold in odoo.com content — not `<strong>` (store CSS ignores it).
- Top-level `.row` in authored HTML must include `mx-0` to prevent mobile horizontal scroll.
- Card grids: fill rows (multiples of column count) or add `justify-content-center`; equal height via `d-flex` + `h-100 w-100`; balance copy volume across sibling cards honestly.
- Valid XML: close every tag; escape `&`, `<`, `>`; no named entities like `&mdash;` (422 errors). Hyperlink long URLs with short anchor text; use `text-break` when the literal URL must show.

### Character set: ASCII-safe English source (apps.odoo.com)

apps.odoo.com reads shipped `index.html` as latin-1, so non-ASCII source glyphs corrupt
(e.g. `—` becomes `â`). faotools.com UTF-8 is fine. Keep English source ASCII-safe.

**Scope: English source only** in `module.description` / `module.feature` / `module.pic` /
`module.conf` / `module.extra.note` / `optional.app` fields that feed the odoo.com index.
**Translations are exempt** (assumed faotools.com-only UTF-8); do not transliterate them.

Allowed: printable ASCII `U+0020`-`U+007E`, newline/tab, XML entities
`&amp;` `&lt;` `&gt;` `&quot;` `&apos;`, and numeric refs `&#NNN;` when a glyph is
semantically required (e.g. `&#246;`). No named entities (`&mdash;`, `&nbsp;`, …).

Write this, not that: ` - ` not `—`/`–`; `'` not `’`; `"` not `“`/`”`; `...` not `…`;
`&gt;` (menus) / `-&gt;` (state flows) not `→`; `-` not `−`; `x` not `×`; `!=` not `≠`;
plain space not NBSP; delete zero-width spaces; no Cyrillic keyboard-typo lookalikes.

## Screenshots (summary)

- Body copy is primary; screenshots are secondary evidence.
- Default one inline screenshot per feature (`module.pic.features = True`); demote or detach (`feature_id = False`) weak shots — never delete pics or attachments.
- Reuse existing `module.pic` from dependency modules when describing bundled apps; capture new shots only for genuinely new UI (see `prepublishment-screenshots.mdc`).

## Source and verification

- Module source: this `tools/` repo; branch from prepublishment `version` (e.g. `19.0` -> `19_suite` / matching branch).
- After edits: run `action_prepare_description` or preview `/apppublish/<version>/<id>/`.
- Verify mobile width (no horizontal overflow ~360px), screenshot inline selection, caption markup, and that summary + sections match actual code behavior.

## 31-prepublishment-screenshots

_Screenshot conventions for faOtools module store pages_

Companion rule for copy/HTML structure: `prepublishment-descriptions.mdc`.

# Screenshot Source: Real UI, Never Generated Images

- Never use image-generation tools (e.g. `GenerateImage`) for app-store screenshots. They are not real UI and must not be uploaded as `module.pic`/`module.description` assets.
- Capture screenshots from an actual running local Odoo instance showing the real views of the module being described.

# Hard gate: demo environment BEFORE any capture

**Do not run Selenium or hand off PNGs until the demo environment passes the checks below.**

Order is mandatory:

1. **Install stack** — docker compose screenshot DB + all apps the shots need (`contacts`, `crm`, `sale_management`, `account`, target module(s), Lost Messages app when routing shots are planned).
2. **Enable every product toggle** — all suite + dependency settings ON (see *Demo data requirements*).
3. **Seed rich demo data** — run `support/devops/seed_screenshot_env.py` (extend it when the shot plan needs more records). Minimal/empty seed is **not** acceptable for suite modules.
4. **Verify assets & icons** — app switcher, systray, and field widgets must render real icons (see *Web assets & app icons*). **Block capture** if the home-menu shows the generic wireframe cube or repeated `default_icon_app.png` tiles.
5. **Walk the shot plan** — manually or via a dry-run checklist: every planned PNG must have its target view open, populated, and the feature control visible *before* automating capture.
6. **Only then capture** — Selenium/`capture_suite_screenshots.py`.

If demo seeding or asset warmup is incomplete, **stop and fix seed/scripts first** — never ship “placeholder” screenshots and iterate later.

# Capture Pipeline (local Odoo + headless Chrome)

1. Create a throwaway Postgres DB (`screenshot_<suite>_<version>`), separate from any `support_*`/`test_*` DB.
2. Install the target module(s) via the project's docker compose test image (`support/devops/docker-compose.screenshot.19.yml`), per the "Use docker compose always for tests" user rule — do not fall back to a bare host `odoo-bin` (host Python lacks Odoo's deps such as `passlib`).
   - The compose `odoo` service entrypoint is already `bash -lc`; pass the shell command directly as the `command`/run argument, do NOT wrap it in another `bash -lc '...'` or it hangs reading stdin.
3. Start Odoo from that same image/DB (`setup_screenshot_stack.sh up` or equivalent), picking a free host port (check with `ss -tlnp`).
4. Complete the **demo gate** above (enable toggles → seed → verify icons → walk shot plan).
5. Drive headless `google-chrome` via Selenium (`pip install selenium` in a local venv, e.g. `/tmp/screenshot-venv`) to log in and open each view/action, then `driver.save_screenshot(...)`.
6. Run **QA reject checks** on every PNG before handoff (see below).
7. Reference scripts: `support/devops/setup_screenshot_stack.sh`, `support/devops/seed_screenshot_env.py`, `support/devops/capture_suite_screenshots.py`, `support/devops/apply_screenshot_legends.py`.

# Demo data requirements (rich consultant demo, not smoke test)

The throwaway DB must look like a **prepared sales demo**, not a fresh install with one row per model.

## Global demo persona

- **Demo user:** `olivia.chen@example.com` / `demo` (**Olivia Chen**) — never `admin` in screenshots.
- Grant every group needed for the shot plan: Settings, CRM/Sales/Project/Contacts apps, Discuss drafts, Email From manager, Lost Messages, message edit/delete, internal thread, citing, routing.
- **Company:** “My Company” with logo if available; disable onboarding tours (`tour_enabled=False`).

## Minimum narrative (Messaging Suite baseline)

Seed a coherent story buyers recognize:

| Entity | Purpose |
|--------|---------|
| **Jane Customer** (`jane@example.com`) | Primary contact — address, phone, avatar, $ invoiced, 1 CRM opportunity |
| **CRM lead** “Website inquiry from Jane” | Composer/draft/routing targets on a second document type |
| **CC partner** | Visible copy recipient in composer shots |
| **Inbound email on Jane’s chatter** | Subject + plain-text body (no raw HTML tags visible); triggers action-menu shots |
| **2–3 composer drafts** | Discuss → My Drafts list + draft picker in composer |
| **4+ schedule presets** | Admin list + Send Later dialog |
| **2+ Email From addresses** | Support + Sales on Mailpit server |
| **1+ Email From rule** | e.g. sales orders → Sales address |
| **1–2 lost messages** | Lost Messages app queue with From/Subject/body/attachments |
| **1 posted customer invoice** | Accounting bridge wizard |
| **Edited message + history** | “(edited)” marker for message_edit shots |

Extend `seed_screenshot_env.py` when the approved shot plan needs more (cite wizard sources, forward thread, private messages, etc.). Document new seed steps in the script header.

## Per-shot data rules

- **List views:** at least **2–3 rows** with every visible column meaningfully filled (no empty Subject/Document/Recipients columns).
- **Forms:** open a **specific record** from the story above — never a blank “New” form unless the shot sells creation UX.
- **Modals/wizards:** the **trigger must be visible** — e.g. attachment reminder shows the **full composer behind** with body text mentioning “attached”; routing wizard shows the **lost message or chatter email** it applies to.
- **Chatter shots:** must show **suite-specific UI** (action menu, extra details, quote composer, private checkbox) — a generic contact form with only standard Send message/Log note is **not** a suite screenshot.
- **Settings shots:** every toggle ON that the product sells; sample text in regex/header fields; link buttons (Scheduled Send Options, Lost Messages) visible.

Re-run seed after changing seed logic; `-u <module>` when JS/XML assets changed.

# Web assets & app icons

Broken icons make listings look unfinished. Treat asset loading as part of demo readiness.

## Install & warmup

- Include **`contacts`** (and every app whose icon appears in the shot) in `SCREENSHOT_MODULES` / stack install list.
- After login, **warm up** before the first capture: open `/web`, `/odoo/contacts`, `/odoo/discuss` (or CRM/Sales as needed), wait for `.o_main_navbar`, run `document.fonts.ready`, open the **app switcher dropdown once** to force menu icon fetches.
- Chrome: do **not** pass `--disable-gpu`; use `--font-render-hinting=medium` (see `capture_suite_screenshots.py`).

## Verification (block capture if failed)

Before the capture loop, confirm:

- Home-menu button shows **`oi-apps`** (or app brand icon), not an empty/broken glyph.
- App switcher dropdown lists **Contacts, CRM, Discuss, …** with **module icons**, not the generic multicolour wireframe cube for every app.
- No screenshot shows `/web/static/img/default_icon_app.png` as the primary app tile when a real module icon exists.
- Systray icons (Discuss, Activities, user avatar) render.

Log network 404s on `web/static/lib/odoo_ui_icons/` or module icon assets and fix before capturing.

# What every screenshot must illustrate

Each `module.pic` sells **one capability** from the prepublishment’s `module.feature` rows. Before capture, write down:

- **Feature ID** (faOtools `module.feature`) this PNG supports
- **User action** visible in the frame (what did Olivia click to get here?)
- **Proof data** (which seeded record/text proves the feature is active?)

### Invalid shots (reject & re-seed/re-capture)

- Generic Odoo chrome with **no suite widget, action, or setting** in frame
- **Empty** list/form views or placeholder-only fields (“e.g. Sales Director” everywhere)
- Modal **orphaned** from its trigger (e.g. attachment warning with no composer/body context)
- **Wrong app icon** / wireframe cube in navbar when marketing a multi-app suite
- Dependency feature shown **without** suite context when the listing sells the bundle (prefer unified Messaging Suite settings + in-context chatter/composer)

### Framing

- **Width: 1130px, strict.** Crop/resize raw capture to exactly 1130px wide before upload.
- Keep **navbar + breadcrumbs** when they anchor the app/context; crop tight only when the dialog itself is self-explanatory **and** trigger context remains visible (stacked modals, composer behind confirm).
- Prefer **one hero control** per shot; avoid clutter, debug tooltips, and unrelated admin menus.

# Coverage requirements (suite / bundle modules)

For **bundle products** (e.g. `email_suite`), screenshot coverage must match **every named feature section** on the prepublishment, not a handful of easy composer panels.

Workflow:

1. Read prepublishment `module.description.feature_ids` via faOtools MCP (`name`, `subheader`, `sequence`).
2. Read existing `module.pic` rows and sibling published versions (same or better coverage).
3. Build a **shot plan table** (feature → PNG → alt_name → seed prerequisites) and get alignment before capture.
4. **Minimum:** at least **one strong screenshot per feature section**, plus native suite-only surfaces not covered by dependency duplicates.
5. **Dependency reuse:** duplicate published dependency PNGs only when quality is good **and** `alt_name`/feature mapping still fits; otherwise **re-capture** in the suite demo DB with proper icons and data.
6. Link each new `module.pic` to a `feature_id` when the feature section exists.

Standalone modules (`odoo_email_from`, `email_suite_accounting`): cover each major settings/list/wizard surface described in their own prepublishments.

# Chrome, menus and demo user

- Log in as **Olivia Chen** (`olivia.chen@example.com` / `demo`).
- Keep Odoo chrome visible unless the shot is intentionally detail-only **and** context is still obvious from `alt_name`.
- Disable tours for the demo user.

# Legends (caption overlay)

**Capture clean UI PNGs by default** — never burn legends inside the Selenium capture loop.

Apply legends when the screenshot sells a **non-obvious control** (CC/BCC tags, Route action, Send private checkbox). Skip when the titled dialog or settings block is self-explanatory.

When legends are used, follow copy/style/pipeline rules in the sections below (unchanged intent):

## Copy style

- Outcome / action captions (*what happens*), not field labels or help-tooltips.
- Center-align text in the bubble body; color `#017e84`, Ubuntu Italic 24px.
- Match `module.pic.alt_name` intent when uploading.

## Visual assets (`support/module_descriptor/static/AppsScreenshots/`)

- Bubbles: `Legends/{corner}-{long|short}.png`; point at the **value** (tag/chip/button), not the whole row.
- No highlight borders; no extra connector lines.

## Pipeline

1. Capture clean PNG (1130px) + `.boxes.json` sidecar where legends may apply.
2. Run `apply_screenshot_legends.py` only when the legend meets all copy/anchor rules.
3. Upload legended PNG when it genuinely helps; otherwise upload the clean capture.

# Reusing dependency screenshots

For dependency modules sold separately (`mail_manual_routing`, `internal_thread`, `message_citing`, `message_edit`, `odoo_email_from`):

- Read their published `module.pic` rows via faOtools MCP.
- **Duplicate** PNG bytes into new attachments on the suite prepublishment — never reparent existing dependency attachments.
- Reuse `alt_name` intent when the same angle is still accurate.
- **Re-capture** when dependency duplicates are low quality (broken icons, empty data, wrong framing) even if bytes exist on an older listing.

# Version coverage (same or better than sibling releases)

Compare adjacent published descriptions (e.g. 18.0 vs 19.0): match or exceed screenshot count, feature angles, and caption intent. Do not drop a published angle without reason.

# QA checklist (every PNG before handoff)

Reject and fix if any check fails:

| Check | Pass criteria |
|-------|----------------|
| Icons | Real app/module icons in navbar/app menu; no wireframe cube grid |
| Data | Seeded story visible; list ≥2 rows; no empty “hero” fields |
| Feature | Suite-specific control/action/setting clearly visible |
| Context | Modals/wizards show what triggered them |
| User | Olivia Chen (not Administrator) |
| Size | Exactly 1130px wide final PNG |
| Caption | `alt_name` matches what a buyer actually sees |

# Handoff for manual faOtools upload (default)

After capture, crop/legend, and **QA pass**, move only final PNGs to:

```
~/Downloads/prepublishment-screenshots/
  <module_technical_name>/
    *.png
  upload_manifest.json   # description_id, sequence, feature_id, alt_name
```

Agent steps: capture → QA → manifest → move finals → tell user the Downloads path. Manual faOtools upload is the default; MCP upload only when explicitly requested and bearer/PUT works.

# Upload via MCP (optional)

When the user explicitly asks for automated upload **and** MCP bearer/PUT is available, upload QA-passed PNGs via faOtools MCP (`odoo_attachments_upload_prepare` → PUT → `odoo_attachments_upload_commit`), then create `module.pic` with `description_id`, `attachment_id`, `alt_name`, `sequence`, `feature_id`.

## 32-video-cover-design

_Design faOtools YouTube video covers in house style_

# faOtools video cover (YouTube thumbnail) design

Reusable recipe for producing video covers in the faOtools house style, derived from
the shipped covers for the **KPI Scorecard** and **Password Manager** demo videos.
Every faOtools module demo cover shares the same skeleton; only the module-specific
content (header keyword, dashboard mockup, themed props, legend) changes.

**Canonical storage** (version-controlled, in the repo):

`support/module_descriptor/static/Covers/`

Save every finished cover here. Use descriptive snake_case names, e.g.
`<module_or_topic>_video_cover.png`. When a cover maps to a known YouTube video,
optionally note the video ID in the rule's quick-reference section (not in the
filename unless the user asks).

Existing reference covers in that folder:

- `kpi_targets_video_cover.png` — KPI Scorecard (`2daDCn1_axI`)
- `password_vault_video_cover.png` — Password Manager (`V-DWe7LzhW0`)
- `cloud_storage_video_cover.png` — Cloud Storage Solutions (`LX3IWv0L6-U`)
- `lost_messages_video_cover.png` — Lost Messages Routing (`K451Col9iEs`)
- `joint_calendar_video_cover.png` — Joint Calendar (`lUy5unL2t6A`)

Cursor chat may also stash working copies under
`~/.cursor/projects/home-feelwhy-Odoo-Odoo17-support/assets/` during generation;
**always copy the post-processed final PNG into `module_descriptor/static/Covers/`**
before considering the task done.

## When to use

- User shares one or more YouTube links and asks for a cover/thumbnail.
- User asks for "another cover / variant" for an existing faOtools video.
- User asks to restyle an arbitrary image into the faOtools cover style.

## Step 0 - Gather the source truth

1. If a YouTube link is given, fetch the page and read the transcript/description to
   learn: the **module name**, its **one-line value proposition**, the **main UI**
   (dashboard, list, cards, side panel) and **themed objects** (keys, shields, targets,
   charts, locks, etc.). The transcript intro paragraph is usually the best summary.
2. Map the link to the module. Known so far:
   - `2daDCn1_axI` -> KPI Scorecard
   - `V-DWe7LzhW0` -> Password Manager
   - `LX3IWv0L6-U` -> Cloud Storage Solutions
   - `K451Col9iEs` -> Lost Messages Routing
   - `lUy5unL2t6A` -> Joint Calendar
3. Derive three text pieces (keep them short, benefit-driven, Title/UPPER case):
   - **Header**: `ODOO` + 1-2 keyword lines (the product or its core promise).
   - **Legend / tagline**: one sentence, 3 short lines, starts with "The tool to ..."
     and ends with "... in Odoo" (this is the faOtools voice).
   - **Mockup content**: 4-8 realistic labels/values for the dashboard cards.

## Canvas & export specs

- Aspect ratio 16:9, landscape. **Final export size: 2752 x 1536 px** (the size the
  user standardizes on). Intermediate generation can be 1536x1024 / 1024x571, then
  resized last.
- Single flat PNG, no transparency needed in the final.

## Layout zones (always the same)

- **Top-left - Title block**: a semi-transparent dark rounded rectangle bleeding off
  the left edge, holding 2 lines of big bold condensed uppercase text. Line 1 begins
  with white `ODOO`; the product keyword(s) are in teal `#017e84`. Wraps to a second
  line when long (e.g. `ODOO` / `PASSWORD` (white) ... `MANAGER`).
- **Top-right - faOtools logo**: do NOT let the image model draw the wordmark (it
  garbles the letterforms). Instead leave the top-right corner clean during generation
  and **composite the real logo** afterward. Canonical transparent asset:
  `module_descriptor/static/Covers/logo_faotools_apps.png` (gray `faOtools` with the
  magenta ring `O`, plus right-aligned `apps` beneath). Paste it at ~0.22 x cover width,
  ~70 px right / ~55 px top margins. The source brand wordmark is gray `~#96968e` with a
  magenta `O` ring `~#9b3c82`; rebuild the asset from it if needed (black background
  becomes transparent via per-pixel alpha = brightness).
- **Center - 3D isometric app mockup** (the hero, see below).
- **Bottom-right - Legend**: 3 lines of white, medium-weight, mixed-case sentence.
- **NEVER** include an AI/Gemini sparkle (4-point diamond). If a source has one in a
  corner, remove it (see post-processing).

## Color palette (exact)

- Title keyword teal: `#017e84` is the base brand teal. For the **header keyword** use a
  slightly brighter teal, normalized to `~#10b0be` / `(16,176,190)` so both covers match
  exactly (the image model drifts between covers; fix it in post-processing).
- Background: a diagonal gradient, **magenta-purple at top-left -> dark blue-violet at
  top-right -> dark teal-green at bottom-right**, deep purple at bottom-left:
  - top-left  ~ `#5a2559` / `#633363`
  - top-right ~ `#27294e`
  - bottom-left ~ `#341747`
  - bottom-right ~ `#166c6d`
- Accent cyan for circuit lines / glows: ~ `#2bd4d4`.
- faOtools `O` accent: magenta/pink ~ `#d63384`.
- Legend & `ODOO` text: white `#ffffff`.

## Typography

- Header: heavy bold, condensed, uppercase sans-serif (Montserrat ExtraBold / Gotham
  Bold feel). Tight leading, two lines max.
- Legend: clean medium-weight sans, mixed case, comfortable leading.

## The 3D isometric mockup (hero)

- A tablet/screen floating in perspective, tilted to face from the lower-left, with a
  soft glowing edge and drop shadow, sitting just right of center.
- It shows a believable Odoo app screen for the module:
  - left vertical **sidebar** with a logo and a few **colored category chips**
    (purple / teal / green / orange gradients),
  - central **grid of cards** (each: icon, title, a couple of values/stars/progress),
  - a right-hand **detail panel** ("Selected ... info" with fields/labels).
- Use module-appropriate icons and the brand teal for highlights.

## Decorative elements (subtle, dark, low-contrast)

- Thin cyan circuit/connector lines and small nodes around the edges.
- A few floating **3D shields with a teal checkmark** (trust/security motif).
- A handful of **themed 3D props** scattered around the mockup that signal the topic
  (e.g. keys/locks for Password Manager; targets, charts, gauges for KPI Scorecard).
- Faint dotted connectors and tiny geometric accents. Keep all of this dim so the
  title, mockup, and legend stay dominant.

## Generation workflow

1. Prefer `GenerateImage` with the closest existing cover from
   `module_descriptor/static/Covers/` passed as a `reference_image_paths` entry,
   instructing it to keep the style/layout and swap only the header, mockup content,
   themed props, and legend.
2. Post-process (see below), then save the final PNG to
   `module_descriptor/static/Covers/<module_or_topic>_video_cover.png`.

## Post-processing (deterministic, do with Pillow)

These pixel steps make results exact and on-brand. Always verify by cropping/zooming.

1. **Remove any Gemini sparkle** (4-point diamond), usually bottom-right near the
   legend. It can overlap a letter; mask it out and keep the letter's bright pixels,
   filling the rest with the local background color. Zoom in to confirm no remnant.
2. **Normalize/brighten the header keyword teal**: detect teal pixels in the title band
   only (top-left, roughly `y < 0.24*H` and `x < 0.50*W`, where `g > r+25 and b > r+15
   and g > 100`) and remap to the bright header teal, preserving shading:
   `t = min(1, g/178)`, `out = (16*t, 176*t, 190*t)`, blended by how teal each pixel is
   so anti-aliased edges stay smooth. Restricting to the band avoids recoloring the
   tablet's teal UI.
3. **Composite the real logo** top-right (see logo bullet above). Do this on the
   2752x1536 canvas so the downscaled logo stays crisp.
4. **Resize to 2752 x 1536** with Lanczos (do the resize before the logo paste).

## Content guidelines for headers & legends

- Header keyword should be the product or its strongest benefit, not a feature dump.
- Legend formula: `The tool to <verb phrase> <object> in Odoo`. Keep ~8-12 words.
- When asked for an alternative cover for the same video, keep the exact style but
  change the header keyword, the legend wording, and the mockup labels so it reads as a
  distinct design (not a duplicate).

## Quick reference - per-video content used

- **KPI Scorecard** (`2daDCn1_axI`): periods, KPI targets, measurements/variables,
  constants, formulas, scorecard with actual-vs-target colors, categories. Props:
  target/bullseye, charts, gauges, trophy.
  - Cover `kpi_targets_video_cover.png`: header **ODOO KPI TARGETS**; legend
    *"The tool to set targets, measure results, and reach your goals in Odoo"*.
- **Password Manager** (`V-DWe7LzhW0`): bundles/vaults, password cards with strength
  stars, access rights, encryption, portal sharing, duplicate detection. Props: keys,
  padlocks, shields.
  - Cover `password_vault_video_cover.png`: header **ODOO PASSWORD VAULT**; legend
    *"The tool to encrypt, share, and control team passwords in Odoo"*.
- **Cloud Storage Solutions** (`LX3IWv0L6-U`): organize attachments, folder-tree single
  view, auto folder rules, sync Odoo with Google Drive / OneDrive / SharePoint /
  Nextcloud / ownCloud / Dropbox. Mockup: white file-manager UI (folder tree sidebar +
  "Cloud Clients" connected list, file/folder cards with type icons and "Synced" badges,
  right "File Preview" panel). Props: 3D cloud, folders, sync arrows, provider badges,
  shields. Note: keep the tablet UI BRIGHT/WHITE and the background magenta-purple ->
  teal (the model tends to drift to a dark UI / navy bg for storage themes — correct it).
  - Cover `cloud_storage_video_cover.png`: header **ODOO CLOUD STORAGE**; legend
    *"The tool to organize, sync, and manage document files in Odoo"*.
- **Lost Messages Routing** (`K451Col9iEs`): detects emails that could not be
  auto-attached ("lost"), routes/attaches them to the right document thread (single or
  batch), allowed-models config, notifications, "Lost Messages Manager" group. Mockup:
  white inbox/list UI (Lost Messages + Configuration sidebar, message rows with
  checkbox/date/subject/author and red "lost" badges, "Route Manual" action, right
  "Route Message" panel with Model + Object selectors and a teal "Attach message"
  button). Props: envelopes (one with a red alert badge), routing-arrow signpost,
  magnifier, shields.
  - Cover `lost_messages_video_cover.png`: header **ODOO LOST MESSAGES**; legend
    *"The tool to catch and route lost email messages in Odoo"*.
- **Joint Calendar** (`lUy5unL2t6A`): merges different Odoo document events
  (opportunities, meetings, activities, sale/purchase orders, tasks, time offs, MOs)
  into one or several configurable "super calendars" via rules; color-coded by model,
  month/week/day/year views, access rights, optional Gantt add-on. Mockup: white Odoo
  Events month-view UI (calendars sidebar + Configuration: Calendars/Rules, color-coded
  event chips across a month grid, right mini-calendar + per-model color legend +
  attendees filter). Props: 3D calendar with check, alarm clock/bell, colorful event
  map-pins, stacked calendar sheets, shields.
  - Cover `joint_calendar_video_cover.png`: header **ODOO JOINT CALENDAR**; legend
    *"The tool to merge all document events into shared calendars in Odoo"*.

## 33-faotools-release

_Prepare and publish a faOtools app release on faotools.com (module.release)_

# faOtools app release

Command: “prepare a release”, “make a release”, “publish a release”.
Live writes go through MCP `user-faotools` (faotools.com). Inspect each tool schema first.
Mutations: `odoo_records_write` / `odoo_records_create` / `odoo_actions_run`, then `odoo_operations_confirm`.

**Scope: `tools` and `odoo-apps-addons` only.** Resolve `tech_name` in those repos. Refuse `support`, `life`, `system`, `faotools_env`. Do not bump local `__manifest__.py` (`11-manifest-version`); Quick GitHub Update writes GitHub.

The user’s “make a release” is the live-write gate. Ask only when the module/serie is ambiguous, the next `exact_version` already has a `module.release`, or the target is a prepublishment.

## Resolve targets

1. Module (`tech_name`) + Odoo serie(s) (`module.description.version`, e.g. `19.0`). Several series → one release each.
2. Search published descriptions only:

```
[("tech_name", "=", "<tech_name>"), ("version", "=", "<serie>"), ("prepublish", "=", False)]
```

Never write the prepublishment (`prepublish=True`).
3. Read that `module.description` (`exact_version`, `name`, `release_ids`) and the last few `module.release` rows for the same app (icons, note headings, tone).

`module.description.exact_version` is the tail without the serie (`1.3.53`). Display name is `{version}.{exact_version}` (`19.0.1.3.53`). Bump **only the last number**: `19.0.1.3.53` → `19.0.1.3.54` (`exact_version` `1.3.54`).

## Public `description` (changelog)

Short, factual, no hype (“significantly”, “seamlessly”, “powerful”). Customer-safe: no exploit steps. Match existing HTML:

```html
<ul style="list-style-type: none;">
    <li class="mt8"><i class="fa fa-refresh text-info mr8"></i> The issue of X has been fixed.</li>
    <li class="mt8"><i class="fa fa-plus text-success mr8"></i> The feature to Y has been added.</li>
</ul>
```

- `fa fa-refresh text-info` — bug or fix
- `fa fa-plus text-success` — new feature or optimization

One `<li>` per change. Read recent `module.release` rows if unsure.

## Internal `notes` (mandatory)

**Every new release must have Before / After notes.** A one-line summary is not enough. Include what broke or how it worked, what it does now, and every critical detail (security/ACL, API, upgrade/install, tests, serie-specific differences, commit SHA / PR). Read the code and the live `module.description` / last releases before writing — do not invent.

```
Before release
-----------------------
<actual previous behavior, including the hole or limitation>

After release
--------------------
<what changed, checks added, tests, SHA / PR>
```

Public `description` stays short; put the important detail here. Do not put tokens or customer-private data in notes.

## Sequence (each `module.description`)

1. Write `exact_version` to the bumped tail. Stop if a `module.release` already exists for that `module_id` + `exact_version`.
2. Create `module.release`: `module_id`, `exact_version` (new tail), `release_date` today, `description`, `notes`. Skip `1_to_check` / `2_checked` (those spawn check activities).
3. Publish: write `state=3_published`.
4. Get GitHub Commits: `odoo_actions_run` on **`module.description`** (`ids` = that description), `method_name=action_get_commits` (UI label “Get GitHub Commits”; the release action maps to `module_id.action_get_commits()`).
5. Auto-link commits: search `github.commit` for that `module_id`, `ingore_commit=False`, preferably `in_release=False`. Pick rows that belong to this change (message, SHA, date after the previous release). Write `commit_ids` on the new `module.release`. If none match, say so — do not attach unrelated history.
6. Quick GitHub Update: `odoo_actions_run` on **`module.description`**, `method_name=action_update_in_github_quick`.
7. `odoo_record_url` for every new `module.release` and paste the links in the reply.
8. **TM-first translate** the public changelog when the description serie is **19.0+** (see below). The release is not done while `/ru/` (and the other seven languages) still show English notes.

Report per release: module, serie, old → new version, state, commit count, URL, and whether changelog translations landed.

## Public changelog translations (19.0+)

Pull `ai_rules` `17-translations`. Public `module.release.description` only (`xml_translate`). **`notes` and `description_html` stay English.**

After the English row is `3_published`:

1. Update TM first: `support/support_translations/tm/website/<tech_name>_<serie>.yaml` → `releases` entry keyed by `module_version` + `exact_version`.
2. Translate every new English sentence to `ru_RU`, `fr_FR`, `de_DE`, `es_ES`, `pt_PT`, `nl_NL`, `it_IT`, `ar_001` (glossary / do-not-translate). Reuse `scripts/fill_release_tm.py` PACKS when the sentence already exists.
3. Apply the loader (`support.translations._apply_description` or `_reapply_for_description`). Never `odoo_records_write` / MCP translations without the YAML.
4. If this 19.0 page also lists older-serie rows (`migration_release_ids`), those public descriptions must be in the same TM list and applied. Do not leave them English.
5. Prove it: `ru_RU` `description` ≠ `en_US` on the new row, and `/<lang>/apps/...` shows the translated sentence.

Skip this block when the target `module.description.version` is 18.0 or older (no new TM for an 18.0-only publish). Store HTML (`resulted_description`) stays `en_US`.
