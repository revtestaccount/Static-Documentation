# Project Assessment — Static Documentation Site

> **Last updated:** 2026-06-16  
> **Active branch:** `dev_contentMigration`  
> **Total commits:** ~140  

---

## 1. Project Overview

**Static-Documentation** is a replacement for the legacy `paye-employers-documentation` project, which was built on deprecated AngularJS and had become difficult to maintain. The new project is a fully static site — plain HTML, CSS, and vanilla JavaScript — with no framework dependency, served by any static web server.

**Source project:** `O:\git\paye-employers-documentation` (AngularJS, deprecated)  
**FAQ project:** `O:\git\paye-employers-pit-faq` (Angular 14, now integrated)  
**Replacement project:** `O:\git\Static-Documentation` (static HTML/CSS/JS)

### Deployments

| Environment | URL | Audience | Notes |
|---|---|---|---|
| **Internal test** | https://revtestaccount.github.io/Static-Documentation/ | Revenue staff only | Current dev build — never share externally |
| **Pre-release (legacy)** | https://revtestaccount.github.io/paye-employers-documentation/ | Revenue staff only | Test/approval of old project — never share externally |
| **Public release** | https://revenue-ie.github.io/paye-employers-documentation/ | Software integrators (public) | Live public-facing site |

On completion, Static-Documentation will replace `paye-employers-documentation` at the public URL.

---

## 2. Architecture

### Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| Markup | Plain HTML5 | Fragment files loaded into `#content` div by router |
| Styling | SCSS → CSS | Compiled via `sass` CLI. Revenue Design System (REVDS) tokens |
| Scripting | Vanilla JavaScript | Single-page router in `assets/js/router.js` |
| Navigation | `assets/js/sitemap.json` | Defines all routes and nav groups |
| Build | Sass CLI only | No bundler, no build step for HTML/JS |
| CI/CD | Jenkins (planned) | Manual deployment currently |
| CSS framework | Bootstrap 5.3 (CDN) | Used for grid/cards — planned for removal |

### Key Files

| File | Purpose |
|---|---|
| `index.html` | Shell — header, navbar, content div, footer |
| `assets/js/router.js` | Hash-based SPA router, nav builder, content loader |
| `assets/js/sitemap.json` | Route map: URL hash → HTML template + title |
| `assets/css/styles.scss` | Master stylesheet (imports REVDS tokens + component partials) |
| `assets/css/styles.css` | Compiled output — this is what the browser loads |
| `content/shared/*.html` | Shared page content fragments |
| `content/PIT3/*.html` | PIT3-specific page content fragments |
| `content/PIT4/*.html` | PIT4-specific page content fragments |

### Routing Model

The router reads `sitemap.json` and maps URL hashes to HTML fragment files:

```
index.html#guidesandusefulinfo
    → loads content/shared/pit-guides.html into #content div
    → sets document.title from sitemap entry
    → builds navbar dropdown from _nav_groups
```

Routes prefixed with `_` (e.g., `_nav_groups`, `_home_nav`) are utility groups used for nav rendering only and are skipped during content lookup.

---

## 3. Branch Structure

| Branch | Purpose | Status |
|---|---|---|
| `main` | Production baseline | Stable |
| `dev_traditionalNavbar` | Navbar redesign + CSS overhaul | Active — styling work |
| `dev_contentMigration` | Content migration from source projects | Active — current branch |
| `dev_cssEdits` | CSS experiments | Parked |
| Others (`addingSass`, `routing`, etc.) | Historical feature branches | Archived/merged |

**Branching convention:** Feature branches off `dev_traditionalNavbar` for styling; `dev_contentMigration` (branched from `dev_traditionalNavbar`) for content work. No direct commits to `main`.

---

## 4. Design System

### Revenue Design System (REVDS)

- **Primary colour:** `#025F63` (Revenue Green / `$base-brandteal`)
- **Border radius:** `0` everywhere — squared corners always
- **Font (internal apps):** Segoe UI 14px
- **Accessibility:** WCAG 2.1 AA target
- **SCSS tokens:** imported from `assets/css/abstracts/`

### Three-Band Header Layout

