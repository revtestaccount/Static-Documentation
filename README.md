# PAYE Modernisation Web Services — Documentation Site

A static documentation portal for Revenue's PAYE Modernisation Public Interface Testing (PIT) environments. Serves technical documentation — PDFs, schemas, WSDLs, JSON/XML examples — to external software developers integrating with Revenue's PAYE web services.

**Deployed:** https://revtestaccount.github.io/Static-Documentation/

> **Replaces** the deprecated AngularJS project `paye-employers-documentation`.  
> **Integrates** the Angular 14 FAQ project `paye-employers-pit-faq` as native static HTML.

---

## Quick Start

### Prerequisites
- Node.js (for Sass compilation only)
- Any static file server (e.g. `npx serve`, Python `http.server`, Live Server)

### Compile SCSS

Compile once:
```
npm run build:scss
```

Compile and watch for changes during development:
```
npm run watch:scss
```

### Run Locally
```bash
npx serve .
```
Open `http://localhost:3000`. The router uses `fetch()` so the site **must** be served over HTTP — `file://` will not work.

---

## Architecture

### Single-Page App with Hash-Based Routing

```
index.html
  └─ router.js
       └─ reads sitemap.json
            └─ maps URL hash → HTML fragment file
                 └─ fetches fragment → injects into #content div
                 └─ builds navbar links from _nav_groups
```

| File | Role |
|---|---|
| `index.html` | Shell — header, navbar, `#content` div, footer |
| `assets/js/router.js` | Hash router, nav builder, content loader |
| `assets/js/sitemap.json` | Route table: hash key → template path + page title |
| `assets/css/styles.scss` | Master SCSS (imports REVDS tokens + partials) |
| `assets/css/styles.css` | Compiled output — do not edit directly |
| `content/shared/*.html` | Shared content fragments (home, cards, guides, FAQ) |
| `content/PIT3/*.html` | PIT3-specific content fragments |
| `content/PIT4/*.html` | PIT4-specific content fragments |

### Routing Convention

- Routes are defined in `assets/js/sitemap.json` as key → `{ template, title }` pairs
- `_`-prefixed keys (`_nav_groups`, `_home_nav`) are utility groups for nav rendering — skipped during content lookup
- Home page navbar renders flat links from `_home_nav`
- Inner page navbar renders a dropdown from the parent `_nav_groups` entry
- Four special child routes are hard-coded in `router.js` to open in a new tab (SOAP/REST schema references)

### Adding a New Route
1. Add an entry to `assets/js/sitemap.json` in the appropriate `routes*` group
2. Add the route key to the relevant `_nav_groups.children` array
3. Create the HTML fragment at the path given in `template`
4. Recompile SCSS if any styling changes were made

---

## Content Structure

### Page Types

| Type | Example | Description |
|---|---|---|
| Home / card grid | `content/shared/home.html` | Bootstrap card grid, top-level navigation |
| Section card hub | `content/shared/pmodpit3cards.html` | Card grid linking to section child pages |
| Document listing | `content/PIT3/soap.html` | `.pit-section` table of downloadable files |
| FAQ | `content/shared/faq.html` | Native `<details>`/`<summary>` accordion |
| Schema browser | `content/PIT3/soap/soap-schema-reference/` | Generated HTML from SOAP schema tool |
| REST API reference | `content/PIT3/rest/paye-employers-rest-api-pit3.html` | Swagger-generated reference |
| Placeholder | `content/shared/demodocument.html` | Temporary placeholder for unbuilt routes |

### Route Coverage (as of 2026-06-10)

| Status | Count |
|---|---|
| Routes with real content | 40 |
| Routes still using `demodocument.html` placeholder | 120 |
| **Total routes** | **160** |

### PIT3 vs PIT4

`PIT3` = Current Version (mirrors live environment)  
`PIT4` = Next Version (upcoming functionality)

All asset paths, route keys, and template names follow this convention consistently.

---

## Styling

### Revenue Design System (REVDS)

- **Primary colour:** `#025F63` (Revenue Green / `$base-brandteal`)
- **Border radius:** `0` — squared corners always, no exceptions
- **Font:** Segoe UI 14px (internal applications)
- **Sizing:** `rem` units throughout — no `px` in authored CSS (border widths use `px` per convention)
- **Accessibility:** WCAG 2.1 AA target

### Key CSS Components

#### `.pit-section` — Document Listing Block
Used on all section content pages. Provides:
- Revenue Green header bar
- Semantic `<table>` for document listings with hover states
- Colour-coded file type badges (squared corners)
- Footnote blocks

#### Badge Variants

| Class | Colour | File type |
|---|---|---|
| `--pdf` | Red `#d9534f` | PDF |
| `--link` | Revenue Green `#025F63` | External/internal link |
| `--zip` | Purple `#6f42c1` | ZIP archive |
| `--schema` | Blue `#0d6efd` | JSON/XSD schema |
| `--csv` | Green `#198754` | CSV |
| `--xlsx` / `--excel` | Dark green `#1d6f42` | Excel |
| `--wsdl` | Grey `#6c757d` | WSDL |
| `--api` | Indigo `#6610f2` | OpenAPI spec |

