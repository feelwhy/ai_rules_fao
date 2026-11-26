# ai_rules_fao

Generated from `src/*.md` by `tools/sync_rules.py`. Do not edit by hand.

## 00-repo-map

_Flat hub repo map, serie resolution, and who owns which rules_

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
| `odoo-apps-addons` | Independent apps-addons. Read-only: its developer changes it (`02-repo-boundaries`) |

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
- **odoo-apps-addons**: read-only for us (`02-repo-boundaries`).

## Who owns rules

- Universal coding / process → `ai_rules`
- Hub map, boundaries, packaging, local Docker, MCP, prepublishment, app releases → `ai_rules_fao`
- Stays in-repo: support SEO/MCP description/index/support-database/v19-migration/translations; tools email-suite / jstree; faotools_env deploy rules; febado committed `.mdc`
- Translations: bans in `17-translation-gates`, glossary and TM in the skill `17-translations`, live apply in article 2139 via that skill. Icon HTML is `ai_rules` `18-xml-translate-html`.
- Demo data: skill `34-demo-data`. KnowSystem demo articles: skill `35-knowsystem-demo`.
- faotools.com FAQ (add or edit an FAQ article): article 2141, then the YAML part in `support` `.cursor/rules/knowsystem-faq.mdc`.
- A major port of the `tools` apps is not done when the last module group is green. The rest is the skill `36-major-version-port`.
- App releases: bans in `33-release-gates`, sequence in KnowSystem article 2137 via the skill `33-faotools-release`.
- Prepublishment: article 2138 via the skill `30-prepublishment-descriptions`.
- App documentation on `/docs`: article 2142 via the skill `38-module-docs`, which also holds the module-to-section table. App videos: article 2143 via the skill `39-module-videos`.
- LinkedIn company-page posts: skill `37-linkedin-publications`. The owner publishes.

## 01-hub-serie

_Change the Odoo serie or pull hub repos (change version, switch branch, pull changes). Prints worktrees and does not check out the shared hub_

# Hub serie discipline

The bans are always-on in `00-repo-map`. This skill is the command.

Each branch has its own working tree. The shared checkout is used when it is already on that branch. Otherwise it is the worktree that has the branch checked out, usually `/home/feelwhy/Odoo/_worktrees/<repo>-<branch>`. A detached worktree does not count. Launching Odoo mounts that tree and does **not** check out the shared hub.

## Rules

1. Before a `git checkout` the user explicitly asked for: `git status -sb` on the affected repos; respect `ai_rules` never-discard-WIP. `env-up` and `env-serie.sh` do not check out anything.
2. Do **not** assume the shared `tools` or `enterprise` checkout is on 19.0. Read the branch. The 19.0 tree may be a worktree.
3. A required repo with no tree on the serie branch is an error. Name the repo and the branch and stop. Do not fall back to another serie, and do not mount the copy baked into the image. The error prints the command that adds the tree. Run it only with the user's OK:
   `git -C /home/feelwhy/Odoo/<repo> worktree add /home/feelwhy/Odoo/_worktrees/<repo>-<branch> <branch>`
   (undo: `git -C /home/feelwhy/Odoo/<repo> worktree remove /home/feelwhy/Odoo/_worktrees/<repo>-<branch>`).
4. `support`, `ai_rules`, `ai_rules_fao` and `faotools_env` ship in a **single version**. Do not put them on 17.0/18.0.
5. Editing happens in the tree Docker will mount. A container that is already running keeps the code it started with until `env-up` recreates it.
6. Do not create parallel `tools-ports/` or `OdooNN/` checkouts. Do not add another worktree for a branch that already has one.
7. These absences are intentional: `odoo-apps-addons` has no `16.0` (demo16 and demo16e do not mount it); `others` has no `20.0` (demo20 and demo20e do not mount it).
8. `19_demo` and `20_demo` are separate branches for demo data. Their trees are `_worktrees/tools-<N>_demo` and `_worktrees/system-<N>_demo`. The `env-demo-*` scripts mount them, and read and write demo files there, never in the shared checkout. They re-render the target, so it serves the `_demo` code until the next `env-up`. A missing tree stops them (rule 3). They do not check out the shared hub.

## Command: “change version / switch branch to \<serie\>”

“change version to 16.0”, “change branch to 16.0”, “switch branch to 18.0”, “switch to 19”,
“let’s work on 17.0” are all the **same command**. A bare major number means `\<major\>.0`.

Run `faotools_env/local/env-serie.sh <serie>`. It prints the tree for each repo that serie mounts. It does not move the shared checkout. If it exits 1, a required tree is missing: report the name and stop.

Work in those trees. Do not `git checkout` the shared hub onto that serie.

- **If the user names repos** (“change tools to 16.0”), report and use only those trees.
- Single-version repos (rule 4) are never moved unless the user explicitly asks.
- Do not pull during this command. Nightly `env-git-daily` (05:00) fast-forwards clean serie trees. Say if `env-serie.sh` reports a tree behind its last fetch.

## Command: “pull changes”

“pull changes”, “pull”, “update the repos” means: fast-forward each repo’s **current branch** from
its upstream.

- **No repo named → every hub checkout**, including the single-version ones (`support`, `ai_rules`,
 `ai_rules_fao`, `faotools_env`) and `odoo` / `enterprise`. Pulling only updates a
 read-only reference; it does not make it editable.
- **Repo named** (“pull tools”) → only that repo’s current checkout. **Branch named** (“pull 18.0”, “pull tools 18.0”)
 → fast-forward the tree that is already on that branch (the shared checkout, or `_worktrees/<repo>-<branch>`). Do not check out the shared hub. If that tree does not exist, stop and say so.

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

## Where to edit

Edit the tree `env-serie.sh` prints for that serie. The shared `/home/feelwhy/Odoo/tools` folder is only the serie it is checked out on. A 19.0 fix made in the 18.0 checkout does not reach a 19.0 container.

## 02-repo-boundaries

_Which hub repos are editable vs read-only reference_

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

## 03-repo-priority

_Which hub repos to read and search first for each task context_

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

## 10-apps-store-packaging

_Apps-store packaging, metadata, and installability expectations for tools modules_

# Apps Store Metadata
- Keep manifests valid Python dictionaries accepted by Odoo 19.
- Preserve `name`, `summary`, `description`, `author`, `website`, `license`, `price`, `currency`, `images`, and `live_test_url` unless explicitly changing listing metadata.
- Version format is `<serie>.x.y.z`; never change `version` unless the user explicitly requests a bump (see `11-manifest-version`). During a 19 → 20 port the saas stand-in takes an **unprefixed** version (`1.3.33`) because `check_version` compares to `saas~19.4` — see `ai_rules` `22-migrate-v19-to-v20` **Manifest version**.

# Module Independence
- A top-level add-on must install with only its manifest dependencies and standard Odoo/Enterprise modules.
- Shared product-family behavior belongs in an explicit base module dependency, not in implicit imports or undeclared XML references.
- Do not make a module depend on a sibling app only to reuse a tiny helper; duplicate small app-local glue when that preserves product independence.

# Static Description
- Keep `static/description/index.html` and manifest `images` in sync.
- Do not remove screenshots, icons, or marketing HTML during code-only tasks.
- Generated/minified listing assets are packaging artifacts; edit source files when available.
- For faOtools prepublishment copy (MCP `module.description` / features / perfect-for), follow the skill `30-prepublishment-descriptions`.

# Licensing
- Preserve proprietary licensing text and `LICENSE` files.
- Do not introduce third-party code or vendored libraries without confirming license compatibility.

## 11-manifest-version

_Never change tools module manifest version unless the user explicitly requests it_

# Manifest Version

- **Never** modify the `version` field in any `__manifest__.py` under `tools/` unless the user explicitly asks. Editing dependencies, assets, data, or metadata is not that ask.
- **Port exception (19 → 20 only):** during the saas-19.4 stand-in (`Gx.3`), drop the
  serie prefix (`19.0.1.3.33` → `1.3.33`) so `check_version` does not set
  `installable=False` on `saas~19.4`. At `Fx` / phase 8, on real 20.0, write
  `20.0.` + that same tail. Do not invent a fourth number. See `ai_rules`
  `22-migrate-v19-to-v20` **Manifest version**.
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
- This is the reference implementation for the pattern: `knowsystem` `action_check_option` in `knowsystem/models/knowsystem_article.py`.
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

## 17-translation-gates

_A translation is not done until it is on the live page_

# Translation gates

A translation file in git is not a translation on the site. The glossary, paths, YAML keys, pic steps, and scripts are the skill `17-translations`. Read it when the task changes copy, `.po`, or `module.description`.

- Done means the live page or the live field no longer shows the English sentence. A loader return code and a report of “MISSING: 0” are not that proof.
- Screenshot titles need their own `pics` entries in the apply payload. Translating the guideline body leaves `/ru/` captions English (Google Drive, 2026-09-01, `Open the Google Auth Platform`). `module.pic.name` and `alt_name` are translated. The PNG stays English. Prove that both live fields equal the TM translation in each shipped language. "Differs from `en_US`" is not that proof: an old title's translation survives a rename.
- Changing English in a template leaves the new term empty on an existing database (Appointments `Any` / `Select`, 2026-09-09). The empty-term fill is part of the same change.
- YAML written in this checkout is not applied by the prepublication hook. That hook reads the copy already on the Functional container. The live apply is still required.
- Store HTML, GitHub manifests, and support mail templates stay `en_US`. KnowSystem article records and `/docs` stay English.
- A 19.0+ release changelog follows `33-release-gates`. Filling the app `.po` is not that translation (Appointments `1.3.33`, 2026-09-10).

## 17-translations

_faOtools glossary and how to apply translations (TM, .po, loader, pic titles). Read when changing copy, i18n, module.description, or screenshot titles_

# faOtools translations

The live-site bans are always-on in `17-translation-gates`. This skill is the glossary, TM YAML, `.po`, and checks. The live apply on faotools.com is KnowSystem article 2139 (**Live apply** below). A gate that fails means the translation is not done.

Pull this skill for any task that adds or changes user-facing strings, `.po` / `.pot` files, website/QWeb copy, `module.description` content, `module.release.description` (public changelog), or languages.

Source of truth is **`support/support_translations/`** (glossary, do-not-translate list, fingerprinted TM). Odoo `.po` files and the DB loader are outputs, not the place to invent wording.

## Where files live

| Surface | Repo / path |
|---------|-------------|
| Glossary, do-not-translate, TM, loader, validators | `support/support_translations/` |
| App UI `.pot` / `.po` | `tools/<module>/i18n/`; `odoo-apps-addons/ai_mcp_server/i18n/` is read-only (a gap goes to its developer, `02-repo-boundaries`) |
| Website QWeb code templates | `support/*/i18n/` plus loader YAML for website-builder (COW) views |
| Cursor rules | this skill, `support/.cursor/rules/translations.mdc` |

Do not add a parallel glossary in `tools/`.

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
- Editing a faotools.com page or 19.0 description → update TM YAML, then loader. That includes every **new or renamed** `module.pic.name` / `alt_name` (see **Screenshot titles** below). Guideline body alone is not enough.
- Publishing a **19.0+** `module.release` follows `33-release-gates` and the skill `33-faotools-release`. This skill does not repeat that sequence. Internal `notes` and `description_html` stay English. A publish of 18.0-only is not a translation target.
- `action_apply_prepublishment` re-applies translations in code; do not skip the hook. That hook reads YAML **already on the Functional container**, not this checkout — new local TM still needs the live apply (**Live apply** below).
- After `git pull` / serie switch of `odoo` / `enterprise`, run the glossary-vs-core drift check before adding new translations.
- Permanent gate: `support/support_translations/scripts/check_translation_coverage.py` (wired into `devops/run_tests.sh` on Odoo 19). `--live` crawls en vs each language. `check_view_term_restyle.py` fails a QWeb restyle that left only the old tagged `.pot` msgid.
- Existing DBs do not pick up a new view msgid on `-u` (`overwrite=False`). `_fill_empty_view_translations` in `support_translations`, `odootools_demo`, and every tools module that owns QWeb `<template>` views writes the `.po` onto empty `arch_db` terms. Do not skip that fill after a template restyle.
- HTML in `xml_translate` fields (`module.feature.body`, `module.release.description`, …) must follow always-on `ai_rules` `18-xml-translate-html`. Never empty `<i></i>` / `<i/>`.

## Live apply

Applying TM to the faotools.com database is KnowSystem article 2139 in section `AI` on faotools.com. The title is for people. Read the article before any live apply. Git history of this file is not the procedure. This id lookup belongs only to this pointer.

https://faotools.com/odoo/knowsystem/2139

1. MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). Inspect the tool schema first (`21-faotools-mcp`).
2. Read `knowsystem.article` 2139.
3. Stop unless that record is active and its section is `AI` (id 157).
4. Read `description` and follow it.

If the host MCP tool returns needs auth or Unauthorized, do not stop and do not ask the owner to log in. Connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Stop only when that path also fails to make a working call, or the read does not return one active record in section `AI`. Do not reconstruct the steps. MCP only reads the article; it cannot run the apply. The bans in `17-translation-gates` and `18-xml-translate-html` still apply.

## Screenshot titles (`module.pic`) — hard gate

Incident 2026-09-01: Google Drive guideline **body** was translated; `/ru/` captions stayed English (`Open the Google Auth Platform`).

PNG files stay English. **`module.pic.name` and `alt_name` are translated.** Replacing or renaming shots is a source-string change, same job as the body.

1. Rewrite TM `confs[].pics` / `features[].pics` / top-level `pics` to the **new** English `name` and `alt_name` (new fingerprint). Do not leave the old titles under the old `sequence`.
2. Translate both fields for every shipped language.
3. The live apply payload **must include `pics`**. Omitting them leaves titles English. Do not apply the previous pic YAML onto the new shots.
4. Loader `_match_child` matches English source/fingerprint first, then sequence. Old source + new title = no match. Sequence fallback can hit the wrong pic; `_apply_field_payload` then skips `plain` fields on a stale fingerprint (`return 0`) — silent English leftover.
5. Body/guideline translated is **not** done. Prove that live `module.pic.name` **and** `alt_name` equal the TM translation in each shipped language. Feature blocks show `alt_name`. "Differs from English" passes on an old title's translation.

## Closing a hub-wide empty-msgstr backlog

Run the checklist in **Closing an "empty msgstr" backlog** below. These are the hub paths for that checklist.

- Full language list lives in `support/support_translations/const.py`
 (`SHIPPED_LANGS`, `PO_STEM_TO_LANG`) — read it, do not re-type the list by hand.
- Core `.po` sources to reuse verbatim strings from: `odoo/odoo/addons/base/i18n/` (base models —
 note the extra nested `odoo/` segment only `base` has), and the flatter
 `odoo/addons/<module>/i18n/` for everything else (`project`, `product`, `mail`, `stock`, …).
- Before filling any `support_connector` / `ticketing` / `support_teams` term, run
 `support/support_translations/scripts/check_mail_templates.py` first to see the current-green
 baseline, and again after the batch to prove it is still green — a fill that turns it red is the
 one class of "progress" that is actually a regression.
- After a `system/odootools_demo` (or any module) batch, re-parse every `i18n/*.po` file for that
 module with `polib` directly — do not trust "MISSING: 0" from a one-off apply script as proof the
 module has zero empty `msgstr` left; it only proves that batch's own msgids landed.
- Finish with one full-hub re-scan (`tools`, `support`, `system`, `odoo-apps-addons`; a gap in `odoo-apps-addons` becomes a task for its developer, not a fill)
 against the complete `SHIPPED_LANGS` list before reporting the backlog closed.

## Out of scope until asked

