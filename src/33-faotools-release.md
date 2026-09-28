---
id: 33-faotools-release
description: Prepare and publish a faOtools app release on faotools.com (module.release)
apply: always
---

# faOtools app release

Command: “prepare a release”, “make a release”, “publish a release”.
Live writes go through MCP `user-faotools` (faotools.com). Inspect each tool schema first.
Mutations: `odoo_records_write` / `odoo_records_create` / `odoo_actions_run`, then `odoo_operations_confirm`.

**Scope: `tools` and `odoo-apps-addons` only.** Resolve `tech_name` in those repos. Refuse `support`, `life`, `system`, `faotools_env`. Do not bump local `__manifest__.py` (`11-manifest-version`). Do not run Quick GitHub Update (`action_update_in_github_quick` / `action_update_in_github`) as part of a release.

The user’s “make a release” is the live-write gate. Ask only when the module/serie is ambiguous, the next `exact_version` already has a `module.release`, or the target is a prepublishment.

**A new-major-serie release is different.** During a major port (`36-major-version-port`) the target is a **standalone prepublication** with no `pre_publish_origin_id` (see `30-prepublishment-descriptions`). Specifics:

- The draft `module.release` lives on that same record and stays valid when the record is promoted in place. **Publish the release while the draft is still hidden, then apply the prepublication** (`36-major-version-port` `Px.3` before `Px.4`). On a standalone draft the apply only clears `prepublish` / `not_supported` / `force_no_git` and re-renders (`module_description.py:859-866`) — it destroys nothing, and it is the write that makes the page public. Publishing the release first is therefore what guarantees the page is never public with an empty changelog.
- It is a **migration** release: `migration=True`, and the first line is the flag entry — `<li class="mt8"><i class="fa fa-flag-checkered text-success mr8"> </i> The app is published to version 20.</li>` — naming the **new** serie, followed by `fa-plus` lines for substantial changes.
- Preserve the `exact_version` tail across the major bump; do not invent an extra increment. (`cloud_base` 18.0 ended at `1.4.44` and its 19.0 migration release was also `1.4.44`.)
- The GitHub update runs **server-side inside Odoo** with the stored `github_connector.github_access_token` — `odoo shell` on the container or the UI button — never through MCP, because `_update_in_git` calls `cr.commit()` per module and aborts an MCP savepoint. Use the **full** update, never the quick variant, and do not build a parallel plain-git export path: the pushed manifest, `index.html` and image layout must stay byte-comparable with previous releases. Assert `not_supported` and `force_no_git` are both False first, or the archive branch deletes the store images.

**Translations are part of the release.** On 19.0+ the job includes step 8 (TM YAML + live loader apply) in the same turn as publish. Do not report published, do not stop at GitHub / demo rebuild, and do not treat “do not redeploy Functional” as a skip. The **only** skip is the user **explicitly** saying to skip translations / do not translate (quote that command; do not mark step 8 done).

**App `.po` fill is not this step.** Completing `tools/<module>/i18n/*.po` does not translate public `module.release.description`. A 19.0+ row that is `3_published` while `/it/` or `/ru/` still shows the English changelog has failed. Incident 2026-09-10: Appointments `1.3.33` shipped English because the publish chat treated the `.po` backlog as “translations done” and never wrote TM / `_apply_description`.

## Resolve targets

1. Module (`tech_name`) + Odoo serie(s) (`module.description.version`, e.g. `19.0`). Several series → one release each.
2. Search published descriptions only:

```
[("tech_name", "=", "<tech_name>"), ("version", "=", "<serie>"), ("prepublish", "=", False)]
```

Never write the prepublishment (`prepublish=True`).
3. Read that `module.description` (`exact_version`, `name`, `release_ids`) and the last few `module.release` rows for the same app (icons, note headings, tone).

`module.description.exact_version` is the tail without the serie (`1.3.53`). Display name is `{version}.{exact_version}` (`19.0.1.3.53`). Bump **only the last number**: `19.0.1.3.53` → `19.0.1.3.54` (`exact_version` `1.3.54`).

## Public `description` (changelog)

Short, factual, no hype (“significantly”, “seamlessly”, “powerful”). Customer-safe: no exploit steps. Match existing HTML:

```html
<ul style="list-style-type: none;">
    <li class="mt8"><i class="fa fa-refresh text-info mr8"> </i> The issue of X has been fixed.</li>
    <li class="mt8"><i class="fa fa-plus text-success mr8"> </i> The feature to Y has been added.</li>
</ul>
```

- `fa fa-refresh text-info` — bug or fix
- `fa fa-plus text-success` — new feature or optimization

One `<li>` per change. Read recent `module.release` rows if unsure.

**Never leave a FontAwesome `<i>` empty.** Write `<i class="fa ..."> </i>` (space inside the pair). Empty `<i></i>` is serialized by Odoo `xml_translate` to `<i/>`. HTML5 treats that as an unclosed start tag, so the changelog renders as a broken `+` / leftover `+` and the rest of the list is swallowed. Same for any other non-void icon/wrapper (`<span>`, `<b>`, `<em>`): never `></tag>` with no text, never self-close. Incident 2026-08-23: 94 translation releases shipped `<i class="fa fa-plus text-success mr8"></i>` and the public notes broke.

## Internal `notes` (mandatory)

**Every new release must have Before / After notes.** A one-line summary is not enough. Include what broke or how it worked, what it does now, and every critical detail (security/ACL, API, upgrade/install, tests, serie-specific differences, commit SHA / PR). Read the code and the live `module.description` / last releases before writing — do not invent.

```
Before release
-----------------------
<actual previous behavior, including the hole or limitation>

After release
--------------------
<what changed, checks added, tests, SHA / PR>
```