```
┌─────────────────────────────────────────┐
│  Header util bar  (#brandteal-darken-10) │  ← context label + Help link
├─────────────────────────────────────────┤
│  Main header      (#025F63)              │  ← Revenue logo + app name
├─────────────────────────────────────────┤
│  Navbar           (#brandteal-darken-10) │  ← nav links + dropdown menus
└─────────────────────────────────────────┘
```

### Card Grid

- Cards use Bootstrap `.row`/`.col-sm` grid
- `.home-card` — `width: 18rem`, `height: 100%`, flexbox column layout
- Equal card heights achieved via `flex: 1` on `.card-body` and fixed `height: 8rem` on `.card-img-top`
- Row gap: `.container .row + .row { margin-top: 2rem }`
- Top gap when paragraph precedes cards: `p ~ .container > .row:first-child { margin-top: 2rem }`

---

## 5. Content Status

### Routes

| Category | Count |
|---|---|
| Routes with real content | **38** |
| Routes still pointing to `demodocument.html` placeholder | **122** |
| Total routes defined | **160** |

### Asset Files in `content/`

| Type | Count |
|---|---|
| `.html` | 1,182 |
| `.png` | 1,231 |
| `.JSON` | 490 |
| `.pdf` | 66 |
| `.css` | 61 |
| `.js` | 54 |
| `.zip` | 52 |
| `.svg` | 20 |
| `.csv` | 19 |
| `.xsd` | 14 |
| `.wsdl` | 12 |
| `.xlsx` | 7 |
| `.gif` | 6 |
| `.pptx` | 2 |
| `.jpg` | 2 |

### Bulk-Migrated Units (complete)

| Unit | Files |
|---|---|
| PIT3 SOAP schema reference (topic*.html + images) | ~1,237 |
| PIT4 SOAP schema reference (topic*.html + images) | ~1,236 |
| PIT3 SOAP v1 schemas & WSDLs | 13 |
| PIT4 SOAP v1 schemas & WSDLs | 13 |
| PIT3 REST API reference | 5 |
| PIT4 REST API reference | 5 |

### Integrated External Projects

| Project | Original Tech | Status |
|---|---|---|
| `paye-employers-pit-faq` | Angular 14 / PrimeNG accordion | ✅ Fully integrated as `content/shared/faq.html` — native `<details>`/`<summary>` accordion, no JS required |

---

## 6. Completed Work

### Infrastructure & Architecture
- ✅ Project scaffolded — plain HTML/SCSS/JS replacing AngularJS
- ✅ Hash-based SPA router implemented (`router.js`)
- ✅ `sitemap.json` — all routes defined (160 total)
- ✅ Three-band REVDS header layout
- ✅ Responsive navbar with Bootstrap collapse + dropdown menus
- ✅ `node_modules` removed from git tracking; `.gitignore` updated
- ✅ Bootstrap 5 loaded from CDN (planned for removal)

### Styling (branch: `dev_traditionalNavbar`)
- ✅ REVDS colour tokens corrected (`#025F63` Revenue Green)
- ✅ `px` → `rem` throughout `styles.scss`
- ✅ Equal-height card grid — flexbox, fixed image height, `height: 100%`
- ✅ Inline `style="width: 18rem"` removed from all card HTML — centralised to CSS
- ✅ `body main .card` specificity conflict resolved
- ✅ Prose text constrained to match Bootstrap container breakpoints at all viewports
- ✅ Cards centred within columns via `justify-content: center`
- ✅ Row gaps: `2rem` between card rows, `2rem` above first row when preceded by paragraph
- ✅ BOM character stripped from `home.html`
- ✅ Mojibake fixed in `home.html` (smart quotes, en-dash)
- ✅ `tools/fix_mojibake.py` utility added

### Content
- ✅ Lorem ipsum placeholder text removed from all card pages
- ✅ 74 missing assets copied from `paye-employers-documentation` (PDFs, XLSXs, CSVs, PPTXs, ZIPs)
- ✅ FAQ integrated from `paye-employers-pit-faq` Angular project
- ✅ FAQ link in `pit-guides.html` updated from external GitHub Pages URL to internal `#faq` route
- ✅ `demodocument.html` retained as a scaffold/demo page (intentional)

---

## 7. Outstanding Work

