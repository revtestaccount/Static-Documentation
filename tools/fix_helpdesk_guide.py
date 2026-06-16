"""
fix_helpdesk_guide.py
=====================
Post-pipeline fixes for the PAYE PIT Help Desk User Guide.

Fix 1 - Remove 13 junk page-header tables.
    The PDF has a repeating 3-column header band on every page (document title
    between two empty cells). These are extracted as empty-body tables and must
    be removed.

Fix 2 - Correct image paths.
    The pipeline writes image srcs as:
        content/pit/paye pit help desk user guide/images/image_N.png
    The canonical images folder (used by the named HTML file) is:
        content/pit/paye pit help desk user guide/images/
    Paths are already correct for the new folder - no change needed IF the
    folder name stays as-is. However we also rewrite to use a leading ./
    for consistency with other pages on the site.

Fix 3 - Rename output file.
    Pipeline produces:  paye pit help desk user guide.html  (spaces in name)
    Required filename:  payepithelpdeskuserguide.html

Usage
-----
    python fix_helpdesk_guide.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

script_dir   = Path(__file__).parent
project_root = script_dir.parent
src_html     = project_root / "content" / "pit" / "paye pit help desk user guide.html"
dest_html    = project_root / "content" / "pit" / "payepithelpdeskuserguide.html"

if not src_html.is_file():
    print(f"Error: source file not found: {src_html}")
    sys.exit(1)

html = src_html.read_text(encoding="utf-8")
original = html
changes = []

# ---------------------------------------------------------------------------
# FIX 1 - Remove junk page-header tables
# ---------------------------------------------------------------------------
# Each page of the PDF has a 3-column header band: [empty | title | empty]
# with an empty tbody. The title cell contains the document title with an
# en dash (U+2013). Match both en dash and hyphen-minus for robustness.

JUNK_TABLE_RE = re.compile(
    r'\n?<table[^>]*>\s*'
    r'<thead>\s*<tr>\s*'
    r'<th[^>]*>\s*</th>\s*'
    r'<th[^>]*>\s*PAYE PIT Help Desk\s*.{1,3}\s*User Guide\s*</th>\s*'
    r'<th[^>]*>\s*</th>\s*'
    r'</tr>\s*</thead>\s*'
    r'<tbody>(?:\s*<tr>(?:\s*<td[^>]*>\s*</td>\s*)+</tr>\s*)+</tbody>\s*'
    r'</table>',
    re.DOTALL
)

html, n = JUNK_TABLE_RE.subn("", html)
changes.append(f"Fix 1: removed {n} junk page-header table(s).")

# ---------------------------------------------------------------------------
# FIX 2 - Normalise image paths
# ---------------------------------------------------------------------------
# Pipeline writes:  src="content/pit/paye pit help desk user guide/images/image_N.png"
# Normalise to:     src="content/pit/paye pit help desk user guide/images/image_N.png"
# (already correct - just ensure no leading ./ discrepancy vs other pages)
# The SPA router loads fragments from the project root so paths without ./
# resolve correctly. No change required here unless paths are wrong.
# Report what we find for confirmation.

img_srcs = re.findall(r'src="([^"]+\.png)"', html)
changes.append(f"Fix 2: {len(img_srcs)} image src(s) found in output.")
for src in img_srcs:
    changes.append(f"       {src}")

# ---------------------------------------------------------------------------
# WRITE + RENAME
# ---------------------------------------------------------------------------

if dest_html.exists():
    dest_html.unlink()
    changes.append(f"Fix 3: removed existing {dest_html.name}")

src_html.write_text(html, encoding="utf-8")
src_html.rename(dest_html)
changes.append(f"Fix 3: renamed to {dest_html.name}")

for line in changes:
    print(line)

print(f"\nOK  Written: {dest_html}")
