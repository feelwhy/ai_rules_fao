---
id: 33-release-gates
description: Live faotools.com release bans that stay in every chat
apply: always
---

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
