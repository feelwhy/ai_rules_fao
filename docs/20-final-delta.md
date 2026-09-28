# saas-19.4 → 20.0 delta on the tools surface

Phase 6 item 31 of the 19.0 → 20.0 program. Released `odoo@20.0` and `enterprise@20.0` compared
with the saas-19.4 pins every group was tested on, over the touchpoint surface of the ported
repos (`tools-20_port`, `system-20.0`). Every finding below was checked against the two source
trees; release-note claims were only used to point the scans (§ Release notes).

Companions: [20-tools-touchpoints.md](20-tools-touchpoints.md) (the surface),
[20-saas-19.4-delta.md](20-saas-19.4-delta.md) (the previous hop).

## Pins

| Ref | SHA | Date |
|---|---|---|
| `odoo@saas-19.4` (tested pin) | `3630379f63633612e5a9e8d435deecbe26eaa15a` | 2026-09-12 |
| `enterprise@saas-19.4` (tested pin) | `8d73a02a8ba9a99fb41b2cd01b1680c6ded4b837` | 2026-09-12 |
| `odoo@20.0` | `c6306830baea390c5fa30a99187358420684089f` | 2026-09-28 09:18 UTC |
| `enterprise@20.0` | `366ecb35b9456c17a1b890af793de1e9c6b22ad7` | 2026-09-28 09:18 UTC |
| `tools@20_port` scanned | `ad04db88a88` | |
| `system@20.0` scanned | `fb515d5` | |

`odoo/release.py` at the 20.0 pin: `version_info = (20, 0, 0, FINAL, 0, '')`. Both `20.0`
branches were fetched without a checkout; the shared `odoo` and `enterprise` trees stay on `19.0`.

**Ancestry.** The tested saas-19.4 pin is **not** an ancestor of `20.0` (same fork pattern as the
saas branches): `odoo` merge-base `0f5525c0c1bc`, 4977 commits in `20.0` absent from the pin and
2124 the other way; `enterprise` merge-base `4c4e2c95af9a`, 3703 / 1331. A fix carried on
saas-19.4 after 2026-09-12 is not automatically on `20.0`. Tree size of the hop: `odoo/` 518 files,
`addons/` 32 553 files, `enterprise` 36 732 files changed (mostly `.po` regeneration, but see §1).

## Method

1. `ai_rules/tools/check_migrate_v20.py` on all 93 `tools-20_port` modules, twice: target
   `origin/20.0` (base = tested pin) and target = tested pin (base = 19.0). The second run is the
   residue the program already accepted; only the difference is 20.0 work. Also run on
   `system-20.0` against `origin/20.0`.
2. A tree comparison over the surface, from git refs only (`/tmp/p6/compare.py`, not committed —
   its durable checks go into the checker in the rule-22 chunk): addon set, declared models,
   fields of the 58 core models we inherit, signatures of every core method we override or call,
   `odoo.*` import resolution, controller base-class method signatures, OWL `t-inherit`, QWeb
   `t-call`, asset bundles, JS import paths, the two demo module lists.
3. Targeted reads of the changed core files for the successor API.

Counting rule: `ast` / XML parsing; occurrence counts are exposure, never a work estimate.

## Confirmed breaks — 10 items

### 1. Font Awesome removed; icons are Material Symbols (`program-wide`)

| | saas-19.4 pin | 20.0 |
|---|---|---|
| `web.fontawesome` bundle in `addons/web/__manifest__.py` | `:532` | **gone**; `web.material_symbols_outlined` / `_rounded` / `_sharp` (`:529-540`), files under `web/static/src/libs/materialsymbols/` |
| `font-awesome.css` | present | **gone** (only the `.ttf` survives for reports) |
| core view/template files with `fa fa-` | 818 | **0** |
| core views with `icon="fa-…"` | 313 | **0**; buttons carry Material names (`icon="edit_square"`, `icon="payments"`, `sale_order_views.xml:434,442`) |
| inline icon markup | `<i class="fa fa-lock"/>` | `<i class="oi" data-icon="lock"/>` (`sale_order_views.xml:451`, `chatter.xml:33-39`) |
| `ViewButton.iconFromString` | branches on `fa-` / `oi-` / src | **one branch**: `class="o_button_icon oi"`, `data-icon=<string>` (`view_button.js:24-30`, `view_button.xml:21`) |