KnowSystem article **records** and `/docs` stay English. Website app-page and ticket-form FAQ text is overlaid from `support/support_translations/tm/website/faqs/` (not Multi Languages). Store HTML stays `en_US`. Screenshot **files** stay English; `module.pic.name` and `alt_name` are translated. Country variants and the extended set are shipped (the list in **Languages** below). Production URL prefixes are Phase 11 activation. Seed from the root locale and analyze each string separately (translations may differ — not a copy, not an SEO-only event).

## Source language

- Source is **en_US**. Never translate into English. Never treat another language as source.
- Prepublishments stay English-only workspaces. Translations are re-applied after publish (loader hook), never authored on the origin by hand.

## TM-first

1. Update glossary / TM YAML first.
2. Run validators (protected terms, placeholders, XML, length).
3. Generate `.po` or let the loader apply website/DB terms.
4. MCP/UI spot fixes are the same loop: TM first, then apply. Never the reverse.

## When source strings change

If the task touches a module that already has `i18n/` or TM chunks:

- Adapt those translations in the same change (or flag the English fingerprint drift).
- Description / page copy edits must update TM for every shipped language, or leave an explicit drift item.
- A new 19.0+ public changelog follows **Bind future work** above (`33-release-gates`, skill `33-faotools-release`).
- Website/ticket FAQ copy lives in `tm/website/faqs/` (overlay). KnowSystem article records stay English. Do not enable KnowSystem Multi Languages. Store `/docs` / `/knowsystem` stay English.
- Version ports (19.0 -> 20.0, including intermediate migration branches) **carry translations**; `copy()` keeps them, then refresh fingerprints.
- **QWeb / demo restyle is a translation change.** If you change English in a `<template>`, `string=`, `title=`, or Layer 1 demo XML, the `.pot` msgid must be the **new** `xml_translate` key — not the old `<strong>…</strong>` / icon wrapper. `_update_translations(overwrite=False)` leaves the new term empty on an existing DB (incident 2026-09-09: Appointments `Any` / `Select` / more details). Same job: glossary or TM, regenerate `.po`, and the empty-term fill (`ir.module.module` hooks in `support_translations`, `odootools_demo`, every tools module that owns QWeb `<template>` views). `check_view_term_restyle.py` fails when XML is bare and the pot still only has the old tagged msgid. Demo values must stay in the module `.pot` (`demo_lint`).

## Do not translate

- Trademarks and product names: Odoo, faOtools, KnowSystem, module **display** names, technical names, slugs, URLs.
- Odoo edition names stay English: Enterprise, Community, Odoo.sh, Odoo Online (`odoo_editions` in `do-not-translate.yaml`; `check_dnt_editions.py`).
- Local technical terms: Bootstrap, Kanban, Omnibox, OWL, QWeb, JSON-LD, MCP, SMTP, IMAP.
- Customer review quotes.
- **faotools.com email templates are never translated.** Support-owned `mail.template` records (`support_connector`, `ticketing`, `support_teams`) pin `<field name="lang">en_US</field>`. Their `model:mail.template,*` `.po` terms stay empty. `check_mail_templates.py` fails the build if either side slips. Do not set `{{ object.lang }}`. Shipped `tools/` templates are the opposite: they must set `lang` to the recipient and fill subject/body terms.
- Generated store blobs: `resulted_description`, `static_description`, GitHub manifest `summary`. `module.description.short_summary` **is** translated on the website; store/GitHub paths stay `en_US` (`_prepare_description`, `get_short_summary()` with `lang=en_US`).

Ambiguous English (one word, several meanings) goes to the review queue with `ambiguous: true`. Ask rather than guess.

## Extraction and wording

- Extract `.pot` files through Odoo (`export_pot_via_odoo.py`). Do not hand-inject msgids (`ensure_pot_msgids.py` is not a source of truth). A `#: model_terms:ir.ui.view` reference must point at the view whose English arch contains the msgid (`check_pot_view_refs.py`).
- Do not split a sentence across a link. Keep the sentence as one term (`o_translate_inline` on a wrapper whose `<a>` has no `t-` attributes, or put the whole sentence inside the `<a>`). `check_link_fragments.py` flags the split.
- Russian action labels (buttons, wizards, menu actions) are perfective infinitive or imperative, never imperfective present (`Выбрать` not `Выбирать`). `check_action_labels` enforces the seed list.
- VAT stays verbatim only as a **legal identifier** (`EU VAT ID: PT332289761`, `VAT PT332289761`). The tax word in running copy still follows the glossary (VAT → НДС).
- File Manager is a UI label, not a trademark. Translate it (ru: Файловый менеджер).
- Product **display** names stay English. Exceptions that **are** translated: the `low_sales_report` menu label, and scoring **tab / field / filter** labels (`Customer Scoring`, `Vendor Scoring`) even though the manifest name stays English.
- `Industry` means business sector (ru Отрасль, pt Setor), not manufacturing. The glossary entry is `ambiguous: true`.
- No shipped msgid may have an empty msgstr except do-not-translate exact matches and support `mail.template` terms (`check_empty_msgstr.py`).

## Permanent gate

`support/support_translations/scripts/check_translation_coverage.py` is the entry point. It runs the detectors (`check_html_structure`, `check_frontend_modules`, `check_code_terms`, `check_action_labels`, `check_dnt_editions`, `check_link_fragments`, `check_mail_templates`, `check_view_term_restyle`) and, with `--live`, crawls faotools.com pages in `en_US` vs each shipped language. `devops/run_tests.sh … 19` runs the static gate. New modules and languages must pass it rather than a later cleanup pass.

Mechanisms the gate is built for:

- `_()` / `_t()` literals need `#. odoo-python` / `#. odoo-javascript` in every language `.po` (`check_code_terms.py`).
- Public OWL/JS modules must be listed in `ir.http._get_translation_frontend_modules_name` (`check_frontend_modules.py`).
- Runtime-created `translate=True` records (`website.menu`, `module.pic.name`) need a write path plus `check_db_records.py`.
- Restyled QWeb must not leave only the old tagged `.pot` msgid (`check_view_term_restyle.py`). Existing DBs need `_fill_empty_view_translations`; a `.po` update alone is not enough.
- Odoo edition names (Enterprise, Community, Odoo.sh) stay English (`odoo_editions` in `do-not-translate.yaml`).
- Non-void HTML must not self-close (`check_html_structure.py`). **Always** follow `18-xml-translate-html`: never empty `<i></i>` / `<i/>` (Odoo `xml_translate` re-serializes them and HTML5 swallows the page, including `en_US`).

Visible leftover empty msgstrs (logger text, technical help) are a tracked follow-up, not this gate's `--full` default.

## Consistency

- One concept, one term, on **app UI and website**. Seed from current Odoo core/enterprise `.po`, then keep the glossary aligned after hub pulls / serie updates (two-axis drift checker).
- Prefer similar length to English for labels and headers (per-language thresholds in TM config).
- Arabic is RTL: check our SCSS/OWL, not only `.po` text.
- `summary_key_words`: locale keyword research, extend-only, never a literal translation.

## Closing an "empty msgstr" backlog — do it exhaustively, not in samples

A request to "translate the missing strings" means **every** shipped language on **every**
touched (or scanned) module, not the 8 base languages, not the "important" ones. Treat the
8-language set as a sampling shortcut only when the user says so explicitly; otherwise scope
to the full list in **Languages** below (currently 42 codes) from the start, so the work is not
redone after someone points out the narrower scope was wrong.

1. **Scan against `.po` msgstr, not against a fixed language subset.** Build the worklist from
 `const.SHIPPED_LANGS` / `const.PO_STEM_TO_LANG`, not a hand-typed list — a hand-typed list
 silently drops languages.
2. **Map language code -> file stem before touching a file.** `PO_STEM_TO_LANG` inverts to
 `LANG_TO_STEM`; a batch script keyed by full lang code (`el_GR`) that assumes the file is
 `el_GR.po` will silently miss `el.po`. After every batch apply, list the file stems the batch
 actually touched and diff them against the language list it claimed to cover.
3. **A msgstr of only whitespace is not "empty."** `msgstr " "` is a deliberate placeholder
 (e.g. an Arabic RTL glyph with no visible text). A completeness check based on `str.strip()`
 will re-flag it forever; check for `msgstr ""` (true empty) and treat a non-empty whitespace
 value as already decided.
4. **Before filling any `mail.template`-sourced term, check the exemption.** A `.po` entry whose
 **only** `#:` reference is `model:mail.template,` on a support-owned template
 (`support_connector`, `ticketing`, `support_teams`) must stay empty (see **Do not translate**).
 Read the template's `lang` field and run `check_mail_templates.py` before and after the batch —
 filling one of these is a regression, not progress, even though it looks like closing a gap.
5. **Source words that duplicate Odoo core verbatim from core's own `.po`.** When a msgid is a
 literal reuse of a core model/field/product display name (its `#:` ref is a core `ir.model` /
 `ir.model.fields` / `product.template` xmlid, not a module-owned one), pull the translation from
 that same string in `odoo/addons/<module>/i18n/` (or `odoo/odoo/addons/base/i18n/` for `base`)
 instead of inventing wording — keeps the term consistent with the rest of the UI. Fall back to
 the parent locale for a country variant missing the entry (e.g. `fr_CA` -> `fr`), and hand-fill
 only the handful of languages core does not ship at all.
6. **Verify with an independent re-scan, not the apply script's own report.** "0 missing" from
 the batch-apply tool only means every msgid it was given landed somewhere; it does not mean the
 module has zero empty `msgstr` left (a string outside that batch, or one the original scan
 missed, can still be empty). Re-parse every touched module's `.po` files with `polib` and
 recount true empties before calling a module done.
7. **Finish with one full-repo re-scan across every repo that ships `.po` files** (`tools`,
 `support`, `system`, `odoo-apps-addons`) against the complete language list, cross-referenced
 against `do-not-translate.yaml` and the mail-template exemption, before reporting
 "all languages done." A per-module "looks complete" is not the same claim. A gap in
 `odoo-apps-addons` becomes a task for its developer, not a fill (`02-repo-boundaries`).

## apps.odoo.com

Store HTML and manifests stay ASCII English. Render/push paths are pinned to `en_US`. Do not ship translated `index.html` to GitHub.

## Languages

Shipped (module list and website list stay identical):

- Bases: `ru_RU`, `fr_FR`, `de_DE`, `es_ES`, `pt_PT`, `nl_NL`, `it_IT`, `ar_001`
- Extended: `tr_TR`, `sv_SE`, `fi_FI`, `pl_PL`, `nb_NO`, `hu_HU`, `cs_CZ`, `da_DK`
- Country: `pt_BR`, `de_CH`, `en_GB`, `fr_BE`, `fr_CA`, `fr_CH`, `nl_BE`, `es_419`, `es_CL`
- Additional: `el_GR`, `lt_LT`, `et_EE`, `hr_HR`, `ro_RO`, `sr@Cyrl`, `bg_BG`, `sl_SI`, `lv_LV`, `vi_VN`, `ko_KR`, `ja_JP`, `zh_CN`, `hi_IN`, `bn_IN`, `id_ID`, `ms_MY`

Only Odoo `res.lang` codes. Serbian is Cyrillic (`sr@Cyrl`). Chinese is Simplified Mandarin (`zh_CN`) only. Source stays `en_US` (never a target). **No language in this program is post-launch.** Production URL prefixes are Phase 11 activation.

Country locales seed from the shipped **root** (`pt_PT` → `pt_BR`, `de_DE` → `de_CH`, `fr_FR` → `fr_BE` / `fr_CA` / `fr_CH`, `nl_NL` → `nl_BE`, `es_ES` → `es_419` / `es_CL`; `en_GB` from `en_US`), then every string is analyzed for that country. Do not copy the root TM. Do not treat variants as hreflang/switcher only.

## 20-local-commands

_faOtools local Docker commands, ports, and Mailpit. Read when launching, shelling, or syncing a local target_

# Local Docker commands

The bans are always-on in `20-local-docker`. This skill is the commands. `env-up` prints the URL, the database name, and Mailpit. Repeat those printed values.

```bash
cd /home/feelwhy/Odoo/faotools_env
./local/env-up.sh demo19          # community all-apps 19 → http://localhost:18190
./local/env-up.sh demo19e         # enterprise all-apps 19 → http://localhost:18191
./local/env-up.sh support         # faotools.com (neutralized) → http://localhost:18100
```

A first launch restores and neutralizes. Prefer the container shell:

```bash
./local/env-shell.sh demo19       # odoo shell
./local/env-shell.sh demo19 psql  # SQL against the local Postgres (host port 15432)
```

Several targets (and Febado) can run at once. Each Odoo has its own HTTP port (`support` 18100, `demo19` 18190, …). Shared Mailpit is on **18025**.

Keep images and databases fresh with `./local/env-sync.sh` (or `./local/env-sync.sh --check`). The full port matrix and sync behavior are in `faotools_env/local/README.md`.

## 20-local-docker

_Local Odoo stays in Docker, and a chat must not leave databases or volumes behind_

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

## 21-faotools-mcp

_Live faOtools MCP usage for production truth on faotools.com_

# Live faOtools MCP

- The real live support database may be reachable through the MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). If it returns needs auth or Unauthorized, connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Do not ask the owner to log in.
- Use it when a task needs production truth that cannot be reliably inferred from code, such as current `ir.ui.view` contents, live website metadata, config parameters, cron state, or app/module records.
- Prefer read-only MCP checks unless the user explicitly asks to update live data.
- Before calling any MCP tool, inspect that tool's descriptor/schema and use the documented parameters.
- Treat live data as production data: do not expose secrets, tokens, customer-private details, or raw sensitive payloads in chat.
- If code and live behavior disagree, consider whether the module has not been upgraded, a view was customized in the database, or cached/generated content is stale.
- App releases (`module.release`): follow the skill `33-faotools-release`, which reads article 2137. Do not invent a parallel publish path.

## Files: upload them yourself

The agent uploads every file itself. Never hand a PDF or image to the owner to attach (`linkedin.post` 6 and 7, 2026-11). The steps (inline, pre-signed PUT, binary fields, `requires_bearer_token`) are KnowSystem article 2140 in section `AI` on faotools.com. Read it through MCP before the first upload. Stop unless it is active and in section `AI` (id 157). Do not fall back to the upload page.

## 30-prepublishment-descriptions

_Rewrite/adapt faOtools apps-store module descriptions before publishment_

# faOtools app page changes

Trigger: переписать / адаптировать описание приложения, features, guidelines, alerts, screenshots, prepublication.

The procedure is KnowSystem article 2138 in section `AI` on faotools.com. The title is for people. Read the article before any write to `module.description` or its children. Git history of this file is not the procedure. This id lookup belongs only to this pointer.

https://faotools.com/odoo/knowsystem/2138

1. MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). Inspect the tool schema first (`21-faotools-mcp`).
2. Read `knowsystem.article` 2138.
3. Stop unless that record is active and its section is `AI` (id 157).
4. Read `description` and follow it.

If the host MCP tool returns needs auth or Unauthorized, do not stop and do not ask the owner to log in. Connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Stop only when that path also fails to make a working call, or the read does not return one active record in section `AI`. Do not reconstruct the steps. The bans in `33-release-gates` (edit only a prepublication, and stop for the owner before apply), `18-xml-translate-html`, and `17-translation-gates` still apply; they are enough to refuse a write.

## 31-prepublishment-screenshots

_Screenshot conventions for faOtools module store pages_

Copy, HTML structure, and the prepublication itself: the skill `30-prepublishment-descriptions` (KnowSystem article 2138).

# Screenshot Source: Real UI, Never Generated Images

