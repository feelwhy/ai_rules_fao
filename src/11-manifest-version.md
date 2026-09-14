---
id: 11-manifest-version
description: Never change tools module manifest version unless the user explicitly requests it
apply: always
---

# Manifest Version

- **Never** modify the `version` field in any `__manifest__.py` under `tools/`.
- When editing manifests (dependencies, assets, data, metadata), leave `version` exactly as it is.
- Bump `version` only when the user explicitly asks for a version increase or release bump.
- **Port exception (19 → 20 only):** during the saas-19.4 stand-in (`Gx.3`), drop the
  serie prefix (`19.0.1.3.33` → `1.3.33`) so `check_version` does not set
  `installable=False` on `saas~19.4`. At `Fx` / phase 8, on real 20.0, write
  `20.0.` + that same tail. Do not invent a fourth number. See `ai_rules`
  `22-migrate-v19-to-v20` **Manifest version**.
- If a task would normally imply a version change, do not bump automatically — ask the user first.
- “Make / publish a release” bumps `module.description.exact_version` on faotools.com (`33-faotools-release`). Do not bump the local `__manifest__.py` unless the user also asks for that.
