# tools 19.0 → 20.0 port — status

Human-readable companion to the machine ledger
[migration/20-tools-port.state.yaml](../migration/20-tools-port.state.yaml). The ledger is
authoritative; if the two disagree, trust the ledger and fix this page.

Process: [36-major-version-port](../src/36-major-version-port.md).
Transforms: `ai_rules` `22-migrate-v19-to-v20`.
Evidence: [20-saas-19.4-delta.md](20-saas-19.4-delta.md),
[20-tools-touchpoints.md](20-tools-touchpoints.md).

**Last updated:** 2026-10-16 (cutover recorded; phases 4, 6, 7 and 10 closed; 4.6 CI still an owner decision)

## Where we are

| Phase | State |
|---|---|
| 1 — saas-19.4 delta analysis | **done** — 34 source-confirmed breaks, hypotheses H1–H7 closed on candidate :14, 3 runtime-reproduced (`ir.access`, `set_param`, `useState`) |
| 2 — living rules + checker + ledger | **amended** — checker kinds include `access-or` and `access-grant` (grouped `ir.rule` on Internal User is not an ACL grant) |
| 3 — branches | **done** — scaffold `971c21a311e`, 21 `tools` branches + `system@20.0`, pushed |
| 4 — infrastructure | **done.** 4.5 closed on candidate :14. 4.6 CI on the 20 branches stays an owner decision and is not done. |
| 5 — per-group loops on saas-19.4 | **Done.** Gx.9 green for all 18 groups. Fresh templates `odooallapps20build` / `odooallapps20ebuild` and accumulated `odooallapps20.odootools.com` / `odooallapps20e.odootools.com` are **ASSERT_OK** (2026-09-28, after deleting the four xmlid-less review rows). Shared `tools` stays `18.0`. |
| 5b — `_port` ↔ numeric module parity | **green** at `20_port` `60d47c3cb79`. Feature-test and lockstep commits re-merged. `diff -rq` of every numeric module folder was empty. |
| 6 — 20.0 upstream release re-analysis | **done.** Items 31 and 32 done. Item 33 superseded by the owner on 2026-10-05 (20_final grows one group at a time). |
| 7 — master infrastructure + faotools.com enablement | **done.** Serving image `env-demo-20:14` (promoted 2026-10-16). `make_enterprise_20` checked on the live enterprise template: edition enterprise, admin (user 2) and `odootools_demo.demo_role_full_admin` hold Documents and Sign. Browser first-click dropped by the owner the same day. |
| 8 — per-group loops on 20.0 | **done.** Demo 20 candidate `env-demo-20:14` (tools 20.0 `b109be09015`) green on both templates (888 / 897 tests, log gate clean, browser OK) and promoted 2026-10-16. `origin/20_final` `f3fb5fc9f67` has the same tree as `origin/20.0` `3e11b376b26`. Do not merge `20_port` `d6685c7ed5e` (static props). |
| 9 — publish loops | **done.** Store pages are public. Px.5 was the owner's GitHub update. No new release rows. The candidate gate closed with the promote of `:14`. |
| 10 — cutover | **in progress.** Image `:14` is live and the 94 pages show v.20. `origin/20.0` `162b4ac0960` and `origin/20_final` `735ca5eb9a8` have the same tree. CI is dropped. Defect 11 is on 19.0 `b4498e1b375`. Test database names are per-run (`faotools_env` `295fffa`). Still open: the Microsoft tenant sentence on Cloud Storage and OneDrive (in the YAML, not applied: MCP cannot read `support.translations`), and 33 summary keyword-tail findings from `check_mt_quality.py`. |

**First runtime evidence, 2026-09-12.** The pilot's `Gx.6` produced the program's first observed
failures on a saas-19.4 instance, and the two most expensive ones were not in this rule's list:

- `ir.rule` and `ir.model.access` were **merged into `ir.access`** at saas-19.4 (both still present
  through `saas-19.3`). Loud — `KeyError: 'ir.rule'` on install — but it hits **86 of 93 modules**.
