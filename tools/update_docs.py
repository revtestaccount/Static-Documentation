"""
update_docs.py
==============
Updates CLAUDE.md, PROJECT_ASSESSMENT.md, MIGRATION_STATUS.md and README.md
to reflect the following completed work:

1. Bootstrap fully removed — home-grid/home-card CSS, vanilla JS navbar toggle,
   CSS-only dropdown, all card pages converted
2. body margin: 0 fix applied
3. run_doc_fixes.py + doc_fixes_registry.json — consolidated all fix scripts
4. Individual fix_*.py scripts deleted
5. Python script location rule enforced (tools/ only)
6. Overview of ROS Payroll Reporting — PIT3 migrated
"""

from pathlib import Path
import re

ROOT = Path(r"O:\git\Static-Documentation")

# ============================================================================
# CLAUDE.md
# ============================================================================
claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")

# Update tech stack note — Bootstrap removed
claude = claude.replace(
    "**No Angular, no React, no Vue, no Node at runtime. No Bootstrap — removed.** Layout uses PrimeFlex and custom CSS only.",
    "**No Angular, no React, no Vue, no Node at runtime. No Bootstrap — removed.** Layout uses custom CSS (home-grid, home-card, site-nav) only."
)

# Update Bootstrap Removal section — mark complete, remove plan text
claude = claude.replace(
    """## Bootstrap Removal (Complete)

Bootstrap 5 has been fully removed. Replaced with:
- **Card grid:** `home-grid` / `home-card` custom CSS classes in `styles.scss`
- **Navbar collapse:** Vanilla JS `toggleNav()` in `index.html` — no framework dependency
- **Scripts used:** `tools/remove_bootstrap.py`, `tools/fix_cards_and_navbar.py`

This is a **customer-facing / public-facing** application:
- **Font:** FiraSans-Regular 16px
- **WCAG 2.1 AA:** Mandatory throughout
- Apply PrimeFlex layouts per REVDS 22 UI rules — never Bootstrap grid""",
    """## Bootstrap Removal (Complete ✅)

Bootstrap 5 fully removed as of 2026-06-25. Replaced with:
- **Card grid:** `home-grid` / `home-card` BEM CSS classes in `styles.scss`
- **Navbar collapse:** Vanilla JS `toggleNav()` in `index.html`
- **Navbar dropdown:** CSS-only hover/focus dropdown (`site-nav__dropdown` + `:hover > .site-nav__dropdown-menu`)
- **body margin:** `margin: 0` added to remove browser default 8px gap around header/footer

This is a **customer-facing / public-facing** application:
- **Font:** FiraSans-Regular 16px
- **WCAG 2.1 AA:** Mandatory throughout
- Use custom CSS classes — never Bootstrap grid or utility classes"""
)

# Update pipeline scripts section — replace individual fix scripts with run_doc_fixes
claude = claude.replace(
    """### `tools/fix_rest_endpoints_table.py`

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

**Pattern for new documents:** If a new PDF has similar issues, create a new script following the same pattern — one `fix_html()` function with numbered fix blocks, each using `re.subn()` with clear change logging.""",
    """### `tools/run_doc_fixes.py` + `tools/doc_fixes_registry.json`

Single entry point for ALL post-pipeline document fixes. Replaces the individual `fix_*.py` scripts.

```powershell
# List all registered documents and their fixes
python tools/run_doc_fixes.py --list

# Fix one document
python tools/run_doc_fixes.py --doc rest_integration_guide --pit PIT3
python tools/run_doc_fixes.py --doc ros_payroll_reporting --pit PIT3

# Fix all documents for one environment
python tools/run_doc_fixes.py --all --pit PIT3

# Fix all documents for both environments
python tools/run_doc_fixes.py --all --pit ALL
```

**`doc_fixes_registry.json`** records which documents need which fixes. Adding a new document:
1. Add entry to `doc_fixes_registry.json`
2. Add `fix_<key>(html, env)` function to `run_doc_fixes.py`
3. Register it in `FIX_REGISTRY` dict at the bottom of the script"""
)

