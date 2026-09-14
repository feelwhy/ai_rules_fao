# tools@19.0 → core/enterprise touchpoint inventory

Phase 1 artifact of the 19.0 → 20.0 migration program. This is the **surface to diff** when
comparing `19.0` against `saas-19.1…19.4` and later released `20.0`: every place our 93 modules
reach into Odoo core or Enterprise. A core change outside this surface cannot break us; a change
inside it must be explained in migration rule 22.

Regenerate this file (not hand-edit it) whenever the module set changes.

## Pins used

| Ref | SHA | Date |
|---|---|---|
| `tools@19.0` (source pin) | `12348603477eead2438bd545b2703a4330a19c97` | 2026-09-12 |
| `odoo@19.0` | `f8496b42a96f35affb6bb9ecac2310e8c174d3e2` | 2026-09-07 |
| `enterprise@19.0` | `78d34d73ec5eccd39432ac16c22cb0f600d8d60b` | 2026-09-07 |
| `odoo@saas-19.4` (first target pin) | `3630379f63633612e5a9e8d435deecbe26eaa15a` | 2026-09-12 |
| `enterprise@saas-19.4` (first target pin) | `8d73a02a8ba9a99fb41b2cd01b1680c6ded4b837` | 2026-09-12 |

Source tree scanned: `/home/feelwhy/Odoo/tools` on `19.0`, 93 modules.

**Counting rules** — stated because an earlier revision of this file published figures that could
not be reproduced. Everything here comes from Python `ast` / XML parsing, never a bare regex:

- A *route* is one `@route` / `@http.route` decorator. A single decorator may declare several URLs,
  so decorators and URL paths are counted separately.
- An *external `_inherit`* is a target that no `tools` class declares as `_name`. Models we own are
  excluded by that test, not guessed at by name prefix.
- Tests are excluded from every count.

## 1. Manifest dependencies (31 distinct external modules)

The full diff surface starts here: only these core/enterprise addons are declared.

| Count | Module | | Count | Module |
|---|---|---|---|---|
| 17 | `mail` | | 2 | `rating` |
| 6 | `website` | | 2 | `hr` |
| 6 | `web` | | 2 | `sale_management` |
| 5 | `product` | | 2 | `html_editor` |
| 5 | `crm` | | 2 | `contacts` |
| 5 | `project` | | 1 | `resource`, `calendar`, `sms` |
| 5 | `purchase` | | 1 | `phone_validation`, `auth_signup` |
| 4 | `website_sale` | | 1 | `documents`, `base`, `base_setup` |
| 4 | `account` | | 1 | `hr_attendance`, `html_builder` |
| 4 | `sale` | | 1 | `website_crm`, `sale_stock`, `base_import` |
| 3 | `web_gantt`, `portal`, `stock` | | | |

**Enterprise-gated modules (4).** These are the only ones that need the enterprise test lane:

- `business_appointment_gantt` — `web_gantt`
- `itlibertas_timesheet_gantt` — `web_gantt`
- `joint_calendar_gantt` — `web_gantt`
- `cloud_base_documents` — `documents`

`mail` is the single largest risk concentration (17 modules), followed by the
`website`/`web`/`product`/`crm`/`project`/`purchase` band.

## 2. Python — model inheritance (55 external targets, 261 sites)

109 distinct `_inherit` strings in total: **54 are models `tools` itself declares** via `_name`, and
**55 are external** (core/enterprise). Only the external ones form a diff surface.

| Sites | Modules | Model |
|---|---|---|
| 35 | 35 | `res.config.settings` |
| 32 | 32 | `ir.module.module` |
| 21 | 14 | `mail.thread` |
| 14 | 10 | `mail.activity.mixin` |
| 11 | 11 | `res.partner` |
| 11 | 11 | `ir.http` |
| 10 | 10 | `product.template` |
| 9 | 3 | `website.published.mixin` |
| 8 | 4 | `website.multi.mixin` |
| 8 | 4 | `portal.mixin` |
| 7 | 7 | `res.users` |
| 7 | 7 | `website` |
| 6 | 6 | `ir.attachment` |
| 5 | 5 | `crm.lead` |

