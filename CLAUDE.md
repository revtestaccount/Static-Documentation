# CLAUDE.md — Project Context for RevAssist / Claude Code

> This file is read automatically at the start of every session.
> It provides the context needed to work effectively on this project without re-explanation.

---

## 1. What This Project Is

**Static-Documentation** is a static HTML/CSS/JS portal that serves technical documentation for Revenue's PAYE Modernisation Public Interface Testing (PIT) environments. It is a direct replacement for the deprecated AngularJS project `paye-employers-documentation`.

**Active branch:** `dev_contentMigration` (branched from `dev_traditionalNavbar`)  
**Source project (legacy):** `O:\git\paye-employers-documentation`  
**FAQ source project:** `O:\git\paye-employers-pit-faq`

The site serves external software developers integrating with Revenue's PAYE web services. It contains PDFs, schemas, WSDLs, JSON/XML examples, and migrated HTML documentation pages.

---

## Deployments

| Environment | URL | Audience | Notes |
|---|---|---|---|
| **Internal test** | https://revtestaccount.github.io/Static-Documentation/ | Revenue staff only | Current dev deployment — not shared externally |
| **Pre-release (legacy)** | https://revtestaccount.github.io/paye-employers-documentation/ | Revenue staff only | Test/approval deployment of old project — **never share externally** |
| **Public release** | https://revenue-ie.github.io/paye-employers-documentation/ | Software integrators (public) | Live public-facing deployment |

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| Markup | Plain HTML5 fragments |
| Styling | SCSS → CSS (Revenue Design System tokens) |
| Scripting | Vanilla JavaScript (hash-based SPA router) |
| Navigation | `assets/js/sitemap.json` — all 160 routes |
| Build | Sass CLI only — no bundler |
| PDF migration | Python 3.11 — PyMuPDF (`fitz`) + pdfplumber |

**No Angular, no React, no Vue, no Node at runtime.** Bootstrap 5 is loaded from CDN (planned for removal).

---

## 3. Key Files

| File | Purpose |
|---|---|
| `index.html` | SPA shell — header, navbar, `#content` div, footer |
| `assets/js/router.js` | Hash router, nav builder, content loader |
| `assets/js/sitemap.json` | Route map: URL hash → HTML fragment + page title |
| `assets/css/styles.scss` | Master SCSS entry point |
| `assets/css/styles.css` | Compiled output — never edit directly |
| `content/shared/*.html` | Shared fragments (home, cards, guides, FAQ) |
| `content/PIT3/*.html` | PIT3-specific content fragments |
| `content/PIT4/*.html` | PIT4-specific content fragments |
| `PROJECT_ASSESSMENT.md` | Full architecture assessment and outstanding work |
| `MIGRATION_STATUS.md` | Asset migration tracking |

---

## 4. Design Conventions (Non-Negotiable)

- **Revenue Green:** `#025F63` — all header/navbar backgrounds
- **Border radius:** `0` everywhere — squared corners, no exceptions
- **Font:** Segoe UI 14px (internal applications)
- **Sizes:** `rem` units throughout — no `px` in authored CSS (border widths excepted)
- **Accessibility:** WCAG 2.1 AA target on all migrated pages
- **`demodocument.html`** — intentional placeholder for ~120 unbuilt routes; do not remove

---

## 5. Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Production baseline — no direct commits |
| `dev_traditionalNavbar` | Navbar + CSS overhaul |
| `dev_contentMigration` | Content migration — **current working branch** |

New contributors should branch from `dev_contentMigration`.

---

## 6. PDF → HTML Migration Pipeline

This is the primary ongoing work. The pipeline converts source PDFs into site-ready HTML fragments.

### Running the Pipeline

```powershell
cd tools
python migration_pipeline.py "../content/PIT3/<section>/<doc>.pdf" --pit PIT3
python migration_pipeline.py "../content/PIT4/<section>/<doc>.pdf" --pit PIT4
```

### What the Pipeline Does Automatically