- Never use image-generation tools (e.g. `GenerateImage`) for app-store screenshots. They are not real UI and must not be uploaded as `module.pic`/`module.description` assets.
- Capture screenshots from an actual running local Odoo instance showing the real views of the module being described.

# Hard gate: demo environment BEFORE any capture

**Do not run Selenium or upload PNGs until the demo environment passes the checks below.**

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
6. Run **QA reject checks** on every PNG before upload (see below).
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

# QA checklist (every PNG before upload)

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

# Translations (hard gate) — titles and alts, not the PNG

Screenshot **files** stay English. **`module.pic.name` and `alt_name` are translated.**

Replacing or adding shots is **not** done when the PNG is on the page. Same job:

1. Rewrite TM `confs[].pics` / `features[].pics` / top-level `pics` to the **new** English `name` and `alt_name` (drop the old titles). A guideline shot is only reachable under `confs[].pics`.
2. Translate both fields for every shipped language (`17-translations`).
3. The live apply (KnowSystem article 2139, skill `17-translations` **Live apply**) **must include `pics`**. Omitting them, or applying the old pic YAML, leaves `/<lang>/` captions in English. MCP cannot run that apply.
4. `action_apply_prepublishment` only re-applies YAML already on the Functional container — new local TM still needs the live apply.
5. Prove it: live `module.pic.name` **and** `alt_name` equal the TM translation in each shipped language. "Differs from English" passes on an old title's translation.

Incident 2026-09-01: Google Drive guideline body was translated; titles such as `Open the Google Auth Platform` stayed English because TM still had the old console titles and the loader apply omitted `pics`.

# Upload

The agent uploads the QA-passed PNGs itself (`21-faotools-mcp`). Never hand them to the owner to attach. Upload steps are KnowSystem article 2140, read through MCP as in `21-faotools-mcp`. Then create `module.pic` on the prepublication with `attachment_id`, `name`, `alt_name`, `sequence`, and `description_id` + `feature_id` for a feature shot or `conf_id` for a guideline shot (KnowSystem article 2138).

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

_Prepare or publish a faOtools app release on faotools.com (module.release), including changelog, exact_version, and phrases like выложи or опубликуй_

# faOtools app release

Trigger: prepare / make / publish a release, выложи, опубликуй.

The procedure is KnowSystem article 2137 in section `AI` on faotools.com. The title is for people. Read the article before any `module.release` write. Git history of this file is not the procedure. This id lookup belongs only to this pointer.

https://faotools.com/odoo/knowsystem/2137

1. MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). Inspect the tool schema first (`21-faotools-mcp`).
2. Read `knowsystem.article` 2137.
3. Stop unless that record is active and its section is `AI` (id 157).
4. Read `description` and follow it.

If the host MCP tool returns needs auth or Unauthorized, do not stop and do not ask the owner to log in. Connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Stop only when that path also fails to make a working call, or the read does not return one active record in section `AI`. Do not reconstruct the steps. The bans in `33-release-gates`, `18-xml-translate-html`, and `11-manifest-version` still apply; they are enough to refuse a write.

## 33-release-gates

_Live faotools.com release bans that stay in every chat_

# Release gates

These bans apply even when the user did not say “publish a release”. The sequence, HTML samples, notes, YAML, and the translation step are KnowSystem article 2137 (`AI`), reached through the skill `33-faotools-release`. Read that article before any `module.release` write.

- Scope is apps in `tools` and `odoo-apps-addons` only. Refuse a release of an app from `support`, `life`, `system`, or `faotools_env`. A prepublication (`prepublish=True`) is only for a substantive change of the description: features, guidelines, alerts. A change of `exact_version`, or the release alone, is written straight on the public description, with no prepublication. When a substantive change is planned, create the prepublication in the same step as those edits; never an empty copy (ai_mcp_server 20.0 prepublication 1347, 2026-11-26, held only `exact_version` 1.2.9). Then edit only that prepublication and stop for the owner before apply. The stop message says where and what to check: the prepublication page URL (`website_absolute_url` of the prepublication), and for each change the section heading on that page and the old -> new sentence. "Check the prepublication" alone is not a stop message (prepublication 1347, 2026-11-26). Do not bump `__manifest__.py` (`11-manifest-version`).
- `commit_ids` are linked after publish (article 2137 steps 4–5). After writing them, read the release back and report the count from that read. A count that was not read back is not reported (releases 1275 and 1276, 2026-11-26, were reported with 7 and 8 linked commits while `commit_ids` were empty).
- A new serie: the changelog is published while the page is still hidden, then the page is made public. A public page with an empty changelog is a failed release.
- No serie named: release on every public serie whose branch has the change. Do not ask which serie. Each major serie bumps its own `exact_version` tail.
- Bump only the last number of `exact_version`. Only the migration release to a new major serie copies the tail of the previous serie. Do not invent an extra number.
- Do not call Quick GitHub Update (`action_update_in_github_quick` / `action_update_in_github`) through MCP. That call commits per module and aborts the MCP transaction.
- Do not call `action_get_commits` through MCP either. It also commits, even when GitHub fails. Run it in `odoo shell` (article 2137).
- “Published” is allowed only after the live page for every shipped language has no new English sentence. A filled `.po` is not that (Appointments `1.3.33`, 2026-09-10, `/ru/` stayed English). A loader return code is not that. An encoding error in the shell payload means rewrite the payload and apply again (2026-09-28). Stop only when the user explicitly says to skip translations.
- A changelog icon has a space inside the tag, `<i class="fa ..."> </i>`. An empty `<i></i>` becomes `<i/>` and swallows the page (2026-08-23). The full rule is `18-xml-translate-html`.

## 34-demo-data

_Demo data for tools apps — layer boundary, quality bar, shared cast, xmlid stability_

# Demo data (tools + odootools_demo)

Pull this rule for any task that adds or changes `tools/*/demo`, a `tools` manifest `demo` key, or `system/odootools_demo` loaders / template setup.

Demo content for a public app is **either** plain XML inside that `tools` module **or** Python inside `system/odootools_demo`. There is no third option, and a `tools` module never ships a Python demo generator.

## Layer boundary

| Layer | Where | Ships to customers |
|---|---|---|
| 1 | `tools/<module>/demo/*.xml` + manifest `demo` | Yes (apps.odoo.com zip, client DB with demo) |
| 2 | `system/odootools_demo` Python | No (our template / clones only) |
| 2b | `system/odootools_demo/demo_scripts/<module>/` (`demo_xmlids.json`, `demo_purge.json`, `asset_signoff.json`) | No — script inventory, never in the public zip |
| 3 | `tools/<module>/i18n/*.po` demo terms | Yes, with the app |
| 4 | `faotools_env/local/env-demo-*.sh` | Local + later production template build |

**Real demo data belongs in `tools`. Basics and scripts belong in `system`.** The records a
customer is meant to look at, click and edit are Layer 1; the machinery that produces or
completes them — loaders, spec tables, upserts, refreshers, credentials, cross-app wiring,
and every JSON the linter / reload scripts read — is Layer 2 / 2b. Odoo never loads
`demo_xmlids.json`, `demo_purge.json`, or `asset_signoff.json`. Those files must not sit
in a `tools` module.

Layer 1: only that module's **own** models plus configuration it owns. Referenced actors are core demo xmlids in the module's transitive `depends`.

Layer 2: users, `res.users` credentials, settings, cross-app targets, homepage, topicality cron, XXTOOLS / Y1TOOLS history.

A `tools` module must not carry spec tables, upsert helpers, `<function>` demo loaders, or hand-written `ir.model.data` rows for demo.

### Why Python demo cannot live in the module

Demo targets are usually core records of apps the product does **not** depend on (`hr`, `crm`, `sale`, `purchase`). `ref("purchase.purchase_order_4")` cannot be used from a module whose `depends` is `["web"]`.

A plain install with demo — **including the apps.odoo.com live preview** — shows only Layer 1. Do not move the generator back into `tools` to "fix" that.

### Layer 1 must be self-sufficient — no plugs

What Layer 1 ships has to stand on its own, because Layer 2 will not be there. A **plug** is a
record whose only content lives in the other layer: a vault with no passwords, a type with no
fields, a section with no articles, a role whose groups are stamped from Python, a rule whose
target is created elsewhere. It is worse than shipping nothing — the app reads as unused, and
that is the page the store preview shows.

Before a family chunk is done, ask of every Layer 1 file: **installed alone, with demo, and
nothing else — is there anything here to look at?**

- **Container implies content.** If Layer 1 creates the parent, Layer 1 creates enough children
 to make the parent worth opening. Splitting the two across layers is the plug.
- **Visibility counts as content.** A record hidden by the module's own record rules is a plug
 even though the row exists. Ship the `*.access` / member / publish rows that let the shipped
 demo user (`base.user_demo`, `base.user_admin`) actually see it.
- **What Layer 1 genuinely cannot produce moves out whole.** Not the parent in `tools` and the
 child in `system` — the whole family goes to `odootools_demo`, and the module ships
 `"demo": []`. `security_user_roles` is the reference case: roles are worthless without real
 groups, so the roles went too.
- **Configuration with nothing configured is still a plug.** A `custom.*` field definition whose
  value no record carries reads as an empty side panel. Definitions may stay in Layer 1 (a
  customer can fill them), but the values are then owed from Layer 2 in the same chunk — the
  generated column is `x_oz_<code>_<id>`, an id-dependent name no XML can reference.

### What Layer 1 can only do at install — Layer 2 owes the rest

A noupdate demo record is **created on install and skipped on every `-u`**
(`convert.py` `_tag_record`). Two Layer 1 patterns therefore work for a customer's fresh
install and silently do nothing on our long-lived demo databases, so the same chunk owes a
Layer 2 re-apply:

- **Dropdown options.** `custom.extra.field.selection` rows do not reach the generated
  `ir.model.fields`; only `custom_extra_field.write` pushes them (`_return_new_field_values`).
  Layer 1 re-declares the field after its options; Layer 2 calls
  `_demo_custom_field_sync_options` so an installed database stops showing an empty dropdown.
- **Updating a foreign record.** A demo file may set a field on another module's xmlid
  (`odoo_password_manager_custom_fields/demo` types the `odoo_password_manager` keys) — the only
  Layer 1 way when the dependency cannot see the dependent. `env-demo-reload.sh` leaves foreign
  xmlids to their owning module, and the `-u` skips the row, so Layer 2 re-stamps the value.

### Layer 1 bans

Never in tools demo XML:

- Models: `res.users`, `res.groups`, `res.company`, `res.lang`, `ir.cron`, `ir.mail_server`, `ir.config_parameter`
- Login credentials: `login` / `password` on `res.users`, and any secret that grants access to a real system. A password the **product itself** stores as business data (`password.key`, `portal.password.bundle`) is content, not a credential — sample values only, never a live one.
- Anything that sends mail
- Posted / validated transactional records: no `<function>` calling `action_post` / `action_confirm` / `button_validate` / `_action_done`; do not write `state` to `posted` / `done` / `sale` / `purchase` on core sale / purchase / invoice / picking models. Draft quotations, draft invoices, planned pickings only.

Every Layer 1 record must be deletable by a client without side effects. `noupdate="1"`. Attachments under `<module>/static/demo/` with source URL + license in `static/demo/SOURCES.md`. HTML per `ai_rules` `18-xml-translate-html` (never empty `<i></i>` / `<i/>`).

Never in `tools/<module>/demo/`: `demo_xmlids.json`, `demo_purge.json`, `asset_signoff.json`,
or any other script JSON. Those live in `system/odootools_demo/demo_scripts/<module>/`.
The linter fails a public module that still ships them.

### Baseline apps before any demo (20.0 onward)

Every template, review and smoke database installs these apps before any demo:
`contacts`, `account` (Invoicing), `sale_management` (with `sale`), `website_sale`,
`crm`, `stock`, `purchase`, `project`, `hr`. They are hard `depends` of
`odootools_demo` on `system` 20.0, so any database that installs it gets them first.
A Layer 2 loader may therefore build on them for any family, so the demo shows more
than one app: roles take sales, purchase, stock and project groups, alerts and
checklists target real orders, tasks and leads. Incident 2026-09-30:
`fx8_20_4` installed only `project` + `portal` under the group, and the Security User
Roles demo silently lost every purchase / stock / sales group.

- Keep tools apps out of `odootools_demo` `depends`: an unported one would block a
 group review database.
- Layer 1 is unchanged. A `tools` module's demo XML still uses only its own
 `depends`, because the apps.odoo.com preview has no `odootools_demo`.
- A build script does not keep its own copy of this list. It installs
 `odootools_demo` (next to the group), and Odoo resolves the rest.

### Layer 2 rules (odootools_demo)

- Guard: `_demo_module_installed("<module>")`, or `"<model>" not in self.env` → return.
- Resolve targets with `self.env.ref(xmlid, raise_if_not_found=False)`; skip and log if missing.
- Upsert by xmlid (`_demo_ensure_xmlid`). Demo `<function>` tags skip on `-u`; setup and `env-demo-reload.sh` call Python loaders directly.
- **`odootools_demo.*` xmlids only.** Never create `ir.model.data` in a `tools` module namespace from `system`.
- Password / extra-module install is gated on `_is_demo_template_db()` (escape hatch `odootools_demo.template_db_names`). Template ships **en_US only**; clones get languages from `after_clone_19`.
- Date shufflers skip records owned by a tools or `odootools_demo` xmlid. Core xmlids (`sale.sale_order_1`, …) still shuffle — so an authored family needs its own refresher (see **Topicality**).

## Shared cast

Resolve by **xmlid**, never by uid.

| Role | Xmlid / stamp |
|---|---|
| 0user | `base.user_demo` (login `demo`; xmlid `odootools_demo.user_0user`) |
| Anita Oliver | `hr.employee_hne` → user `anita.oliver@example.com` |
| Other team | core `hr` demo employees (Doris Cole, Ernest Reed, Sharlene Rhodes, Paul Williams) |
| abs-xyz | `product.product_product_acoustic_bloc_screens_white` |
| manual-cd | `product.product_product_4c` |
| ODS-900 | `product.product_order_01` |
| Sales teams | `sales_team.team_sales_department` → Europe; `sales_team.crm_team_1` → America |

Password `faotools` for 0user and the team. **Never** touch OdooBot or Administrator passwords. Scrub real-looking portal identities (e.g. Dhruv Fefar). TZ `Europe/Brussels` on users and `resource.calendar`.

Vendors in copy: **Gemini Furniture**, **Ready Mat**, **Azure Interior**, **Anita Oliver** (not Olivier, not GeM Designs).

## Quality bar

Demo must read as if a human prepared a customer database.

- **Correct.** Numbers add up; every person, company and product named in free text exists as a record; every `ref` resolves.
- **Current.** No fixed historical period, no validity window ending in the past. Dates are `eval` / relative or maintained by the topicality cron.
- **Consistent.** One spelling per persona. One casing convention per model.
- **Not an advertisement.** No "(added by the tool …)" footers, no `apps.odoo.com` / `faotools.com` links, no hardcoded serie number in demo text.
- **Clean text.** ASCII-only English source (apps.odoo.com zip is latin-1); no Cyrillic/Greek lookalikes inside Latin words; no NBSP, zero-width, smart quotes, or named entities.
- **Attachments.** If a record has an image or file field, attach a real professional-looking, close-to-real example from the internet — not a blank, not generated, not a screenshot of an older Odoo. Images: ≥1024 px on the long side, JPEG or WebP, ≤200 KB. Store under `<module>/static/demo/`.
- **No copyright infringement.** Every demo asset and every demo text must be something we have the right to redistribute commercially (Layer 1 and Layer 2). Allowed: CC0 / public domain, content we created, or a license kept on file next to the asset (source URL + license in a comment or `static/demo/SOURCES.md`). Forbidden: branded product photos, trademarked logos, identifiable people, scraped stock, and full-text copies of third-party licenses, agreements, or articles. This applies to pictures, PDFs, email attachments, and KnowSystem / documentation bodies.

