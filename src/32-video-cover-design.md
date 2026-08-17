---
id: 32-video-cover-design
description: Design faOtools YouTube video covers in house style
apply: agent
---

# faOtools video cover (YouTube thumbnail) design

Reusable recipe for producing video covers in the faOtools house style, derived from
the shipped covers for the **KPI Scorecard** and **Password Manager** demo videos.
Every faOtools module demo cover shares the same skeleton; only the module-specific
content (header keyword, dashboard mockup, themed props, legend) changes.

**Canonical storage** (version-controlled, in the repo):

`support/module_descriptor/static/Covers/`

Save every finished cover here. Use descriptive snake_case names, e.g.
`<module_or_topic>_video_cover.png`. When a cover maps to a known YouTube video,
optionally note the video ID in the rule's quick-reference section (not in the
filename unless the user asks).

Existing reference covers in that folder:

- `kpi_targets_video_cover.png` — KPI Scorecard (`2daDCn1_axI`)
- `password_vault_video_cover.png` — Password Manager (`V-DWe7LzhW0`)
- `cloud_storage_video_cover.png` — Cloud Storage Solutions (`LX3IWv0L6-U`)
- `lost_messages_video_cover.png` — Lost Messages Routing (`K451Col9iEs`)
- `joint_calendar_video_cover.png` — Joint Calendar (`lUy5unL2t6A`)

Cursor chat may also stash working copies under
`~/.cursor/projects/home-feelwhy-Odoo-Odoo17-support/assets/` during generation;
**always copy the post-processed final PNG into `module_descriptor/static/Covers/`**
before considering the task done.

## When to use

- User shares one or more YouTube links and asks for a cover/thumbnail.
- User asks for "another cover / variant" for an existing faOtools video.
- User asks to restyle an arbitrary image into the faOtools cover style.

## Step 0 - Gather the source truth

1. If a YouTube link is given, fetch the page and read the transcript/description to
   learn: the **module name**, its **one-line value proposition**, the **main UI**
   (dashboard, list, cards, side panel) and **themed objects** (keys, shields, targets,
   charts, locks, etc.). The transcript intro paragraph is usually the best summary.
2. Map the link to the module. Known so far:
   - `2daDCn1_axI` -> KPI Scorecard
   - `V-DWe7LzhW0` -> Password Manager
   - `LX3IWv0L6-U` -> Cloud Storage Solutions
   - `K451Col9iEs` -> Lost Messages Routing
   - `lUy5unL2t6A` -> Joint Calendar
3. Derive three text pieces (keep them short, benefit-driven, Title/UPPER case):
   - **Header**: `ODOO` + 1-2 keyword lines (the product or its core promise).
   - **Legend / tagline**: one sentence, 3 short lines, starts with "The tool to ..."
     and ends with "... in Odoo" (this is the faOtools voice).
   - **Mockup content**: 4-8 realistic labels/values for the dashboard cards.

## Canvas & export specs

- Aspect ratio 16:9, landscape. **Final export size: 2752 x 1536 px** (the size the
  user standardizes on). Intermediate generation can be 1536x1024 / 1024x571, then
  resized last.
- Single flat PNG, no transparency needed in the final.

## Layout zones (always the same)

- **Top-left - Title block**: a semi-transparent dark rounded rectangle bleeding off
  the left edge, holding 2 lines of big bold condensed uppercase text. Line 1 begins
  with white `ODOO`; the product keyword(s) are in teal `#017e84`. Wraps to a second
  line when long (e.g. `ODOO` / `PASSWORD` (white) ... `MANAGER`).
- **Top-right - faOtools logo**: do NOT let the image model draw the wordmark (it
  garbles the letterforms). Instead leave the top-right corner clean during generation
  and **composite the real logo** afterward. Canonical transparent asset:
  `module_descriptor/static/Covers/logo_faotools_apps.png` (gray `faOtools` with the
  magenta ring `O`, plus right-aligned `apps` beneath). Paste it at ~0.22 x cover width,
  ~70 px right / ~55 px top margins. The source brand wordmark is gray `~#96968e` with a
  magenta `O` ring `~#9b3c82`; rebuild the asset from it if needed (black background
  becomes transparent via per-pixel alpha = brightness).
- **Center - 3D isometric app mockup** (the hero, see below).
- **Bottom-right - Legend**: 3 lines of white, medium-weight, mixed-case sentence.
- **NEVER** include an AI/Gemini sparkle (4-point diamond). If a source has one in a
  corner, remove it (see post-processing).

## Color palette (exact)

- Title keyword teal: `#017e84` is the base brand teal. For the **header keyword** use a
  slightly brighter teal, normalized to `~#10b0be` / `(16,176,190)` so both covers match
  exactly (the image model drifts between covers; fix it in post-processing).
- Background: a diagonal gradient, **magenta-purple at top-left -> dark blue-violet at
  top-right -> dark teal-green at bottom-right**, deep purple at bottom-left:
  - top-left  ~ `#5a2559` / `#633363`
  - top-right ~ `#27294e`
  - bottom-left ~ `#341747`
  - bottom-right ~ `#166c6d`
- Accent cyan for circuit lines / glows: ~ `#2bd4d4`.
- faOtools `O` accent: magenta/pink ~ `#d63384`.
- Legend & `ODOO` text: white `#ffffff`.

## Typography

- Header: heavy bold, condensed, uppercase sans-serif (Montserrat ExtraBold / Gotham
  Bold feel). Tight leading, two lines max.
- Legend: clean medium-weight sans, mixed case, comfortable leading.

## The 3D isometric mockup (hero)

- A tablet/screen floating in perspective, tilted to face from the lower-left, with a
  soft glowing edge and drop shadow, sitting just right of center.
