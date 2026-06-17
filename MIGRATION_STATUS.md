# Migration Status

> **Last updated:** 2026-06-16  
> **Branch:** `dev_contentMigration` (branched from `dev_traditionalNavbar`)  
> **Total commits:** ~140

---

## Deployments

| Environment | URL | Audience |
|---|---|---|
| **Internal test** | https://revtestaccount.github.io/Static-Documentation/ | Revenue staff only — never share externally |
| **Pre-release (legacy)** | https://revtestaccount.github.io/paye-employers-documentation/ | Revenue staff only — never share externally |
| **Public release** | https://revenue-ie.github.io/paye-employers-documentation/ | Software integrators (public) |

On completion, Static-Documentation will replace `paye-employers-documentation` at the public URL. The WYSIWYG editor and all page-editing scripts must not be present in the public release.

---

## Summary

`paye-employers-documentation` (AngularJS) → `Static-Documentation` (plain HTML/CSS/JS)  
`paye-employers-pit-faq` (Angular 14) → integrated as `content/shared/faq.html`

### Binary Asset Migration

| Type | Source | Destination | Status |
|---|---|---|---|
| PDF | 66 | 66 | ✅ Complete |
| ZIP | 52 | 52 | ✅ Complete |
| XLSX | 7 | 7 | ✅ Complete |
| CSV | 15 | 19 | ✅ Complete (destination has extras) |
| PPTX | 2 | 2 | ✅ Complete |

### Route Coverage

| Category | Count |
|---|---|
| Routes with real content | **40** |
| Routes pointing to `demodocument.html` placeholder | **120** |
| **Total routes defined in sitemap.json** | **160** |

---

## Completed

### Infrastructure
- ✅ Static site scaffold — plain HTML/SCSS/JS, no framework
- ✅ Hash-based SPA router (`assets/js/router.js`)
- ✅ `sitemap.json` — all 160 routes defined
- ✅ Three-band REVDS header (utility bar / main header / navbar)
- ✅ Responsive navbar — Bootstrap collapse + Revenue-styled dropdowns
- ✅ `node_modules` excluded from git

### Styling
- ✅ REVDS colour tokens corrected (`#025F63` Revenue Green)
- ✅ All `px` values converted to `rem` in `styles.scss`
- ✅ Equal-height card grid — flexbox, `height: 100%`, fixed image area
- ✅ Inline `style="width: 18rem"` removed from all card HTML (24 occurrences)
- ✅ `body main .card` specificity conflict resolved
- ✅ Prose text width constrained to match Bootstrap container breakpoints
- ✅ Cards centred within columns
- ✅ `2rem` gap between card rows; `2rem` top gap when paragraph precedes cards
- ✅ Lorem ipsum removed from all card pages
- ✅ BOM character stripped from `home.html`
- ✅ Mojibake fixed in `home.html` (smart quotes, en-dash restored)
- ✅ `tools/fix_mojibake.py` utility script added

### Content Migration
- ✅ All 66 PDFs migrated from source project
- ✅ All 52 ZIP files migrated
- ✅ All 7 XLSX files migrated
- ✅ All CSV and PPTX files migrated
- ✅ PIT3 + PIT4 SOAP schema reference browsers (topic*.html, ~2,473 files total)
- ✅ PIT3 + PIT4 SOAP v1 WSDLs and XSDs (26 files)
- ✅ PIT3 + PIT4 REST API reference HTML/JSON (10 files)
- ✅ PIT3 + PIT4 JSON/XML scenario files (~490 JSON files)
- ✅ PAYE PIT Help Desk User Guide (`content/pit/payepithelpdeskuserguide.html`)
- ✅ PIT Self-Service Guide (`content/pit/pitselfserviceguide.html`)

### PDF → HTML Migration (new)
- ✅ PIT3 REST Web Service Integration Guide (`content/PIT3/rest/rest_web_service_integration_guide.html`)
- ✅ PIT3 REST Connectivity Handshake Guide (`content/PIT3/rest/rest_connectivity_handshake_guide.html`)
- ✅ PIT4 REST Web Service Integration Guide (`content/PIT4/rest/rest_web_service_integration_guide.html`)
- ✅ PIT4 REST Connectivity Handshake Guide (`content/PIT4/rest/rest_connectivity_handshake_guide.html`)