The static linter (chunk 4) and runtime tests (chunk 5) enforce this. Until they exist, follow the bar by hand.

## Xmlids

- Stable and family-local. Do not rename an existing demo xmlid without a migration reason (noupdate contract).
- No absolute database ids. Map `Source ID` / `MEASURE(n)` / `user_id.id = 9` through `env-demo-xml.sh resolve`, and leave the xmlid in an XML comment.
- Dump source-less families with `env-demo-xml.sh dump`, then edit to the bar (relative dates, refs, no ads).

## No obsolete demo data

**The template database contains only records the current demo files own.** A record left over
from an older demo generation is a defect, even when it looks harmless: the customer sees two
knowledge bases, the UI review is unreadable, and translations key on text nobody maintains.

Odoo does not clean this up for us. Removing a record from a demo file, or renaming its xmlid,
deletes the `ir.model.data` row and leaves the record, so it survives every later `-u` as a
record with no xmlid at all.

Each family therefore declares the models it owns in
`system/odootools_demo/demo_scripts/<module>/demo_purge.json`:

```json
{"models": ["knowsystem.article", "knowsystem.section", "knowsystem.tag"]}
```

- **Order children first** — the purge unlinks in the listed order.
- **Only models the family owns.** Never a shared model (`res.partner`, `ir.attachment`,
  `mail.message`): a stray there belongs to someone else.
- **Never a runtime model** (`knowsystem.article.revision`, `know.view.stat`). Those records are
  created by the application, have no xmlid by design, and die with their parent by cascade.

`env-demo-reload.sh` purges before it resets (`--no-purge` opts out), and the build assertion
fails when any declared model still holds a record without an xmlid. A family whose demo writes
to an owned model and has no `demo_scripts/<module>/demo_purge.json` has not finished the chunk.

## Topicality

Demo must read as if a human prepared it last week, not in the year the template was built.
`res.company.action_amend_demo_data` (`system/odootools_demo`) is the only mechanism that keeps a
long-lived template current, and it does **not** cover a new family by itself:

- Its date shufflers **skip records owned by a tools / `odootools_demo` xmlid**
  (`_demo_without_authored`), so authored dates freeze at load time and age with the template.
- Engagement stats do the opposite: no authored filter, `(6, 0, …)` writes, and a random
  `create_uid` rewrite — they overwrite what the family authored.
- Records the cron never heard of (revisions, progress rows, view counters, version labels such as
  "2025 range") stay exactly as loaded, forever.

So every family chunk, before it may be called done:

1. **List** its ageing records: create / write dates, deadlines, counters, progress, "last revision",
   date-shaped names.
2. **Name the mechanism** that keeps each one current: an existing cron shuffler, a family refresher
   called from the loader path, or a relative `eval` re-anchored on every load.
3. **Add the missing refresher** in `odootools_demo` in the **same** chunk, idempotent: a second run
   must not multiply rows or break chronology (created before the first revision, revisions in order,
   no future dates unless the field means the future).
4. **Do not let the cron fight authored intent.** A refresher that owns a field keeps the family's
   cast author, relative order, and the story the copy tells.
5. **Report the outcome** in the chunk report. "Nothing needs refreshing" is valid only with the
   record list behind it.

A family that ages into "created two years ago, never revised, zero views" has failed the quality
bar even though every record is correct.

## Translations

Same change as the English demo (`17-translations`). Demo terms are `model` / `model_terms` in the module `.po`. The 8 phase-1 languages are gate-blocking; the extended 17 may trail. Noupdate copy does not re-apply on `-u` — fix means `env-demo-reload.sh` (delete xmlids, then re-init) or a template rebuild.

KnowSystem article records stay English until the multilang decision in that family chunk. Install `knowsystem_multilang` on the template.

## Family loop

0. Decide the layer per record (**real data → `tools`, basics and scripts → `system`**) and check Layer 1 against the no-plugs test above. Script JSON (`demo_xmlids.json`, `demo_purge.json`, `asset_signoff.json`) goes in `odootools_demo/demo_scripts/<module>/`, never in the public module.
1. Author Layer 1 XML (and Layer 2 loaders if the target is outside `depends`). Any image or file field gets a **licensed real-world attachment** (source URL + license recorded); drop or replace anything we do not have the right to ship.
2. Resolve every absolute id; fix that family's known defects.
3. Topicality pass (see above): list the ageing records, name the mechanism, add the missing refresher.
4. Static linter green; `env-up.sh demo19 --test <module>`.
5. `env-demo-reload.sh demo19 <modules>` into local demo19; user reviews UI.
6. Russian `.po` → user reviews; then the other 7 phase-1 languages; then the extended 17.

Stop after each numbered step that needs a user look. Do not publish or swap the production template except on explicit command (`33-faotools-release`; production swap is a later chunk).

## Local commands

```bash
./local/env-demo-build.sh --smoke     # tiny DB, setup, assert, drop
./local/env-demo-reload.sh demo19 sticky_notes,smart_warnings
./local/env-demo-xml.sh purge demo19 knowsystem --check   # obsolete records, report only
./local/env-demo-xml.sh resolve demo19 res.partner 15,46
./local/env-demo-xml.sh dump demo19 sticky.note --limit 20 --out /tmp/sticky_notes.xml
```

`env-demo-build.sh` calls `res.company.action_setup_demo_template()`.
`env-demo-reload.sh` purges obsolete records, deletes that module's **demo** xmlids, runs `-u`, then `_reload_tools_demo_data()`. Renaming either method breaks the scripts. `--no-reset` is the old `-u`-only path, `--no-purge` keeps records no demo file owns.

New Python loaders: idempotency case in `odootools_demo/tests/test_demo_template.py` (run twice → same record count). `env-up.sh demo19 --test odootools_demo`.

## Releases

One `module.release` per module whose **demo** changed, `exact_version` last number +1, note confirmed first (`33-faotools-release`). Do not bump local `tools` `__manifest__.py` `version` (`11-manifest-version`). Merge `19_demo` → `19.0` only when publishing.

## Screenshot seed (side-goal)

Demo DBs seed store recaptures (`31-prepublishment-screenshots`). Read `static/description/` PNGs + `index.html` alt; skip `icon.png` / `main.png` / `main_nopromo.png` / `app_icon_*`. Recreate the document type, visible text, and ≥2–3 list rows. Do not attach those PNGs as demo `ir.attachment` unless the product stores images.

## Serie-proofing

No serie bump in this work. Xmlids stay stable and family-local; no absolute ids; the serie number is never typed into demo content; demo XML lives in the module it belongs to.

## Major-version port (`36-major-version-port` `Gx.4` / `Gx.5` / `Gx.8`)

A group port uses **the same 19.0 generators** for the **touched modules only**, then
improves those generators when the stand-in needs it. There is no third demo path.

- **Layer 1** stays in `tools/<module>/demo`. Port it with the module (`Gx.4`). Empty
  `"demo": []` is valid only when 19.0 also ships empty and Layer 2 owns the family.
- **Layer 2** stays in `system/odootools_demo` (`_load_demo_<family>`,
  `demo_scripts/<module>/`). `Gx.5` **runs** `_reload_tools_demo_data` /
  `env-demo-reload.sh` on the stand-in. Grep-for-`get_param` is not a check.
- **Hard `depends` on an unported app is a `Gx.5` defect**, not a reason to skip.
  Loaders already no-op via `_demo_module_installed`. Drop or guard the extra depend
  so `odootools_demo` can install next to the group; keep skipping families whose
  modules are absent.
- **Improve the loader in the same group** when saas-19.4 breaks it: typed ICP,
  `datas` → `raw`, `env.cr.commit()` on a piped saas `odoo shell` (stdin rolls back
  otherwise), create `base.user_demo` / `demo`/`demo` if core `--without-demo=` did
  not, create `faotools-mailpit` `ir.mail_server` when the stand-in has none
  (`20_suite` Gx.5 From addresses skipped), topicality. Do not invent a
  parallel `/tmp/*_seed.py` as the resting generator.
- **`Gx.8` refresh** is `env-demo-reload.sh <target> <touched-modules>` (or
  `Company._reload_tools_demo_data()`), same as 19.0. A one-off seed is a walk aid
  only while `Gx.5` is still open.
- Prove it with **counts**, not kinds: `demo`/`demo` authenticates, and every
  family the 19.0 loader creates is present (2 joint calendars **with events**,
  3 reminders, KPI categories + periods + targets + items). One invented KPI
  / calendar / reminder row is a failed `Gx.5`. A later group that hands over
  `Gx.8` while those loaders have not run has failed the same way `20_5` did.

## 35-knowsystem-demo

_KnowSystem demo articles must obey the contract of their editor_type (arch/description pair, real blocks, inlined mail-print body, revisions)_

# KnowSystem demo articles

Pull this rule together with `34-demo-data` for any task that writes `knowsystem*` demo data
(articles, revisions, templates, documentation sections).

A `knowsystem.article` is not "a record with some HTML". Each article declares an
`editor_type`, and that type owns **how the two body fields must relate**. Demo data that
ignores the contract looks fine in a list view and then breaks the moment a human opens the
editor, prints the article, mails it, or restores a revision.

## The two body fields

| Field | Role |
|---|---|
| `description_arch` | The **editable source** the editor writes and re-opens |
| `description` | The **rendered/consumed** body: website and portal display, printing report, `_notify_of_revisions` mail, clipboard copy, `indexed_description` (search), `kanban_description` |

`knowsystem/models/knowsystem_article.py` `_update_description_safe` pairs them on `create` /
`write`: if only one is given, the **other is set to the same raw value**. That fallback exists
for imports, not for demo. Demo data that supplies one field ships an article whose consumed
body was never produced by its editor.

**Always write both fields explicitly**, with `description` equal to what that editor type
actually produces:

| `editor_type` | `description_arch` | `description` |
|---|---|---|
| `text` | plain text | same text with `\n` replaced by `<br />` (JS `_updateEditor`) |
| `html` | authored HTML | byte-identical to the arch (`SimpleHtml` passes no adapter) |
| `backend_editor` | builder document (see below) | **CSS-inlined, table-based** output of `toInline` from `@mail/views/web/fields/html_mail_field/convert_inline` (`KnowSystemHtml.adaptReadonly`) |

There are exactly **three** editor types on 19.0 (`_selection_editor_types`): `backend_editor`
("Backend Builder"), `html`, `text`. `website_editor` is a **stale value** left in old
databases — never author it, and re-type any record that still carries it.

## backend_editor: the arch is a builder document

The arch must be the real wrapper plus real snippet sections, because the builder re-parses it:

```html
<div data-name="KnowSystem" class="o_layout knowsystem_layout oe_unremovable oe_unmovable">
  <style id="design-element">...design CSS variables...</style>
  <div class="container knowsystem_wrapper knowsystem_regular oe_unremovable">
    <div class="row mw-100 mx-0">
      <div class="col knowsystem_no_options knowsystem_wrapper_td bg-white oe_structure">
        <section class="s_text_block ..."> ... </section>
      </div>
    </div>
  </div>
</div>
```

- Wrapper comes from `knowsystem.wrap_window` / `knowsystem.KnowSystemLayout`
  (`views/editor/snippets.xml`, `static/src/wrap/wrapper.xml`). `KnowSystemHtml.wrapNewArticle`
  injects it for an empty body; a demo arch without it opens as a foreign document.
- Content is **snippet sections** from the KnowSystem snippet set (`s_text_block`,
  `s_text_image`, `s_three_columns`, `s_media_list`, headings blocks, …) with their own classes
  and `data-` attributes — never hand-rolled `<div>` soup, never Bootstrap markup invented for
  the occasion. The builder must be able to select, move, duplicate and re-style every block.
- Design options live in the `<style id="design-element">` block. Keep the one the editor wrote;
  do not hand-edit CSS variables.
- `description` is the mail/print body: a `<table role="presentation">` tree with inline
  `style="..."`. It is roughly **twice** the arch size. Hand-writing it is not possible and not
  allowed.
- With `knowsystem_multilang` installed, `description` and `description_arch` are `translate=True`
  Html fields, so always-on `ai_rules` `18-xml-translate-html` governs them: an icon span must be
  `<span class="fa fa-info-circle …"> </span>`, never an empty pair. Card snippets such as
  `s_three_columns` ship exactly that empty span in older articles — fix it when you reuse their
  markup.

## Therefore: capture backend_editor bodies from the editor, never by hand

For `backend_editor` (and for any block-based body), the only correct authoring loop is:

1. Author the **arch** in the module's demo XML (wrapper + real snippet sections), or build the
   article in the editor in a local demo target.
2. Run the capture, which drives the real editor in a headless browser and lets **its** code
   write the pair, then merges both fields back into the demo XML:

```bash
./local/env-demo-capture.sh demo19 knowsystem.demo_article_welcome[,more_xmlids]
```

- Browser half: `system/odootools_demo/tests/test_demo_capture.py` (tag `demo_capture`, out of
  the standard suite). It clicks Edit, waits for the builder iframe, triggers the module's own
  commit so `adaptReadonly` inlines the document, saves through the editor's Save button, and
  dumps the result.
- Merge half: `faotools_env/local/lib/demo_capture.py` rewrites `description_arch` and
  `description` of that record in place.
- The synced `env-demo-*` images carry no browser, so the script builds a thin local image from
  `lib/capture.Dockerfile` (Chrome + `websocket-client`) and rebuilds it whenever the base image
  moves. Never install a browser into a running container: that vanishes on recreate.
3. Re-load (`env-demo-reload.sh`) and re-open the article in the editor to prove it is still a
   live builder document. Expect the editor to have normalized the arch and added its
   `<style id="design-element">` block — that normalized arch is what belongs in the XML.

`text` and `html` articles may be authored directly in XML, because their `description` is a
mechanical transform of the arch.

## Porting to a new major serie: re-capture, never copy

When these articles move to the next serie (19.0 -> 20.0 and onward), **the body pair must be
produced again by that serie's editor in a real headless browser.** Copying the previous serie's
`description` (or its arch) is wrong even when it renders fine, because every producer of those
strings can change between series:

- the inliner itself (`toInline` / `getCSSRules` in `@mail/views/web/fields/html_mail_field/convert_inline`),
- the KnowSystem wrapper templates (`knowsystem.wrap_window`, `knowsystem.KnowSystemLayout`),
- the snippet set and each snippet's markup, classes and `data-` attributes,
- the design-element CSS variables and the editor's normalization of the arch,
- the builder's own save path (`KnowSystemHtml._commitChanges` / `adaptReadonly`).

A copied body therefore ships last serie's HTML into this serie's editor, and the first user who
opens it gets a document the builder no longer understands.

Port procedure:

1. Bring the demo XML over unchanged (the arch is the input, not the deliverable).
2. Put the hub on the new serie and load the module in that serie's demo target.
3. Run `env-demo-capture.sh <new-serie-target> <every backend_editor xmlid>` and let the new
   editor rewrite both fields.
4. Review the diff on the arch as well as the description: a changed wrapper or snippet markup is
   a real port finding, not noise.
5. Refresh the translation fingerprints afterwards, since the source text the TM keys on has
   changed (`17-translations`).

The same applies to any other body a serie's editor produces, and to a re-capture triggered by a
new base image rather than a new serie.

## Revisions