### High Priority
- ❌ **122 routes** still pointing to `demodocument.html` placeholder — need real content pages authored
- ❌ **WYSIWYG page editor** — bare-bones editor in place; needs improvement to support all pipeline-generated components (TOC, tables, code blocks, headings, lists) and editing of existing pages
- ❌ **Public/internal feature gating** — editor and all page-editing scripts must be excluded from public release deployment; gating mechanism to be designed and implemented
- ❌ **Bootstrap removal** — replace `.row`, `.col-sm`, `.card`, `.container` with native CSS or REVDS equivalents; remove Bootstrap CDN from `index.html`
- ❌ **Font migration** — update to Nunito Sans stack (deferred)

### Content Pages Needed
These `sitemap.json` routes exist but have no real content yet:

| Section | Pages Needed |
|---|---|
| PIT Guides | Conformance Testing Scenarios, Help Desk Registration, Help Desk Login, PIT Next Version Features |
| PMOD PIT3 | All 6 child pages (self-service, guide, SOAP, REST, supporting docs, examples) |
| PMOD PIT4 | All 6 child pages |
| ERR PIT3 | ERR Supporting Documentation |
| ERR PIT4 | ERR Supporting Documentation |
| Screens | All ROS Payroll Reporting sub-pages |
| Guide | Documentation Guide, Schema Publication Changelog, Compression Guide |
| SOAP | All SOAP sub-pages (definitions, schemas, guides) |
| REST | All REST sub-pages (OpenAPI spec, integration guides) |
| Supporting Docs | All data items, validation rules, error message guide pages |
| Examples | All 10 PAYE Modernisation life-cycle examples |
| Scenarios | PSDA Scenarios |

### Technical Debt
- ❌ `sitemap.json` location — currently in `assets/js/`; consider moving to project root
- ❌ SOAP schema topic pages — generated HTML with legacy `charset=windows-1252` meta; legitimate UTF-8 content but inconsistent meta declarations
- ❌ `demodocument.html` — contains Lorem ipsum intentionally; should be removed before production
- ❌ Validation rules XLSX files not yet linked from content pages
- ❌ Some content HTML paths use mixed case (`Screens`, `Scenarios`) — normalised to lowercase on copy but source paths differ

---

## 8. PDF Migration Pipeline

A full PDF → HTML migration pipeline is now in place across three scripts:

### Scripts

| Script | Location | Purpose |
|---|---|---|
| `pdfToMarkdown.py` | `migrationScripts/` | PDF → Markdown (PyMuPDF + pdfplumber) |
| `convert_new.py` | `create_page/` | Markdown → site-ready HTML with TOC |
| `migration_pipeline.py` | `tools/` | Single-command orchestrator — runs both scripts in sequence |
| `fix_rest_endpoints_table.py` | `tools/` | Post-pipeline fixes for REST Web Service Integration Guide |
| `fix_pre_tabindex.py` | `tools/` | Patches missing `tabindex="0"` on hand-authored `<pre>` elements (WCAG 2.1) |
| `accessibility_audit.py` | `tools/` | Static WCAG 2.1 AA audit across all migrated HTML files |

### Pipeline Usage
```
cd tools
python migration_pipeline.py "../content/PIT3/<section>/<doc>.pdf" --pit PIT3
python migration_pipeline.py "../content/PIT4/<section>/<doc>.pdf" --pit PIT4
```

### What the Pipeline Does Automatically
1. Converts PDF → Markdown (font-size heading detection, image extraction, table merging)
2. Converts Markdown → HTML (TOC generation, bullet conversion, REVDS classes)
3. Injects `<head>` with correct relative stylesheet path
4. Injects SVG branding block after `<h1>`
5. Adds `tabindex="0"` to all `<table>` and `<pre>` elements (WCAG 2.1.3)
6. Validates environment hostnames (PIT3 vs PIT4)
7. Updates `sitemap.json` route to point to HTML (not PDF)
8. Updates section listing page — changes `href` and badge from PDF to LINK

