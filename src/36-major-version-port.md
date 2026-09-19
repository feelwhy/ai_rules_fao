---
id: 36-major-version-port
description: Process for porting the tools apps to a new major Odoo serie (branches, gates, ledger, publish)
apply: agent
---

# Major-version port (tools apps)

How a whole serie of faOtools apps moves to a new major Odoo version: branch topology, per-group
gates, durable state, and the publish loop. The **technical** transforms live in `ai_rules`
`22-migrate-v19-to-v20` (one rule per serie pair). This rule is the process around them.

Current program: 19.0 → 20.0 via `saas-19.4`. Evidence base:
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
   and `Px.7` only.
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

- Group accepted on the pre-release serie → merge into `_port`; later group changes re-merge there.
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
| `Gx.3` technical port | **Python + JS + XML + security**, all in this stage. Apply every successor already in rule 22 / the checker (replay list below) before claiming green. Rule-22 transforms; **drop** the manifest serie prefix (`19.0.1.3.33` → `1.3.33`); **`check_migrate_v20.py` clean** including `manifest-version`, `js-symbol` / `js-import`, `owl-xpath` exact `class="…" position=`, and `owl-this` on `panelState` / `env` / `.bind` / getter idents / `t-on-*` arrows that call a method without `this.` / a whole-expression `t-if="projectUser"` / a bare `t-props="viewProps"`, and `js-symbol` `archInfo.openAction` / `.\w+_id[0]` / `...CharField.props` / `...FormController.props` (successor `props = props({ ...formControllerProps, extra })`) / `config.orderBy = []` (successor `list.load({ orderBy })`) / `asc: !this.asc` (19.0 sortBy-toggle leftover; successor `this.asc` on jstree notify too) / `getRecordClasses(` (successor `getCardClasses`) / `(jstreeData || [])` (keep `False`/`None`; do not coerce) / `store.emojiLoader` (successor `emojiLoader.load()`; leftover `this.store.emojiLoader.loaded` is `undefined.loaded`) / `history.addStep` (successor `history.commit()`), `python-api` `safe_eval(get_str` without `or` (successor `get_str(...) or "[]"`) / leftover `_notify_thread(..., msg_vals=)` (successor write `message.partner_ids` + `notify_skip_followers`), and `owl-xpath` `contains(@class, 'o_form_button_save')` on `web.FormView.Buttons` (successor `DialogButtons` + `buttonDialogTemplate`), `js-symbol` `record.data.id` (successor `record.resId`), `owl-this` PascalCase `prop="prop"` (successor `this.prop`; `20_7` TimeTableTable), and `python-api` `"web_icon_data": self.web_icon_data` (successor `bool(icon)`). First-click of every designer the contract names (formula search, PDF preview, scorecard) **and** every group kanban / login dialog **and Discuss when the group patches `mail.message`** belongs here when the group owns those surfaces. A clean run that still lets a first-click compile error through is a checker bug — fix the checker **and** the group's JS/XML in the same job. Re-prefix to `20.0.x` at `Fx`, not here. |
| `Gx.4` Layer-1 demo | `tools` XML/assets for **this group's modules**, same bar as 19.0 (`34-demo-data`): no plugs, licenses, topicality, editor re-capture where the body is editor-produced. `"demo": []` is valid only when 19.0 also ships empty **and** Layer 2 owns the family. |
| `Gx.5` Layer-2 demo | **Run** the 19.0 loaders for the touched modules (`env-demo-reload.sh` / `_reload_tools_demo_data` / `_load_demo_<family>`). Grep-for-`get_param` is not a check. If `odootools_demo` cannot install, fix its depends/loaders in `system@20.0` in the same group — do not mark green. Improve the generator when the stand-in needs it (commit on saas shell, create `base.user_demo`, typed ICP, `raw`, source rows when core demo is absent). **Prove it with counts**, not a seed script: every family the 19.0 loader creates must exist (2 joint calendars with events, 3 reminders, KPI categories + periods + targets + items — whatever that group ships). Never combined with `Gx.4`. A `/tmp` seed does not close this stage. |
| `Gx.6` install matrix | fresh install per closure, with and without demo, one update, community + enterprise as applicable |
| `Gx.7` behavior | module + group tests, warning gate, browser/console smoke, each its own run. Smoke is **first-click every group menu** and the first tab of every designer/wizard the contract names (calendar, kanban, Filters), **including Refresh / Save / Export** on a forecast client action. A compile-time inherit miss or `undefined.bind` / `undefined.collapsed` is a Gx.3 miss, not a walk finding. **Then launch the review DB** (`gx8_<group>`, 19.0 loader counts, `en_US`, `admin`/`admin` + `demo`/`demo`) and **hand over the URL**. **Filestore + report.url are a gate:** `faotools_env/local/env-gx8-filestore.sh gx8_<group>` must print `GX8_FILESTORE_OK` and `GX8_REPORT_URL_OK` (fills from sibling volumes if `-i` wrote to `/tmp`; stamps `report.url=http://127.0.0.1:8069` so wkhtmltopdf can fetch CSS). Do not hand the URL while `store_fname` files are missing or print is unstyled (`20_7` Gx.8). A Gx.7 that only has test logs has not finished. |
| `Gx.8` review DB | owner walk of the URL `Gx.7` already handed over. Do not relaunch unless the walk found a defect that needs a rebuild. Cumulative base + active group, **demo reloaded the 19.0 way** for touched modules **and Gx.5 counts green**, **en_US** active and admin in English, `demo`/`demo` from `base.user_demo` / the loader (not a leftover `/tmp` user); first-click every group menu **and** the formula / PDF / scorecard / Filters surfaces the contract names; portal `get_views` on the **running** worker for generated sharing fields (see Quality gates). `/tmp` compose+seed is a walk aid only while `Gx.5` is still open — then `Gx.5` stays open and the Gx.7 URL is **not** ready. Do not hand over admin-only. |
| `Gx.9` acceptance | on owner confirmation merge to `_port` (worktree only; do not switch shared `tools`), reconcile requirements, cumulative checker smoke. Push only if asked. |

