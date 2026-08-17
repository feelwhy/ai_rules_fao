---
id: 10-apps-store-packaging
description: Apps-store packaging, metadata, and installability expectations for tools modules
apply: agent
---

# Apps Store Metadata
- Keep manifests valid Python dictionaries accepted by Odoo 19.
- Preserve `name`, `summary`, `description`, `author`, `website`, `license`, `price`, `currency`, `images`, and `live_test_url` unless explicitly changing listing metadata.
- Version format is `19.0.x.y.z`; never change `version` unless the user explicitly requests a bump (see `manifest-version` rule).

# Module Independence
- A top-level add-on must install with only its manifest dependencies and standard Odoo/Enterprise modules.
- Shared product-family behavior belongs in an explicit base module dependency, not in implicit imports or undeclared XML references.
- Do not make a module depend on a sibling app only to reuse a tiny helper; duplicate small app-local glue when that preserves product independence.

# Static Description
- Keep `static/description/index.html` and manifest `images` in sync.
- Do not remove screenshots, icons, or marketing HTML during code-only tasks.
- Generated/minified listing assets are packaging artifacts; edit source files when available.
- For faOtools prepublishment copy (MCP `module.description` / features / perfect-for), follow `prepublishment-descriptions.mdc`.

# Licensing
- Preserve proprietary licensing text and `LICENSE` files.
- Do not introduce third-party code or vendored libraries without confirming license compatibility.
