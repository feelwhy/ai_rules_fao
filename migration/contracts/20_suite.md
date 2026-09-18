# `20_suite` feature contract

`Gx.1` of the 19 → 20 port. Live 19.0 pages on faotools.com, source, and checks.

Seeded at `Gx.0` from `tools@19.0` `c06d7622722` (branch `20_suite`, worktree
`/home/feelwhy/Odoo/_worktrees/tools-20_suite`, seed `80ed2b25212`). Shared
`/home/feelwhy/Odoo/tools` stays `19.0`.

`Gx.2`–`Gx.9` are **green**. Review DB stays at :18208. Owner accepted
2026-09-18. B1 `bsu_26732` 0/112.

## Modules and live pages

| Module | Live name | `module.description` | 19.0 `exact_version` |
|---|---|---|---|
| `mail_manual_routing` | Lost Messages Routing | 1037 | 1.2.18 |
| `message_citing` | — | 1077 | 1.0.8 |
| `message_edit` | — | 1105 | 1.2.4 |
| `internal_thread` | — | 1103 | 1.0.4 |
| `internal_thread_accounting` | — | 1104 | 1.0.3 |
| `odoo_email_from` | — | 1162 | 1.0.3 |
| `odoo_email_from_accounting` | — | 1168 | 1.0.3 |
| `email_suite` | — | 1155 | 1.0.4 |
| `email_suite_accounting` | — | 1164 | 1.0.2 |

Community (`mail`; accounting bridges need `account`). Suite `depends` pull routing /
edit / thread / citing / email_from. No enterprise lane.

Layer 1: `email_suite/demo/demo_drafts.xml` (3 drafts). The others ship `"demo": []`
or no key. Layer 2 `_load_demo_email_suite_wiring` / `_demo_es_refresh`.

## Claims and checks

| # | Claim | Check |
|---|---|---|
| S1 | Suite settings persist dependency ICP | `email_suite` tests; Gx.8 Settings |
| S2 | Send Later presets resolve in the user timezone | Gx.2 green after defect 9 test hunk |
| R1 | Lost Messages list + Route manual | `mail_manual_routing` tests; Gx.8 |
| E1 | Own / any / portal edit ACL | `message_edit` tests; Gx.8 chatter |
| E2 | Delete keeps history | Gx.2 green after defect 10 test hunk |
| C1 | Cite wizard joins bodies | `message_citing` tests |
| F1 | Email From rules + composer pickers | `odoo_email_from` tests; Gx.8 |
| T1 | Private / internal subtype | `internal_thread` tests; Gx.8 Send privately |

## Gx.2–Gx.7 evidence

- **Gx.2** PREFIX `g2s_221553`: 0/107. Defects 9/10 fixed on shared `tools@19.0`
  working tree (parallel release chat commits); hunks copied onto `20_suite`.
- **Gx.3** checker 0 findings. Store API, `ir.access`, named `res_access_*`
  computes, `mail.ChatterComposer` RecipientsInput, `store.self`.
- **Gx.4** Layer 1 unchanged (3 drafts).
- **Gx.5** `gsu_284241` GX5_OK: addrs=2 rules=1 lost=2 hist=1 drafts=4 + xmlids
  + `demo`/`demo`. Loader creates Mailpit when the stand-in has no server.
- **Gx.6** no-demo / with-demo / `-u` green. log-gate FAIL 0 RECORD 5.
- **Gx.7** 0/109 tests. Review:
  [http://127.0.0.1:18208/web/login](http://127.0.0.1:18208/web/login)
  (`admin`/`admin`, `demo`/`demo`, `en_US`, Mailpit `:18025`).
- **Gx.8** owner walk: Discuss `emojiLoader.load()`; filestore
  `--with-demo` + `/var/lib/odoo`; settings = demo19; Route
  `msg_vals` successor; Cite `history.commit()`; lost form has no
  suite Route Message; wizard domain is computed Json.
- **Gx.9** B1 `bsu_26732` 0/112. Bugbot none. Security no medium+.