Public `description` stays short; put the important detail here. Do not put tokens or customer-private data in notes.

## Sequence (each `module.description`)

1. Write `exact_version` to the bumped tail. Stop if a `module.release` already exists for that `module_id` + `exact_version`.
2. Create `module.release`: `module_id`, `exact_version` (new tail), `release_date` today, `description`, `notes`. Skip `1_to_check` / `2_checked` (those spawn check activities).
3. Publish: write `state=3_published`.
4. Get GitHub Commits: `odoo_actions_run` on **`module.description`** (`ids` = that description), `method_name=action_get_commits` (UI label “Get GitHub Commits”; the release action maps to `module_id.action_get_commits()`).
5. Auto-link commits: search `github.commit` for that `module_id`, `ingore_commit=False`, preferably `in_release=False`. Pick rows that belong to this change (message, SHA, date after the previous release). Write `commit_ids` on the new `module.release`. If none match, say so — do not attach unrelated history.
6. Do **not** run Quick GitHub Update (`action_update_in_github_quick` / `action_update_in_github`). MCP wraps the call in a savepoint; that method’s `cr.commit()` then aborts the cursor (`InFailedSqlTransaction`). The operator runs it from the UI if needed.
7. `odoo_record_url` for every new `module.release` and paste the links in the reply.
8. **TM-first translate** the public changelog when the description serie is **19.0+** (see below). Start it in the **same turn** as publish. Do not end the turn after step 7. Do not ask “translate it?” / “proceed with step 8?”. Chunk-gate does not split this step off. The release is **not done** until the live page scan below is green for every shipped language. The **only** skip is the user **explicitly** saying to skip translations (quote that command; do not mark step 8 done).

Report per release only after that scan: module, serie, old → new version, state, commit count, URL, and the page-scan result (every shipped language, or the list that is still English). A reply that says published / готово / all ok before the scan is a failed release.

## Public changelog translations (19.0+)

Pull `ai_rules` `17-translations`. Public `module.release.description` only (`xml_translate`). **`notes` and `description_html` stay English.**

**Hard gate.** A 19.0+ publish that leaves any new changelog sentence in English on a shipped language page has failed the release. One translated line next to English lines is a failure. Do not report “published” until the live page scan has passed. The user must not have to open the site and ask again.

These do **not** skip or postpone this block (they are not an explicit “skip translations”):

- “do not redeploy / rebuild Functional” (faotools.com). Changelog apply is a loader write on the live DB, not a project rebuild.
- Demo / master project rebuilds, GitHub update, or “YAML is in git”.
- “the YAML is not on the container disk yet.”
- An MCP parse error, a `\u` escape the bridge ate, a payload that is “too big”, or a diacritic the call rejected. Change the text so the call succeeds, then apply. Do not stop and do not tell the user that encoding blocked the release.

After the English row is `3_published`:

1. Update TM first: `support/support_translations/tm/website/<tech_name>_<serie>.yaml` → `releases` entry keyed by `module_version` + `exact_version`. Every new English sentence, every code in `support_translations.const.SHIPPED_LANGS` (read the list; do not type a subset). `python3 support/support_translations/scripts/check_release_tm.py` must not report a gap for this release. Reuse `scripts/fill_release_tm.py` PACKS when the sentence already exists. Keep real Unicode in the YAML.
2. Translate glossary-first (do-not-translate terms stay as-is: Odoo, Bearer, MB).
3. **Apply now on faotools.com** via MCP `odoo_actions_run` on `support.translations`, method `_apply_description`, args = `[payload, lang_codes, path]`, then `odoo_operations_confirm`. A preview is not an apply. `payload` is the YAML `match` plus the new `releases` entry. Sentence-only `source` strings (no HTML, no icon): the loader wraps the icon. Do **not** wait for a Functional image rebuild. Never `odoo_records_write` translations that are not in the YAML.
4. If this 19.0 page also lists older-serie rows (`migration_release_ids`), those public descriptions must be in the same TM list and applied. Do not leave them English.
5. **Live page scan, every shipped language, before any “done” reply.** Read each `res.lang` `url_code` for `SHIPPED_LANGS`. GET `https://faotools.com/<url_code>/apps/<slug>`. Cut from `>{version}.{exact_version}</h5>` to the next version heading. The block fails when it still contains any full English sentence from this release. Re-apply that language and scan again. `en_GB` may still show the English sentence when the wording has no British spelling difference — say so; it is the only allowed match. A loader result `[1, N, []]` and a `ru_RU` field read are not this scan.

### MCP payload that actually applies (incident 2026-09-28, `ai_mcp_server` 1.1.0)

The bridge rejects the call **before Odoo** when the arguments are not one JSON object. That is not a reason to leave the page in English.

- Build the arguments with `json.dumps(..., separators=(",", ":"), ensure_ascii=False)` and `json.loads` them before sending. Do not pretty-print. The default `ensure_ascii=True` writes `\uXXXX`, and the bridge eats that backslash. A hand-wrapped payload with an extra `]` / `}` before the language list dies as `Extra data` / `Failed to parse arguments`.
- Send that compact text as raw UTF-8. It works for Cyrillic, Arabic, and CJK.
- If a language still will not parse, rewrite **that** translation so the call succeeds (ASCII fold of Latin diacritics is allowed on the live write; the YAML keeps the real letters). Confirm, then re-scan the page. Do not drop letters (`ı` / `ş` / `ł` must not vanish).
- Apply in language batches when one payload is too large. Every code in `SHIPPED_LANGS` still has to land.

Skip this block only when the target `module.description.version` is 18.0 or older (no new TM for an 18.0-only publish), or when the user **explicitly** commanded a skip. Store HTML (`resulted_description`) stays `en_US`.
