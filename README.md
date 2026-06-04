# Revenue static site generator

Application used for the creation, maintenance and static deployment of Revenue articles.

Deployed link:

https://revtestaccount.github.io/Static-Documentation/


# Important
Run: `npm run watch:scss` to ensure SCSS compiles.

---

## Project Overview — PAYE Modernisation Web Services Documentation Site

A **static documentation portal** for Revenue's PAYE Modernisation Public Interface Testing (PIT) environment. It serves technical documentation (PDFs, schemas, WSDLs, examples) to external software developers integrating with Revenue's PAYE web services.

---

## Architecture

### Single Page App with Hash-Based Routing

```
index.html  ←  loads router.js
               ↓
           reads sitemap.json  →  maps URL hash to template file
               ↓
           injects template HTML into #content div
           injects sidebar links into #sidebarLinks div
```

- **`index.html`** — Shell page. Bootstrap 5 grid layout with a fixed header, a sidebar `<nav>`, and a `<main>` content area. The Revenue logo and page title live here.
- **`assets/js/router.js`** — Vanilla JS hash router. Watches `window.location.hash`, looks up the route in `sitemap.json`, fetches the corresponding template HTML, and injects it into the page. Also builds the sidebar nav dynamically from the route group.
- **`assets/js/sitemap.json`** — The routing table. Organised into route groups (`general_routes`, `routes1`–`routes15`). Each group represents a section. Within a group, one entry is the "parent" page (e.g. `home2`) and the rest are child document entries (currently pointing to `demodocument.html` as placeholders).

---

## Template Structure

### `home*.html` — Section Landing Pages

The 13 `home*.html` files are the section landing pages. Each maps to a route group in `sitemap.json`:

| File | Route Group | Section |
|---|---|---|
| `pit-guides.html` | `routes1` | Public Interface Testing – Guides and useful info |
| `pit3-self-service.html` | `routes3` | PIT Self Service and ROS Payroll Reporting – Current Version |
| `pit3-guide.html` | `routes4` | Guide – Current Version |
| `pit3-soap.html` | `routes5` | PAYE Web Service Specifications (SOAP/XML) – Current Version |
| `pit3-rest.html` | `routes6` | PAYE Web Service Specifications (REST/JSON) – Current Version |
| `pit3-supporting-docs.html` | `routes7` | Supporting Documentation – Current Version |
| `pit3-examples.html` | `routes8` | PAYE Web Service Examples – Current Version |
| `pit4-self-service.html` | `routes10` | PIT Self Service and ROS Payroll Reporting – Next Version |
| `pit4-guide.html` | `routes11` | Guide – Next Version |
| `pit4-soap.html` | `routes12` | PAYE Web Service Specifications (SOAP/XML) – Next Version |
| `pit4-rest.html` | `routes13` | PAYE Web Service Specifications (REST/JSON) – Next Version |
| `pit4-supporting-docs.html` | `routes14` | Supporting Documentation – Next Version |
| `pit4-examples.html` | `routes15` | PAYE Web Service Examples – Next Version |

### Hub / Card Pages

Two hub pages act as navigation intermediaries between the root landing page and the section pages:

- **`pmodpit3cards.html`** (`routes2`) — PMOD PIT3 (Current Version) hub. Bootstrap card grid linking to `pit3-self-service` through `pit3-examples`.
- **`pmodpit4cards.html`** (`routes9`) — PMOD PIT4 (Next Version) hub. Bootstrap card grid linking to `pit4-self-service` through `pit4-examples`.
- **`errpit3cards.html`** (`routes16`) — ERR PIT3 (Current Version) hub. Bootstrap card grid linking to `err-pit3-soap`, `err-pit3-rest`, and `err-pit3-supporting-docs`.
- **`errpit4cards.html`** (`routes17`) — ERR PIT4 (Next Version) hub. Bootstrap card grid linking to `err-pit4-soap`, `err-pit4-rest`, and `err-pit4-supporting-docs`.

### Root Landing Page

- **`home.html`** — Root page (`/`). Bootstrap card grid with 6 top-level section links (PIT Guides, PMOD PIT3, PMOD PIT4, ERR PIT3, ERR PIT4, Support).

---

## Styling

- **`assets/css/styles.scss`** — Main stylesheet compiled via Sass. Imports Revenue Design System abstracts (`$base-brandteal`, `$base-white`, `$bold-font-weight`, etc.) and all component/page partials.
- **Bootstrap 5.3.2** — Loaded via CDN in `index.html`. Used for the grid layout, sidebar, cards, and general structure.
- **PrimeNG / PrimeIcons** — npm dependencies used within the Revenue Design System.

### `.pit-section` BEM Component

All 13 section pages (`home1.html`–`home13.html`) use a shared `.pit-section` BEM block defined in `styles.scss`. It provides:
- Revenue Green (`#025F63`) section header bar
- Semantic `<table>` for document listings
- Colour-coded file type badges (squared corners per Revenue conventions)
- Footnote reference superscripts and footnote blocks
- Row hover states

