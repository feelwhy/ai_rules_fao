---
id: 30-prepublishment-descriptions
description: Rewrite/adapt faOtools apps-store module descriptions before publishment
apply: agent
---

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
