---
id: 21-faotools-mcp
description: Live faOtools MCP usage for production truth on faotools.com
apply: always
---

# Live faOtools MCP

- The real live support database may be reachable through the MCP server for faotools.com. The namespace name depends on the host (`user-faotools`, `faotools`). If it returns needs auth or Unauthorized, connect using faotools_env `.cursor/rules/redeploy-verify-live.mdc` (MCP session) and call MCP directly. Do not ask the owner to log in.
- Use it when a task needs production truth that cannot be reliably inferred from code, such as current `ir.ui.view` contents, live website metadata, config parameters, cron state, or app/module records.
- Prefer read-only MCP checks unless the user explicitly asks to update live data.
- Before calling any MCP tool, inspect that tool's descriptor/schema and use the documented parameters.
- Treat live data as production data: do not expose secrets, tokens, customer-private details, or raw sensitive payloads in chat.
- If code and live behavior disagree, consider whether the module has not been upgraded, a view was customized in the database, or cached/generated content is stale.
- App releases (`module.release`): follow the skill `33-faotools-release`, which reads article 2137. Do not invent a parallel publish path.

## Files: upload them yourself

The agent uploads every file itself. Never hand a PDF or image to the owner to attach (`linkedin.post` 6 and 7, 2026-11). The steps (inline, pre-signed PUT, binary fields, `requires_bearer_token`) are KnowSystem article 2140 in section `AI` on faotools.com. Read it through MCP before the first upload. Stop unless it is active and in section `AI` (id 157). Do not fall back to the upload page.