#### Badge Variants

| Class | Colour | Used for |
|---|---|---|
| `pit-section__badge--pdf` | Red `#d9534f` | PDF documents |
| `pit-section__badge--link` | Revenue Green `#025F63` | External/internal links |
| `pit-section__badge--zip` | Purple `#6f42c1` | ZIP archive files |
| `pit-section__badge--schema` | Blue `#0d6efd` | JSON/XSD schema files |
| `pit-section__badge--csv` | Green `#198754` | CSV data files |
| `pit-section__badge--xlsx` | Dark green `#1d6f42` | Excel XLSX files |
| `pit-section__badge--excel` | Dark green `#1d6f42` | Excel files (labelled "Excel File") |
| `pit-section__badge--wsdl` | Grey `#6c757d` | WSDL web service definition files |
| `pit-section__badge--api` | Indigo `#6610f2` | OpenAPI specification files |

---

## Key Conventions

- **`PIT3` = Current Version, `PIT4` = Next Version** — consistent throughout asset paths, template names, and route keys.
- **`sitemap.json` drives everything** — new pages need a route entry here; new sections need a new route group.
- **The sidebar is dynamic** — rendered from all routes in the current route group. The router derives `href` values by lowercasing the route title and stripping spaces.
- **Child document routes** — most still point to `demodocument.html` as placeholders. The migration work in `migrationScripts/` is progressively replacing these with real rendered content.
- **SOAP Schema Reference and REST API Reference links** — hard-coded in `router.js` to open in a new tab (these are standalone HTML reference sites, not injected templates).

---

## Directory Structure

```
├── index.html                  # SPA shell
├── assets/
│   ├── css/
│   │   ├── styles.scss         # Main SCSS entry point
│   │   ├── styles.css          # Compiled output (do not edit directly)
│   │   ├── abstracts/          # SCSS variables, mixins, functions
│   │   ├── components/         # Component-level SCSS partials
│   │   ├── pages/              # Page-level SCSS partials
│   │   └── vendors/            # PrimeNG designer theme files
│   ├── js/
│   │   ├── router.js           # Hash-based SPA router
│   │   └── sitemap.json        # Route configuration table
│   └── images/
│       └── ictl_logo.png       # Revenue logo
├── templates/
│   ├── home.html               # Root landing page
│   ├── pit-guides.html         # PIT Guides and useful info
│   ├── pit3-self-service.html  # PIT Self Service – Current Version
│   ├── pit3-guide.html         # Guide – Current Version
│   ├── pit3-soap.html          # SOAP/XML specs – Current Version
│   ├── pit3-rest.html          # REST/JSON specs – Current Version
│   ├── pit3-supporting-docs.html # Supporting docs – Current Version
│   ├── pit3-examples.html      # Web service examples – Current Version
│   ├── pit4-self-service.html  # PIT Self Service – Next Version
│   ├── pit4-guide.html         # Guide – Next Version
│   ├── pit4-soap.html          # SOAP/XML specs – Next Version
│   ├── pit4-rest.html          # REST/JSON specs – Next Version
│   ├── pit4-supporting-docs.html # Supporting docs – Next Version
│   ├── pit4-examples.html      # Web service examples – Next Version
│   ├── pmodpit3cards.html      # PMOD PIT3 hub/card page
│   ├── pmodpit4cards.html      # PMOD PIT4 hub/card page
│   ├── errpit3cards.html       # ERR PIT3 hub/card page
│   ├── errpit4cards.html       # ERR PIT4 hub/card page
│   ├── demodocument.html       # Placeholder for child document routes
│   ├── 404.html                # Not found page
│   ├── soap/                   # SOAP schema files (WSDLs, XSDs)
│   └── home/                   # SVG icons used on landing/hub pages
├── create_page/
│   ├── create_page.html        # In-browser content authoring tool
│   └── create_page_script.js   # Authoring tool logic
├── migrationScripts/
│   ├── pdfToMarkdown.py        # Converts PDFs to Markdown
│   ├── extractImagesFromPdf.py # Extracts images from PDFs
│   └── [document folders]/     # Converted Markdown + images output
└── package.json                # npm scripts and dependencies
```

---

## Development

### Prerequisites

- Node.js and npm
- Sass (installed via npm)

### Setup

```bash
npm install
```

### Compile SCSS

```bash
npm run watch:scss
```

This watches `assets/css/styles.scss` and compiles to `assets/css/styles.css` on every save.

### Running Locally

Serve the project root with any static file server, for example:

```bash
npx serve .
```

Then open `http://localhost:3000` in your browser.

> **Note:** The router uses `fetch()` to load templates, so the site must be served over HTTP — opening `index.html` directly as a `file://` URL will not work.