- It shows a believable Odoo app screen for the module:
  - left vertical **sidebar** with a logo and a few **colored category chips**
    (purple / teal / green / orange gradients),
  - central **grid of cards** (each: icon, title, a couple of values/stars/progress),
  - a right-hand **detail panel** ("Selected ... info" with fields/labels).
- Use module-appropriate icons and the brand teal for highlights.

## Decorative elements (subtle, dark, low-contrast)

- Thin cyan circuit/connector lines and small nodes around the edges.
- A few floating **3D shields with a teal checkmark** (trust/security motif).
- A handful of **themed 3D props** scattered around the mockup that signal the topic
  (e.g. keys/locks for Password Manager; targets, charts, gauges for KPI Scorecard).
- Faint dotted connectors and tiny geometric accents. Keep all of this dim so the
  title, mockup, and legend stay dominant.

## Generation workflow

1. Prefer `GenerateImage` with the closest existing cover from
   `module_descriptor/static/Covers/` passed as a `reference_image_paths` entry,
   instructing it to keep the style/layout and swap only the header, mockup content,
   themed props, and legend.
2. Post-process (see below), then save the final PNG to
   `module_descriptor/static/Covers/<module_or_topic>_video_cover.png`.

## Post-processing (deterministic, do with Pillow)

These pixel steps make results exact and on-brand. Always verify by cropping/zooming.

1. **Remove any Gemini sparkle** (4-point diamond), usually bottom-right near the
   legend. It can overlap a letter; mask it out and keep the letter's bright pixels,
   filling the rest with the local background color. Zoom in to confirm no remnant.
2. **Normalize/brighten the header keyword teal**: detect teal pixels in the title band
   only (top-left, roughly `y < 0.24*H` and `x < 0.50*W`, where `g > r+25 and b > r+15
   and g > 100`) and remap to the bright header teal, preserving shading:
   `t = min(1, g/178)`, `out = (16*t, 176*t, 190*t)`, blended by how teal each pixel is
   so anti-aliased edges stay smooth. Restricting to the band avoids recoloring the
   tablet's teal UI.
3. **Composite the real logo** top-right (see logo bullet above). Do this on the
   2752x1536 canvas so the downscaled logo stays crisp.
4. **Resize to 2752 x 1536** with Lanczos (do the resize before the logo paste).

## Content guidelines for headers & legends

- Header keyword should be the product or its strongest benefit, not a feature dump.
- Legend formula: `The tool to <verb phrase> <object> in Odoo`. Keep ~8-12 words.
- When asked for an alternative cover for the same video, keep the exact style but
  change the header keyword, the legend wording, and the mockup labels so it reads as a
  distinct design (not a duplicate).

## Quick reference - per-video content used

- **KPI Scorecard** (`2daDCn1_axI`): periods, KPI targets, measurements/variables,
  constants, formulas, scorecard with actual-vs-target colors, categories. Props:
  target/bullseye, charts, gauges, trophy.
  - Cover `kpi_targets_video_cover.png`: header **ODOO KPI TARGETS**; legend
    *"The tool to set targets, measure results, and reach your goals in Odoo"*.
- **Password Manager** (`V-DWe7LzhW0`): bundles/vaults, password cards with strength
  stars, access rights, encryption, portal sharing, duplicate detection. Props: keys,
  padlocks, shields.
  - Cover `password_vault_video_cover.png`: header **ODOO PASSWORD VAULT**; legend
    *"The tool to encrypt, share, and control team passwords in Odoo"*.
- **Cloud Storage Solutions** (`LX3IWv0L6-U`): organize attachments, folder-tree single
  view, auto folder rules, sync Odoo with Google Drive / OneDrive / SharePoint /
  Nextcloud / ownCloud / Dropbox. Mockup: white file-manager UI (folder tree sidebar +
  "Cloud Clients" connected list, file/folder cards with type icons and "Synced" badges,
  right "File Preview" panel). Props: 3D cloud, folders, sync arrows, provider badges,
  shields. Note: keep the tablet UI BRIGHT/WHITE and the background magenta-purple ->
  teal (the model tends to drift to a dark UI / navy bg for storage themes — correct it).
  - Cover `cloud_storage_video_cover.png`: header **ODOO CLOUD STORAGE**; legend
    *"The tool to organize, sync, and manage document files in Odoo"*.
- **Lost Messages Routing** (`K451Col9iEs`): detects emails that could not be
  auto-attached ("lost"), routes/attaches them to the right document thread (single or
  batch), allowed-models config, notifications, "Lost Messages Manager" group. Mockup:
  white inbox/list UI (Lost Messages + Configuration sidebar, message rows with
  checkbox/date/subject/author and red "lost" badges, "Route Manual" action, right
  "Route Message" panel with Model + Object selectors and a teal "Attach message"
  button). Props: envelopes (one with a red alert badge), routing-arrow signpost,
  magnifier, shields.
  - Cover `lost_messages_video_cover.png`: header **ODOO LOST MESSAGES**; legend
    *"The tool to catch and route lost email messages in Odoo"*.
- **Joint Calendar** (`lUy5unL2t6A`): merges different Odoo document events
  (opportunities, meetings, activities, sale/purchase orders, tasks, time offs, MOs)
  into one or several configurable "super calendars" via rules; color-coded by model,
  month/week/day/year views, access rights, optional Gantt add-on. Mockup: white Odoo
  Events month-view UI (calendars sidebar + Configuration: Calendars/Rules, color-coded
  event chips across a month grid, right mini-calendar + per-model color legend +
  attendees filter). Props: 3D calendar with check, alarm clock/bell, colorful event
  map-pins, stacked calendar sheets, shields.
  - Cover `joint_calendar_video_cover.png`: header **ODOO JOINT CALENDAR**; legend
    *"The tool to merge all document events into shared calendars in Odoo"*.
