# ai_rules_fao

faOtools-specific Cursor / agent rules for the flat hub at `/home/feelwhy/Odoo`.

Universal coding/process rules live in sibling [`ai_rules`](https://github.com/feelwhy/ai_rules).

## Layout

Same as `ai_rules`:

| Path | Role |
|------|------|
| `src/*.md` | **Canonical** sources |
| `overrides/<id>.md` | Optional overrides |
| `tools/sync_rules.py` | Generator (identical to `ai_rules`) |
| `.cursor/rules/*.mdc` | **Generated** |
| `AGENTS.md` | **Generated** |

## Sync workflow

```bash
cd /home/feelwhy/Odoo/ai_rules_fao
python3 tools/sync_rules.py
python3 tools/sync_rules.py --check
```

## Contents (high level)

- Hub repo map + serie discipline (`env-serie.sh` / git branch)
- Repo boundaries, apps-store packaging, manifest version, boolean settings, search views
- Local Docker (`faotools_env/local/`)
- Live faOtools MCP
- Prepublishment descriptions/screenshots + video covers

Support/tools keep only repo-specific rules in-tree; shared material is here or in `ai_rules`.