There is no `fa-` compatibility layer anywhere in `addons/web/static/src` at 20.0. An
`icon="fa-check"` button renders `data-icon="fa-check"`, i.e. a ligature that does not exist;
`class="fa fa-…"` renders an empty inline element.

Exposure in `tools-20_port`: **53 modules**, 98 `icon="fa-…"` sites in 54 files, 747
`fa fa-…` class sites in 113 files, 183 distinct icon names. Heaviest: `cloud_base` 24 files,
`knowsystem` 23, `odoo_password_manager` 13, `business_appointment` 13,
`business_appointment_website` 11, `kpi_scorecard` 10, `documentation_builder` 10. `system`: 4
files. Release note (September 2026): "Font Awesome icons have been replaced by Material Symbols
icons." — confirmed.

This is a rename table per icon plus a markup change, so it belongs in rule 22 as a mechanical
transform with a checker kind, and every group's Fx.1 carries it.

### 2. OWL refs: compat shims and `t-custom-ref` dropped (`20_3`, `20_4`, `20_5`, `20_14`, `20_15`, `20_16`, `20_6`, `20_9`)

`addons/web/static/src/owl2/owl3_compatibility_layer.js` no longer assigns `owl.useRef`,
`owl.onRendered`, `owl.provideEnv`, `owl.useChildEnv`, `owl.useChildSubEnv`,
`owl.useExternalListener`, and no longer registers the `t-custom-ref` directive (saas pin `:303`
rewrote it to `createRefSignal`; 20.0 has no `custom-ref` handling at all). Core `t-custom-ref`
files: 397 → **0**; core `useRef(` in `web`: 88 → **0**; `t-ref="this.…"` in 100 `web` files.

| Gone at 20.0 | From | Successor (core pattern) |
|---|---|---|
| `useRef` | `@web/owl2/utils`, compat `owl.useRef`, not in `owl.d.ts` | class field `root = signal.ref()` with `signal` from `@odoo/owl`; template `t-ref="this.root"` (`core/action_swiper/action_swiper.js:43-46`, `.xml:5`) |
| `t-custom-ref="name"` | compat directive | `t-ref="this.name"` |
| `useChildRef`, `useForwardRefToParent`, `useRefListener`, `useServiceProtectMethodHandling` | `@web/core/utils/hooks` | forwarded ref as a static prop: `modalRef = useProps.static("modalRef", t.signal(t.ref()).optional(() => signal.ref()))` (`core/dialog/dialog.js:66-74`) |
| `useChildSubEnv` | `@web/owl2/utils` | `useSubEnv` from `@web/owl2/utils` (`dialog.js:97`) |
| `onRendered` | `@web/owl2/utils` | core rewrote its 4 sites to `onMounted` / `useEffect` (`dropdown_popover.js:43`, `dropdown.js`) — per-site decision |

`@web/owl2/utils` now exports only `onWillRender render useEnv useLayoutEffect useSubEnv`.
`owl.d.ts` declares `ref`, `signalRef`, `signal`, `useEffect`, `onMounted`, `onPatched`, … —
unchanged between the pins; the removal is entirely in the compat layer.

Exposure: `useRef` in 9 JS files (`kpi_scorecard`, `knowsystem` ×2, `product_management`,
`odoo_password_manager`, `business_appointment`, `cloud_base` ×3); `t-custom-ref` at 31 template
sites (`product_stock_balance` 8, `cloud_base` 7, `knowsystem` 5, `business_appointment` 4,
`short_urls` 2, `product_management` 2, `odoo_password_manager` 2, `kpi_scorecard` 1);
`useChildRef` 6 files, `useForwardRefToParent` 1, `onRendered` 1, `useChildSubEnv` 1 (all
`knowsystem`, `odoo_password_manager`, `business_appointment`). Checker `js-symbol` reports 19 of
these; `t-custom-ref` needs a new kind.

### 3. `@web/webclient/actions/action_service` removed (`20_5`, `20_7`, `20_11`, `20_14`)