# Update Python script location rule
claude = claude.replace(
    "### Python Script Location Rule (mandatory)\n**All Python scripts must be created in `tools/`.** Never create `.py` files in the project root or any other directory. One-off patch/helper scripts also go in `tools/` and are deleted once their job is done.",
    "### Python Script Location Rule (mandatory)\n**All Python scripts must be created in `tools/`.** Never create `.py` files in the project root or any other directory. One-off patch/helper scripts also go in `tools/` and are deleted immediately after their job is done. Only permanent, reusable scripts are committed."
)

(ROOT / "CLAUDE.md").write_text(claude, encoding="utf-8")
print("OK: CLAUDE.md updated")

# ============================================================================
# PROJECT_ASSESSMENT.md
# ============================================================================
pa = (ROOT / "PROJECT_ASSESSMENT.md").read_text(encoding="utf-8")

# Update last updated date
pa = re.sub(r'> \*\*Last updated:\*\* \d{4}-\d{2}-\d{2}', '> **Last updated:** 2026-06-25', pa)

# Update Bootstrap in technology stack table
pa = pa.replace(
    "| CSS framework | Bootstrap 5.3 (CDN) | Used for grid/cards — planned for removal |",
    "| CSS framework | Custom CSS (BEM) | Bootstrap removed — home-grid, home-card, site-nav classes |"
)

# Update Bootstrap in completed work
pa = pa.replace(
    "- ✅ Bootstrap 5 loaded from CDN (planned for removal)",
    "- ✅ Bootstrap 5 **fully removed** — replaced with custom CSS (home-grid, home-card, site-nav__collapse, CSS-only dropdown)"
)
pa = pa.replace(
    "- ✅ Responsive navbar with Bootstrap collapse + dropdown menus",
    "- ✅ Responsive navbar — vanilla JS hamburger toggle + CSS-only hover dropdown (no Bootstrap)"
)

# Update card grid description to remove Bootstrap references
pa = pa.replace(
    """### Card Grid

- Cards use Bootstrap `.row`/`.col-sm` grid
- `.home-card` — `width: 18rem`, `height: 100%`, flexbox column layout
- Equal card heights achieved via `flex: 1` on `.card-body` and fixed `height: 8rem` on `.card-img-top`
- Row gap: `.container .row + .row { margin-top: 2rem }`
- Top gap when paragraph precedes cards: `p ~ .container > .row:first-child { margin-top: 2rem }`""",
    """### Card Grid

- **Bootstrap-free** — uses `.home-grid` / `.home-grid__row` / `.home-card` BEM CSS classes
- `.home-card` — `width: 18rem`, flexbox column layout, full-card `<a>` link
- Equal-height rows via CSS flexbox `gap: 1.5rem` on `.home-grid__row`
- Fixed image area `height: 8rem` with `object-fit: contain`
- Row gap: `margin-bottom: 1.5rem` on `.home-grid__row`"""
)

# Remove Bootstrap from Outstanding Work / High Priority
pa = pa.replace(
    """- ❌ **Bootstrap removal** — replacement plan identified and ready to execute:
  - **Phase 1 (card grid):** Replace `container`/`row`/`col-sm`/`card` with PrimeFlex `grid`/`col-12 md:col-4` and existing `.home-card` CSS
  - **Phase 2 (navbar collapse):** Replace Bootstrap JS hamburger toggle with custom vanilla JS; remove `bootstrap.bundle.min.js` CDN reference
  - **Note:** Customer-facing app — FiraSans-Regular 16px, `RevdsExternalPreset`, WCAG 2.1 AA mandatory throughout""",
    "- ✅ **Bootstrap removal** — complete. Custom CSS classes throughout, vanilla JS navbar toggle, CSS-only dropdown."
)

# Update Known Issues — remove Bootstrap CDN issue
pa = pa.replace(
    "| Bootstrap CDN dependency | External dependency; minor CORS risk | Planned for removal |",
    "| ~~Bootstrap CDN dependency~~ | Removed | ✅ Complete |"
)