`Fx` repeats the port against the released serie and adds translations
(`Fx.3`, diff-driven) and the publication drafts (`Fx.6`, `Fx.7`). The same
`Fx` pass **re-prefixes** each module's manifest `version` to `20.0.` + the tail
that `Gx.3` left unprefixed — that is the one bump `11-manifest-version` allows.

`Px` publishes one group. The ledger records these stage ids, so they are enumerated here — a
resuming session must be able to map `Px.6` to concrete actions without reading a chat transcript.

| Stage | Gate |
|---|---|
| `Px.1` publication readiness | re-read the live draft; reconcile it row by row against the `Fx.6` / `Fx.7` intent; screenshot QA passes |
| `Px.2` code publication | merge the group to the published branch, push, verify the remote tree and module list, freeze the group branch |
| `Px.3` release publication | publish the migration release (`state=3_published`) on the draft **while it is still hidden**, run `action_get_commits`, link only the relevant commits, no Quick GitHub Update |
| `Px.4` description publication | `action_apply_prepublishment` on the standalone draft — it promotes that record in place and **that write is what makes the page public**; verify no current-serie record changed |
| `Px.5` full GitHub update | the **full** update, server-side inside Odoo (`odoo shell` on the container or the UI button), never through MCP, never the quick variant |
| `Px.6` GitHub output gate | fast-forward the local published branch, inspect the generated manifest / `index.html` / images commit, run the packaging and static checks |
| `Px.7` live translations | TM-first apply of description, `pics` and `releases` payloads through the loader; prove `ru_RU` ≠ `en_US` per page, caption and release, and that the HTML is closed |
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
  timeTableId="timeTableId"/>`; t-as aliases stay bare).
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
  `timeTableId="timeTableId"` (`20_7` Gx.8)). Do not excuse them
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