`create` always writes one `knowsystem.article.revision` snapshot, and `write` on any of
`name`, `description`, `section_id`, `tag_ids`, `attachment_ids`, `kanban_manual_description`
adds another and posts the revision notification. A demo article therefore starts with exactly
one revision that mirrors the loaded body — a knowledge base with no history looks unused.

Demo revisions must follow the same contract as the article:

- Carry the matching `editor_type` and **both** `description` and `description_arch`. The
  revision model has no pairing logic, so a missing field stays empty and
  `action_recover_this_revision` would wipe the article body.
- Use `author_id` from the shared demo cast (`34-demo-data`) and **relative** `change_datetime`,
  ordered oldest to newest.
- Make the older bodies genuinely shorter or different: `description_change` is a length delta,
  so identical snapshots render an empty, pointless history. `write_revision_date`,
  `write_revision_uid` and `contributor_ids` are computed from the newest revision, so the
  history is also what makes "Last revision by" believable.
- A restored revision must be a valid document for its editor type — same wrapper and snippet
  rules as above.

## Companion modules

- `knowsystem_multilang` is what makes `name`, `description`, `description_arch` and node names
  translatable (`translate=True`). Without it these strings are `translate=False` and no `.po`
  can carry them. Demo translations for the family therefore require it installed at export
  time.
- `is_published` / `website_published` on articles, sections and tags come from
  `knowsystem_website`. Publish flags belong in that module's demo, not in `knowsystem/demo`.
- `documentation.section` (`documentation_builder`) has its own `translate=True` fields and
  consumes `action_get_published_name` plus the published body — the same arch/description
  pairing applies to anything it renders.

## 36-major-version-port

_Process for porting the tools apps to a new major Odoo serie (branches, gates, ledger, publish)_

# Major-version port (tools apps)

How a whole serie of faOtools apps moves to a new major Odoo version: branch topology, per-group
gates, durable state, and the publish loop. The **technical** transforms live in `ai_rules`
`22-migrate-v19-to-v20` (one rule per serie pair). This rule is the process around them.

Current program: 19.0 → 20.0. `saas-19.4` stood in for 20.0 until its release (2026-09-28); core and enterprise are now on `20.0`. Evidence base:
`docs/20-saas-19.4-delta.md`, surface inventory `docs/20-tools-touchpoints.md`,
live state `migration/20-tools-port.state.yaml`, human tracker `docs/20-tools-port-status.md`.

## Non-negotiables

1. **Agents never write the current serie.** No code, no live `module.description`, no releases on
   the serie being ported *from*. This is not "the branch is frozen" — the owner edits it freely.
2. **A current-serie bug blocks its group.** Report it, stop the group, wait for the owner's fix,
   then fetch, re-pin, re-seed, and re-run the baseline. Never implement a new-serie-only
   workaround, and never record a known-red baseline as green. The owner may **explicitly**
   accept `Gx.9` with that defect still open — record the command, leave the defect `open`,
   and do not copy an uncommitted 19.0 WIP onto the port branch. That is not a skip of the
   defect and not a 20-only fix (incident 2026-09-14, `20_c` defect 6).
3. **Latest current-serie source is always the port source.** Re-fetch and re-pin at every group
   stage; do not port from a stale pin.
4. **Compare trees, not ancestry.** `saas-x.y` branches are independent forks; a fix on the stable
   serie may be absent from the target (measured: 8638 such commits for 19.0 → saas-19.4).
5. **After the pilot, `Gx.0`–`Gx.7` is one authorized batch** (including Layer-1 and
   Layer-2). **`Gx.7` is not done without the review-DB URL.** Launch `gx8_<group>`
   in that same batch and put the login link in the reply. Do not stop after tests
   to ask “proceed with Gx.8?”. The owner walks that already-running database
   (`Gx.8`); `Gx.9` waits for that confirmation. A completed test inside the batch
   does not end the turn. Hard stops still apply: a failing check, a current-serie
   bug, a live write, a push, or a merge. The pilot stayed per-stage so the loop
   could be calibrated.
6. **Nothing enters the technical rule as fact unless source-confirmed** against a stated pin.
   Hypotheses carry their named check and stay out of porting instructions.
7. **Feature review is `en_US` until the translation stages.** `Gx.6`–`Gx.9` (and later
   group review DBs) keep `en_US` active and Mitchell Admin / the demo user on `en_US`.
   Do not `--load-language` a shipped list that omits `en_US`, and do not run
   `_demo_activate_shipped_langs` "because Gx.8 needs them". Translations are `Fx.3`
   and `Px.7` only. `Fx.3` is not green until the group's review database has every
   shipped language loaded from the refreshed `.po` files (`res.lang.action_unarchive`,
   which loads installed modules) and a non-English term on that database differs from
   English. Leave `admin` and `demo` on `en_US`; the owner switches language to check.
   **Loading a language is not the whole of `Fx.3`.** The system demo loaders
   (`odootools_demo`: custom-field types, labels and options, checklists, po appliers)
   write only the languages that are active when they run, and the review database was
   stamped in `Fx.2` with `en_US` alone. After the languages are active, `Fx.3` calls
   `res.company._demo_apply_all_translations()` (languages, every loader, then a gap
   check) and requires it to return `[]`. The `tools` `.po` files do not carry demo
   records: Odoo merges each `.po` with its `.pot` and skips entries the `.pot` does not
   list, so do not translate demo strings into the tools `.po` files. The same call is
   the weekly template refresh and the template build, so a new template is translated
   by the same path the review databases use.
   **Reading the `Fx.3` export.** `odoo i18n export -d <review db> -o <file> <module>` lists
   terms the shipped pot never had, and not all of them are for the `.po`: demo records
   (`model:<demo model>,name:`) belong to the system layer, and selection keys read out of a
   `(key, _("…"))` tuple (`ascii_50`, `hex`) are not terms. Keep the ones from views, code,
   `base.module_*` (name, summary, description) and the core models the module extends; take
   core wording from the core `.po` (`HTTP Routing`, `Module`), and keep English where core
   itself has none. An old msgid the export lost is dropped only when its text is gone from the
   source; one that moved only by whitespace keeps its msgstr. A msgid kept with a msgstr equal
   to the English source is a finding for app names (`20_2` Sticky Notes, `20_4` Password
   Manager), not for `ID` / `URL`. `ir.module.module.shortdesc` is **not** rewritten by
   `_update_translations(overwrite=True)`: a changed app name needs a per-language write on the
   review database (a fresh database takes it from the `.po`).
8. **Owner-asked fixes stay in the plan and are applied on the newest group.** When the
   owner asks to fix anything (first-click crash, missing `demo`/`demo`, checker miss),
   the successor is written into rule 22 + the checker **and** becomes a required
   `Gx.3` / `Gx.5` / `Gx.8` check on every later group. A later `Gx.3` that rediscovers
  `useState`, a bare `state.` / `panelState.`, an exact `class="…"` inherit,
  `update.bind="handleChange"`, a `t-on-*` arrow without `this.`, a formula
  `browse([False])`, or a review DB with no demo user / no 19.0 loader
  counts has failed. A green
   checker does not skip a named successor. Retro-scan already-ported groups for the
   same class in the same job (`20_5` Filters → `20_14` `rule_parent` already prefixed;
   `20_2` had no FieldFilter).
9. **JavaScript and XML are `Gx.3`, not a walk finding.** OWL templates, QWeb arches,
   security XML, JS patches, and `t-inherit` XPath are the same job as Python. A
   Python-only port with leftover `useState`, bare `panelState`, or a dead
   `class="o_calendar_sidebar"` inherit has not finished `Gx.3`.
10. **Demo is the 19.0 path for the touched modules, and the generators improve on
    the port.** `Gx.4` / `Gx.5` must produce the same records the 19.0 loaders produce
    for those modules (`env-demo-reload.sh` → `_reload_tools_demo_data` /
    `_load_demo_<family>`), not a `/tmp` seed. If `odootools_demo` cannot install
    because of a hard `depends` on an unported app, **that is a `Gx.5` defect**:
    guard or drop that depend (`_demo_module_installed` already skips missing apps)
    and run the touched-module loaders. Improving a loader (saas shell
    `env.cr.commit()`, `base.user_demo`, typed ICP, `raw`, topicality) is in-scope
    for that group. A `/tmp` walk seed does not close `Gx.5`.
11. **The program ends with working infra, not only ported modules.** The Docker
    image (`env-serie-image.sh` / `faotools/env-demo-20`), local targets
    (`demo20` / `demo20e`), `env-demo-reload.sh` / `env-demo-build.sh`,
    `odootools_demo` setup/reload, `faotools_after_init` / after_clone / post-install
    scripts, and later `7_master_infrastructure` stay first-class. A group that
    leaves demo as a one-off compose + `/tmp` seed has not finished the infra half
    of that group. Phase 4.1–4.4 tooling done is not phase 4 closed (`4.5` still
    blocked; no `demo20` DB yet).

## Branch topology

One shared scaffold commit derived from the current serie, containing **only** the top-level
technical files. Every group branch and aggregate starts from that exact commit, so ordinary merges
work and history stays usable. Do not create unrelated orphan roots.

```
<current serie>  ──►  scaffold (tech files only)
                        ├── one branch per group (e.g. 20_2 … 20_17)
                        ├── <next>_port   aggregate: pre-release ports accumulate here
                        ├── <next>_final  aggregate: what the master template runs pre-cutover
                        └── <next>.0      the published branch
```

Propagation invariant:

- Group accepted on the pre-release serie → merge into `_port`; later group changes
  re-merge there **the same turn**. `_port` is integration only. The family module
  folders on the numeric branch and on `_port` stay identical (tests, i18n, JS, XML
  included — they are the module).
- At the final-serie transition, initialize `_final` from the complete `_port`.
- Group accepted on the final serie → merge into **both** `_port` and `_final`.
- At publish, merge the group into `<next>.0` and **freeze the group branch**. Later fixes originate
  on `<next>.0` and flow to `_final`.
- Before cutover, `git diff --exit-code <next>.0 _final` must be empty.

Top-level technical files need a parity check at every aggregate merge; requirements are the union
required by the modules present.

Major serie branches are never deleted. Stale work branches go only with explicit per-branch
confirmation, and only after a content-level proof — `git branch --merged` is not that proof.

## Group order

The owner's group/order file is authoritative. At branch creation, assert every module is assigned
exactly once and matches that file. A manifest `depends` scan only **reports** ordering constraints;
it does not reorder anything.

Expect the pilot group to be unrepresentative. The 2026-09-12 claim that `20_2` and `20_c` had
no confirmed finding is false: `ir.access` already hits both, and `20_c` Gx.8 found defect 6
(portal sharing cache). The pilot still calibrates the loop; do not extrapolate effort from it.

## Per-group loop

`Gx` runs on the pre-release serie, `Fx` on the released serie, `Px` publishes.
After the pilot, `Gx.0`–`Gx.7` is one chunk; that chunk **ends with the review-DB
URL**. `Gx.8` is the owner walk of that URL; `Gx.9` is acceptance. Each stage
still has its own gate — do not mark a stage done whose check has not passed.

| Stage | Gate |
|---|---|
| `Gx.0` source seed | fetch + pin latest current-serie SHA; mechanical copy incl. `i18n/`; tree equals pin + tech files |
| `Gx.1` feature contract | reconcile live description, docs, source; map features to automated or named-manual checks |
| `Gx.2` current-serie baseline | test slice passes on the pinned current serie; a new bug here **blocks** (non-negotiable 2) |
| `Gx.3` technical port | **Python + JS + XML + security**, all in this stage. Apply every successor already in rule 22 / the checker (replay list below) before claiming green. Rule-22 transforms; **drop** the manifest serie prefix (`19.0.1.3.33` → `1.3.33`); **`check_migrate_v20.py` clean** including `manifest-version`, `js-symbol` / `js-import`, `owl-xpath` exact `class="…" position=`, and `owl-this` on `panelState` / `env` / `.bind` / getter idents / `t-on-*` arrows that call a method without `this.` / a whole-expression `t-if="projectUser"` / a bare `t-props="viewProps"`, and `js-symbol` `archInfo.openAction` / `.\w+_id[0]` / `...CharField.props` / `...FormController.props` (successor `props = props({ ...formControllerProps, extra })`) / `config.orderBy = []` (successor `list.load({ orderBy })`) / `asc: !this.asc` (19.0 sortBy-toggle leftover; successor `this.asc` on jstree notify too) / `getRecordClasses(` (successor `getCardClasses`) / `(jstreeData || [])` (keep `False`/`None`; do not coerce) / `store.emojiLoader` (successor `emojiLoader.load()`; leftover `this.store.emojiLoader.loaded` is `undefined.loaded`) / `history.addStep` (successor `history.commit()`), `python-api` `safe_eval(get_str` without `or` (successor `get_str(...) or "[]"`) / leftover `_notify_thread(..., msg_vals=)` (successor write `message.partner_ids` + `notify_skip_followers`), and `owl-xpath` `contains(@class, 'o_form_button_save')` on `web.FormView.Buttons` (successor `DialogButtons` + `buttonDialogTemplate`), `js-symbol` `record.data.id` (successor `record.resId`), `owl-this` PascalCase `prop="prop"` (successor `this.prop`; `20_7` TimeTableTable), and `python-api` `"web_icon_data": self.web_icon_data` (successor `bool(icon)`), and `js-symbol` FormController `static template` that is not `web.FormView` (successor drop it; keep `buttonTemplate` on the view — `20_15` `.knowsystem-editor` timeout), leftover `o_editable_selectors` (successor `savable_selectors`), leftover `clean_for_save_handlers` (successor `clean_for_save_processors`), and a custom HtmlBuilder with no `builderOptionsTemplate` (successor `"<module>.BuilderOptions"` — `20_15` `Missing template: "undefined"`). First-click of every designer the contract names (formula search, PDF preview, scorecard) **and** every group kanban / login dialog **and Discuss when the group patches `mail.message`** belongs here when the group owns those surfaces. A clean run that still lets a first-click compile error through is a checker bug — fix the checker **and** the group's JS/XML in the same job. Re-prefix to `20.0.x` at `Fx`, not here. |
| `Gx.4` Layer-1 demo | `tools` XML/assets for **this group's modules**, same bar as 19.0 (`34-demo-data`): no plugs, licenses, topicality, editor re-capture where the body is editor-produced. `"demo": []` is valid only when 19.0 also ships empty **and** Layer 2 owns the family. |
| `Gx.5` Layer-2 demo | **Run** the 19.0 loaders for the touched modules (`env-demo-reload.sh` / `_reload_tools_demo_data` / `_load_demo_<family>`). Grep-for-`get_param` is not a check. If `odootools_demo` cannot install, fix its depends/loaders in `system@20.0` in the same group — do not mark green. Improve the generator when the stand-in needs it (commit on saas shell, create `base.user_demo`, typed ICP, `raw`, source rows when core demo is absent). **Prove it with counts**, not a seed script: every family the 19.0 loader creates must exist (2 joint calendars with events, 3 reminders, KPI categories + periods + targets + items — whatever that group ships). Never combined with `Gx.4`. A `/tmp` seed does not close this stage. |
| `Gx.6` install matrix | fresh install per closure, with and without demo, one update, community + enterprise as applicable. **Drop every matrix database in the same batch** (`20-local-docker` Lifecycle); a leftover `*_d` / `*_nd` / `cov*` is an open `Gx.6` |
| `Gx.7` behavior | module + group tests, warning gate, browser/console smoke, each its own run. Smoke is **first-click every group menu** and the first tab of every designer/wizard the contract names (calendar, kanban, Filters), **including Refresh / Save / Export** on a forecast client action. A compile-time inherit miss or `undefined.bind` / `undefined.collapsed` is a Gx.3 miss, not a walk finding. **Then launch the review DB** (`gx8_<group>`, 19.0 loader counts, `en_US`, `admin`/`admin` + `demo`/`demo`), register it (`./local/env-review.sh keep gx8_<group> --hours 72`, compose `restart: "no"`), and **hand over the URL**. **Filestore + report.url are a gate:** `faotools_env/local/env-gx8-filestore.sh gx8_<group>` must print `GX8_FILESTORE_OK` and `GX8_REPORT_URL_OK` (fills from sibling volumes if `-i` wrote to `/tmp`; stamps `report.url=http://127.0.0.1:8069` so wkhtmltopdf can fetch CSS). Do not hand the URL while `store_fname` files are missing or print is unstyled (`20_7` Gx.8). A Gx.7 that only has test logs has not finished. |
| `Gx.8` review DB | owner walk of the URL `Gx.7` already handed over. Do not relaunch unless the walk found a defect that needs a rebuild. Cumulative base + active group, **demo reloaded the 19.0 way** for touched modules **and Gx.5 counts green**, **en_US** active and admin in English, `demo`/`demo` from `base.user_demo` / the loader (not a leftover `/tmp` user); first-click every group menu **and** the formula / PDF / scorecard / Filters surfaces the contract names; portal `get_views` on the **running** worker for generated sharing fields (see Quality gates). `/tmp` compose+seed is a walk aid only while `Gx.5` is still open — then `Gx.5` stays open and the Gx.7 URL is **not** ready. Do not hand over admin-only. |
| `Gx.9` acceptance | on owner confirmation merge to `_port` (worktree only; do not switch shared `tools`), reconcile requirements, cumulative checker smoke. **Then** `diff -rq` each group module folder on `tools-<group>` vs `tools-<next>_port` (exclude `__pycache__` / `*.pyc`). Empty diff is the gate; a mismatch is investigated and reported before the next group. Push only if asked. **Then tear the review stack down** (`./local/env-review.sh down gx8_<group>`) unless the owner asks to keep it. |