# Update scripts table in section 8
pa = pa.replace(
    """| Script | Location | Purpose |
|---|---|---|
| `pdfToMarkdown.py` | `migrationScripts/` | PDF → Markdown — embedded image extraction with artefact filter, caption ordering fix |
| `convert_new.py` | `create_page/` | Markdown → site-ready HTML — TOC, REVDS classes, `.figure-caption` injection |
| `migration_pipeline.py` | `tools/` | Single-command orchestrator — 5 steps including mojibake fix |
| `fix_mojibake.py` | `tools/` | Mojibake fix — called automatically by pipeline, also available standalone |
| `fix_rest_endpoints_table.py` | `tools/` | Post-pipeline fixes for REST Web Service Integration Guide |
| `fix_ros_payroll_reporting_guide.py` | `tools/` | Post-pipeline fixes for Overview of ROS Payroll Reporting |
| `fix_pre_tabindex.py` | `tools/` | Patches missing `tabindex="0"` on hand-authored `<pre>` elements (WCAG 2.1) |
| `accessibility_audit.py` | `tools/` | Static WCAG 2.1 AA audit across all migrated HTML files |""",
    """| Script | Location | Purpose |
|---|---|---|
| `pdfToMarkdown.py` | `migrationScripts/` | PDF → Markdown — embedded image extraction, artefact filter, caption ordering fix |
| `convert_new.py` | `create_page/` | Markdown → site-ready HTML — TOC, REVDS classes, `.figure-caption` injection |
| `migration_pipeline.py` | `tools/` | Single-command orchestrator — 5 steps including mojibake fix |
| `run_doc_fixes.py` | `tools/` | Single entry point for ALL post-pipeline document fixes — replaces individual fix scripts |
| `doc_fixes_registry.json` | `tools/` | Registry of documents and their required fixes |
| `fix_mojibake.py` | `tools/` | Mojibake fix — called automatically by pipeline, also available standalone |
| `fix_pre_tabindex.py` | `tools/` | Patches missing `tabindex="0"` on hand-authored `<pre>` elements (WCAG 2.1) |
| `accessibility_audit.py` | `tools/` | Static WCAG 2.1 AA audit across all migrated HTML files |"""
)

(ROOT / "PROJECT_ASSESSMENT.md").write_text(pa, encoding="utf-8")
print("OK: PROJECT_ASSESSMENT.md updated")

# ============================================================================
# MIGRATION_STATUS.md
# ============================================================================
ms = (ROOT / "MIGRATION_STATUS.md").read_text(encoding="utf-8")

# Update last updated date
ms = ms.replace("> **Last updated:** 2026-06-16", "> **Last updated:** 2026-06-25")

# Update navbar entry — Bootstrap removed
ms = ms.replace(
    "- ✅ Responsive navbar — Bootstrap collapse + Revenue-styled dropdowns",
    "- ✅ Responsive navbar — vanilla JS hamburger toggle + CSS-only dropdown (Bootstrap-free)"
)

# Update styling — Bootstrap removal
ms = ms.replace(
    "- ✅ Equal-height card grid — flexbox, `height: 100%`, fixed image area",
    "- ✅ Bootstrap fully removed — home-grid/home-card BEM CSS, vanilla JS toggle, CSS-only dropdown\n- ✅ Equal-height card grid — flexbox, `height: 100%`, fixed image area"
)