- The saas-19.4 **image itself** exposed `hr_homeworking`, a module upstream deleted, because the
  Debian package's python-only addons tree is a portion of the `odoo.addons` namespace package and
  the re-core only replaced `odoo/`. Fixed and asserted; see the incident in the ledger.

**2026-09-14 review crash.** Opening a Smart Alert form on that DB died with
`TypeError: useState is not a function` at `FormRenderer.setup`. saas-19.4 ships OWL 3.
Phase 1 skipped `@odoo/owl` as a loader alias; the compat layer does not restore `useState`.
`smart_warnings` / `sticky_notes` patch `FormRenderer`, so this is every backend form, not
one view. Folded as findings 26–34. `Gx.8` is not a walkable review until those three files
are ported.

Every other "confirmed" break below is confirmed **against source trees at pinned SHAs**.

## Pins

| Ref | SHA |
|---|---|
| `tools@19.0` | `57ca6ad2d412` |
| `odoo@19.0` | `f8496b42a96f` |
| `enterprise@19.0` | `78d34d73ec5e` |
| `odoo@saas-19.4` | `3630379f6363` |
| `enterprise@saas-19.4` | `8d73a02a8ba9` |

## Branches

All 21 `tools` branches point at one scaffold commit, `971c21a311e` ("tools: 20.0 initial
commit"): parent is the `19.0` tip, tree is the top-level technical files only
(`.cursor/rules/*`, `.cursorignore`, `.cursorindexingignore`, `.gitignore`, `.gitlab-ci.yml`,
`requirements.txt`). That mirrors the previous cut, `da67cbeb41c` on `18.0`, so ordinary merges
into `19.0`-derived work keep behaving.

18 group branches (`20_2`, `20_c`, `20_14`, `20_5`, `20_6`, `20_9`, `20_10`, `20_4`, `20_12`,
`20_suite`, `20_11`, `20_7`, `20_15`, `20_16`, `20_3`, `20_13`, `20_8`, `20_17`) plus `20_port`,
`20_final` and `20.0`.

`system@20.0` is **not** a scaffold: it is the full `19.0` tree at `f42c38f`, because phase 4.2
ports the existing system modules in place rather than re-creating them.

All 22 refs are on `origin`. The assertion that gates this:

```bash
python3 migration/check_group_assignment.py --repo /home/feelwhy/Odoo/tools
```

`.gitlab-ci.yml` carries over unchanged and is stale (it still names `VERSION: "11.0"`), exactly
as it is on `19.0`. Still undecided (ledger `4.6_ci_on_20_branches`): local Docker is the test
path for `Gx.7`, so CI on these branches is a choice, not a blocker.

## The saas-19.4 image

Docker Hub publishes no `odoo:saas-19.4` and no `odoo:20.0` tag — only 17.0, 18.0, 19.0 — so a
pre-release serie cannot use the normal `FROM odoo:<serie>` base. Core therefore comes from git,
which is the mechanism master project images already use
(`env.project._render_core_overlay_step`).

```bash
cd /home/feelwhy/Odoo/faotools_env
./local/env-serie-image.sh --ref saas-19.4 --expect 3630379f6363
./local/env-serie-image.sh --ref 20.0 --tag faotools/env-demo-20:20.0   # after the release
```

`faotools/env-demo-20:current` = the synced `env-demo-19` image (its OS layer, patched
wkhtmltopdf and `env_dbfilter_header` reused untouched) with core replaced from
`odoo/odoo@saas-19.4`. `odoo.release.version` reads `saas~19.4`. Custom addons and `enterprise`
still bind-mount from the hub, so only core is baked. Build takes under three minutes; a rerun
with an unchanged base and branch tip is a no-op.

**One deliberate difference from master:** master does `cp -a` *on top of* the baked core, which
leaves behind files the new branch deleted. That would hide the very breaks we test for — a
removed view or addon would still be present — so here the baked core is removed first and
replaced wholesale. Master should adopt this in phase 7.

`--expect` fails the build when the branch tip has moved past the ledger pin, so re-pinning stays
a deliberate act rather than a silent change of what we test against.

## The demo20 targets

`demo20` (`odooallapps20.odootools.com`, port 18200) and `demo20e`
(`odooallapps20e.odootools.com`, 18201) are **local-only** while the port runs: the worker has
neither an image nor a dump for a pre-release serie, so `env-sync.sh` skips them and both halves
are produced here — `env-serie-image.sh` for the image, `env-demo-build.sh` for the database.

The substantive change is that **branch resolution is now per repo**. "One serie, one branch"
only holds once a serie is released; here three answers are needed at once:

| Repo | Branch | Why |
|---|---|---|
| `odoo` (via the image), `enterprise` | `saas-19.4` | Odoo ships no `20.0` branch |
| `tools` | `20_port` | the aggregate; `PORT_BRANCH=20_5` reviews one group branch |
| `system` | `20.0` | ported in place, it has no aggregate |
| `others`, `odoo-apps-addons` | not mounted | no 20 branch, and other-serie third-party code is worse than none |

`env-demo-*` still overrides `tools` / `system` to `20_demo`, as on 19. Both `20_demo` branches
now exist (`tools` from `20_port`, `system` from `20.0`), local only.

Two things to know: `enterprise` is a single shared checkout, so launching `demo20e` moves it to
`saas-19.4` and `demo19e` cannot serve simultaneously — the same trade-off `demo17e` already has.
And `env-serie.sh 20.0` would still mis-resolve the upstream repos; it is not on the launch path,
so it was left alone rather than half-fixed.

## System port (4.3)

`system@20.0` is installable on the saas-19.4 image. Manifests are unprefixed (`1.0.2`, not
`19.0.x` or `20.0.x`) — `check_version` compares to `saas~19.4`, so a serie prefix sets
`installable=False`. Re-prefix at `Fx` / phase 8. `kwkhtmltopdf_assets` was dropped (hook
absent at both refs). Homepage ticket links now name `20.0` (`version_info[0]` is `'saas~19'`
on the image, not `19`). Checker gained `manifest-version` (saas refs only). Smoke
(`env-demo-build.sh`) waits for a ported tools group.

## Warning gate (4.4a)

`env-up.sh --test` / `env-test.sh` tee the oneshot stdout to
`~/env-sync/logs/<target>/test-window.log` and classify that window only
(`local/lib/odoo_log_gate.py`). Tools/system `WARNING` and any `ERROR`/`CRITICAL`
fail the run. Core warnings are printed as `RECORD` fingerprints. Allowlist:
`migration/20-warning-allowlist.yaml` (empty). `LOG_GATE=0` skips.

## Drift runner (4.4b)

`./local/env-port-drift.sh` compares `saas-19.4` tips to the ledger pins and the
baked `env-demo-20` image. It never checks out a hub repo. Tests run only when
`20_port` already has addons, tools/system are already on the port branches and
clean, and demo20 exists. Pin drift exits 2 and does not rewrite the ledger.

`./local/install-port-drift.sh` enables a Monday 10:30 user timer — not run yet.

First `--check` (2026-09-12): odoo tip still `3630379f6363`; **enterprise tip
moved** to `aedd5f5db507` (pin is `8d73a02a8ba9`). Re-pin is a separate decision.

## Group board

Order is the owner's `Apps_Migration.md`. "Known breaks" are the pre-port baseline from the checker
plus the delta analysis — the work each group already owes before anyone edits it.

| # | Group | Modules | Stage | Known breaks |
|---|---|---|---|---|
| 1 | `20_2` **pilot** | 5 | `Gx.9` **green** | merged to `20_port` (`d7254425af9`, pushed) |
| 2 | `20_c` | 8 | `Gx.9` **green** | merged to `20_port` (`e5c5d4ad5c0`). Defect 6 ported (`cfb985df48f`). |
| 3 | `20_14` | 9 | `Gx.9` **green** | merged to `20_port` `2be60303496` |
| 4 | `20_5` | 4 | `Gx.9` **green** | B1; http://localhost:18202; access-or + access-grant |
| 5 | `20_6` | 3 | `Fx.8` **green** | on `20_final` `2c50405aecc`; changelog TM 0 gaps; cumulative 0 failed; reviews :18238 / :18237 until 2026-10-10 12:15 |
| 6 | `20_9` | 5 | `Fx.2` **green** | http://127.0.0.1:18240/web/login until 2026-10-10 15:37; community :18239; smoke 10/10 |
| 7 | `20_10` | 4 | `Gx.9` **green** | B1; http://localhost:18205; `list.set`; `view_task_card`; `cr` not `rc` |
| 8 | `20_4` | 4 | `Gx.9` **green** | B1; http://localhost:18206; merged `18ee0d5a1d0`; OWL leftovers; Extra Security hints; role avatars |
| 9 | `20_12` | 3 | `Gx.9` **green** | B1 `b12_190810`; http://127.0.0.1:18207; merged `1cb1794876c`; child chips + small tooltip close |
| 10 | `20_suite` | 9 | `Fx.8` **green** | on `20_final` `c75e0a7695e`; changelog TM 0 gaps; cumulative 0 failed; reviews :18236 / :18235 until 2026-10-08 18:39 |
| 11 | `20_11` | 3 | `Fx.8` **green** | on `20_final` `8a9ee216`; changelog TM 0 gaps; cumulative 0 failed |
| 12 | `20_7` | 3 | `Fx.8` **green** | on `20_final` `b361c623`; changelog TM 0 gaps; cumulative 0 failed |
| 13 | `20_15` | 7 | `Fx.2` **green** | community http://127.0.0.1:18247 and enterprise http://127.0.0.1:18248 (admin/admin, demo/demo, en_US, kept until 2026-10-13); 57 articles / 30 published / 4 docs; 7 overview PDFs in Downloads |
| 14 | `20_16` | 9 | `Gx.9` **green** | owner walk demo20e; B1 0/61; i18n step-5 session walk; visibility inherit dropped |
| 15 | `20_3` | 5 | `Gx.9` **green** | owner walk demo20e; B1 0/4; mappingproxy mass action; jstree off-proxy; RFQ `uom_id` |
| 16 | `20_13` | 4 | `Gx.9` **green** | B1 `b29ef140fd9` / merge `1d07d34fbb0`; composer FORBIDDEN; Mailpit; :18214 |
| 17 | `20_8` | 4 | `Gx.9` **green** | B1 `e7289b3349b` / merge `7c0e7ddacc8`; 0/15 on `test_b1_20817`; demo20e :18201 |
| 18 | `20_17` | 4 | `Fx.8` **green** | Demo 20 community and enterprise both have scoring demo 3/3/6/20; rebuild task 4603 |

All 18 groups carry confirmed work. The 2026-09-12 “pilot and `20_c` have none” claim was
the `@odoo/owl` skip. `ir.access` already hits 86 of 93 modules; OWL 3 `useState` hits 25
on top. The pilot still calibrated the loop; do not extrapolate per-module effort from it.

Scheduling notes:

- `20_12` sits immediately after `20_4` (owner 2026-09-16). `20_suite` stays after that. `20_7` sits after `20_11`, then `20_15` before `20_16` (owner 2026-09-19).
- `20_5`, `20_7`, `20_16` need the enterprise lane (`web_gantt`); `20_14` needs `documents`.

## Open hypotheses

Must not be written into a port as fact.

| # | Hypothesis | Check | Phase |
|---|---|---|---|
| H1 | asset bundles unchanged | **closed, refuted.** Font Awesome is gone. Candidate :14 loaded the 20.0 bundles (`browser_ok`, WebSuite 0 failed). |
| H2 | no further field renames in surviving models | **closed.** Candidate `-u all` then 0 failed of 888 and 897. |
| H5 | optional product on `sale.order.line` affects our line creation | **closed.** The wizard writes `product.template.optional_product_ids`. It does not create sale lines. |
| H6 | attendance ACL + geolocation affect kiosk code | **closed.** `scan_barcode` takes latitude, longitude and the check-in image. Enterprise candidate 0 failed of 897. |
| H7 | which deprecation warnings our code triggers | **closed.** `gate_warnings` 0 on both editions of `:14`. |

H3 (portal hook signatures) and H4 (JS patch targets) are closed — see the delta doc.

## 19.0 defects found by analysis

Agents do not fix these on their own initiative. Each blocks its group until 19.0 is fixed and the
pin is refreshed. Defects 3–5 were fixed on the owner's command (2026-09-12) and committed in
`84e7d1c4840`. Defect 6 is fixed on 19.0 (`a9154df3008`) and ported onto `20_c`.

| # | Module | Group | Issue | State |
|---|---|---|---|---|
| 1 | `business_appointment_sale` | `20_16` | wrote `product_uom` on `sale.order.line` | fixed by owner in `12348603477e` |
| 2 | `vendor_portal_management` | `20_8` | read `product_uom` on `product.supplierinfo` | fixed by owner in `12348603477e` |
| 3 | `knowsystem` | `20_15` | overrides `_generate_order_by_inner` / `_inherits_join_calc`, absent from core at both refs | fixed and committed in `84e7d1c4840` |
| 4 | `odoo_password_manager` | `20_4` | overrides `_generate_order_by`, absent from core at both refs — **two** sites (`password_key.py`, `portal_password_key.py`) | fixed and committed in `84e7d1c4840` |
| 5 | `message_edit` | `20_suite` | `isEmpty` prototype patch shadowed by upstream `fields.Attr`; dead since 19.0, and `editable` read the wrong flag as a result | fixed and committed in `84e7d1c4840` |
| 6 | `task_custom_fields` | `20_c` | `project.task._portal_accessible_fields` `@ormcache(cache='stable')` not invalidated when a portal-editable custom field is written; sharing form OWL `field is undefined` | fixed on 19.0 `a9154df3008`, ported to `20_c` `47d58c3ad8a` |
| 7 | `cloud_base` | `20_14` | `test1_general_cron_triggering` Case 6: after deactivate/reactivate, `COMPANY 1` has 0 child folders (expected 1) | **fixed** `51543980c6c` (`active_test=False`) |
| 8 | `owncloud_odoo` | `20_14` | a handled 429 retry logged WARNING, and the one real degradation (share URL missing) went to the server log instead of `clouds.log` | **fixed** `57ca6ad2d41` |
| 9 | `email_suite` | `20_suite` | `test_schedule_option_computes_future_datetime` asserts UTC hour 9; product stores user-tz 09:30 as 07:30 UTC | **fixed_on_working_tree** — Gx.2 `g2s_221553` |
| 10 | `message_edit` | `20_suite` | `test_delete_message_keeps_removed_content_history` uses `message.sudo()` in the admin test env; author check fails | **fixed_on_working_tree** — Gx.2 `g2s_221553` |

Only #4's first site came from the checker; `portal.password.key` names no core parent in its own
class, so the chain check skipped it and a grep found it. That gap is now closed — see below.

Regression cover added with the fixes: `knowsystem/tests/test_article_ordering.py` (4 tests) and
`odoo_password_manager/tests/test_password_ordering.py` (4 tests, new `tests/` package), both green
on a cloned test DB. They assert the **emitted SQL**, because a row-order assertion cannot
discriminate here: every `env-sync` database is `en_US.utf8`, where Postgres already ignores case
while ordering, so mixed-case rows come back sorted even with the hook dead. The row-order evidence
first reported for these fixes was therefore worthless; the SQL shape was the real check.

**Still open:** `message_edit` has no browser regression test. Locking the reactive behaviour needs a
hoot suite in `static/tests` wired into `web.assets_unit_tests` (precedent: `odoo_typo_reporter`).
It was not written because such a suite runs inside the shared `web` JS run, not
`--test message_edit`, so it cannot be proven green here first.

## Port work recorded late

Neither of these is a 19.0 bug (both work today), and neither is reachable by the checker, because
the dead-hook check requires a `super()` call and both overrides have none.

| Module | Group | Item |
|---|---|---|
| `variant_price_system` | `20_8` | `_set_product_lst_price` — core renamed the `lst_price` inverse to `_inverse_product_lst_price` at saas-19.4 |
| `business_appointment` | `20_16` | `_onchange_hours` — core deleted that onchange on `resource.calendar.attendance` |

Outside every group: `odoo-apps-addons/ai_mcp_server` reads `msg.tracking_value_ids` in
`services/tool_service.py:1256` and `services/catalog_service.py:245`, which raises on 20.0. The
group list covers `tools` only, so nothing schedules it yet.

## Running the checker

```bash
python3 ../ai_rules/tools/check_migrate_v20.py \
    --repo /home/feelwhy/Odoo/tools \
    --odoo /home/feelwhy/Odoo/odoo --odoo-ref origin/saas-19.4 --odoo-base-ref origin/19.0 \
    --enterprise /home/feelwhy/Odoo/enterprise --enterprise-ref origin/saas-19.4 \
    --modules <group modules>
```

~30s per group, ~3.2min for all 93 modules. Baseline at the pins above, with defects 3–5 fixed in
the working tree: 16 `dead-hook`, 25 `js-import`, 4 `patch-target`, 3 `view-xmlid`, 24 `field-lit`,
**0** `stale-override`, **0** `patch-shadow`. Before the fixes it was 3 `stale-override` and 1
`patch-shadow`; the other five counts are unchanged, which is how we know the hardening below added
no false positives.

Two kinds added on 2026-09-12 after the pilot's `Gx.6`, both from things the checker could not see:

| Kind | Whole-repo count | What it found |
|---|---|---|
| `security-model` | **181** in 86 of 93 modules | `ir.rule` / `ir.model.access` data files. `ir.access` replaced both at `saas-19.4` (still present through `saas-19.3`), so nearly every module blocks its own `Gx.6` until its security files are ported |
| `view-anchor` | **6** in 5 modules | inherit anchors that exist in no target view: `crm`'s `lead_priority` (`complementary_lead_data`, `opportunity_custom_fields`) and `base`'s partner filter `type_person` (`crm_duplicates`, `customer_scoring`, `partner_duplicates`, `vendor_scoring`) |

All 6 `view-anchor` hits were verified against the target trees by hand — no false positives — and
the check reproduces `complementary_lead_data/views/crm_lead.xml:31` when pointed at the 19.0
source, while reporting clean on the fixed worktree. `security-model` is the more important number:
`181` is the size of the security rewrite the whole program owes, and it is per-module work that
each group's `Gx.3` must do.

New kind **`manifest-version`**: a serie-prefixed `__manifest__.py` `version` while `--odoo-ref`
is a `saas-*` branch. System is clean. `sticky_notes` (`19.0.1.0.11`) flags on saas-19.4 and is
silent on a `20.0` ref. Every current `tools` module still carries `19.0.x` until its `Gx.3`.

Hardened 2026-09-12, each change prompted by a real miss:

- new **`patch-shadow`** kind — a `patch(X.prototype, …)` member that upstream declares as a class
  field (`fields.Attr`) can never run. Reproduced defect 5 at `message_model.js:82`. Bound to the
  **patched class** via the name its module exports (`import { Message as MessageModel }` means the
  class to find is `Message`), ancestors followed through `extends`, and members located by brace
  depth after blanking comments and string literals — a whole-file scan or an assumed indent width
  reports "clean" for the wrong reasons.
- a class with **no core parent** now falls back to the implicit `base` ancestor instead of being
  skipped, which is what hid `portal.password.key._generate_order_by`.
- `_name = X` with `_inherit = [X, …]` keeps `X` as the core parent. Discarding it had been hiding
  `odoo_email_from`'s `mail.compose.message` entirely, and once the `base` fallback landed it
  reported five live core methods there as stale.
- repo-internal `super()` chains are suppressed by definition site, not by owning module, so a
  second class of the same model inside one module is no longer flagged.