## After phase 5 — `_port` ↔ numeric module-tree parity

Phase 5 is the per-group `Gx` loops on the pre-release serie. **Before phase 6**
(final-serie re-analysis), walk **every** accepted group in the owner's order
file. For each module listed for that group, the folder on `tools-<group>` and
the same folder on `tools-<next>_port` must be identical (`__pycache__` /
`*.pyc` excluded). Tests, i18n, JS, and XML are the module — a numeric-only
`tests/` tree is a missed re-merge, not "extra". Any mismatch is investigated
and reported (what differs and why) before phase 6 starts. Repeat the same
check after every later `Gx.9` merge and after every lockstep walk fix.

`Fx` repeats the port against the released serie and adds translations
(`Fx.3`, diff-driven) and the publication drafts (`Fx.6`, `Fx.7`). The same
`Fx` pass **re-prefixes** each module's manifest `version` to `20.0.` + the tail
that `Gx.3` left unprefixed — that is the one bump `11-manifest-version` allows.

**The `Fx.6` migration release lists substantial changes only.** Its `description` is the flag
line ("The app is published to version 20.") plus one line for each change a customer would
notice: a removed or moved feature, a changed layout, a behavior fix. Nothing else goes in.
Not substantial, so never a line: an icon set change, "works as before on Odoo 20", a manifest
or access-file move, an upgrade-time key rename, anything the customer cannot see or act on.
A port with no such change ships the flag line alone. Those details belong in the internal
`notes` (Before / After), not the public text. `Fx.7` mirrors the live release row exactly:
the same lines in the TM file, every shipped language filled, and `check_release_tm.py` at
0 gaps. A line added after `Fx.6` is written to the live release and the TM file in the same
turn. Incident 2026-09-30: 20_2 and 20_c drafted 11 of 13 releases with filler lines; ten shrank to the flag line.

**`Fx.6` also rewrites the copied page wherever behavior changed.** The draft starts as a copy of
the 19.0 page, so every sentence describing changed behavior is wrong on it until edited. For each
substantial change in the release, search the draft for every place that describes the old
behavior and rewrite it in English. Check the summary, `perfect_for`, the keyword tail, each
feature `subheader` and `body`, and each screenshot `name` and `alt_name`. Unchanged sentences stay
exactly as copied, so their translations still apply. A changelog line with the page still
describing 19.0 is not a green `Fx.6`. Record every edited record and field in the ledger. A shot
whose frame no longer matches the new behavior goes on the screenshot work list. Incident
2026-10-07, 20_suite: the release said "Cc uses Odoo's own field", while the features still sold
"Add CC and BCC in the full composer".

**Every English text changed in `Fx.6` is translated, never left on the 19.0 wording.** A copied
record keeps its 19.0 translations, so an edited English sentence shows the old meaning in every
other language. `Fx.7` puts each changed source into the 20.0 TM file with all shipped languages
filled. `Px.7` applies those translations to every active language on faotools.com, not only
`ru_RU`. The gate is that no active language still shows a 19.0 sentence on a field whose English
changed.

**`Fx.1` is not green, and no `Fx` review URL is handed, without the `Gx.7` browser
first-click on the 20.0 image.** Tests, `-i`/`-u`, shell loader counts and a login probe
never construct an OWL component; on 20_2 all of them were green while every form view
in the group died on the owner's first click, twice (`env.isSmall`, `static props` —
rule 22 F12 / F13, incident `fx_review_owl_construction_20_2`). Run the checker with
`--odoo-ref origin/20.0` (kinds `owl-static-props`, `env-removed`, `owl-props-spread`,
`owl-ref`), then drive a headless browser over every group form, menu, dialog and
notebook tab the contract names (`selenium/standalone-chromium` on the
`faotools-env-local` network, BiDi console capture) and require zero `.o_error_dialog`
and zero console errors before the URL leaves the chat. The 20_2 runner is the template
(`~/env-sync/p6/selenium/smoke_20_2.py`, not source).

**`Fx.1` retargets every store and live-test link to the released serie.** A module copied
from 19.0 still sends its settings page to `apps.odoo.com/apps/modules/19.0/<tech>/` and asks the
store's Live Test for `ticket_version=19.0`. In the same `Fx.1` as the re-prefix, rewrite both to
`20.0` in views, Python and manifests (not `static/description/`, which the GitHub update writes),
then run the checker kind `serie-link` against `origin/20.0` and require zero findings. Open the
group's Settings section in the `Fx.1` browser pass and check that each add-on link names `20.0`.
Rule 22 F15.
Incident 2026-10-07: every 20.0 settings page that offers an add-on still linked the 19.0 store,
on all 21 tools 20 branches.

**`Fx.2` also stands up the 20.0 enterprise review database and hands the screenshot
overview.** Store screenshots for this serie are taken on enterprise, not community, so
each group's `Fx.2` creates `fx8_<group>e` on `faotools/env-demo-20:20.0` with the
enterprise-20.0 worktree on the addons path and `web_enterprise` installed, same demo
and loaders as the community review DB, `en_US`, `admin`/`admin` and `demo`/`demo`,
kept 72h. Then one PDF per module goes to the owner's Downloads: for every live 19.0
`module.pic` (MCP, published description of that technical name), the file name
(`reference`), the title (`name`) and the alt (`alt_name`), followed by the PNG from
the module's `static/description/`. That is the shot list. Do not capture in this step.

**Every review database installs `odootools_demo`, and so carries the baseline apps**
(`34-demo-data` **Baseline apps before any demo**): `gx8_<group>`, `fx8_<group>` and
`fx8_<group>e` alike. A review database without `sale_management`, `website_sale`,
`crm`, `stock`, `purchase`, `project`, `account`, `hr` and `contacts` shows a thinner
demo than the template the customer will get, and it cannot be handed over.

**`Fx.8` is the live Demo 20 templates, not a local install.** Push `20_final`
first. Demo 20 builds from that branch. A local cumulative database does not close
this stage, and a green local test is not a reason to skip the template.

Rebuild the Demo 20 project image from the pushed `20_final`, apply it, then install
every module of this group that the community template (`odooallapps20.odootools.com`)
does not yet have. Use `--with-demo`. Then run `action_setup_demo_template` so the
family's loaders and refreshers stamp topical demo. Every refresher the family owns
is called from `action_amend_demo_data`, not only from the one-shot loader. Then
recreate the enterprise template from that community database the same way as the
first Demo 20 pair: clone, `make_enterprise` for 20.0, swap the enterprise pointer.

`Fx.8` is green only when both live templates show the family's demo counts. A
community template that is missing the group, or an enterprise template that was
not rebuilt from it, is not done. Modules the demo program keeps uninstalled
(`partner_duplicates`) stay uninstalled after setup; the others must be installed.

`Px` publishes one group. The ledger records these stage ids, so they are enumerated here — a
resuming session must be able to map `Px.6` to concrete actions without reading a chat transcript.

Live procedures: `Px.3` is KnowSystem article 2137 (skill `33-faotools-release`), `Px.4` is article
2138 (skill `30-prepublishment-descriptions`), `Px.7` is article 2139 (skill `17-translations`,
**Live apply**). Read the article before that stage. The gates below still apply.

| Stage | Gate |
|---|---|
| `Px.1` publication readiness | re-read the live draft; reconcile it row by row against the `Fx.6` / `Fx.7` intent, including the page copy that describes changed behavior; screenshot QA passes |
| `Px.2` code publication | merge the group to the published branch, push, verify the remote tree and module list, freeze the group branch |
| `Px.3` release publication | publish the migration release (`state=3_published`) on the draft **while it is still hidden**, run `action_get_commits` in `odoo shell` (never through MCP), link only the relevant commits, no Quick GitHub Update |
| `Px.4` description publication | `action_apply_prepublishment` on the standalone draft — it promotes that record in place and **that write is what makes the page public**; verify no current-serie record changed. Leave `force_no_git` **False**. Do not set it back on |
| `Px.5` full GitHub update | the **full** update, server-side inside Odoo (`odoo shell` on the container or the UI button), never through MCP, never the quick variant. Before the button: `force_no_git` is False and `github_to_update` is True on every record in the group |
| `Px.6` GitHub output gate | fast-forward the local published branch, inspect the generated manifest / `index.html` / images commit, run the packaging and static checks |
| `Px.7` live translations | TM-first apply of description, features, `pics` and `releases` payloads through the loader, for **every active language** on faotools.com. Every field whose English changed in `Fx.6` must carry the new translation in each language; none may still show the copied 19.0 wording. Prove the live values equal the TM translations per page, caption (`name` and `alt_name`) and release, and that the HTML is closed |
| `Px.8` master sync | merge the published branch into `_final`, run the candidate full matrix, and stop; promote / redeploy master only on the next confirmation, then verify containers and public demo URLs |
| `Px.9` handoff | hand over the faotools.com page links and the exact store-ready branch and version; the owner performs the Odoo store publication |

**`Px.3` before `Px.4`: publish the release while the draft is hidden, apply second.** Read
`action_apply_prepublishment` before reordering these two. On a **standalone** draft it takes the
`else` branch and only writes `prepublish` / `pre_publish_origin_id` / `not_supported` /
`force_no_git` to False, then re-renders
(`support/module_descriptor/models/module_description.py:859-866`). So:

- the apply is **not** destructive here — the `unlink()` and child reparenting live in
  `_copy_all_values` (`:937-981`), reached **only** when `pre_publish_origin_id` is set, which is
  exactly what a major port does not have;
- the apply **is** the moment the page goes public. Publishing the release first means the page is
  complete the instant it appears. Applying first opens a window where the public page has no
  changelog row, and a failure in between leaves that window open.

Ordering the other way round was tried on 2026-09-12 and reverted the same day: the justification
("verify the destructive apply before anything is public") does not survive reading the method. The
pre-apply snapshot is still worth writing for the origin-linked case, and is not needed here.

**After `Px.4`, `force_no_git` stays False.** The apply already clears it. Do not set it back
to True to hold the GitHub cron or for any other reason. `_update_in_git` returns with no
error and no push when `force_no_git` is True or `github_to_update` is False
(`github_connector/models/module_description.py`). The button still writes
`last_github_update`, so a click looks like it ran. Before `Px.5`, on every description
in the group: `force_no_git` is False and `github_to_update` is True. Incident 2026-10-06,
`20_2`: the guard was put back after apply and the owner's GitHub Update did nothing.

### Confirmation model

Strict per-chunk confirmation through the pilot. After that, the default authorized
batch is **`Gx.0`–`Gx.7`**. Declare that sequence, then execute without asking between
stages. The batch ends with the review-DB URL. The owner reviews that already-running
database (`Gx.8`); `Gx.9` waits for that confirmation. Do not ask “proceed with
Gx.8?” after a green Gx.7. Batching never removes a hard stop — stop and report
immediately on any failing check, and before any live write, push, merge, or
master promotion.

## Quality gates

- **Warnings.** Fail on any `ERROR`/`CRITICAL`, and on any **test-window** `WARNING` attributed to a
  ported module or its demo package. Use a structured parser with logger attribution, never
  `grep WARNING` over a historic log. Core/enterprise warnings are recorded, fingerprinted, and
  non-blocking. Allowlist entries carry `(logger_prefix, message_regex, issue_url, expiry, rationale)`.
  Absolute zero warnings including core is not achievable and must not be promised.
- **The test window is narrower than the log, and "ours" is narrower than the repo.** Three scoping
  rules, each of which produced a false failure on a green pilot run before it existed:
  - the window **ends** at `Initiating shutdown`; after it the healthcheck races the closing pool
    and logs `cursor already closed` plus `Exception during request handling`;
  - **ours** is the modules **under test** plus the demo package — an all-apps clone has every
    module installed, and a third module's routing-map warning is not evidence about this group;
  - an error a passing test provokes **deliberately** must be declared (`covers_errors: true`),
    never silently tolerated. A plain allowlist row must not be able to mask `ERROR`/`CRITICAL`.
  Attribution works off a module name in the logger or message, so a core logger that names only a
  **model** cannot be attributed and will record. Read those by hand for the owning group.
- **Silent failures are the main risk.** Dead hooks, discarded field writes and string-keyed field
  names emit nothing. The static checker is the only thing that catches them; run it, read it.