The file is gone; `standardActionServiceProps` is exported from
`@web/webclient/actions/action_plugin` (`action_plugin.js:101`). Six imports:
`cloud_base/static/src/components/cloud_logs/cloud_logs.js:7`,
`cloud_base/.../photos_slideshow_action/photos_slideshow_action.js:5`,
`kpi_scorecard/.../kpi_report/kpi_report.js:9`, `odoo_menu_management/.../menu_ui/menu_ui.js:7`,
`sales_forecast_by_periods/.../forecast/forecast.js:8`, `stock_qty_forecast/.../forecast/forecast.js:7`.
Checker `js-import` reports all six.

### 4. `CustomerPortal._prepare_home_portal_values` removed — portal cards go blank silently (`20_4`, `20_8`, `20_14`, `20_15`, `20_16`)

`addons/portal/controllers/portal.py`: saas pin `:193 def _prepare_home_portal_values(self, counters)`;
20.0 has no such method. Counters are now computed by a jsonrpc route
`/my/counters` → `counters(self, counters, **kw)` (`:203-228`), which asks the new hook
`_prepare_portal_counter_values(self, counter)` (`:193-201`) for a
`(model_name, domain, access)` triple and runs one `search_count` per badge; results are cached
as booleans in `request.session['portal_counters']`, which `portal.portal_docs_entry`
(`portal_templates.xml:262-269`) reads to decide card visibility. `home()` calls
`self.counters({})` (`:230-233`). Core consumer: `sale/controllers/portal.py:16-22`.

`portal.entry` records already exist on the saas pin (our `data/portal_entry_data.xml` files were
written for it), so only the counter hook changes. Our six overrides are never called at 20.0:
no error, no warning, the card's `placeholder_count` never becomes truthy and the card is
`d-none`. Sites: `knowsystem_website/controllers/main.py:44`,
`documentation_builder/controllers/main.py:15`, `odoo_password_manager/controllers/portal.py:15`,
`business_appointment_website/controllers/main.py:72`,
`vendor_portal_management/controllers/main.py:15`, `cloud_base/controllers/portal_files.py:16`.

The checker's `dead-hook` kind resolves hooks against **models**; controller hooks are a hole. New
kind needed (controller base-class method existence + signature), which also covers items 8–9.

### 5. `odoo.tools.constants.PREFETCH_MAX` removed (`20_5`)

`odoo/tools/constants.py:13 PREFETCH_MAX = 1000` at the saas pin; absent at 20.0 (no definition
anywhere under `odoo/`; `orm/fields.py` no longer imports it). `joint_calendar/models/joint_event.py:9`
imports it at module load, so the module fails to import. Successor: a module-local constant.

### 6. `ir.attachment` file-store API re-signed (`20_14`)

`odoo/addons/base/models/ir_attachment.py` def drift between the pins:

| saas pin | 20.0 |
|---|---|
| `_file_read(self, fname: str) -> BinaryValue` | `_file_read(self) -> BinaryValue` — record-based, `LocalBinaryFile(self)` reads `self.store_fname` (`:145-151`) |
| `_file_write(self, bin_value, checksum)` | `_file_write(self, fname: str, bin_value: io.IOBase) -> None` |
| `_get_path(self, file, sha)` | `_file_fname(self, sha: str) -> str` |
| `_set_attachment_data(self, get_data)` | **removed** |
| `_gc_file_store_unsafe(self)` | `_gc_file_store_unsafe(self, grace_period)` |
| `LocalBinaryFile.__init__(self, path, model)` | `__init__(self, record)` |

`cloud_base/models/ir_attachment.py:299` overrides `_file_read(self, fname, attach_cloud_id=False)`
and calls `_file_read(attach.store_fname, attach)` at `:69`, `:73`, `super()._file_read(fname=fname)`
at `:311`; `_file_delete(fname)` at `:265` keeps its shape. Core's single caller is
`attach._file_read()` inside `_compute_raw` (`:382`). This is a rework of the cloud read path, not
a rename.

### 7. `HrAttendance.scan_barcode` merged with its geolocation twin (`20_7`)