1. **PDF → Markdown** (`migrationScripts/pdfToMarkdown.py`) — embedded image extraction with 10KB artefact filter and MD5 deduplication, font-size heading detection, table extraction via pdfplumber, repeating header/footer suppression, visual TOC suppression, bullet conversion, code block detection, automatic caption/image ordering fix
2. **Markdown → HTML** (`create_page/convert_new.py`) — TOC generation, REVDS classes, `tabindex="0"` on tables/pre, stylesheet injection, `.figure-caption` class applied to all Figure N captions
3. Injects SVG branding block after `<h1>`
4. Validates environment hostnames (warns if wrong environment hostname detected)
5. Updates `sitemap.json` route to point to HTML (not PDF)
6. Updates section listing page — changes `href` and badge from PDF to LINK
7. **Mojibake fix** — automatically corrects corrupted smart quotes and dashes

### After Every Pipeline Run — Manual Checks Required

1. **Review the generated HTML in the browser** — the pipeline cannot fix everything
2. **Check tables** — complex tables spanning PDF page breaks often split incorrectly
3. **Check code blocks** — HTTP request examples sometimes render as `<table>` instead of `<pre><code>`
4. **Check footnotes** — the pipeline sometimes merges multiple footnote paragraphs into one `<p>`
5. **Check version history** — cover page version history tables can spill into body sections
6. **Hostname check** — pipeline warns automatically; fix with PowerShell replace if needed
7. **After hand-authoring any `<pre>` blocks** — run `fix_pre_tabindex.py` to ensure `tabindex="0"` is present (WCAG 2.1)

### PIT3 Hostname Fix (required for PIT3 REST Web Service Integration Guide)

```powershell
(Get-Content "content/PIT3/rest/rest_web_service_integration_guide.html" -Raw) `
  -replace "softwaretestnextversion\.ros\.ie", "softwaretest.ros.ie" `
  | Set-Content "content/PIT3/rest/rest_web_service_integration_guide.html" -NoNewline
```

---

## 7. Document-Specific Post-Pipeline Fix Scripts

Some documents have known structural issues the pipeline cannot auto-fix. Document-specific Python fix scripts live in `tools/` and are run immediately after the pipeline.

### `tools/fix_rest_endpoints_table.py`

Fixes the REST Web Service Integration Guide (PIT3 + PIT4). Run after every pipeline regeneration of this document:

```powershell
cd tools
python fix_rest_endpoints_table.py --pit PIT3
python fix_rest_endpoints_table.py --pit PIT4
```

**What it fixes:**

| Fix | Description |
|---|---|
| Fix 1 | Replaces broken section 2.1 REST Endpoints tables (split across PDF pages) with a single clean 5-column hand-authored table |
| Fix 2 | Removes misplaced ERN/Monthly ERR table appearing after section 2.1.1 |
| Fix 3 | Removes orphaned "1.0 Release Candidate 2" table |
| Fix 4 | Removes version history continuation table spilling into Document context section |
| Fix 5 | Replaces HTTP request example `<table>` with proper `<pre><code>` block |
| Fix 6 | Replaces broken section 4.1.3 headers table with clean 2-column table and moves footnote paragraphs to after the table |

**Pattern for new documents:** If a new PDF has similar issues, create a new script following the same pattern — one `fix_html()` function with numbered fix blocks, each using `re.subn()` with clear change logging.

### `tools/fix_pre_tabindex.py`

Ensures all hand-authored `<pre>` elements have `tabindex="0"` for WCAG 2.1 keyboard accessibility. The pipeline adds this automatically, but hand-authored `<pre>` blocks in fix scripts bypass that step.

```powershell
cd tools
python fix_pre_tabindex.py "../content/PIT3/rest/rest_web_service_integration_guide.html"
```

Idempotent — safe to run multiple times. Run against any HTML file after hand-authoring `<pre>` blocks.

---

## 8. WYSIWYG Page Editor

A bare-bones WYSIWYG page editor is in place but needs significant improvement. Planned enhancements:

- Support for all page components generated by the migration pipeline: TOC, tables, code blocks, headings, lists
- Ability to edit existing pages (not just create new ones)
- **Must NOT be available in the public release deployment** — the editor and any page-editing scripts are internal tools only

See Section 3 below for the deployment access control requirements.

