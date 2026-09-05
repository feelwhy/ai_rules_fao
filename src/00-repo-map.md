---
id: 00-repo-map
description: Flat hub repo map, serie resolution, and who owns which rules
apply: always
---

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
- Translations (glossary, TM, loader): `support/support_translations/` — hub rule `17-translations` is always-on. `xml_translate` HTML: always-on `ai_rules` `18-xml-translate-html`. New or replaced `module.pic` titles (`name` / `alt_name`) are TM + live loader in the **same** job as the shots; PNG files stay English.
- Demo data for public apps: XML in the `tools` module, Python generators and script JSON (`demo_xmlids.json`, `demo_purge.json`, `asset_signoff.json`) in `system/odootools_demo` — `34-demo-data`. KnowSystem articles additionally follow their `editor_type` contract — `35-knowsystem-demo`.
- App store releases (`module.release` on faotools.com): `33-faotools-release` (`tools` / `odoo-apps-addons` only). 19.0+ public `description` is TM-first **and loader-applied on the live DB in the same publish** (`17-translations`). Do not leave `/ru/` English unless the user explicitly skips translations.
