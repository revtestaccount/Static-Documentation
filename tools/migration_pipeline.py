"""
migration_pipeline.py
=====================
Single-command PDF -> HTML migration pipeline.

Chains pdfToMarkdown.py and convert_new.py in sequence, deriving all
intermediate paths automatically from the source PDF and --pit argument.

Usage
-----
    python migration_pipeline.py <pdf_path> --pit <PIT3|PIT4>

Examples
--------
    # Migrate a PIT3 document
    python migration_pipeline.py "../content/PIT3/guide/some_guide.pdf" --pit PIT3

    # Migrate a PIT4 document
    python migration_pipeline.py "../content/PIT4/rest/rest_web_service_integration_guide.pdf" --pit PIT4

Output (all derived automatically)
-----------------------------------
    <pdf_dir>/<doc_name>.md           - intermediate Markdown
    <pdf_dir>/<doc_name>/images/      - extracted images
    <pdf_dir>/<doc_name>.html         - final site-ready HTML fragment

The content-path prefix passed to convert_new.py is derived from the
resolved output path relative to the project root, so image src attributes
resolve correctly when the page is loaded via the SPA router.

Project root detection
----------------------
The script walks up from its own location to find the directory containing
assets/js/sitemap.json - that is treated as the project root.
"""

import os
import sys
import re
import json
import argparse
import subprocess


# ---------------------------------------------------------------------------
# PROJECT ROOT DETECTION
# ---------------------------------------------------------------------------