`addons/hr_attendance/controllers/main.py`: saas pin `:274 scan_barcode(self, token, barcode, check_in_image=None)`
and `:278 scan_barcode_with_geolocation(self, token, barcode, latitude=False, longitude=False, check_in_image=None)`;
20.0 `:297 scan_barcode(self, token, barcode, latitude=False, longitude=False, check_in_image=None)`
owns the `/hr_attendance/attendance_barcode_scanned` route and the kiosk calls it through
`makeRpcWithGeolocation('attendance_barcode_scanned', …)` (`public_kiosk_app.js:228`).
`itlibertas_timesheet/controllers/attendance.py:32-49` overrides both: the `scan_barcode`
override rejects `latitude`/`longitude` (`TypeError`) and the route override calls
`super().scan_barcode_with_geolocation` (`AttributeError`).

### 8. `AttachmentController.mail_attachment_delete` is a batch call (`20_suite`)

`addons/mail/controllers/attachment.py:112`: `mail_attachment_delete(self, access_token_by_attachment_id, keep_on_messages=False)`
replaces `(self, attachment_id, access_token=None)`. `message_edit/controllers/attachment.py:18`
re-declares the route with the old signature and forwards positionally, so every attachment
delete from the composer raises at 20.0.

### 9. `sale.crm_team_salesteams_view_form` removed (`20_10`)

`addons/sale/views/crm_team_views.xml`: the saas pin defined `crm_team_salesteams_view_form`
(`:75`, inheriting `sales_team.crm_team_view_form`); 20.0 keeps only
`crm_team_view_kanban_dashboard`. `sale_order_checklist/views/crm_team.xml:7` inherits the removed
id and adds a page `<notebook position="inside">`. Successor: inherit `sales_team.crm_team_view_form`
directly — it still carries the `<notebook>` (`sales_team/views/crm_team_views.xml:21,57`). Checker
`view-xmlid` reports it.

### 10. Fork ancestry (program-wide, method)

Same rule as phase 1: the tested pin is not an ancestor of `20.0`; every later saas-19.4 fix must
be re-checked on the 20.0 tree, and the phase-1 "a 19.0 fix may be absent on target" rule now
reads "a saas-19.4 fix may be absent on 20.0".

## Confirmed clean

- **Addon set.** `odoo` 661 → 660 addons (21 removed, 20 added), `enterprise` 836 → 877 (19 removed,
  60 added), 3 moved community→enterprise (`l10n_tr_nilvera*`). None of our **31** external manifest
  deps is removed or moved; `documents` and `web_gantt` are present. The 5 names the demo lists
  already skip (`hr_org_chart`, `website_sale_comparison*`, `website_sale_*wishlist`) were absent
  on the saas pin too (build logs: "invalid module names, ignored") — list hygiene, not 20.0.
- **Models.** 2542 → 2684 declared models; 56 removed (`stock.quantity.history`,
  `calendar.provider.config`, `sdd.mandate`, …). None of our 58 external `_inherit` targets or
  string-referenced models is among them.
- **Fields.** 239 fields left the inherited models between the pins; no literal use of any of them in
  `tools` or `system` (the two name hits, `children` / `disabled`, are jstree node keys and form
  attributes, not `res.users` fields).
- **Model hooks.** Every method we override on a core model still exists at 20.0 with the same
  signature except `_file_read` (item 6). Checker `dead-hook`, `patch-target`, `patch-shadow`,
  `security-model`: 0 new findings. `mail/tools/discuss.py`: no def drift; `mail_thread.py`: only
  additions plus a new `force_direct_send` kwarg on `_web_push_send_notification`;
  `res_users.py`: additions only; `ir_config_parameter.py`: unchanged.
- **Python imports.** All `odoo.addons.*` reach-ins resolve. `odoo.tools.safe_eval` became a package
  (`safe_eval/{evaluation,expression,runtime}.py`) whose `__all__` still exports `safe_eval`,
  `datetime`, `dateutil`, `time`, `json`, `wrap_module`, `test_python_expr`, `const_eval`, so
  `joint_calendar` / `kpi_scorecard` imports hold. `odoo.tools.replace_exceptions`, `email_normalize`,
  `email_split`, `consteq`, `get_lang`, `html2plaintext`, `is_html_empty`, `single_email_re`,
  `file_open` are re-exported through `from .mail import *` / `from .misc import *`.
  `odoo.http.request_var` exists (`http/__init__.py:13`); `system` already guards the 19.0
  `_request_stack` fallback with `try/except ImportError`.