- **Learned-successor replay (every `Gx.3`).** Before the checker is called green, apply
  the successors already named in rule 22 and this rule — do not wait for the owner to
  hit the same crash again. Minimum replay (grows when the owner asks to fix something):
  `ir.access`; operation letters in `crud` order (`cr` not `rc`;
  `access-op`); empty grouped ACL (`access-or` — put the domain on the CSV
  row, or write explicit `[(1, '=', 1)]`; a core sibling empty permission
  such as `sale_stock` location must AND in `_access_domain` unless Super);
  grouped `ir.rule` on
  `base.group_user` must not become a write permission (`access-grant` —
  product-group + 19.0 ACL ops; keep Internal User write when 19.0
  `ir.model.access` already granted it — `20_4` portal vaults);
  `_check_access` → `_access_domain` + `res_access_*`; typed ICP;
  `datas` → `raw` (leave `export_data` `datas` — still the export matrix);
  `Stream` from `odoo.http.stream`; `invalidate_ormcache`;
  `useState` / `reactive` → `proxy`; `t-custom-ref`; `this.` on OWL scope / bind /
  getters / `t-on-*` arrows; exact `class="…"` inherit (calendar rail vs `o_calendar_sidepanel_content`);
  New button on `web.KanbanView.Buttons`; vendored jquery + jstree off-proxy;
  `t-esc` → `t-out` in `ir.ui.view`; drop calendar `date_delay`; `@api.ormcache`;
  portal cards as `portal.entry`; `website.default_website` →
  `base.default_website` (tests included); `request.website` →
  `request.env.website`; `StaticList._replaceWith` → `list.set(ids)`;
  kanban `card_id` shells (`project.view_task_kanban` → inherit
  `project.view_task_card`; parent-bound `view-anchor`);
  `_order_field_to_sql` drop `query` (`table, field_expr, direction, nulls`;
  `_order_to_sql(table, order)` — 19.0 five-arg form dies at install,
  `20_4` Gx.6);
  leftover `_field_to_sql(table,` → `table.<field>` (`python-api` —
  `20_15` Gx.7 article LOWER);
  saas `get_current_website()` in tests needs `fallback=True`
  (`20_15` Gx.7 `/knowsystem` 403);
  19.0 `groups=base.group_portal` partner rules stay on
  `base.group_portal`, not a product group internals also get (`20_4`
  vaults OR leak);
  `t-out="title"` / `#{id}` → `this.` (`owl-this`);
  `t-if="projectUser"` → `this.projectUser` (`owl-this` —
  `20_4` Gx.8 systray);
  `archInfo.openAction` → `this.props.openAction` (`js-symbol` —
  `20_4` Gx.8 bundle card);
  `t-props="viewProps"` / `modalRef="modalRef"` → `this.` (`owl-this` —
  `20_4` Gx.8 login dialog);
  dialog Save inherit `web.FormView.DialogButtons` +
  `buttonDialogTemplate` (`owl-xpath` `contains(@class)` —
  `20_4` Gx.8 login footer);
  `record.data.<m2o>[0]` → `.id` (`js-symbol` —
  `20_4` Gx.8 eye/copy `Invalid falsy real id`);
  `static props = { ...CharField.props }` → instance
  `props = props({ ...charFieldProps, extra })` (`js-symbol` —
  `20_4` Gx.8 login regenerate / Enter);
  `static props = { ...FormController.props }` → instance
  `props = props({ ...formControllerProps, extra })` (`js-symbol` —
  `20_11` Gx.8 Refresh / Save / Export `refreshReport is not a function`);
  writing `config.orderBy` then `sortBy(fieldName)` →
  `list.load({ orderBy })` (`js-symbol` `config.orderBy = []` —
  `20_4` Gx.8 Sort by cleared to name);
  leftover `asc: !this.asc` on jstree notify → `this.asc`
  (`js-symbol` — `20_4` Gx.9 Bugbot after Sort by used `this.asc`);
  `getRecordClasses()` → `getCardClasses()` (`js-symbol` —
  `20_4` Gx.8 PWM / `20_14` File Manager selected checkbox);
  `safe_eval(get_str(...))` without `or` → `get_str(...) or "[]"`
  (`python-api` — `20_4` Gx.8 portal vault 500 on stored empty);
  `(jstreeData || [])` → copy only arrays, keep `False`/`None`
  (`js-symbol` — `20_4` Gx.8 Portal Vaults header with the
  setting off). File Manager `NodeJsTree` already keeps the
  sentinel;
  `RecipientsInput` on `mail.Chatter` → inherit
  `mail.ChatterComposer`, handler on `Composer`,
  `recipient_type: "to"`, `store.self` not `self_partner`
  (`owl-xpath` / `js-symbol` — `20_suite` Gx.3);
  `res_access_*` `compute=lambda` / Field `depends="name"` →
  named `_compute_res_access_<op>` + `@api.depends`
  (`python-api` — `20_suite` Gx.6 field `'m'`);
  `this.store.emojiLoader.loaded` → `emojiLoader.load()`
  (`js-symbol` — `20_suite` Gx.8 Discuss `undefined.loaded`);
  leftover `_notify_thread(..., msg_vals=)` → write
  `message.partner_ids` then
  `notify_skip_followers` (`python-api` — `20_suite` Gx.8
  Route `ValueError`);
  `history.addStep` → `history.commit()` (`js-symbol` —
  `20_suite` Gx.8 Cite `addStep is not a function`);
  `"web_icon_data": self.web_icon_data` → `bool(icon)`
  (`python-api` — `20_7` Gx.8 Menu Management
  `UnicodeDecodeError` 0x89; saas Binary is BinaryValue,
  jsonrpc `.content.decode()` dies on PNG);
  `record.data.id` → `record.resId` (`js-symbol` —
  `20_7` Gx.8 timetable open `Invalid falsy real id`);
  PascalCase child `prop="prop"` → `this.prop`
  (`owl-this` — `20_7` `<TimeTableTable
  timeTableId="timeTableId"/>`; t-as aliases stay bare);
  FormController `static template` that is not
  `web.FormView` → drop it (`js-symbol` —
  `20_15` Gx.7 `.knowsystem-editor` timeout;
  keep `buttonTemplate` on the view);
  leftover `htmlFieldProps` (`js-symbol` —
  `20_15` KnowSystemHtml);
  inherit-only `<t t-inherit>` with no `t-name`
  still scanned for `owl-this` (`20_15` multilang
  `state.uniqueId` → `this.state.uniqueId`);
  leftover `htmlFieldProps` / instance
  `props = props({ ...htmlFieldProps, extra })` →
  `static props = { ...HtmlField.props, extra }`
  (`js-symbol` — `20_15` KnowSystemHtml
  `getNoMoreCommit is not a function`; mass_mailing
  successor);
  inner `t-set` of `size` / `mobileSize` on a snippet
  `t-call` → `t-call` attributes (`qweb-tcall` —
  `20_15` Gx.7 `10 - size` None during
  `html_builder` palette render);
  inner `t-set` of `service` / `entries` / `card_href` /
  `card_records` / `_classes` / `no_breadcrumbs` /
  `additional_title` → `t-call` attributes or sibling
  `t-set` (`qweb-tcall` — `20_16` Gx.7 Appointments
  `KeyError: service`, empty card links, missing
  `#ba_functional_buttons`);
  Char `update_field_translations` in `lang=en_US` →
  `record.write({fname: {"en_US": current, **mapping}})`
  then `flush_recordset` (`20_16` Gx.7 stepper stays
  English — saas write-back drops other JSON keys;
  dict write is cache-only until flush; `cr.commit()`
  is forbidden; `prefetch_langs=True` dies
  `StoredTranslations`); leftover QWeb
  `website.ba_stepN` → `website._ba_frontend_text`
  / `_ba_step_labels()` (`qweb-tcall` — `20_16`
  HttpCase page chrome was ru, stepper/`<title>`
  stayed English after flush; maps when stored
  lang equals English source);
  leftover `o_editable_selectors` →
  `savable_selectors` (`js-symbol` —
  `20_15` Gx.7 iframe never contenteditable;
  saas requires `.o_savable`);
  leftover `clean_for_save_handlers` →
  `clean_for_save_processors` (`js-symbol` —
  `20_15` setup / customize plugins);
  custom HtmlBuilder without
  `builderOptionsTemplate` →
  `"<module>.BuilderOptions"` plus
  `builderOptionsRegistry` (`js-symbol` —
  `20_15` `OwlError Missing template: "undefined"`;
  mass_mailing successor);
  `type="base64" file=` in data/demo XML →
  `type="bytes"` (`data-base64` — saas
  `convert.py` DeprecationWarning that the gate
  blames on us; on `ir.attachment.raw` it is also
  the wrong payload);
  a 19.0 ACL + `ir.rule` pair folded into **both**
  `ir.access.csv` and a converted `security.xml` →
  keep the CSV only (`20_15`: 14 duplicate
  public/portal permissions; `Domain.OR` of two
  identical domains hides it, and no checker kind
  sees a redundant permission — read the pair);
  a `t-set` body moved onto a `t-call` attribute →
  `name.translate="…"`, never `name="'…'"`
  (`20_15`: bare expressions leave the `.pot` and
  already-translated terms revert to English);
  leftover `...IntegerField.props` →
  `props = props({ ...integerFieldProps, extra })`
  (`js-symbol` — `20_15` likes showed a bare number);
  leftover `resources.builder_options` on a
  `website-plugins`-only file → `website-options.add`
  plus inherit `website.BuilderOptions` at
  `page_options_hook` (`js-symbol` — `20_15` Customize
  empty; switchable inherit views need
  `BuilderCheckbox action="'websiteConfig'"`);
  docs / website `t-field` that only matches
  `editor_type == 'website_editor'` → also
  `backend_editor` and `html` (`20_15` in-page
  article edit);
  leftover `resource_calendar_id.tz` / a `tz` field
  on `resource.calendar` / leftover `timezone(self.tz)`
  on a calendar method → `resource.tz` or
  context/user/`UTC` (`field-lit` — `20_16` Layer-1
  demo died `Invalid field 'tz'`; Gx.5
  `_ba_attendance_intervals` then died
  `AttributeError`; saas attendance also dropped
  `name`);
  leftover `base64.b64encode(...)` into Image/Binary
  → `BinaryBytes(raw)` (`python-api` — `20_16` Gx.5
  car-rent variant `TypeError: use BinaryValue
  instead of bytes`).
  A group that still has any of these in *its* tree
  has not finished `Gx.3`.
- **First-click OWL.** Before calling `Gx.8` ready, open every group menu and the first tab of
  every designer the contract names, **including formula search, PDF preview, and the
  scorecard**. `cannot be located in element tree`, `undefined.bind`,
  `undefined.collapsed`, and `Invalid handler expression` / `Invalid falsy real id`
  are Gx.3 / checker misses (incident 2026-09-16, `20_5` Gx.8: `o_calendar_sidebar`,
  `panelState`, `update.bind="handleChange"`, then formula
  `_onSearchNavigation` without `this.` + `browse([False])`;
  `20_4` Gx.8: `t-if="projectUser"` hid the Task Numbers systray;
  then Password Manager `archInfo.openAction` / `t-props="viewProps"`;
  then login Save / `bundle_id[0]` / leftover
  `...CharField.props`; then Sort by `config.orderBy` +
  `sortBy` cleared the list;   then selected cards had no
  checkbox because leftover `getRecordClasses` never ran;
  then portal vault login 500 because `safe_eval(get_str(..., "[]"))`
  of a stored empty ICP;
  then Portal Vaults header stayed on All Passwords because
  `(jstreeData || [])` made `False` truthy and admin `canUpdate`
  painted the section;
  then Discuss died `undefined.loaded` because leftover
  `this.store.emojiLoader` after the `loadEmoji` import rewrite
  (`20_suite` Gx.8);
  then Route died `msg_vals` and Cite died `history.addStep`
  (`20_suite` Gx.8 — leftover kwargs / leftover plugin
  method; Gx.7 never opened those dialogs);
  then forecast Refresh / Save / Export died
  `refreshReport is not a function` because leftover
  `...FormController.props` (`20_11` Gx.8 — Gx.7 never
  clicked those buttons);
  then opening a timetable died `Invalid falsy real id`
  because leftover `record.data.id` and
  `timeTableId="timeTableId"` (`20_7` Gx.8);
  then KnowSystem backend editor save died
  `OwlError Missing template: "undefined"` because
  leftover HtmlBuilder never set
  `builderOptionsTemplate`, then waited 30s for
  contenteditable because leftover
  `o_editable_selectors` never added `.o_savable`
  (`20_15` Gx.7)). Do not excuse them
  with a green checker — extend the checker in the same job.
- **Demo parity (touched modules).** `Gx.5` / `Gx.8` prove the 19.0 loaders ran: `demo`/`demo`
  authenticates (`base.user_demo`), and the family's **19.0 record counts** exist (2
  joint calendars with events, 3 `total.notify`, KPI categories + periods + targets
  + items — whatever that group's 19.0 loader creates). Invented walk rows in
  `/tmp/*_seed.py` are not that proof. `Gx.8` is not ready while `Gx.5` is open.
  If the generator is wrong on saas-19.4, fix the generator in the same group.
  **`-i` must write the filestore onto the same volume the review compose
  mounts** (`--data-dir=/var/lib/odoo` → `~/env-sync/filestore/<db>`). A
  throwaway `--data-dir=/tmp/odoo-*` leaves `ir.attachment` rows with no
  files — partner / product images are missing even though demo loaded
  (`20_suite` Gx.8: 502 `store_fname`, 17 files). Pass **`--with-demo`**
  (`env-demo-build.sh`); `--without-demo=` skips core demo (5 partners,
  no avatars). Prove `$data_dir/filestore/$db/<store_fname>` exists
  **and** `res.partner` is more than the 5 base rows before handing
  the URL.   **Every Gx.7** runs `faotools_env/local/env-gx8-filestore.sh <db>`
  and keeps the URL back until it prints `GX8_FILESTORE_OK`
  **and** `GX8_REPORT_URL_OK` (`report.url=http://127.0.0.1:8069`
  so wkhtmltopdf can fetch `/web/assets` — host
  `web.base.url` `:18210` is `ConnectionRefused` inside
  the container; `20_7` Work schedule print). A stamp shell must be `docker run -i` or saas exits before
  the heredoc.
- **Infra progress.** A group that needs Layer-2 demo must leave `odootools_demo`
  installable on that stand-in (or a documented, committed slim path — not `/tmp`).
  `env-demo-reload.sh` / `env-demo-build.sh` / `faotools_after_init` / after_clone stay
  on the program path. Do not call phase 4 closed while `4.5` is blocked or there is
  no `demo20` database.
- **Portal sharing / generated fields.** `Gx.8` must HTTP `get_views` as a **portal** user on the
  **running** worker and compare arch vs `fields_get` for every generated `x_oz_*` (or other
  custom column) on sharing forms. A fresh `odoo shell` is a new process cache and is not that
  check. A container restart that makes the form open is not a fix. Do not 20-only workaround;
  invalidate on 19.0 (`task_custom_fields` / `project.task._portal_accessible_fields`
  `@ormcache(cache='stable')` at both refs). Incident 2026-09-14, `20_c` Gx.8, defect 6.
- **Browser tests must prove they ran.** A green suite whose browser tests skipped is not acceptance.
- **Tests clone.** Never mutate the served review database.
- **Review language is `en_US`.** `res.lang.active` defaults to False; `install_lang`
  activates only the **first** `--load-language` code (or `en_US` when unset) and that
  becomes `ir.default` partner lang. `SHIPPED_LANGS` / `SHIPPED_DEMO_LANGS` start with
  `ru_RU` and exclude `en_US`, so using that list as `--load-language` leaves English
  inactive and Preferences hides it (incident 2026-09-14, `20_2` Gx.8). A Gx.7 test
  that reads `ru_RU` may activate **that** language after `en_US`; it is not a reason
  to ship a Russian review DB.

## Durable state

The ledger `migration/20-tools-port.state.yaml` is the contract that lets a **fresh session with no
memory** resume safely. It records, per group: stage and status, the pinned current-serie/target/
system SHAs, test artifact paths, live record ids, translation fingerprints, and locks.

Rules:

- Update the ledger at every stage boundary, in the same chunk as the work.
- A new session reads the ledger **and** the live records, then refuses an ambiguous next step
  instead of guessing.
- Git branch tips are not state. They cannot express "stage `Gx.7`, green, on these SHAs".
- Never mark a stage done whose gate did not pass. Blocked is a status, not a skip.

## Live publication

- Draft the new-serie description as a **standalone prepublication**: copy of the published current
  serie with the major version switched, **no** origin pointer, `prepublish=True` +
  `force_no_git=True`, docs cleared, no carried videos. Applying it promotes that same record in
  place, so release links stay valid.
- **`not_supported=True` is banned** on any record intended for publication: it switches the GitHub
  writer to the archive branch, which deletes the store images and rewrites the author.
- The GitHub update runs **server-side inside Odoo** with the stored token, never through MCP, and
  never the "quick" variant. Do not build a parallel plain-git path.
- Snapshot before any destructive apply; on partial failure treat it as an incident rather than
  retrying blindly.
