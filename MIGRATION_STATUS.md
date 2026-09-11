# Migration Status

> **Last updated:** 2026-09-09  
> **Branch:** `dev_contentMigration` (branched from `dev_traditionalNavbar`)  
> **Total commits:** ~141

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
| Routes with real content | **41** |
| Routes pointing to `demodocument.html` placeholder | **119** |
| **Total routes defined in sitemap.json** | **160** |

---

## Completed

### Infrastructure
- ✅ Static site scaffold — plain HTML/SCSS/JS, no framework
- ✅ Hash-based SPA router (`assets/js/router.js`)
- ✅ `sitemap.json` — all 160 routes defined
- ✅ Three-band REVDS header (utility bar / main header / navbar)
- ✅ Responsive navbar — vanilla JS hamburger toggle + CSS-only dropdown (Bootstrap-free)
- ✅ `node_modules` excluded from git

### Styling
- ✅ REVDS colour tokens corrected (`#025F63` Revenue Green)
- ✅ All `px` values converted to `rem` in `styles.scss`
- ✅ Bootstrap fully removed — home-grid/home-card BEM CSS, vanilla JS toggle, CSS-only dropdown
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
- ✅ Conformance Test Scenarios - Connectivity Testing (`content/pit/conformance test scenarios - connectivity testing.html`) — completed 2026-07-24. Fixed duplicate/garbage TOC and heading entries left over from the cover-page title split, rebuilt 3 phantom-column tables (Version History, Document References, Abbreviations and Acronyms) with proper `pit-section__table` styling, fixed a run-on list item and a run-on bullet list, split sections 4.1/4.2 back into their own independent test-definition tables (pipeline had incorrectly merged both scenarios' rows into a single table), and restored a truncated `<e.g. ...>` text fragment. Aligned the cover-page Version/Version Date fields into separate left/right-aligned rows per user feedback. Wired the `conformance` sitemap route (previously a `demodocument.html` placeholder) to the new page and updated the PIT Guides listing page link from a direct PDF link to an internal router link. Also fixed a site-wide CSS specificity bug found via axe DevTools testing on this page: `.document-content table.table thead th` and `.pit-section__table thead th` were both targeting the same `<th>` elements on tables carrying both classes, causing dark `#222` text to render on the teal header background instead of white — fixed in `assets/css/styles.scss` (affects all migrated documents using this dual-class table pattern, e.g. also `payepithelpdeskuserguide.html`).

### PDF → HTML Migration (new)
- ✅ PIT3 REST Web Service Integration Guide (`content/PIT3/rest/rest_web_service_integration_guide.html`)
- ✅ PIT3 REST Connectivity Handshake Guide (`content/PIT3/rest/rest_connectivity_handshake_guide.html`)
- ✅ PIT4 REST Web Service Integration Guide (`content/PIT4/rest/rest_web_service_integration_guide.html`)
- ✅ PIT4 REST Connectivity Handshake Guide (`content/PIT4/rest/rest_connectivity_handshake_guide.html`)
- ✅ PIT3 Overview of ROS Payroll Reporting (`content/PIT3/screens/overview_of_ros_payroll_reporting_pit3.html`)
- ✅ PIT4 Overview of ROS Payroll Reporting (`content/PIT4/screens/overview_of_ros_payroll_reporting_pit4.html`) — completed 2026-06-26. Fixed duplicate figure_15 reference before Figure 25 caption, extracted missing figure_28.png from source PDF (dropped by original pipeline run), confirmed TOC entry for section 3.5 (TWSS). Root cause patched in `tools/run_doc_fixes.py` (Fix 12a/12c) — image-reuse fixes were applying PIT3-specific quirks unconditionally; now guarded by file-existence checks per environment.
- ✅ PIT3 ROS Payroll Reporting Message Guide (`content/PIT3/screens/ros_payroll_reporting_message_guide.html`) — completed 2026-07-03. Fixed fragmented Version History / Document References / JSON Message Data Items / Schema Reference tables, removed 2 orphaned single-column fragment tables (pdfplumber cell-wrap splitting artefacts), moved Schema Reference table from Section 5 (Digital Signature) into its correct home under Section 4 (Schemas), and split run-on bullet list items in Sections 2 and 3 into proper separate `<li>` elements. Fixed via `tools/run_doc_fixes.py` (`fix_ros_payroll_message_guide`, Fixes 1–9).
- ✅ PIT4 ROS Payroll Reporting Message Guide (`content/PIT4/screens/ros_payroll_reporting_message_guide.html`) — completed 2026-07-03, same fixes as PIT3 above.
- ✅ PIT4 Temporary Wage Subsidy Scheme (TWSS) Operational Phase Description (`content/PIT4/screens/twss_operational_phase_csv_description.html`) — completed 2026-07-08, FULLY CONFIRMED 2026-07-09 (PIT4 only, no PIT3 equivalent document exists). Fixed the Column Descriptions/Latest Version History/Audience headings being bunched together with both tables misplaced near the end of the document instead of under their own headings; fixed the main data-dictionary table (Employer Name...Tier 3 MWWS), which had been fragmented by the PDF extraction into phantom-empty-column and wrongly-promoted-header-row pieces, was missing an entire 'EE PRSI paid' row, and had 2 continuation-only text fragments stranded as orphaned blank-cell rows instead of merged into their parent rows. Fixed via `tools/run_doc_fixes.py` (`fix_twss_operational_phase`). User visually confirmed the heading/table reorder in-browser (2026-07-08) and the main data table fix (2026-07-09) — EE PRSI paid row present, Tier 1 MWWS/Tier 3 continuation text merged correctly, no broken/orphaned rows. **Fully closed out.**
- 🟡 **IN PROGRESS** — PIT4 Temporary Wage Subsidy Scheme (TWSS) Reconciliation Description (`content/PIT4/screens/twss_reconciliation_csv_description.html`) — started 2026-07-09 (PIT4 only, no PIT3 equivalent document exists). `fix_twss_reconciliation()` and its registry entry now exist in `tools/run_doc_fixes.py` / `tools/doc_fixes_registry.json`. 2026-07-22: fixed an `IndentationError` that had made the fix function fail to parse at all (confirmed valid via `ast.parse`). However, the current on-disk HTML was generated by an earlier/incorrect version of the fix and still contains the **wrong** Latest Version History table content (TWSS Operational Phase's 4-row history instead of Reconciliation's own correct 1-row history). **The HTML on disk is NOT ready for review** — must be regenerated fresh from the pipeline plus the now-corrected fix function, then re-verified against source PDF ground truth. See `SESSION_LOG.md` 2026-07-22 entry for full detail.

### Tooling (new)
- ✅ `migrationScripts/pdfToMarkdown.py` — PDF → Markdown (PyMuPDF + pdfplumber, heading detection, table merging, image deduplication)
- ✅ `create_page/convert_new.py` — Markdown → HTML (TOC, REVDS classes, bullet conversion, tabindex, stylesheet injection)
- ✅ `tools/migration_pipeline.py` — single-command pipeline (PDF → MD → HTML → sitemap update → listing page update)
- ✅ `tools/run_doc_fixes.py` + `tools/doc_fixes_registry.json` — consolidated post-pipeline fix scripts (replaces all individual fix_*.py scripts)
- ✅ `tools/fix_pre_tabindex.py` — patches missing `tabindex="0"` on hand-authored `<pre>` elements (WCAG 2.1 keyboard accessibility)
- ✅ `tools/accessibility_audit.py` — static WCAG 2.1 AA audit across all migrated HTML files
- ✅ `tools/run_doc_fixes.py` Fix 12a/12c patched (2026-06-26) — fixed a string-concatenation bug (`'...' + env + '...'` inside single quotes, never interpolated) and added file-existence guards so PIT3-specific image-reuse quirks (figure_10→figure_7, figure_25→figure_15) are no longer applied unconditionally to environments that have their own genuine images
- ✅ `tools/run_doc_fixes.py` — new `fix_ros_payroll_message_guide()` function added (2026-07-03), registered in `tools/doc_fixes_registry.json` as `ros_payroll_message_guide`. Fixes 4 fragmented tables via clean literal replacement (following the established `ROS_CLEAN_VERSION_TABLE` pattern), removes 2 orphaned fragment tables, relocates the misplaced Schema Reference table to its correct section, and splits run-on bullet lists into individual `<li>` items
- ✅ `tools/migration_pipeline.py` — added Step 3.5, a cross-environment routing checker that flags `sitemap.json` routes where a PIT4 route's `template` path incorrectly points into `content/PIT3/...` (or vice versa) — added after this exact class of bug was found and fixed manually in `sitemap.json` (see below)

### Bug Fixes (new)
- ✅ `assets/js/sitemap.json` — fixed 3 cross-environment routing bugs (2026-07-03): the PIT4 `rospayrollreportingmessageguide.` route was pointing at the PIT3 HTML file instead of PIT4's own; the PIT4 `restwebserviceintegrationguide.` and `restconnectivityhandshakeguide.` routes were pointing at PIT3's REST guide files instead of PIT4's. Also corrected minor stray-indentation formatting left over from prior edits, elsewhere in the same file.

### External Project Integration
- ✅ `paye-employers-pit-faq` (Angular 14 / PrimeNG accordion) → `content/shared/faq.html`
  - Native `<details>`/`<summary>` accordion — no JS, fully accessible (WCAG)
  - 4 sections: TDM/Certificates, SOAP/REST, Common Errors, Reporting Issues
  - `pit-guides.html` FAQ link updated from external GitHub Pages URL to internal `#faq` route
  - `sitemap.json` `faq` route updated to point to new page

---

## Outstanding

### Content — Pages Still Needed (121 placeholder routes)

| Section | Routes Still Needed |
|---|---|
| PIT Guides | Help Desk Registration, Help Desk Login, PIT Next Version Features |
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
- ✅ Bootstrap removal — complete
- ❌ Font migration — Nunito Sans stack (deferred pending decision)
- ❌ `sitemap.json` move to project root (currently `assets/js/`)
- ❌ Validation rules XLSX files not yet linked from content pages
- ❌ `demodocument.html` to be removed before production go-live
- ❌ ERR supporting docs pages (PIT3 + PIT4) still point to `demodocument.html`
- ❌ **Audit bulk-copied SOAP schema reference files (PIT3/PIT4 `topic*.html`, ~2,473 files, copied wholesale from `O:\git\paye-employers-documentation`)** — these were copied as a complete unit rather than curated, so may include unused/orphaned pages, dead internal links, or content not actually needed in this project. Needs a review pass to identify and remove anything superfluous before public release.

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