Also touched, fewer sites each: `mail.compose.message`, `mail.message`, `mail.mail`,
`mail.activity`, `product.product`, `project.task`, `project.project`, `project.task.type`,
`res.company`, `ir.ui.menu`, `ir.binary`, `ir.actions.server`, `hr.employee`, `crm.stage`,
`product.supplierinfo`, `product.attribute`, `resource.calendar`,
`resource.calendar.attendance`, `stock.location`, `stock.quant`, `sale.order`, `sale.order.line`,
`rating.rating`, `website.page`, `website.page.properties`,
`base.partner.merge.automatic.wizard`.

The 54 tools-owned targets (`custom.extra.field`, `clouds.client`, `knowsystem.node`,
`business.appointment`, `product.sample.wizard`, `kpi.help`, …) are excluded: extending our own
model is not a core dependency.

`res.config.settings` (35) and `ir.module.module` (32) dominate by count. `ir.http` (11) matters
because `_slugify` and the frontend-translation hooks live there. `mail.thread` at 21 sites across
14 modules is the largest *behavioral* dependency, which is why the 19.3 tracking rework hit us.

## 3. Python — reach-in imports

517 plain `from odoo import` plus these specific internals, which are the fragile ones:

| Count | Import |
|---|---|
| 8 | `odoo.addons.mail.tools.discuss` |
| 7 | `odoo.addons.base.models.res_partner` |
| 5 | `odoo.addons.portal.controllers.portal` |
| 2 | `odoo.addons.website_sale.controllers.main` |
| 2 | `odoo.addons.mail.controllers.attachment` |
| 2 | `odoo.addons.account.models.product` |
| 1 | `odoo.addons.website.controllers.main` |
| 1 | `odoo.addons.web.controllers.binary` |
| 1 | `odoo.addons.phone_validation.tools` |
| 1 | `odoo.addons.mail.controllers.thread` |
| 1 | `odoo.addons.mail.controllers.mail` |
| 1 | `odoo.addons.hr_attendance.controllers.main` |
| 1 | `odoo.addons.calendar.controllers.main` |
| 1 | `odoo.addons.base.models.ir_cron` |

Framework-level: `odoo.exceptions` (86), `odoo.tools.safe_eval` (74), `odoo.tests` (43),
`odoo.tools.translate` (37), `odoo.http` (34), `odoo.tools` (23), `odoo.fields` (11),
`odoo.modules.module` (10), `odoo.tools.misc` (8), plus single uses of `odoo.tools.intervals`,
`odoo.tools.constants`, `odoo.tools.mail`, `odoo.tools.image`, `odoo.tools.date_utils`, `odoo.api`.

`odoo.modules.module` (10) and `odoo.tools.intervals` are the least stable of these.

## 4. Controllers — 87 route decorators (110 URLs) in 22 files

| Axis | Values |
|---|---|
| `type=` | 46 `http`, 41 `jsonrpc` (no legacy `json` left) |
| `auth=` | 56 `public`, 31 `user` |

Core controller classes we subclass, one count per `class` statement:

| Count | Base |
|---|---|
| 8 | `CustomerPortal` (`portal`) |
| 4 + 4 | `http.Controller` / bare `Controller` |
| 2 | `AttachmentController` (`mail`) |
| 1 each | `Website`, `WebsiteSale`, `MailController`, `ThreadController`, `CalendarController`, `HrAttendance` |

`CustomerPortal` is the heaviest dependency — its `_prepare_home_portal_values` /
`_prepare_portal_layout_values` signature is a recurring migration break point.

## 5. JS / OWL — 211 distinct core import paths

Top imports (count):

`@web/core/registry` 94, `@web/core/utils/hooks` 93, `@web/core/l10n/translation` 87,
`@odoo/owl` 52, `@web/core/utils/patch` 38, `@web/core/domain` 28, `@html_editor/plugin` 25,
`@web/core/assets` 23, `@web/core/network/rpc` 22, `@web/views/view_dialogs/form_view_dialog` 21,
`@web/views/fields/standard_field_props` 16, `@web/public/interaction` 12, `@web/core/user` 12,
`@web/core/dialog/dialog` 12, `@web/core/browser/browser` 11.

