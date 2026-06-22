"""
fix_ros_payroll_reporting_guide.py
===================================
Post-pipeline fixes for Overview of ROS Payroll Reporting (PIT3 + PIT4).

Fix 1: Replaces broken multi-column version history table with clean
       4-column hand-authored table (with rowspan for merged version cells).

Usage:
    python fix_ros_payroll_reporting_guide.py --pit PIT3
    python fix_ros_payroll_reporting_guide.py --pit PIT4
"""

import argparse
import os
import re

# ---------------------------------------------------------------------------
# Clean version history table — data extracted from source PDF
# ---------------------------------------------------------------------------
CLEAN_VERSION_TABLE = """<h4 id="version_history">Version History</h4>
<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Version</th>
<th scope="col">Change Date</th>
<th scope="col">Section</th>
<th scope="col">Change Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>0.1</td>
<td>05/04/2018</td>
<td>All</td>
<td>Document published.</td>
</tr>
<tr>
<td rowspan="2"><strong>1.0 Release Candidate 2</strong></td>
<td>24/05/2018</td>
<td></td>
<td>Version updated to 1.0 Release Candidate 2</td>
</tr>
<tr>
<td>29/04/2019</td>
<td>2</td>
<td>Added image of view payroll submission feature</td>
</tr>
<tr>
<td></td>
<td></td>
<td>5</td>
<td>Added section describing the view payroll functionality</td>
</tr>
<tr>
<td></td>
<td>02/09/2019</td>
<td>3.2.1</td>
<td>Specified that RPNs for the following year can be looked up at any time in the PIT next version environment</td>
</tr>
<tr>
<td></td>
<td></td>
<td>3.2.1</td>
<td>Specified that employment ID is not required for specific employee RPN lookup in PIT next version</td>
</tr>
<tr>
<td></td>
<td>01/11/2019</td>
<td>3.3</td>
<td>Updated returned RPN screen to show Cessation Date field for PIT next version.</td>
</tr>
<tr>
<td></td>
<td>02/03/2020</td>
<td>3.2.1</td>
<td>Employment ID not required for either environment</td>
</tr>
</tbody>
</table>"""