- **Templates and bundles.** 26 OWL `t-inherit` targets and 10 foreign QWeb `t-call` targets exist
  at 20.0. 9 of 10 foreign asset bundles exist; `web.assets_qweb` in
  `knowsystem_custom_fields/__manifest__.py:25` is defined at **neither** pin — a pre-existing dead
  bundle, to clean at Fx, not a 20.0 break.
- **JS import paths.** 125 distinct foreign paths; only `action_service` (item 3) is missing.
- **Runtime floor.** `MIN_PY_VERSION = (3, 12)` and `MIN_PG_VERSION = 16` are identical at both pins
  (`odoo/release.py:39,41`). The `faotools/env-demo-20` image runs Python 3.12.3 on Ubuntu 24.04 and
  the local server is PostgreSQL 16. `requirements.txt`: only `xlwt==1.3.0` dropped (unused by us);
  `debian/control` unchanged. `odoo/service/db.py` is absent at both pins (the `env_dbfilter_header`
  runtime addon already fails on saas-19.4 for that reason).
- **Official image.** Docker Hub `library/odoo` has no `20.0` tag as of 2026-09-16 (latest
  `19.0-20260908`); item 32 keeps the source-overlay image.

## Checker runs (evidence)

| Run | Findings | New vs the other run |
|---|---|---|
| `tools-20_port` @ `origin/20.0` (base = saas pin) | 50 | **25 new**: 6 `js-import` (item 3), 18 `js-symbol` (item 2), 1 `view-xmlid` (item 9) |
| `tools-20_port` @ saas pin (base = 19.0) | 25 | 0 unique — the accepted residue: 13 `record.data.id` / `FormController.template` hints, 5 `base64.b64encode` hints, 2 `qweb-tcall additional_title`, 2 `owl-this modalRef`, 1 `field-lit product_uom`, 1 `qweb-tesc`, 1 `view-anchor`, 1 `set_param` in a test |
| `system-20.0` @ `origin/20.0` | 13 | saas-era kinds only (`get_param` ×9 incl. tests, `verifalia` `ir.model.access.csv` on an `installable=False` module, `website.default_website`, one `t-esc`, one stale override) |

Logs: `/tmp/p6/checker-tools-20.0.json`, `/tmp/p6/checker-tools-saas194.json`,
`/tmp/p6/checker-system-20.0.json`, `/tmp/p6/compare2.txt`.

The checker found 3 of the 10 items on its own (2, 3, 9). Items 1, 4, 5, 6, 7, 8 need new or
widened kinds — that is the rule-22 chunk that must land before any Fx.1.

## Release notes checked against source

| Claim (Odoo 20 release notes, September 2026) | Verdict | Our exposure |
|---|---|---|
| Font Awesome replaced by Material Symbols | **confirmed** (item 1) | 53 modules |
| Python 3.12 / PostgreSQL 16 minimum | confirmed, **unchanged from saas-19.4** | none |
| `db` XML-RPC service removed; JSON-2 API | `odoo/service/db.py` absent at both pins | `env_dbfilter_header` (known) |
| Record rules removed, domain on access rights | already `ir.access` on the saas pin | none new |
| Tracking values removed | already on the saas pin (phase-1 finding 12–13) | none new |
| Many2one field rework, push notifications, account/asset/return/MRP changes | not on our surface | none |

## What this changes in the plan

- Rule 22 gets five new facts (items 1–2 as transforms with icon rename table and ref recipe; 3, 5, 9
  as one-liners; 4, 6, 7, 8 as port recipes) and the checker gets: `fa-icon` (any `fa-` class or
  `icon="fa-…"`), `owl-ref` (`t-custom-ref`, `useRef`, `useChildRef`, `useForwardRefToParent`,
  `onRendered`, `useChildSubEnv` from any path), `ctrl-hook` (controller base-class method
  existence + signature, resolving the base by import path), `py-import` (named import of a
  removed module constant). Until that lands, no group may start Fx.1.
- Every one of the 18 groups carries Fx.1 work because of item 1; the ref and portal items
  concentrate in `20_14`, `20_15`, `20_4`, `20_16`, `20_5`.
- Item 4 is the silent class again: no test we have would notice a hidden portal card. Fx.4 needs an
  HTTP assertion per portal module that `/my` renders the card with a non-zero counter.