Deeper (more fragile) paths in use: `@web/views/kanban/*` (renderer/record/view/controller),
`@web/views/form/{form_view,form_controller}`, `@web/views/list/*`,
`@web/model/relational_model/{relational_model,record,dynamic_record_list,utils}`,
`@web/search/search_model`, `@web/core/templates`, `@web/core/ensure_jquery`,
`@html_builder/core/utils`, `@html_builder/utils/option_sequence`, `@html_editor/fields/html_field`.

**`patch()` targets (core prototypes we monkey-patch)** — each is a hard break if the class moves:

`ActivityMenu` 4, `Chatter` 3, `Thread` 2, `MessageModel` 2, `HtmlField` 2, `FormRenderer` 2,
`FormCompiler` 2, `Composer` 2, `ActionMenus` 2, and one each of `Message`, `Store`,
`WebsiteSale`, `PortalSearchPanel`, `NewContentSystrayItem`, `ScheduledDateDialog`,
`SaleSidebar`, `HtmlMailField`, `DocumentsKanbanRecord`, `CropImageAction`,
`AttachmentUploadService`, `AttachmentModel`, `AttachmentList`, `Attachment`,
`kioskAttendanceApp`, plus the grid `sizingX`/`sizingY`/`sizingGrid` helpers.

The `mail` OWL surface (`Chatter`, `Composer`, `Thread`, `Message`, `MessageModel`, `Store`,
attachment stack) is where most of the JS risk sits.

**Correction 2026-09-14.** `@odoo/owl` (52 imports) is a loader alias, not a file. Phase 1
treated that as “skip”. saas-19.4 ships OWL 3: `useState` is gone, compat does not restore
it, and the two `FormRenderer` patches above (`smart_warnings`, `sticky_notes`) take every
backend form down with them. Named OWL / same-path JS exports are checker kind `js-symbol`.
`@t-ref` inherit XPath is `owl-xpath`. Do not read “52 owl imports, path exists” as clean.

## 6. XML — view and template inheritance

- **168 `inherit_id` refs into core/enterprise, 88 distinct** (plus 91 into our own views, 0 unprefixed).
- **50 `t-inherit` into core, 22 distinct.**
- **184 XPath `expr=`**, of which only **1** uses a banned selector axis:
  `task_numbers/views/project_task_portal.xml:6` matches
  `span[@t-esc='task.id' or @t-out='task.id']` (`ai_rules` rule 11 bans `@t-esc`/`@t-raw`/`@string`
  selectors; this one already hedges with `@t-out`).

Most-inherited core views:

| Count | View |
|---|---|
| 12 | `base.res_config_settings_view_form` |
| 12 | `base.view_partner_form` |
| 7 | `base.view_res_partner_filter` |
| 5 | `base.view_partner_tree`, `base.res_partner_kanban_view` |
| 4 | `mail.email_compose_message_wizard_form`, `crm.crm_lead_view_form`, `base.view_users_form_simple_modif` |
| 3 | `product.product_template_only_form_view`, `product.product_normal_form_view`, `product.product_variant_easy_edit_view`, `base.view_users_simple_form`, `base.view_users_form`, `project.view_task_form2`, `crm.view_crm_case_opportunities_filter`, `crm.view_crm_case_leads_filter`, `mail.res_config_settings_view_form`, `website.res_config_settings_view_form`, `account.account_move_send_wizard_form` |

OWL templates inherited (`t-inherit`): `web.KanbanView` 5, `web.KanbanRenderer` 5,
`web.FormView` 5, `web.FormView.Buttons` 4, `web.KanbanRecord` 4, `mail.ActivityMenu` 3,
`mail.Chatter` 3, `web.KanbanView.Buttons` 2, `web.CalendarSidePanel` 2, `web.ActionMenus` 2,
`web.FormCogMenu` 2, `web.ListView` 2, `web.Many2ManyTagsField` 2, and one each of
`web.Many2One`, `web.CharField`, `web.CalendarController`, `mail.Message`, `mail.AttachmentList`,
`mail.ScheduledDateDialog`, `html_builder.ImageToolOption`,
`hr_attendance.public_kiosk_app`, `hr_attendance.attendance_menu`.