def fix_html(html: str) -> tuple[str, list[str]]:
    changes = []

    # ------------------------------------------------------------------
    # Fix 0: Image paths — pipeline writes absolute-style paths
    # (content/PIT3/screens/...) but the router serves from project root
    # so paths need to be relative to the HTML file location
    # ------------------------------------------------------------------
    html, count0 = re.subn(
        r'src="content/PIT3/screens/overview_of_ros_payroll_reporting/images/',
        'src="overview_of_ros_payroll_reporting/images/',
        html
    )
    if count0 > 0:
        changes.append(f"Fix 0: Fixed {count0} image path(s) - removed absolute prefix")

    # ------------------------------------------------------------------
    # Fix 0b: Fix mojibake in headings - replace \u6639 (朹) with en dash
    # ------------------------------------------------------------------
    html, count0b = re.subn(r'\u6639', '\u2013', html)
    if count0b > 0:
        changes.append(f"Fix 0b: Fixed {count0b} mojibake dash character(s) in headings")

    # ------------------------------------------------------------------
    # Fix 1: Replace broken multi-column version history table
    # ------------------------------------------------------------------
    pattern = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)*'
        r'<th[^>]*>Version History</th>[\s\S]*?</table>',
        re.DOTALL
    )

    html, count = re.subn(pattern, CLEAN_VERSION_TABLE, html)
    if count > 0:
        changes.append(f"Fix 1: Replaced broken version history table ({count} occurrence(s))")
    else:
        changes.append("Fix 1: WARNING - version history table pattern not found")

    # ------------------------------------------------------------------
    # Fix 2a: Replace incorrectly extracted paragraph tables with <p> tags
    # Tables 2+3 (section 3.3 first summary screen)
    # ------------------------------------------------------------------
    old_t2 = (
        '<table class="table" tabindex="0">\n'
        '<thead>\n<tr>\n'
        '<th scope="col">This screen makes the user aware of how many RPNs on their request were successful. The three</th>\n'
        '</tr>\n</thead>\n'
        '<tbody>\n'
        '<tr>\n<td>possible outcomes are:</td>\n</tr>\n'
        '<tr>\n<td>\ufffd RPNs not returned - This is the number of employee RPNs that were not returned</td>\n</tr>\n'
        '<tr>\n<td>\ufffd Validation errors \ufffd This is the number of validation errors in the request</td>\n</tr>\n'
        '</tbody>\n</table>'
    )
    new_t2 = (
        '<p>This screen makes the user aware of how many RPNs on their request were successful. '
        'The three possible outcomes are:</p>\n'
        '<ul>\n'
        '<li>RPNs not returned - This is the number of employee RPNs that were not returned</li>\n'
        '<li>Validation errors \u2013 This is the number of validation errors in the request</li>\n'
        '</ul>'
    )
    if old_t2 in html:
        html = html.replace(old_t2, new_t2)
        changes.append("Fix 2a: Converted section 3.3 first summary table to paragraph + list")

    old_t3 = (
        '<table class="table" tabindex="0">\n'
        '<thead>\n<tr>\n'
        '<th scope="col">An RPN response file is automatically downloaded for the user in their selected file format which</th>\n'
        '</tr>\n</thead>\n'
        '<tbody>\n'
        '<tr>\n<td>details the outcome of the RPN request. The user can then input this file to their payroll software in</td>\n</tr>\n'
        '<tr>\n<td>order to complete the next stage of their payroll process.</td>\n</tr>\n'
        '<tr>\n<td></td>\n</tr>\n'
        '<tr>\n<td></td>\n</tr>\n'
        '<tr>\n<td></td>\n</tr>\n'
        '</tbody>\n</table>'
    )
    new_t3 = (
        '<p>An RPN response file is automatically downloaded for the user in their selected file format which '
        'details the outcome of the RPN request. The user can then input this file to their payroll software in '
        'order to complete the next stage of their payroll process.</p>'
    )
    if old_t3 in html:
        html = html.replace(old_t3, new_t3)
        changes.append("Fix 2b: Converted section 3.3 response file table to paragraph")

    old_t4 = (
        '<table class="table" tabindex="0">\n'
        '<thead>\n<tr>\n'
        '<th scope="col"></th>\n'
        '</tr>\n</thead>\n'
        '<tbody>\n'
        '<tr>\n<td>The other summary screen the user may get is if they have completed the online form to request RPNs</td>\n</tr>\n'
        '<tr>\n<td>for new employees or requested RPNs for a specific subset of existing employees:</td>\n</tr>\n'
        '<tr>\n<td></td>\n</tr>\n'
        '</tbody>\n</table>'
    )
    new_t4 = (
        '<p>The other summary screen the user may get is if they have completed the online form to request RPNs '
        'for new employees or requested RPNs for a specific subset of existing employees:</p>'
    )
    if old_t4 in html:
        html = html.replace(old_t4, new_t4)
        changes.append("Fix 2c: Converted section 3.3 second summary intro table to paragraph")

    # Empty 2-column table (split TOC artifact)
    old_t5 = (
        '<table class="table" tabindex="0">\n'
        '<thead>\n<tr>\n'
        '<th scope="col"></th>\n'
        '<th scope="col"></th>\n'
        '</tr>\n</thead>\n'
        '<tbody>\n'
        '<tr>\n<td></td>\n<td></td>\n</tr>\n'
        '</tbody>\n</table>'
    )
    if old_t5 in html:
        html = html.replace(old_t5, '')
        changes.append("Fix 2d: Removed empty split-TOC artifact table")

    old_t6 = (
        '<table class="table" tabindex="0">\n'
        '<thead>\n<tr>\n'
        '<th scope="col">This screen will make the user aware of how many RPNs on their request were successful. The three</th>\n'
        '</tr>\n</thead>\n'
        '<tbody>\n'
        '<tr>\n<td>possible outcomes are:</td>\n</tr>\n'
        '<tr>\n<td>\ufffd RPNs not returned - This is the number of employee RPNs that were not returned</td>\n</tr>\n'
        '<tr>\n<td>\ufffd Validation errors \ufffd This is the number of validation errors in the request</td>\n</tr>\n'
        '</tbody>\n</table>'
    )
    new_t6 = (
        '<p>This screen will make the user aware of how many RPNs on their request were successful. '
        'The three possible outcomes are:</p>\n'
        '<ul>\n'
        '<li>RPNs not returned - This is the number of employee RPNs that were not returned</li>\n'
        '<li>Validation errors \u2013 This is the number of validation errors in the request</li>\n'
        '</ul>'
    )
    if old_t6 in html:
        html = html.replace(old_t6, new_t6)
        changes.append("Fix 2e: Converted section 3.3 second summary screen table to paragraph + list")

    old_t7 = (
        '<table class="table" tabindex="0">\n'
        '<thead>\n<tr>\n'
        '<th scope="col">An RPN response file is automatically downloaded for the user in their selected file format which</th>\n'
        '</tr>\n</thead>\n'
        '<tbody>\n'
        '<tr>\n<td>details the outcome of the RPN request. The user can then input this file to their payroll software in</td>\n</tr>\n'
        '<tr>\n<td>order to complete the next stage of their payroll process.</td>\n</tr>\n'
        '</tbody>\n</table>'
    )
    new_t7 = (
        '<p>An RPN response file is automatically downloaded for the user in their selected file format which '
        'details the outcome of the RPN request. The user can then input this file to their payroll software in '
        'order to complete the next stage of their payroll process.</p>'
    )
    if old_t7 in html:
        html = html.replace(old_t7, new_t7)
        changes.append("Fix 2f: Converted section 3.3 second response file table to paragraph")

    # ------------------------------------------------------------------
    # Fix 2: Remove duplicate cover page headings and version string
    # that appear before Audience section (same pattern as selfservice guide)
    # ------------------------------------------------------------------
    pattern2 = re.compile(
        r'<h2[^>]*id="overview_of_ros_payroll_reporting"[^>]*>.*?</h2>\s*'
        r'<h2[^>]*id="paye_modernisation"[^>]*>.*?</h2>\s*',
        re.DOTALL
    )
    html, count2 = re.subn(pattern2, '', html)
    if count2 > 0:
        changes.append(f"Fix 2: Removed {count2} duplicate cover page heading(s)")

    # Remove orphaned version string paragraph before Audience
    pattern3 = re.compile(r'<p>Version [^<]*Version Date [^<]*</p>\s*')
    html, count3 = re.subn(pattern3, '', html)
    if count3 > 0:
        changes.append(f"Fix 3: Removed orphaned version string paragraph ({count3} occurrence(s))")

    # Remove stray duplicate "Table of Contents" <h3> heading that appears mid-page
    # after the version history table. The real TOC uses <h2> + <ul id="toc"> at the
    # top of the document — only <h3> variants are stray duplicates.
    pattern4 = re.compile(r'<h3[^>]*id="table_of_contents"[^>]*>Table of Contents</h3>\s*')
    html, count4 = re.subn(pattern4, '', html)
    if count4 > 0:
        changes.append(f"Fix 4: Removed {count4} stray duplicate 'Table of Contents' <h3> heading(s)")

    # ------------------------------------------------------------------
    # Fix 5: Remove dead TOC <li> entries for cover-page headings that the
    # pipeline suppressed from the body — links to non-existent anchors
    # (#overview_of_ros_payroll_reporting and #paye_modernisation)
    # ------------------------------------------------------------------
    pattern5 = re.compile(
        r'<li><a href="#overview_of_ros_payroll_reporting">[^<]*</a></li>'
        r'|<li><a href="#paye_modernisation">[^<]*</a></li>'
    )
    html, count5 = re.subn(pattern5, '', html)
    if count5 > 0:
        changes.append(f"Fix 5: Removed {count5} dead cover-page TOC entry/entries")

    return html, changes


def main():
    parser = argparse.ArgumentParser(
        description="Fix Overview of ROS Payroll Reporting guide HTML"
    )
    parser.add_argument("--pit", required=True, choices=["PIT3", "PIT4"])
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(
        project_root, "content", args.pit, "screens",
        "overview_of_ros_payroll_reporting.html"
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