# Update completed PDF migrations
ms = ms.replace(
    "### PDF → HTML Migration (new)\n- ✅ PIT3 REST Web Service Integration Guide (`content/PIT3/rest/rest_web_service_integration_guide.html`)\n- ✅ PIT3 REST Connectivity Handshake Guide (`content/PIT3/rest/rest_connectivity_handshake_guide.html`)\n- ✅ PIT4 REST Web Service Integration Guide (`content/PIT4/rest/rest_web_service_integration_guide.html`)\n- ✅ PIT4 REST Connectivity Handshake Guide (`content/PIT4/rest/rest_connectivity_handshake_guide.html`)",
    "### PDF → HTML Migration (new)\n- ✅ PIT3 REST Web Service Integration Guide (`content/PIT3/rest/rest_web_service_integration_guide.html`)\n- ✅ PIT3 REST Connectivity Handshake Guide (`content/PIT3/rest/rest_connectivity_handshake_guide.html`)\n- ✅ PIT4 REST Web Service Integration Guide (`content/PIT4/rest/rest_web_service_integration_guide.html`)\n- ✅ PIT4 REST Connectivity Handshake Guide (`content/PIT4/rest/rest_connectivity_handshake_guide.html`)\n- ✅ PIT3 Overview of ROS Payroll Reporting (`content/PIT3/screens/overview_of_ros_payroll_reporting.html`)"
)

# Update tooling — replace individual fix scripts with run_doc_fixes
ms = ms.replace(
    "- ✅ `tools/fix_rest_endpoints_table.py` — post-pipeline fixes for REST Web Service Integration Guide (section 2.1 table, 4.1.3 table, footnote ordering, code blocks, version history spillover)",
    "- ✅ `tools/run_doc_fixes.py` + `tools/doc_fixes_registry.json` — consolidated post-pipeline fix scripts (replaces all individual fix_*.py scripts)"
)

# Remove Bootstrap from Outstanding Technical section
ms = ms.replace(
    "- ❌ Bootstrap removal — replace `.row`, `.col-sm`, `.container` with native CSS",
    "- ✅ Bootstrap removal — complete"
)

(ROOT / "MIGRATION_STATUS.md").write_text(ms, encoding="utf-8")
print("OK: MIGRATION_STATUS.md updated")

# ============================================================================
# README.md
# ============================================================================
readme = (ROOT / "README.md").read_text(encoding="utf-8")

# Update card grid description
readme = readme.replace(
    "#### `.home-card` — Navigation Cards\n- `width: 18rem`, `height: 100%` — equal-height cards in a row\n- Fixed image area `height: 8rem` with `object-fit: contain`\n- `flex: 1` on `.card-body` — vertically centres text regardless of line count\n- Bootstrap `stretched-link` makes the entire card clickable",
    "#### `.home-card` — Navigation Cards\n- **Bootstrap-free** — uses `.home-grid` / `.home-card` BEM CSS classes\n- `width: 18rem` — equal-height rows via CSS flexbox gap\n- Fixed image area `height: 8rem` with `object-fit: contain`\n- Full-card `<a>` link wraps image and text — no `stretched-link` dependency"
)

# Update tools table — replace individual fix scripts with run_doc_fixes
readme = readme.replace(
    "| `tools/fix_rest_endpoints_table.py` | Post-pipeline fixes for REST Web Service Integration Guide (PIT3 + PIT4) |",
    "| `tools/run_doc_fixes.py` | Single entry point for all post-pipeline document fixes (see `tools/doc_fixes_registry.json`) |"
)

# Update page types table — remove Bootstrap reference
readme = readme.replace(
    "| Home / card grid | `content/shared/home.html` | Bootstrap card grid, top-level navigation |",
    "| Home / card grid | `content/shared/home.html` | home-grid CSS card layout, top-level navigation |"
)

# Update directory structure — replace old fix scripts with run_doc_fixes
readme = readme.replace(
    "│   ├── fix_rest_endpoints_table.py  # Post-pipeline fixes for REST Web Service Integration Guide",
    "│   ├── run_doc_fixes.py             # Single entry point for all post-pipeline document fixes"
)
readme = readme.replace(
    "│   ├── fix_ros_payroll_reporting_guide.py  # Post-pipeline fixes for ROS Payroll Reporting Guide\n",
    "│   ├── doc_fixes_registry.json      # Registry: which documents need which fixes\n"
)

# Update font note
readme = readme.replace(
    "- **Font:** Segoe UI 14px (internal applications)",
    "- **Font:** FiraSans-Regular 16px (customer-facing / public-facing application)"
)

(ROOT / "README.md").write_text(readme, encoding="utf-8")
print("OK: README.md updated")

print("\nAll docs updated.")