## 7. Asset bundles

| Count | Bundle |
|---|---|
| 34 | `web.assets_backend` |
| 14 | `web.assets_frontend` |
| 5 | `website.website_builder_assets` |
| 2 | `web.report_assets_common`, `website.assets_editor` |
| 1 | `web.assets_backend_lazy`, `web.assets_qweb`, `web.assets_unit_tests`, `web.assets_unit_tests_setup`, `hr_attendance.assets_public_attendance` |

Plus our own bundles: `business_appointment.time_slots`, `cloud_base.slider`,
`knowsystem.assets_builder`, `knowsystem.assets_iframe_style`.

`web.assets_qweb` and the `website.assets_editor` / `website.website_builder_assets` pair are the
bundles most likely to be renamed or restructured between series.

## 8. Known-deprecation baseline (19.0 is clean)

Scanned for every pattern rule 20 (17→18) and rule 21 (18→19) call out. Result: the 19.0 port was
thorough. Zero occurrences of `_sql_constraints`, `groups_id`, `<tree>`, `view_mode="tree"`,
`type="json"`, `odoo.osv`, `.read_group(`, `auto_join`, `@api.returns`, `self._context`,
`self._cr`, `check_access_rights`, `_check_recursion`, `_lt(`, `useService("user")`,
`useService("rpc")`, `archParseBoolean`, `oe_chatter`, `ir.cron` `numbercall`.

So rule 22's checker starts from a clean slate: anything it flags will be genuinely new in 20.

`product_uom` survives only where core 19.0 still has that exact field name — namely
`stock.move.product_uom`, used by `stock_qty_forecast` as a group-by/domain key. saas-19.4 renames
it, so that is now a confirmed break rather than a watch item (delta doc finding 6).

## 9. Defects found in 19.0 during this scan

Agents never edit 19.0. A 19.0 defect is reported to the owner, **blocks that module's group**, and
the group is re-seeded from the fixed commit once it lands (see the plan's standing principles).

1. **`business_appointment_sale` — combo expansion wrote a non-existent field.** Built
   `sale.order.line` vals with `"product_uom"`, but core 19.0 renamed it to `product_uom_id`
   (`odoo/addons/sale/models/sale_order_line.py:132`), so `_expand_combos` raised whenever an order
   held a combo product whose combos each have one item. Group `20_16`.
   **Fixed by the owner in `12348603477e` (2026-09-12) while this analysis was running** — the line
   now reads `"product_uom_id"`. This file's `tools` pin is that commit.

2. **`vendor_portal_management` — portal template read a non-existent field.** Rendered
   `t-field="price.product_uom"` / `line.product_uom` over `vendor.product.price_ids`, a One2many to
   `product.supplierinfo` (`vendor_product_management/models/vendor_product.py:108`), whose 19.0
   field is `product_uom_id` (`odoo/addons/product/models/product_supplierinfo.py:25`). Only users in
   `uom.group_uom` reached it. Group `20_8`. **Fixed by the owner in the same commit.**

3. **Three overrides of ORM internals that no longer exist on 19.0 either** (`stale-override` in the
   checker). `knowsystem/models/knowsystem_article.py:220,229` override `_generate_order_by_inner`
   and `_inherits_join_calc`; `odoo_password_manager/models/password_key.py:180` overrides
   `_generate_order_by`. None of the three is defined anywhere in `odoo` at **either** ref, so these
   `super()` chains have been dead for at least one serie. Groups `20_15` and `20_4`. Pre-existing
   defects, not porting work — but they indicate the custom ordering/join behavior those methods were
   meant to provide is silently absent today.

4. **`message_edit` — `isEmpty` patch has never taken effect.** `message_edit` patches
   `MessageModel.prototype` with a `get isEmpty()`, but upstream declares `isEmpty` as
   `fields.Attr(...)` — an own instance property — **already on 19.0**
   (`mail/static/src/core/common/message_model.js:338` at 19.0, `:392` at saas-19.4). A prototype
   getter is shadowed by the instance field, so the override is dead on both series. This is a
   pre-existing 19.0 defect, **not** a port break; it surfaced only because the JS patch audit bound
   each patched member to its real target. Group `20_suite`.