### Tooling (new)
- ✅ `migrationScripts/pdfToMarkdown.py` — PDF → Markdown (PyMuPDF + pdfplumber, heading detection, table merging, image deduplication)
- ✅ `create_page/convert_new.py` — Markdown → HTML (TOC, REVDS classes, bullet conversion, tabindex, stylesheet injection)
- ✅ `tools/migration_pipeline.py` — single-command pipeline (PDF → MD → HTML → sitemap update → listing page update)
- ✅ `tools/fix_rest_endpoints_table.py` — post-pipeline fixes for REST Web Service Integration Guide (section 2.1 table, 4.1.3 table, footnote ordering, code blocks, version history spillover)
- ✅ `tools/fix_pre_tabindex.py` — patches missing `tabindex="0"` on hand-authored `<pre>` elements (WCAG 2.1 keyboard accessibility)
- ✅ `tools/accessibility_audit.py` — static WCAG 2.1 AA audit across all migrated HTML files

### External Project Integration
- ✅ `paye-employers-pit-faq` (Angular 14 / PrimeNG accordion) → `content/shared/faq.html`
  - Native `<details>`/`<summary>` accordion — no JS, fully accessible (WCAG)
  - 4 sections: TDM/Certificates, SOAP/REST, Common Errors, Reporting Issues
  - `pit-guides.html` FAQ link updated from external GitHub Pages URL to internal `#faq` route
  - `sitemap.json` `faq` route updated to point to new page

---

## Outstanding

### Content — Pages Still Needed (122 placeholder routes)

| Section | Routes Still Needed |
|---|---|
| PIT Guides | Conformance Testing Scenarios, Help Desk Registration, Help Desk Login, PIT Next Version Features |
| PMOD PIT3 | Self-service guide, Guide, SOAP specs, REST specs, Supporting docs, Examples |
| PMOD PIT4 | Self-service guide, Guide, SOAP specs, REST specs, Supporting docs, Examples |
| ERR PIT3 | Supporting Documentation |
| ERR PIT4 | Supporting Documentation |
| Screens (PIT3 + PIT4) | Portal login, Self-service guide, Payroll reporting guide, Message guide, JSON examples, Schema, CSV responses |
| Guide (PIT3 + PIT4) | Documentation guide, Schema changelog, Compression guide |
| SOAP (PIT3 + PIT4) | All service definitions, schemas, integration guides, examples, handshake guides |
| REST (PIT3 + PIT4) | OpenAPI spec, sample messages |
| REST PIT3 + PIT4 | Sample messages page |
| Supporting Docs (PIT3 + PIT4) | Data items, validation rules, error guide, line item correction, employment ID guide, regulations |
| Examples (PIT3 + PIT4) | All 10 life-cycle examples, ERR scenarios, REST auth presentation |
| Scenarios | PSDA Scenarios |

### Technical
- ❌ Bootstrap removal — replace `.row`, `.col-sm`, `.container` with native CSS
- ❌ Font migration — Nunito Sans stack (deferred pending decision)
- ❌ `sitemap.json` move to project root (currently `assets/js/`)
- ❌ Validation rules XLSX files not yet linked from content pages
- ❌ `demodocument.html` to be removed before production go-live
- ❌ ERR supporting docs pages (PIT3 + PIT4) still point to `demodocument.html`

### WYSIWYG Editor
- ❌ Improve editor to support all pipeline-generated components (TOC, tables, code blocks, headings, lists)
- ❌ Add ability to edit existing pages (not just create new ones)
- ❌ Design and implement public/internal feature gating — editor must not appear in public release deployment

---

## Bulk-Migrated Units

> Tracked as complete units — not file-by-file.

| Unit | Files | Status |
|---|---|---|
| PIT3 SOAP schema reference | ~1,237 | ✅ |
| PIT4 SOAP schema reference | ~1,236 | ✅ |
| PIT3 SOAP v1 schemas & WSDLs | 13 | ✅ |
| PIT4 SOAP v1 schemas & WSDLs | 13 | ✅ |
| PIT3 REST API reference | 5 | ✅ |
| PIT4 REST API reference | 5 | ✅ |
| PIT3 JSON scenarios | ~250 | ✅ |
| PIT4 JSON scenarios | ~240 | ✅ |
