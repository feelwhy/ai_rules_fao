---
id: 01-hub-serie
description: Hub serie discipline — shared checkout branch is intentional
apply: always
---

# Hub serie discipline

The flat hub uses **one working tree per repo**. Checking out another serie changes what every Cursor session and every bind-mounted Docker target sees.

## Rules

1. Before `env-serie.sh`, `git checkout`, or `env-up` that switches branches: `git status -sb` on affected repos; respect `ai_rules` never-discard-WIP.
2. Do **not** assume `tools` / `odoo` are on 19.0 — read the branch or ask.
3. Prefer `faotools_env/local/env-serie.sh <serie>` over hand-checking out a subset of repos (keeps the hub consistent).
4. `life` and `faotools_env` are not serie-switched; do not “fix” them onto 17.0/18.0.
5. After a serie switch, warn that running containers may still be on the previous image/DB until recreated with `env-up`.
6. Do not create parallel `tools-ports/` or `OdooNN/` checkouts for day-to-day work — serie = branch.

## Intentional shared checkout

If the user is browsing or testing on a branch, keep **this chat’s work on that same shared checkout** unless they ask for a side worktree. Parking work only in a disconnected worktree while the shared tree stays elsewhere breaks live Docker bind-mounts and SCM visibility.