#### `.home-card` — Navigation Cards
- `width: 18rem`, `height: 100%` — equal-height cards in a row
- Fixed image area `height: 8rem` with `object-fit: contain`
- `flex: 1` on `.card-body` — vertically centres text regardless of line count
- Bootstrap `stretched-link` makes the entire card clickable

#### `.faq` — FAQ Accordion
- Native `<details>`/`<summary>` — no JavaScript required
- Revenue Green section title bars matching `.pit-section__header`
- CSS chevron rotates on open/close
- Fully keyboard accessible

---

## Directory Structure

```
├── index.html                        # SPA shell
├── README.md
├── PROJECT_ASSESSMENT.md             # Full project assessment and status
├── migration_status.md               # Asset migration tracking
├── assets/
│   ├── css/
│   │   ├── styles.scss               # Master SCSS entry point
│   │   ├── styles.css                # Compiled output (do not edit directly)
│   │   ├── abstracts/                # SCSS tokens — colours, fonts, lengths
│   │   ├── components/               # Component SCSS partials
│   │   └── vendors/                  # PrimeNG designer theme
│   ├── js/
│   │   ├── router.js                 # Hash-based SPA router + nav builder
│   │   └── sitemap.json              # All 160 route definitions
│   └── images/
│       └── ictl_logo.png             # Revenue logo
├── content/
│   ├── shared/                       # Shared pages (home, cards, guides, FAQ)
│   │   ├── home.html                 # Root landing page (6-card grid)
│   │   ├── faq.html                  # Integrated FAQ (was paye-employers-pit-faq)
│   │   ├── pit-guides.html           # PIT Guides section
│   │   ├── pmodpit3cards.html        # PMOD PIT3 hub
│   │   ├── pmodpit4cards.html        # PMOD PIT4 hub
│   │   ├── errpit3cards.html         # ERR PIT3 hub
│   │   ├── errpit4cards.html         # ERR PIT4 hub
│   │   ├── support.html              # Support Facilities
│   │   └── demodocument.html         # Placeholder (122 routes) — remove pre-production
│   ├── pit/                          # PIT Help Desk guides
│   ├── PIT3/                         # PIT3 content and assets
│   │   ├── *.html                    # Section content fragments
│   │   ├── soap/                     # SOAP schemas, WSDLs, schema browser
│   │   ├── rest/                     # REST API reference + examples
│   │   ├── examples/                 # ZIP/JSON/PDF examples
│   │   ├── scenarios/                # JSON/XML scenario files
│   │   ├── screens/                  # Screen upload examples + CSVs
│   │   ├── guide/                    # PDF guides
│   │   ├── data-items/               # PDF data item specs
│   │   └── validation-rules/         # XLSX validation rule files
│   └── PIT4/                         # PIT4 content and assets (mirrors PIT3)
├── templates/                        # Mirror of content/ (legacy — kept for reference)
├── migrationScripts/
│   ├── pdfToMarkdown.py              # PDF → Markdown converter (PyMuPDF + pdfplumber)
│   └── extractImagesFromPdf.py       # Image extraction utility (called by pdfToMarkdown)
├── create_page/
│   └── convert_new.py               # Markdown → HTML converter with TOC generation
├── tools/
│   ├── fix_mojibake.py              # Byte-level encoding fix utility
│   ├── fix_links.py                 # Batch link/badge updater
│   ├── update_migration_status.py   # Migration status tracker
│   ├── migration_pipeline.py        # Single-command PDF → HTML pipeline
│   └── accessibility_audit.py       # Static WCAG 2.1 AA audit tool
└── package.json
```

---

## Development Notes

### Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Production baseline |
| `dev_traditionalNavbar` | Navbar redesign + CSS overhaul (styling work) |
| `dev_contentMigration` | Content migration (branched from `dev_traditionalNavbar`) |

No direct commits to `main`. Feature branches are merged via PR.

### Key Conventions

- **All sizes in `rem`** — no `px` in authored CSS (border widths are the only accepted exception)
- **Squared corners always** — `border-radius: 0` everywhere, no exceptions
- **Revenue Green `#025F63`** — used for all header/navbar backgrounds
- **`demodocument.html`** — intentional placeholder; must be replaced with real content before production
- **SCSS must be recompiled** after any change to `.scss` files — run `npm run build:scss` or keep `npm run watch:scss` running during development

### Tools

| Tool | Purpose |
|---|---|
| `tools/fix_mojibake.py` | Fixes double-encoded UTF-8 smart quotes/dashes in HTML files |
| `tools/fix_links.py` | Batch link/badge updater for section listing pages |
| `tools/update_migration_status.py` | Updates migration status tracking |
| `tools/migration_pipeline.py` | Single-command PDF → Markdown → HTML migration pipeline |
| `tools/accessibility_audit.py` | Static WCAG 2.1 AA audit across all migrated HTML files |
| `migrationScripts/pdfToMarkdown.py` | Converts PDF to Markdown using PyMuPDF + pdfplumber |
| `create_page/convert_new.py` | Converts Markdown to site-ready HTML fragment with TOC |

### Further Documentation

- [`PROJECT_ASSESSMENT.md`](PROJECT_ASSESSMENT.md) — full architecture assessment, design decisions, outstanding work
- [`migration_status.md`](migration_status.md) — asset migration tracking from source projects