def find_project_root(start_dir):
    """
    Walk up from start_dir until we find the directory containing
    assets/js/sitemap.json - that is the project root.
    """
    current = os.path.abspath(start_dir)
    while True:
        if os.path.isfile(os.path.join(current, "assets", "js", "sitemap.json")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            # Reached filesystem root without finding it
            return None
        current = parent


# ---------------------------------------------------------------------------
# ARGUMENT PARSING
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(
    description="PDF -> Markdown -> HTML migration pipeline for the static documentation site."
)
parser.add_argument(
    "pdf",
    help="Path to the source PDF file (absolute or relative to cwd)"
)
parser.add_argument(
    "--pit",
    required=True,
    choices=["PIT3", "PIT4"],
    help="Target environment: PIT3 (current) or PIT4 (next version)"
)
args = parser.parse_args()


# ---------------------------------------------------------------------------
# PATH RESOLUTION
# ---------------------------------------------------------------------------

pdf_path = os.path.abspath(args.pdf)

if not os.path.isfile(pdf_path):
    print(f"Error: file not found: {pdf_path}")
    sys.exit(1)

pdf_dir      = os.path.dirname(pdf_path)
pdf_basename = os.path.basename(pdf_path)

if not pdf_path.lower().endswith(".pdf"):
    print(f"Error: input file must be a PDF, got: {pdf_basename}")
    print(f"       Usage: python migration_pipeline.py <path/to/document.pdf> --pit PIT3|PIT4")
    sys.exit(1)
doc_name     = os.path.splitext(pdf_basename)[0]

md_path   = os.path.join(pdf_dir, doc_name + ".md")
html_path = os.path.join(pdf_dir, doc_name + ".html")

# Detect project root so we can build the content-path prefix.
# This script lives in tools/ which is a direct child of the project root.
script_dir   = os.path.dirname(os.path.abspath(__file__))
project_root = find_project_root(script_dir)

if project_root is None:
    print("Error: could not locate project root (directory containing assets/js/sitemap.json).")
    print("       Ensure you are running from within the Static-Documentation project.")
    sys.exit(1)

# content_path is the path from project root to pdf_dir, used by convert_new.py
# to prefix relative image src attributes so they resolve from the project root.
content_path = os.path.relpath(pdf_dir, project_root).replace("\\", "/") + "/"

# Paths to the two scripts — both are siblings of tools/ at the project root level
pdf_to_md_script = os.path.join(project_root, "migrationScripts", "pdfToMarkdown.py")
convert_script   = os.path.join(project_root, "create_page", "convert_new.py")

for script in [pdf_to_md_script, convert_script]:
    if not os.path.isfile(script):
        print(f"Error: script not found: {script}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# SUMMARY BEFORE RUNNING
# ---------------------------------------------------------------------------

print("=" * 60)
print("  Migration Pipeline")
print("=" * 60)
print(f"  PDF        : {pdf_path}")
print(f"  Environment: {args.pit}")
print(f"  Output MD  : {md_path}")
print(f"  Output HTML: {html_path}")
print(f"  Content path (image prefix): {content_path}")
print(f"  Project root: {project_root}")
print("=" * 60)
print()
sys.stdout.flush()


# ---------------------------------------------------------------------------
# STEP 1 - PDF -> MARKDOWN
# ---------------------------------------------------------------------------

print("[ Step 1 ] PDF -> Markdown  (pdfToMarkdown.py)\n")
sys.stdout.flush()

result = subprocess.run(
    [sys.executable, pdf_to_md_script, pdf_path, "--output", pdf_dir],
    cwd=os.path.dirname(pdf_to_md_script)
)

if result.returncode != 0:
    print(f"\nError: pdfToMarkdown.py failed with exit code {result.returncode}.")
    sys.exit(result.returncode)

if not os.path.isfile(md_path):
    print(f"\nError: expected Markdown file not found after conversion: {md_path}")
    sys.exit(1)

print(f"\nOK Markdown written to: {md_path}")
sys.stdout.flush()


# ---------------------------------------------------------------------------
# STEP 2 - MARKDOWN -> HTML
# ---------------------------------------------------------------------------

print("\n[ Step 2 ] Markdown -> HTML  (convert_new.py)\n")
sys.stdout.flush()

# Calculate stylesheet href depth: e.g. content/PIT3/rest/file.html = 3 levels deep
html_rel_depth = len(os.path.relpath(html_path, project_root).replace("\\", "/").split("/")) - 1
stylesheet_href = "../" * html_rel_depth + "assets/css/styles.css"

result = subprocess.run(
    [
        sys.executable, convert_script,
        md_path,
        "--output", html_path,
        "--content-path", content_path,
        "--stylesheet", stylesheet_href
    ],
    cwd=os.path.dirname(convert_script),
    capture_output=True,
    text=True
)

# Replay stdout so it still appears in the terminal
print(result.stdout)
if result.stderr:
    print(result.stderr)

# Capture hostname warning for the final summary
hostname_warning = ""
for line in result.stdout.splitlines():
    if "HOSTNAME WARNING" in line:
        hostname_warning = line.strip()

if result.returncode != 0:
    print(f"\nError: convert_new.py failed with exit code {result.returncode}.")
    sys.exit(result.returncode)

if not os.path.isfile(html_path):
    print(f"\nError: expected HTML file not found after conversion: {html_path}")
    sys.exit(1)

print(f"OK HTML written to: {html_path}")
sys.stdout.flush()


# ---------------------------------------------------------------------------
# STEP 2.5 - INJECT STYLESHEET AND SVG BRANDING BLOCK
# ---------------------------------------------------------------------------

print("\n[ Step 2.5 ] Injecting SVG branding block\n")
sys.stdout.flush()

try:
    with open(html_path, "r", encoding="utf-8") as f:
        html_text = f.read()

    # Calculate the relative path depth from the HTML file back to the project root.
    # e.g. content/PIT3/rest/file.html is 3 levels deep -> ../../../
    rel_from_root = os.path.relpath(html_path, project_root)
    depth = len(rel_from_root.replace("\\", "/").split("/")) - 1
    root_prefix = "../" * depth

    SVG_BLOCK = (
        '<div style="display:flex; gap:2rem; justify-content:center; '
        'align-items:center; margin:1.5rem 0;">\n'
        f'    <img alt="Workflow icon" src="{root_prefix}assets/images/icon-helpdesk-workflow.svg" width="240" height="240" />\n'
        f'    <img alt="Filing icon" src="{root_prefix}assets/images/icon-helpdesk-filing.svg" width="240" height="240" />\n'
        f'    <img alt="Sync icon" src="{root_prefix}assets/images/icon-helpdesk-sync.svg" width="240" height="240" />\n'
        '</div>'
    )

    # Inject SVG branding block after the document <h1>
    if 'icon-helpdesk-workflow.svg' not in html_text:
        html_text = re.sub(
            r'(<h1[^>]*>.*?</h1>)',
            r'\1\n' + SVG_BLOCK,
            html_text,
            count=1,
            flags=re.DOTALL
        )
        print(f"  SVG branding block added after <h1>.")
    else:
        print(f"  SVG branding block already present. No change needed.")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_text)

    print(f"\nOK HTML post-processing complete.")

except Exception as e:
    print(f"  Warning: could not post-process HTML: {e}")
    print(f"  Please add the SVG branding block manually after <h1>.")

sys.stdout.flush()


# ---------------------------------------------------------------------------
# STEP 3 - UPDATE sitemap.json
# ---------------------------------------------------------------------------

print("\n[ Step 3 ] Updating sitemap.json\n")
sys.stdout.flush()

sitemap_path = os.path.join(project_root, "assets", "js", "sitemap.json")

# Build the template value the sitemap would use for the HTML file.
# sitemap templates are stored as "./content/PIT3/rest/doc_name.html"
html_rel    = os.path.relpath(html_path, project_root).replace("\\", "/")
pdf_rel     = os.path.relpath(pdf_path, project_root).replace("\\", "/")
html_template = "./" + html_rel
pdf_template  = "./" + pdf_rel

try:
    with open(sitemap_path, "r", encoding="utf-8-sig") as f:
        sitemap_text = f.read()
    sitemap = json.loads(sitemap_text)

    sitemap_updated = False
    for route_group in sitemap.values():
        if not isinstance(route_group, dict):
            continue
        for route_key, route_val in route_group.items():
            if not isinstance(route_val, dict):
                continue
            template = route_val.get("template", "")
            # Match either an existing PDF reference or a demodocument placeholder
            # whose key matches the doc name (normalised, no underscores/hyphens)
            doc_key_norm = doc_name.lower().replace("_", "").replace("-", "")
            route_key_norm = route_key.lower().replace("_", "").replace("-", "").rstrip(".")
            if template == pdf_template or template == html_template:
                # Already pointing at PDF or HTML — update to HTML
                if template != html_template:
                    route_val["template"] = html_template
                    sitemap_updated = True
                    print(f"  Updated route '{route_key}': {template} -> {html_template}")
                else:
                    print(f"  Route '{route_key}' already points to HTML. No change needed.")
            elif route_key_norm == doc_key_norm and "demodocument" in template:
                # Placeholder route whose key matches the doc name — update it
                route_val["template"] = html_template
                sitemap_updated = True
                print(f"  Updated placeholder route '{route_key}': {template} -> {html_template}")

    if sitemap_updated:
        with open(sitemap_path, "w", encoding="utf-8") as f:
            json.dump(sitemap, f, indent=" ", ensure_ascii=False)
        print(f"\nOK sitemap.json updated.")
    else:
        print(f"  No matching route found in sitemap.json for this document.")
        print(f"  Expected template value: {html_template}")
        print(f"  Please update sitemap.json manually if a route exists for this document.")

except Exception as e:
    print(f"  Warning: could not update sitemap.json: {e}")
    print(f"  Please update manually: set template to '{html_template}'")

sys.stdout.flush()


# ---------------------------------------------------------------------------
# STEP 4 - UPDATE SECTION LISTING PAGE
# ---------------------------------------------------------------------------

print("\n[ Step 4 ] Updating section listing page\n")
sys.stdout.flush()

# The section listing page lives at content/<PIT>/rest.html, soap.html, etc.
# We identify it by searching content/<PIT>/*.html files for an <a> whose href
# contains the PDF filename.
pdf_filename  = pdf_basename                          # e.g. rest_web_service_integration_guide.pdf
html_filename = doc_name + ".html"                   # e.g. rest_web_service_integration_guide.html
pit_content_dir = os.path.join(project_root, "content", args.pit)

listing_updated = False
try:
    for fname in os.listdir(pit_content_dir):
        if not fname.endswith(".html"):
            continue
        listing_path = os.path.join(pit_content_dir, fname)
        with open(listing_path, "r", encoding="utf-8") as f:
            listing_text = f.read()

        # Case-insensitive search — filenames in hrefs may differ in case from
        # the actual file on disk (e.g. REST_Connectivity_Handshake_Guide.pdf
        # vs rest_connectivity_handshake_guide.pdf)
        listing_lower = listing_text.lower()
        if pdf_filename.lower() not in listing_lower and html_filename.lower() not in listing_lower:
            continue

        original = listing_text

        # Replace any case variant of the PDF filename with the HTML filename.
        # re.IGNORECASE handles mixed-case hrefs like REST_Connectivity_Handshake_Guide.pdf
        listing_text = re.sub(
            re.escape(pdf_filename),
            html_filename,
            listing_text,
            flags=re.IGNORECASE
        )
        # Replace --pdf badge with --link badge (first occurrence only)
        listing_text = re.sub(
            r'pit-section__badge--pdf">PDF</span>',
            'pit-section__badge--link">LINK</span>',
            listing_text,
            count=1
        )

        if listing_text != original:
            with open(listing_path, "w", encoding="utf-8") as f:
                f.write(listing_text)
            print(f"  Updated section listing: content/{args.pit}/{fname}")
            print(f"    href: {pdf_filename} -> {html_filename}")
            print(f"    badge: PDF -> LINK")
            listing_updated = True
        else:
            print(f"  Found reference in content/{args.pit}/{fname} but no changes were needed.")
            listing_updated = True
        break

    if not listing_updated:
        print(f"  No section listing page found referencing '{pdf_filename}'.")
        print(f"  Please update the section listing page manually.")
    else:
        print(f"\nOK Section listing page updated.")

except Exception as e:
    print(f"  Warning: could not update section listing page: {e}")
    print(f"  Please update manually.")

sys.stdout.flush()


# ---------------------------------------------------------------------------
# POST-GENERATION: CHECK FOR EMPTY-BODY TABLES
# ---------------------------------------------------------------------------

empty_table_warnings = []
try:
    from bs4 import BeautifulSoup
    with open(html_path, "r", encoding="utf-8") as f:
        html_check = f.read()
    soup = BeautifulSoup(html_check, "lxml")
    for table in soup.find_all("table"):
        thead = table.find("thead")
        tbody = table.find("tbody")
        if not thead:
            continue
        header_cells = [th.get_text(strip=True) for th in thead.find_all("th") if th.get_text(strip=True)]
        header_preview = " | ".join(header_cells[:4]) if header_cells else "(no header text)"
        if tbody:
            data_rows = tbody.find_all("tr")
            all_empty = all(
                all(not td.get_text(strip=True) for td in row.find_all("td"))
                for row in data_rows
            )
            if all_empty and data_rows:
                empty_table_warnings.append(header_preview)
        else:
            empty_table_warnings.append(header_preview)
except Exception:
    pass


# ---------------------------------------------------------------------------
# DONE
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("  Pipeline complete")
print("=" * 60)
print(f"  Markdown : {md_path}")
print(f"  HTML     : {html_path}")
print()
print("  Manual review still required:")
print("  1. Review the generated HTML for any table splits or")
print("     formatting issues that the scripts could not auto-fix.")
if hostname_warning:
    print()
    print("  !! HOSTNAME WARNING (action required before publishing):")
    print(f"     {hostname_warning}")
else:
    print("  2. Hostname check passed - no wrong-environment hostnames found.")
if empty_table_warnings:
    print()
    print(f"  !! EMPTY TABLE BODY DETECTED ({len(empty_table_warnings)} table(s)) - likely cross-page split:")
    for w in empty_table_warnings:
        print(f"     Table header: {w!r}")
    print("     Check these tables manually against the source PDF.")
print("=" * 60)