- Raise the public "topical version" ceiling only when the owner says so — a half-populated new
  serie storefront is worse than none.

## Living rules

A port that reveals a new technical fact does **not** pause by default. Decide the fix, apply it
**on the current group**, prove it on the stand-in (install or the check that failed), then write
the fact into `ai_rules` rule 22 **and** `tools/check_migrate_v20.py` in the same job so the
**newest** group's `Gx.3` applies it. The same for a demo-generator or infra fix: write it into
`34-demo-data` / `env-demo-*` / `faotools_after_init` and run it, do not leave a `/tmp` copy as
the source of truth. Pause only when:

- the issue is a **current-serie (19.0) defect** that must be fixed there before the group
  continues (non-negotiable 2);
- there is a **real choice** (two viable successors, a behaviour trade-off). No choice → do
  not ask.

A process correction updates this rule and the tracker before the affected stage is marked done.
Every rule-22 entry carries its evidence and tested SHA; an entry without evidence does not
belong there.

## Cutover lessons (2026-10-16)

- **Candidate, then promote.** `action_build_candidate` refuses to start when
  `candidate_state` is `building` or `testing`. Green means `state==done`,
  `tests_ok`, `tests_total>0`, `gate_errors==0`, `gate_warnings==0`, and
  `browser_ok is True`. `action_promote_candidate` copies
  `candidate_image_tag` onto `image_tag`, sets `candidate_state` back to
  `none`, and queues the stack apply. It does **not** clear
  `needs_project_image`. A gated build leaves that flag True; after promote,
  clear it (`_clear_pending_action("needs_project_image")`) or the next weekly
  backup enqueue dies in `_assert_no_pending_apply`.
- **The Demo 20 image carries a browser.** `WebSuite` skips when Chrome or
  `websocket-client` is missing, and the log gate counts that skip as a
  warning. The project Dockerfile installs both only when the slug is
  `demo-20`. A local one-off uses the Chrome overlay and `--shm-size=1g`.
- **Expected ERROR lines are silenced in the test.** The log gate counts
  WARNING/ERROR/CRITICAL whose logger starts with `odoo.addons.<tested
  module>`. It does not skip an ERROR a passing test writes on purpose.
  Put `@mute_logger` on that test. Do not weaken the gate.
- **Demo bookings stay inside one company.** Appointment loaders pick a
  customer whose company is empty or equal to the resource's company, and a
  resource that is free for that slot. A customer of another company makes
  `_create_reservation` log the overlap warning.

## 37-linkedin-publications

_LinkedIn company-page posts that draw attention to one faOtools app feature_

# LinkedIn company-page publications

The procedure is KnowSystem article 2136 in section `AI` on faotools.com. The title is for people. Read the article before any `linkedin.post` write, short URL, or upload. Git history of this file is not the procedure. This id lookup belongs only to this pointer.

https://faotools.com/odoo/knowsystem/2136

1. MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). Inspect the tool schema first (`21-faotools-mcp`).
2. Read `knowsystem.article` 2136.
3. Stop unless that record is active and its section is `AI` (id 157).
4. Read `description` and follow it.

If the host MCP tool returns needs auth or Unauthorized, do not stop and do not ask the owner to log in. Connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Stop only when that path also fails to make a working call, or the read does not return one active record in section `AI`. Do not reconstruct the steps. The result is a draft `linkedin.post`. The owner publishes. The agent never logs into LinkedIn.

## 38-module-docs

_Prepare or update the public documentation of a faOtools app or app family on faotools.com /docs, including phrases like документация, docs, подготовь документацию, обнови документацию_

# faOtools app documentation

Trigger: документация, docs, подготовь документацию, обнови документацию, for an app or an app family.

The procedure is KnowSystem article 2142 in section `AI` on faotools.com. The title is for people. Read the article before any write on faotools.com. Git history of this file is not the procedure. This id lookup belongs only to this pointer.

https://faotools.com/odoo/knowsystem/2142

1. MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). Inspect the tool schema first (`21-faotools-mcp`).
2. Read `knowsystem.article` 2142.
3. Stop unless that record is active and its section is `AI` (id 157). The article is not published on the website. It is internal on purpose, so that is not a reason to stop.
4. Read `description` and follow it.

If the host MCP tool returns needs auth or Unauthorized, do not stop and do not ask the owner to log in. Connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Stop only when that path also fails to make a working call, or the read does not return one active record in section `AI`. Do not reconstruct the steps. The bans in `18-xml-translate-html` and `33-release-gates` still apply; they are enough to refuse a write.

## Module-to-section table

The article reads this table. Built from the 20.0 `tools` tree and live faotools.com ids on 2026-11-26.

- A family is a main module and the modules whose 20.0 `module.description` has it in `extension_toapp_id`. The family has one documentation: the section of the main module.
- The number after a module is its 20.0 `module.description` id.
- `new` means the section or KnowSystem subsection does not exist yet. `?` means the human picks the `/docs` category when that app's docs start.
- An extension subsection marked `new under <id>` goes inside the main module's subsection. Cloud Storage keeps its family section 94 Clouds, with one subsection per connector.
- Live `documentation_url` values are not kept here. The article reads them on every run.
- If an app is not in the table, stop and ask the human.

| Main module | Extensions → KnowSystem subsection | Docs section | `/docs` category | KnowSystem subsection |
|---|---|---|---|---|
| `mail_activity_notification` 1343 | — | new | ? | new |
| `activities_todo` 1310 | — | new | ? | new |
| `odoo_menu_management` 1284 | — | 34 Advanced Menu Management | 3 Extra utilities | 65 Extra utilities > 150 Advanced Menu Management |
| `variant_price_system` 1338 | — | new | ? | new |
| `cloud_base` 1267 | `amazon_s3_odoo` 1273 → new under 94 Clouds; `box_odoo` 1269 → new under 94 Clouds; `cloud_base_documents` 1270 → new under 94 Clouds; `dropbox` 1275 → 94 Clouds > 99 DropBox; `google_drive_odoo` 1272 → 94 Clouds > 96 Google Drive; `nas_odoo` 1274 → new under 94 Clouds; `onedrive` 1271 → 94 Clouds > 97 OneDrive / SharePoint; `owncloud_odoo` 1268 → 94 Clouds > 98 OwnCloud / NextCloud | 18 Cloud Storage Solutions | 5 Management apps | 94 Clouds > 95 Cloud Storage Solutions |
| `opportunity_custom_fields` 1256 | `opportunity_custom_fields_website` 1258 → new, inside the main module's new subsection | new | ? | new |
| `partner_color_codes` 1311 | — | 2 Contacts color coding | 3 Extra utilities | 65 Extra utilities > 48 Contacts color coding |
| `partner_duplicates` 1301 | — | 12 Contacts Duplicates Real Time Search | 7 Sales apps | 86 Sales Apps > 82 Contacts Duplicates Real Time Search |
| `crm_checklist` 1306 | — | 14 CRM Check List and Approval Process | 7 Sales apps | 86 Sales Apps > 85 CRM Check List and Approval Process |
| `notification_crm` 1344 | — | new | ? | new |
| `crm_duplicates` 1300 | — | 13 CRM Duplicates Real Time Search | 7 Sales apps | 86 Sales Apps > 83 CRM Duplicates Real Time Search |
| `partner_custom_fields` 1257 | — | new | ? | new |
| `product_custom_fields` 1259 | `product_custom_fields_website_sale` 1260 → new, inside the main module's new subsection | new | ? | new |
| `project_custom_fields` 1261 | — | new | ? | new |
| `task_custom_fields` 1262 | — | new | ? | new |
| `custom_fields` 1255 | — | new | ? | new |
| `customer_scoring` 1312 | — | new | ? | new |
| `complementary_employee_data` 1250 | — | 7 Partners contact full details | 3 Extra utilities | 65 Extra utilities > 69 Partners contacts full details |
| `itlibertas_timesheet` 1285 | `itlibertas_timesheet_gantt` 1283 → new under 148 Flexible Timetables and Shifts | 33 Flexible Timetables and Shifts | 5 Management apps | 73 Management Apps > 148 Flexible Timetables and Shifts |
| `header_clock` 1313 | — | new | ? | new |
| `joint_calendar` 1276 | `joint_calendar_gantt` 1277 → new under 105 Joint Calendar | 23 Joint Calendar | 3 Extra utilities | 65 Extra utilities > 105 Joint Calendar |
| `knowsystem` 1316 | `knowsystem_custom_fields` 1320 → new under 79 Knowsystem; `knowsystem_website_custom_fields` 1321 → new under 79 Knowsystem; `knowsystem_eshop` 1319 → new under 79 Knowsystem; `knowsystem_multilang` 1322 → new under 79 Knowsystem; `knowsystem_website` 1318 → new under 79 Knowsystem; `documentation_builder` 1317 → new under 79 Knowsystem | 10 KnowSystem: Knowledge Base System | 5 Management apps | 73 Management Apps > 79 Knowsystem |
| `kpi_scorecard` 1279 | — | 16 KPI Balanced Scorecard | 5 Management apps | 73 Management Apps > 88 KPI |
| `mail_manual_routing` 1289 | — | 17 Lost Messages Routing | 4 Messaging apps | 66 Messaging apps > 90 Lost Messages Routing |
| `low_sales_report` 1280 | — | new | ? | new |
| `product_add_suppliers` 1339 | — | new | ? | new |
| `message_citing` 1290 | — | new | ? | new |
| `message_edit` 1286 | — | 5 Message/note editing | 4 Messaging apps | 66 Messaging apps > 67 Message note editing |
| `odoo_email_from` 1291 | `odoo_email_from_accounting` 1292 → new, inside the main module's new subsection | new | ? | new |
| `email_suite` 1295 | `email_suite_accounting` 1296 → new, inside the main module's new subsection | new | ? | new |
| `odoo_typo_reporter` 1304 | — | new | ? | new |
| `complementary_lead_data` 1252 | — | 7 Partners contact full details | 3 Extra utilities | 65 Extra utilities > 69 Partners contacts full details |
| `res_partner_completeness` 1314 | — | new | ? | new |
| `complementary_contact_data` 1254 | — | 7 Partners contact full details | 3 Extra utilities | 65 Extra utilities > 69 Partners contacts full details |
| `odoo_password_manager` 1263 | `odoo_password_manager_custom_fields` 1264 → new under 72 Password manager | 9 Password manager | 5 Management apps | 73 Management Apps > 72 Password manager |
| `internal_thread` 1287 | `internal_thread_accounting` 1288 → new under 68 Private thread | 6 Private thread | 4 Messaging apps | 66 Messaging apps > 68 Private thread |
| `product_dynamic_code` 1299 | — | new | ? | new |
| `product_management` 1332 | `product_management_accounting` 1333 → new under 103 Product Management Interface; `product_management_website_sale` 1334 → new under 103 Product Management Interface; `product_management_purchase` 1335 → new under 103 Product Management Interface; `product_management_stock` 1336 → new under 103 Product Management Interface | 27 Product Management Interface | 7 Sales apps | 86 Sales Apps > 103 Product Management Interface |
| `purchase_order_checklist` 1308 | — | new | ? | new |
| `recurrent_activities` 1309 | — | new | ? | new |
| `total_notify` 1278 | — | 32 Periodic Reporting and Reminders | 3 Extra utilities | 65 Extra utilities > 147 Periodic Reporting and Reminders |
| `sale_order_checklist` 1307 | — | 15 Sale Order Approval Check Lists | 7 Sales apps | 86 Sales Apps > 87 Sale Order Approval Check Lists |
| `sales_forecast_by_periods` 1281 | — | 35 Sales Trends and Forecast | 7 Sales apps | 86 Sales Apps > 151 Sales Trends and Forecast |
| `security_user_roles` 1265 | — | 31 Security User Roles | 3 Extra utilities | 65 Extra utilities > 144 Security User Roles |
| `mail_composer_on_send_message` 1342 | — | new | ? | new |
| `smart_warnings` 1253 | — | 3 Smart Alerts | 3 Extra utilities | 65 Extra utilities > 57 Smart alerts |
| `sticky_notes` 1251 | — | 4 Sticky notes | 3 Extra utilities | 65 Extra utilities > 63 Sticky notes |
| `stock_qty_forecast` 1282 | — | 38 Stock Demand Trends and Forecast | 9 Inventory apps | 100 Inventory apps > 152 Stock Demand Trends and Forecast |
| `stock_limitation` 1298 | — | 25 Stock Access Rules | 9 Inventory apps | 100 Inventory apps > 101 Stocks Access Rules |
| `product_stock_balance` 1297 | — | 26 Stocks by Locations | 9 Inventory apps | 100 Inventory apps > 102 Stocks by Locations |
| `task_numbers` 1266 | — | new | ? | new |
| `task_checklist` 1305 | — | 37 Task Check List and Approval Process | 3 Extra utilities | 86 Sales Apps > 154 Task Check List and Approval Process |
| `notification_project` 1345 | — | new | ? | new |
| `business_appointment` 1323 | `business_appointment_custom_fields` 1324 → new under 142 Universal Appointments; `business_appointment_custom_fields_website` 1325 → new under 142 Universal Appointments; `business_appointment_gantt` 1326 → new under 142 Universal Appointments; `business_appointment_hr` 1327 → new under 142 Universal Appointments; `business_appointment_website` 1330 → new under 142 Universal Appointments; `business_appointment_sale` 1328 → new under 142 Universal Appointments; `business_appointment_time_tracking` 1329 → new under 142 Universal Appointments; `business_appointment_website_sale` 1331 → new under 142 Universal Appointments | 30 Universal Appointments and Time Reservations | 5 Management apps | 73 Management Apps > 142 Universal Appointments |
| `website_url_translations` 1302 | — | 28 URL Transliterations for Website Pages | 3 Extra utilities | 65 Extra utilities > 111 URL Transliterations for Website Pages |
| `vendor_product_management` 1337 | — | new | ? | new |
| `vendor_portal_management` 1340 | — | new | ? | new |
| `vendor_scoring` 1315 | — | new | ? | new |
| `short_urls` 1303 | — | 29 Website URL Shortener | 3 Extra utilities | 65 Extra utilities > 114 Website URL Shortener |

Not in the table:

- Sections 19 Google Drive, 20 OneDrive / SharePoint, 21 OwnCloud / NextCloud, and 22 Dropbox are archived, in the archived category 8. They are sources for the connector articles only.
- Sections 8 No auto subscription, 24 Limited Access to Products, and 36 Messages: Schedule Send Option belong to apps that are not in the 20.0 tree.

## 39-module-videos

_Plan, script, record, and publish the videos of a faOtools app on faotools.com (youtube.reference) - pieces, overview, setup videos, YouTube texts - including phrases like видео, ролик, сценарий, обзор_

# faOtools app videos

Trigger: видео, ролик, сценарий, обзор, for an app or an app family.

The procedure is KnowSystem article 2143 in section `AI` on faotools.com. The title is for people. Read the article before any `youtube.reference` write. Git history of this file is not the procedure. This id lookup belongs only to this pointer.

https://faotools.com/odoo/knowsystem/2143

1. MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). Inspect the tool schema first (`21-faotools-mcp`).
2. Read `knowsystem.article` 2143.
3. Stop unless that record is active and its section is `AI` (id 157). The article is not published on the website. It is internal on purpose, so that is not a reason to stop.
4. Read `description` and follow it.

If the host MCP tool returns needs auth or Unauthorized, do not stop and do not ask the owner to log in. Connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Stop only when that path also fails to make a working call, or the read does not return one active record in section `AI`. Do not reconstruct the steps. The bans in `33-release-gates` still apply. The cover design is the skill `32-video-cover-design`.