### pdfToMarkdown.py Improvements (implemented)
- ✅ Font-size heading detection (PyMuPDF `get_text("dict")`)
- ✅ pdfplumber table extraction with consecutive table merging
- ✅ Image deduplication (MD5 hash)
- ✅ Repeating header/footer suppression
- ✅ Visual TOC detection and suppression
- ✅ Bullet character (•) → markdown list conversion
- ✅ Sub-bullet (`o `) → indented markdown list item
- ✅ Code block detection (HTTP methods, headers, signature components)
- ✅ `(request-target):` and signature lines detected as code blocks
- ✅ Split URL fragment joining before linkification
- ✅ Page 1 images suppressed (cover logos replaced by SVG branding block)
- ✅ Paragraph joining for flowing body text

### Known Remaining Limitations (manual fix required after pipeline)
- Complex multi-column tables split across PDF page breaks may not merge cleanly — use `fix_rest_endpoints_table.py` as a template for document-specific fix scripts
- HTTP example blocks formatted as PDF tables may render as `<table>` not `<pre><code>` — fixed for REST Web Service Integration Guide
- Cover page version history tables may have phantom empty columns from merged PDF cells
- Visual TOC suppression works across blocks but relies on heading numbering patterns — verify on each new document
- Appendix numbered lists where PDF indents continuation lines need manual cleanup
- Footnote paragraphs may be merged into a single `<p>` by the pipeline — may need splitting post-migration

---

## 9. Accessibility

### WCAG 2.1 AA Compliance
All migrated HTML pages target WCAG 2.1 AA compliance. The following measures are in place:

- `<html lang="en">` on all hand-authored pages
- `<title>` element present and descriptive
- `tabindex="0"` on all `<table>` and `<pre>` elements (keyboard scrollability)
- `scope="col"` / `scope="row"` on all `<th>` elements
- Decorative SVG images marked `alt="" role="presentation"`
- TOC links use `href="#id"` anchors (not `javascript:void(0)`)
- Heading hierarchy checked — no skipped levels

### Tooling
- **`tools/accessibility_audit.py`** — static WCAG 2.1 AA audit script; run against all migrated HTML files
- **`tools/fix_pre_tabindex.py`** — run against any HTML file containing hand-authored `<pre>` blocks to ensure `tabindex="0"` is present
- **Axe DevTools** — in-browser tool used for runtime checks (colour contrast, focus order, dynamic ARIA)

### Audit Workflow
1. Run `python tools/accessibility_audit.py` after each migration
2. Run `python tools/fix_pre_tabindex.py <file>` after hand-authoring any `<pre>` blocks
3. Run Axe DevTools in-browser on each migrated page
4. Report findings; fix in HTML and/or update pipeline scripts to prevent recurrence

---

## 10. Known Issues

| Issue | Impact | Status |
|---|---|---|
| Bootstrap CDN dependency | External dependency; minor CORS risk | Planned for removal |
| `demodocument.html` as 120 route placeholder | Users see demo content instead of real pages | Accepted — content authoring in progress |
| SOAP schema topic HTML has legacy meta charset | No visible issue; browser handles correctly | Low priority |
| Some file names contain spaces | Works on Windows/Mac; potential issues on Linux servers | Monitor |
| PIT3 REST Web Service Integration Guide PDF contains wrong hostname | `softwaretestnextversion.ros.ie` in signature example | Fixed manually post-migration via PowerShell replace; source PDF error |
| REST Web Service Integration Guide tables split across PDF page breaks | Section 2.1, 4.1.3 tables and HTTP example block render incorrectly | Fixed via `tools/fix_rest_endpoints_table.py` — run after pipeline for this document |

---

## 9. Development Notes

### Compiling CSS
```powershell
node "C:\NodeJs\node-v22.14.0-win-x64\node_modules\sass\sass.js" `
  "assets/css/styles.scss" `
  "assets/css/styles.css" `
  --no-source-map `
  --silence-deprecation=import `
  --silence-deprecation=global-builtin `
  --silence-deprecation=color-functions
```

### Adding a New Route
1. Add entry to `assets/js/sitemap.json` in the appropriate `routes*` group
2. Add route key to `_nav_groups.children` array if it should appear in nav dropdown
3. Create the HTML fragment file at the path specified in `template`
4. Compile SCSS if styling changes were made

### Content HTML Fragment Structure
Content files are HTML fragments (no `<html>/<head>/<body>` required for most, though some include them). They are fetched and injected into `#content` by the router. Stylesheets from the main `index.html` apply automatically.
