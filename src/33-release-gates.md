---
id: 33-release-gates
description: Live faotools.com release bans that stay in every chat
apply: always
---

# Release gates

These bans apply even when the user did not say “publish a release”. The sequence, HTML samples, notes, YAML, and the MCP payload recipe are the skill `33-faotools-release`. Read that skill before any `module.release` write.

- Scope is `tools` and `odoo-apps-addons` only. Refuse `support`, `life`, `system`, `faotools_env`. Do not write a row with `prepublish=True`. Do not bump `__manifest__.py` (`11-manifest-version`).
- A new serie: the changelog is published while the page is still hidden, then the page is made public. A public page with an empty changelog is a failed release.
- Bump only the last number of `exact_version`. Across a major serie, keep the same tail. Do not invent an extra number.
- Do not call Quick GitHub Update (`action_update_in_github_quick` / `action_update_in_github`) through MCP. That call commits per module and aborts the MCP transaction.
- “Published” is allowed only after the live page for every shipped language has no new English sentence. A filled `.po` is not that (Appointments `1.3.33`, 2026-09-10, `/ru/` stayed English). A loader return code is not that. An MCP or encoding error means rewrite the payload and apply again (2026-09-28). Stop only when the user explicitly says to skip translations.
- A changelog icon has a space inside the tag, `<i class="fa ..."> </i>`. An empty `<i></i>` becomes `<i/>` and swallows the page (2026-08-23). The full rule is `18-xml-translate-html`.
