---
id: 33-faotools-release
description: Prepare or publish a faOtools app release on faotools.com (module.release), including changelog, exact_version, and phrases like выложи or опубликуй
apply: agent
---

# faOtools app release

Trigger: prepare / make / publish a release, выложи, опубликуй.

The procedure is KnowSystem article 2137 in section `AI` on faotools.com. The title is for people. Read the article before any `module.release` write. Git history of this file is not the procedure. This id lookup belongs only to this pointer.

https://faotools.com/odoo/knowsystem/2137

1. MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). Inspect the tool schema first (`21-faotools-mcp`).
2. Read `knowsystem.article` 2137.
3. Stop unless that record is active and its section is `AI` (id 157).
4. Read `description` and follow it.

If the host MCP tool returns needs auth or Unauthorized, do not stop and do not ask the owner to log in. Connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Stop only when that path also fails to make a working call, or the read does not return one active record in section `AI`. Do not reconstruct the steps. The bans in `33-release-gates`, `18-xml-translate-html`, and `11-manifest-version` still apply; they are enough to refuse a write.
