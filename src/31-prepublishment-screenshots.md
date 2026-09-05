---
id: 31-prepublishment-screenshots
description: Screenshot conventions for faOtools module store pages
apply: agent
---

Companion rule for copy/HTML structure: `prepublishment-descriptions.mdc`.

# Screenshot Source: Real UI, Never Generated Images

- Never use image-generation tools (e.g. `GenerateImage`) for app-store screenshots. They are not real UI and must not be uploaded as `module.pic`/`module.description` assets.
- Capture screenshots from an actual running local Odoo instance showing the real views of the module being described.

# Hard gate: demo environment BEFORE any capture

**Do not run Selenium or hand off PNGs until the demo environment passes the checks below.**

Order is mandatory:

1. **Install stack** — docker compose screenshot DB + all apps the shots need (`contacts`, `crm`, `sale_management`, `account`, target module(s), Lost Messages app when routing shots are planned).
2. **Enable every product toggle** — all suite + dependency settings ON (see *Demo data requirements*).
3. **Seed rich demo data** — run `support/devops/seed_screenshot_env.py` (extend it when the shot plan needs more records). Minimal/empty seed is **not** acceptable for suite modules.
4. **Verify assets & icons** — app switcher, systray, and field widgets must render real icons (see *Web assets & app icons*). **Block capture** if the home-menu shows the generic wireframe cube or repeated `default_icon_app.png` tiles.
5. **Walk the shot plan** — manually or via a dry-run checklist: every planned PNG must have its target view open, populated, and the feature control visible *before* automating capture.
6. **Only then capture** — Selenium/`capture_suite_screenshots.py`.

If demo seeding or asset warmup is incomplete, **stop and fix seed/scripts first** — never ship “placeholder” screenshots and iterate later.

# Capture Pipeline (local Odoo + headless Chrome)

1. Create a throwaway Postgres DB (`screenshot_<suite>_<version>`), separate from any `support_*`/`test_*` DB.
2. Install the target module(s) via the project's docker compose test image (`support/devops/docker-compose.screenshot.19.yml`), per the "Use docker compose always for tests" user rule — do not fall back to a bare host `odoo-bin` (host Python lacks Odoo's deps such as `passlib`).
   - The compose `odoo` service entrypoint is already `bash -lc`; pass the shell command directly as the `command`/run argument, do NOT wrap it in another `bash -lc '...'` or it hangs reading stdin.
3. Start Odoo from that same image/DB (`setup_screenshot_stack.sh up` or equivalent), picking a free host port (check with `ss -tlnp`).
4. Complete the **demo gate** above (enable toggles → seed → verify icons → walk shot plan).
5. Drive headless `google-chrome` via Selenium (`pip install selenium` in a local venv, e.g. `/tmp/screenshot-venv`) to log in and open each view/action, then `driver.save_screenshot(...)`.
6. Run **QA reject checks** on every PNG before handoff (see below).
7. Reference scripts: `support/devops/setup_screenshot_stack.sh`, `support/devops/seed_screenshot_env.py`, `support/devops/capture_suite_screenshots.py`, `support/devops/apply_screenshot_legends.py`.

# Demo data requirements (rich consultant demo, not smoke test)

The throwaway DB must look like a **prepared sales demo**, not a fresh install with one row per model.

## Global demo persona

- **Demo user:** `olivia.chen@example.com` / `demo` (**Olivia Chen**) — never `admin` in screenshots.
- Grant every group needed for the shot plan: Settings, CRM/Sales/Project/Contacts apps, Discuss drafts, Email From manager, Lost Messages, message edit/delete, internal thread, citing, routing.
- **Company:** “My Company” with logo if available; disable onboarding tours (`tour_enabled=False`).

## Minimum narrative (Messaging Suite baseline)

Seed a coherent story buyers recognize:

| Entity | Purpose |
|--------|---------|
| **Jane Customer** (`jane@example.com`) | Primary contact — address, phone, avatar, $ invoiced, 1 CRM opportunity |
| **CRM lead** “Website inquiry from Jane” | Composer/draft/routing targets on a second document type |
| **CC partner** | Visible copy recipient in composer shots |
| **Inbound email on Jane’s chatter** | Subject + plain-text body (no raw HTML tags visible); triggers action-menu shots |
| **2–3 composer drafts** | Discuss → My Drafts list + draft picker in composer |
| **4+ schedule presets** | Admin list + Send Later dialog |
| **2+ Email From addresses** | Support + Sales on Mailpit server |
| **1+ Email From rule** | e.g. sales orders → Sales address |
| **1–2 lost messages** | Lost Messages app queue with From/Subject/body/attachments |
| **1 posted customer invoice** | Accounting bridge wizard |
| **Edited message + history** | “(edited)” marker for message_edit shots |

