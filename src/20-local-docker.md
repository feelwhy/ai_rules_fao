---
id: 20-local-docker
description: faotools_env local Docker: env-up, env-serie, env-shell, ports, Mailpit
apply: always
---

# Local Database Access

- Local Odoo runs **only in Docker** via `faotools_env/local/` — never a host Python virtualenv or host `odoo-bin`.
- Launch a target (restores + neutralizes on first run):

```bash
cd /home/feelwhy/Odoo/faotools_env
./local/env-up.sh demo19          # community all-apps 19 → http://localhost:18190
./local/env-up.sh demo19e         # enterprise all-apps 19 → http://localhost:18191
./local/env-up.sh support         # faotools.com (neutralized) → http://localhost:18100
```

- Prefer Odoo ORM via the container shell:

```bash
./local/env-shell.sh demo19       # odoo shell
./local/env-shell.sh demo19 psql  # SQL against the local Postgres (host port 15432)
```

- Several targets (and Febado) can run at once — each Odoo has its own HTTP port
  (`support` 18100, `life` 18110, `demo19` 18190, …); shared Mailpit is on **18025**.
  See `faotools_env/local/README.md`.
- Keep images/DBs fresh: `./local/env-sync.sh` (or `./local/env-sync.sh --check`).
- Never store local database credentials, tokens, or connection strings in repository files.
- Details: `faotools_env/local/README.md`.

## Lifecycle: leave nothing behind

WSL shares one VM (and 18 GB) between Cursor and every container, and its disk
files never shrink on their own. Incident 2026-09-28: 22 Odoo containers booted
together with Docker Desktop, 167 databases (152 agent leftovers), 62 orphaned
~1.2 GB volumes; the two VHDX files had reached ~400 GB.

- **Stop what you started.** When this chat is done with a target it launched,
  `./local/env-down.sh <target>`. Odoo containers are `restart: "no"`; nothing but
  Postgres, Mailpit and the registry proxy boots with Docker.
- **No hand-made stacks or databases.** Anything outside the target table (review
  DB, install-matrix DB, probe) is created by a script or registered at once:
  `./local/env-review.sh keep <db> --hours N`. Unregistered, it is removed by
  `env-gc.sh` after 12h.
- **The creator drops it.** A batch that creates databases (install matrix,
  coverage, builds) drops them in the same batch; `env-up.sh --test` already drops
  its `test_*` clone. `./local/env-review.sh down <db>` removes a stack completely.
- **Remove containers with their volume.** `env-down.sh --remove`,
  `env-review.sh down` or `docker rm -f -v`. Never `docker compose down` / `rm -v`
  alone: they leave the ~1.2 GB baked-addons copy.
- **Cleanup = `./local/env-gc.sh`** (dry run) then `--apply`. `env-sync.sh` runs it
  at the end. Never `docker system prune` / `volume prune --all`: they also delete Febado's
  stopped containers and named volumes.
- After a large cleanup, tell the user to run `local/windows/compact-wsl-disks.ps1`
  from an elevated PowerShell (it shuts WSL down, so an agent cannot run it).


## Serie + bind mounts

- Custom addons bind from `/home/feelwhy/Odoo/<repo>`; tools serie = git branch.
- `./local/env-serie.sh <serie>` before cross-serie work; `env-up` also ensures the target serie.
- **Same target again** (already running, or last launched in this chat): only
  `./local/env-up.sh <target> --restart`. No serie switch, prepare, sync, or
  other edits — see `ai_rules` `30-command-vocabulary`.
- See `faotools_env/local/README.md` for full port matrix and sync behavior.
