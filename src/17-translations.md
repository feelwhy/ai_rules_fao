---
id: 17-translations
description: faOtools glossary and how to apply translations (TM, .po, loader, pic titles). Read when changing copy, i18n, module.description, or screenshot titles
apply: agent
---

# faOtools translations

The live-site bans are always-on in `17-translation-gates`. This skill is the glossary, TM YAML, `.po`, and checks. The live apply on faotools.com is KnowSystem article 2139 (**Live apply** below). A gate that fails means the translation is not done.

Pull this skill for any task that adds or changes user-facing strings, `.po` / `.pot` files, website/QWeb copy, `module.description` content, `module.release.description` (public changelog), or languages.

Source of truth is **`support/support_translations/`** (glossary, do-not-translate list, fingerprinted TM). Odoo `.po` files and the DB loader are outputs, not the place to invent wording.

## Where files live

| Surface | Repo / path |
|---------|-------------|
| Glossary, do-not-translate, TM, loader, validators | `support/support_translations/` |
| App UI `.pot` / `.po` | `tools/<module>/i18n/` and `odoo-apps-addons/ai_mcp_server/i18n/` |
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
- Existing DBs do not pick up a new view msgid on `-u` (`overwrite=False`). `_fill_empty_view_translations` in `support_translations`, `odootools_demo`, and every tools / `odoo-apps-addons` module that owns QWeb `<template>` views writes the `.po` onto empty `arch_db` terms. Do not skip that fill after a template restyle.
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
- Finish with one full-hub re-scan (`tools`, `support`, `system`, `odoo-apps-addons`)
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
- **QWeb / demo restyle is a translation change.** If you change English in a `<template>`, `string=`, `title=`, or Layer 1 demo XML, the `.pot` msgid must be the **new** `xml_translate` key — not the old `<strong>…</strong>` / icon wrapper. `_update_translations(overwrite=False)` leaves the new term empty on an existing DB (incident 2026-09-09: Appointments `Any` / `Select` / more details). Same job: glossary or TM, regenerate `.po`, and the empty-term fill (`ir.module.module` hooks in `support_translations`, `odootools_demo`, every tools / `odoo-apps-addons` module that owns QWeb `<template>` views). `check_view_term_restyle.py` fails when XML is bare and the pot still only has the old tagged msgid. Demo values must stay in the module `.pot` (`demo_lint`).

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
 "all languages done." A per-module "looks complete" is not the same claim.

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
