---
id: 17-translations
description: Hub wiring for faOtools translations (support_translations TM, tools .po, no store leak)
apply: always
---

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