Extend `seed_screenshot_env.py` when the approved shot plan needs more (cite wizard sources, forward thread, private messages, etc.). Document new seed steps in the script header.

## Per-shot data rules

- **List views:** at least **2–3 rows** with every visible column meaningfully filled (no empty Subject/Document/Recipients columns).
- **Forms:** open a **specific record** from the story above — never a blank “New” form unless the shot sells creation UX.
- **Modals/wizards:** the **trigger must be visible** — e.g. attachment reminder shows the **full composer behind** with body text mentioning “attached”; routing wizard shows the **lost message or chatter email** it applies to.
- **Chatter shots:** must show **suite-specific UI** (action menu, extra details, quote composer, private checkbox) — a generic contact form with only standard Send message/Log note is **not** a suite screenshot.
- **Settings shots:** every toggle ON that the product sells; sample text in regex/header fields; link buttons (Scheduled Send Options, Lost Messages) visible.

Re-run seed after changing seed logic; `-u <module>` when JS/XML assets changed.

# Web assets & app icons

Broken icons make listings look unfinished. Treat asset loading as part of demo readiness.

## Install & warmup

- Include **`contacts`** (and every app whose icon appears in the shot) in `SCREENSHOT_MODULES` / stack install list.
- After login, **warm up** before the first capture: open `/web`, `/odoo/contacts`, `/odoo/discuss` (or CRM/Sales as needed), wait for `.o_main_navbar`, run `document.fonts.ready`, open the **app switcher dropdown once** to force menu icon fetches.
- Chrome: do **not** pass `--disable-gpu`; use `--font-render-hinting=medium` (see `capture_suite_screenshots.py`).

## Verification (block capture if failed)

Before the capture loop, confirm:

- Home-menu button shows **`oi-apps`** (or app brand icon), not an empty/broken glyph.
- App switcher dropdown lists **Contacts, CRM, Discuss, …** with **module icons**, not the generic multicolour wireframe cube for every app.
- No screenshot shows `/web/static/img/default_icon_app.png` as the primary app tile when a real module icon exists.
- Systray icons (Discuss, Activities, user avatar) render.

Log network 404s on `web/static/lib/odoo_ui_icons/` or module icon assets and fix before capturing.

# What every screenshot must illustrate

Each `module.pic` sells **one capability** from the prepublishment’s `module.feature` rows. Before capture, write down:

- **Feature ID** (faOtools `module.feature`) this PNG supports
- **User action** visible in the frame (what did Olivia click to get here?)
- **Proof data** (which seeded record/text proves the feature is active?)

### Invalid shots (reject & re-seed/re-capture)

- Generic Odoo chrome with **no suite widget, action, or setting** in frame
- **Empty** list/form views or placeholder-only fields (“e.g. Sales Director” everywhere)
- Modal **orphaned** from its trigger (e.g. attachment warning with no composer/body context)
- **Wrong app icon** / wireframe cube in navbar when marketing a multi-app suite
- Dependency feature shown **without** suite context when the listing sells the bundle (prefer unified Messaging Suite settings + in-context chatter/composer)

### Framing

- **Width: 1130px, strict.** Crop/resize raw capture to exactly 1130px wide before upload.
- Keep **navbar + breadcrumbs** when they anchor the app/context; crop tight only when the dialog itself is self-explanatory **and** trigger context remains visible (stacked modals, composer behind confirm).
- Prefer **one hero control** per shot; avoid clutter, debug tooltips, and unrelated admin menus.

# Coverage requirements (suite / bundle modules)

For **bundle products** (e.g. `email_suite`), screenshot coverage must match **every named feature section** on the prepublishment, not a handful of easy composer panels.

Workflow:

1. Read prepublishment `module.description.feature_ids` via faOtools MCP (`name`, `subheader`, `sequence`).
2. Read existing `module.pic` rows and sibling published versions (same or better coverage).
3. Build a **shot plan table** (feature → PNG → alt_name → seed prerequisites) and get alignment before capture.
4. **Minimum:** at least **one strong screenshot per feature section**, plus native suite-only surfaces not covered by dependency duplicates.
5. **Dependency reuse:** duplicate published dependency PNGs only when quality is good **and** `alt_name`/feature mapping still fits; otherwise **re-capture** in the suite demo DB with proper icons and data.
6. Link each new `module.pic` to a `feature_id` when the feature section exists.