---

## 8a. Public vs Internal Feature Gating

Certain features must only be available in the internal test deployment and must be excluded from the public release:

| Feature | Internal | Public |
|---|---|---|
| WYSIWYG page editor | ✅ | ❌ |
| Page edit/create scripts | ✅ | ❌ |
| Any UI that allows content modification | ✅ | ❌ |

When implementing the editor and any related tooling, ensure there is a clear mechanism to gate these features out of the public build.

---

## Bootstrap Removal (Next Task)

Bootstrap 5 (CDN) is the last external dependency. Removal plan identified:

### Phase 1 — Card grid (straightforward)
Replace `container` / `row` / `col-sm` / `card` / `card-body` / `card-img-top` / `stretched-link`
with PrimeFlex grid (`grid` / `col-12 md:col-4`) and custom `.home-card` CSS already in `styles.scss`.

### Phase 2 — Navbar collapse/hamburger (requires custom JS)
Bootstrap JS powers the mobile hamburger toggle via `data-bs-toggle="collapse"`.
Needs a small vanilla JS implementation before Bootstrap JS (`bootstrap.bundle.min.js`) can be removed.
The toggle logic will live in `assets/js/router.js` or a new `assets/js/nav.js`.

### Important — Customer-Facing Application
This is a **public-facing** application. All styling decisions must use:
- **Font:** FiraSans-Regular 16px (`RevdsExternalPreset`)
- **REVDS preset:** `externalPreset` (not `internalPreset`)
- **WCAG 2.1 AA:** Mandatory throughout
- REVDS 22 UI rules loaded as session context — apply PrimeFlex layouts (Rule 6), never Bootstrap grid

---

## 9. Completed PDF → HTML Migrations

| Document | PIT3 | PIT4 |
|---|---|---|
| REST Web Service Integration Guide | ✅ | ✅ |
| REST Connectivity Handshake Guide | ✅ | ✅ |
| Overview of ROS Payroll Reporting | ✅ | ⏳ |

---

## 9. Route Coverage

| Status | Count |
|---|---|
| Routes with real content | ~40 |
| Routes pointing to `demodocument.html` placeholder | ~120 |
| **Total routes** | **160** |

The majority of remaining work is migrating the ~120 placeholder routes to real HTML pages — primarily by running the pipeline on source PDFs from `O:\git\paye-employers-documentation`.

---

## 10. Source PDFs Location

All source PDFs are in the legacy project:

```
O:\git\paye-employers-documentation\
```

The directory structure mirrors the destination `content/` structure. When migrating a new document:

1. Find the PDF in `O:\git\paye-employers-documentation\`
2. Copy it to the appropriate `content/PIT3/` or `content/PIT4/` subdirectory
3. Run the pipeline
4. Run any document-specific fix script if one exists
5. Review the output HTML in the browser
6. Commit and push to `dev_contentMigration`

---

## 11. Compiling SCSS

```powershell
node "C:\NodeJs\node-v22.14.0-win-x64\node_modules\sass\sass.js" `
  "assets/css/styles.scss" `
  "assets/css/styles.css" `
  --no-source-map `
  --silence-deprecation=import `
  --silence-deprecation=global-builtin `
  --silence-deprecation=color-functions
```

---

## 12. Git Workflow

```powershell
git status --short
git add -A
git commit -m "Descriptive message"
git push origin dev_contentMigration
```

> The `fatal: could not write multi-pack-index: Permission denied` warning on commit is a known VM issue — it does not affect the commit or push.

---

## 13. Python Environment

- **Python version:** 3.11 (`C:/Program Files/Python3.11/python.exe`)
- **Key packages:** `PyMuPDF` (fitz), `pdfplumber`, `Pillow`
- All migration scripts are in `migrationScripts/`, `create_page/`, and `tools/`

---

## 14. Further Reading

- [`PROJECT_ASSESSMENT.md`](PROJECT_ASSESSMENT.md) — full architecture, design decisions, outstanding work
- [`MIGRATION_STATUS.md`](MIGRATION_STATUS.md) — detailed asset migration tracking
- [`README.md`](README.md) — project overview and quick start
