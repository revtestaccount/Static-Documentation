"""
fix_selfservice_coverpage.py
============================
Fixes the cover page section of pitselfserviceguide.html:
  - Removes duplicate h2 headings ("PIT Self Service Application Guide"
    and "PAYE Modernisation") that appear after the version paragraph
  - Fixes the "Audience" paragraph (removes the word "Audience" prefix)
  - Replaces the broken multi-column version history table with a clean
    4-column hand-authored table

Usage:
    python fix_selfservice_coverpage.py --pit PIT3
    python fix_selfservice_coverpage.py --pit PIT4
"""

import argparse
import os
import re

CLEAN_VERSION_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Version</th>
<th scope="col">Date</th>
<th scope="col">Section</th>
<th scope="col">Change Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>0.1</td>
<td>20/03/2018</td>
<td>All</td>
<td>Initial draft</td>
</tr>
<tr>
<td></td>
<td></td>
<td>Appendices</td>
<td>7.3 Known Issues section added</td>
</tr>
<tr>
<td>1.0 Release Candidate 2</td>
<td>25/05/2018</td>
<td></td>
<td>Version updated to 1.0 Release Candidate 2</td>
</tr>
<tr>
<td></td>
<td>29/06/2018</td>
<td>Section 7</td>
<td>Added</td>
</tr>
<tr>
<td></td>
<td>20/07/2018</td>
<td>Section 6.1</td>
<td>Added</td>
</tr>
<tr>
<td></td>
<td>31/07/2018</td>
<td>Appendix</td>
<td>Added Returns Reconciliations endpoints</td>
</tr>
<tr>
<td></td>
<td>29/04/2019</td>
<td>Section 6</td>
<td>Added customer with fada description</td>
</tr>
<tr>
<td></td>
<td>09/08/2019</td>
<td>Section 3</td>
<td>Added detail about new employee overview screen and the new request specific certificate button</td>
</tr>
<tr>
<td></td>
<td></td>
<td>Section 4.0</td>
<td>Added section on employee overview</td>
</tr>
<tr>
<td></td>
<td></td>
<td>Section 4.1</td>
<td>Added section on edit employee</td>
</tr>
<tr>
<td></td>
<td></td>
<td>Section 5.2</td>
<td>Added section on Request Specific Employee button</td>
</tr>
</tbody>
</table>"""


def fix_html(html: str) -> tuple[str, list[str]]:
    changes = []

    # ------------------------------------------------------------------
    # Fix 1: Remove the two duplicate h2 headings and fix Audience para
    # Pattern: h2 "PIT Self Service..." + h2 "PAYE Modernisation" +
    #          <p>Audience This document...
    # Replace with just the clean audience paragraph
    # ------------------------------------------------------------------
    pattern_headings = re.compile(
        r'<h2[^>]*id="pit_self_service_application_guide"[^>]*>.*?</h2>\s*'
        r'<h2[^>]*id="paye_modernisation"[^>]*>.*?</h2>\s*'
        r'<p>Audience (This document.*?)</p>',
        re.DOTALL
    )

    def replace_headings(m):
        changes.append("Removed duplicate h2 headings and fixed Audience paragraph")
        return f'<p>{m.group(1)}</p>'

    html, count = re.subn(pattern_headings, replace_headings, html)
    if count == 0:
        changes.append("NOTE: duplicate headings not found (may already be clean)")

    # ------------------------------------------------------------------
    # Fix 2: Replace broken multi-column version history table with
    # clean 4-column table
    # ------------------------------------------------------------------
    pattern_table = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*></th>\s*)*'
        r'<th[^>]*>Version History</th>[\s\S]*?</table>',
        re.DOTALL
    )

    html, count2 = re.subn(pattern_table, CLEAN_VERSION_TABLE, html)
    if count2 > 0:
        changes.append("Replaced broken version history table with clean 4-column table")
    else:
        changes.append("NOTE: version history table not found (may already be clean)")

    return html, changes


def main():
    parser = argparse.ArgumentParser(description="Fix cover page of pitselfserviceguide.html")
    parser.add_argument("--pit", required=True, choices=["PIT3", "PIT4"])
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(
        project_root, "content", args.pit, "screens", "pitselfserviceguide.html"
    )

    if not os.path.isfile(html_path):
        print(f"ERROR: file not found: {html_path}")
        return

    print(f"Processing: {html_path}")

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    fixed_html, changes = fix_html(html)

    for change in changes:
        print(f"  {change}")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(fixed_html)

    print(f"OK - written to {html_path}")


if __name__ == "__main__":
    main()