Standalone modules (`odoo_email_from`, `email_suite_accounting`): cover each major settings/list/wizard surface described in their own prepublishments.

# Chrome, menus and demo user

- Log in as **Olivia Chen** (`olivia.chen@example.com` / `demo`).
- Keep Odoo chrome visible unless the shot is intentionally detail-only **and** context is still obvious from `alt_name`.
- Disable tours for the demo user.

# Legends (caption overlay)

**Capture clean UI PNGs by default** — never burn legends inside the Selenium capture loop.

Apply legends when the screenshot sells a **non-obvious control** (CC/BCC tags, Route action, Send private checkbox). Skip when the titled dialog or settings block is self-explanatory.

When legends are used, follow copy/style/pipeline rules in the sections below (unchanged intent):

## Copy style

- Outcome / action captions (*what happens*), not field labels or help-tooltips.
- Center-align text in the bubble body; color `#017e84`, Ubuntu Italic 24px.
- Match `module.pic.alt_name` intent when uploading.

## Visual assets (`support/module_descriptor/static/AppsScreenshots/`)

- Bubbles: `Legends/{corner}-{long|short}.png`; point at the **value** (tag/chip/button), not the whole row.
- No highlight borders; no extra connector lines.

## Pipeline

1. Capture clean PNG (1130px) + `.boxes.json` sidecar where legends may apply.
2. Run `apply_screenshot_legends.py` only when the legend meets all copy/anchor rules.
3. Upload legended PNG when it genuinely helps; otherwise upload the clean capture.

# Reusing dependency screenshots

For dependency modules sold separately (`mail_manual_routing`, `internal_thread`, `message_citing`, `message_edit`, `odoo_email_from`):

- Read their published `module.pic` rows via faOtools MCP.
- **Duplicate** PNG bytes into new attachments on the suite prepublishment — never reparent existing dependency attachments.
- Reuse `alt_name` intent when the same angle is still accurate.
- **Re-capture** when dependency duplicates are low quality (broken icons, empty data, wrong framing) even if bytes exist on an older listing.

# Version coverage (same or better than sibling releases)

Compare adjacent published descriptions (e.g. 18.0 vs 19.0): match or exceed screenshot count, feature angles, and caption intent. Do not drop a published angle without reason.

# QA checklist (every PNG before handoff)

Reject and fix if any check fails:

| Check | Pass criteria |
|-------|----------------|
| Icons | Real app/module icons in navbar/app menu; no wireframe cube grid |
| Data | Seeded story visible; list ≥2 rows; no empty “hero” fields |
| Feature | Suite-specific control/action/setting clearly visible |
| Context | Modals/wizards show what triggered them |
| User | Olivia Chen (not Administrator) |
| Size | Exactly 1130px wide final PNG |
| Caption | `alt_name` matches what a buyer actually sees |

# Translations (hard gate) — titles and alts, not the PNG

Screenshot **files** stay English. **`module.pic.name` and `alt_name` are translated.**

Replacing or adding shots is **not** done when the PNG is on the page. Same job:

1. Rewrite TM `confs[].pics` / `features[].pics` to the **new** English `name` and `alt_name` (drop the old titles).
2. Translate both fields for every shipped language (`17-translations`).
3. MCP `_apply_description` **must include `pics`**. Omitting them, or applying the old pic YAML, leaves `/<lang>/` captions in English.
4. `action_apply_prepublishment` only re-applies YAML already on the Functional container — new local TM still needs `_apply_description`.
5. Prove it: `/ru/` caption ≠ English (`module.pic.name` `ru_RU` ≠ `en_US`).

Incident 2026-09-01: Google Drive guideline body was translated; titles such as `Open the Google Auth Platform` stayed English because TM still had the old console titles and the loader apply omitted `pics`.

# Handoff for manual faOtools upload (default)

After capture, crop/legend, and **QA pass**, move only final PNGs to:

```
~/Downloads/prepublishment-screenshots/
  <module_technical_name>/
    *.png
  upload_manifest.json   # description_id, sequence, feature_id, alt_name
```

Agent steps: capture → QA → manifest → move finals → tell user the Downloads path. Manual faOtools upload is the default; MCP upload only when explicitly requested and bearer/PUT works.

# Upload via MCP (optional)

When the user explicitly asks for automated upload **and** MCP bearer/PUT is available, upload QA-passed PNGs via faOtools MCP (`odoo_attachments_upload_prepare` → PUT → `odoo_attachments_upload_commit`), then create `module.pic` with `description_id`, `attachment_id`, `alt_name`, `sequence`, `feature_id`.
