"""
fix_ros_payroll_reporting_guide.py
===================================
Post-pipeline fixes for Overview of ROS Payroll Reporting (PIT3 + PIT4).

These fixes address artefacts that the migration pipeline cannot automatically
resolve due to the structure of this specific PDF.

Fix 1:  Replaces broken multi-column version history table with clean
        4-column hand-authored table (with rowspan for merged version cells).
Fix 2:  Removes duplicate cover page headings and orphaned version string.
Fix 3:  Removes orphaned version string paragraph.
Fix 4:  Removes stray duplicate Table of Contents h3 heading.
Fix 5:  Removes dead TOC entries for suppressed cover page headings.
Fix 6:  Promotes version history heading from h4 to h2.pmod.
Fix 8:  Merges split section 4.1 heading into a single h2.
Fix 9:  Merges split section 4.2.2 heading into a single h3.
Fix 10: Corrects the TOC entries for sections 4.1 and 4.2.2 to match.

NOTE: The following fixes were removed because the improved pipeline
      (page rendering, caption ordering, mojibake) now handles them:
  - Fix 0:  image path correction (pipeline writes correct paths)
  - Fix 0b: mojibake in headings (pipeline is clean throughout)
  - Fix 7:  stray cover image (page rendering; no cover images escape)
  - Fix 11: missing Figure 1 image (page rendering includes all pages)
  - Fix 12: missing Figure 12 caption (pipeline caption ordering)

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
    # Fix 2a/2e: Replace section 3.3 bullet-list tables with proper ul/li
    # ------------------------------------------------------------------
    _BULLET_LIST_NEW = (
        '<p>{intro} The three possible outcomes are:</p>\n'
        '<ul>\n'
        '<li>RPNs not returned \u2013 This is the number of employee RPNs that were not returned</li>\n'
        '<li>Validation errors \u2013 This is the number of validation errors in the request</li>\n'
        '</ul>'
    )
    for intro, label in [
        ('This screen makes the user aware of how many RPNs on their request were successful.', '2a'),
        ('This screen will make the user aware of how many RPNs on their request were successful.', '2e'),
    ]:
        pat = re.compile(
            r'<table[^>]*>\s*<thead>\s*<tr>\s*'
            r'<th[^>]*>' + re.escape(intro) + r' The three</th>\s*'
            r'</tr>\s*</thead>\s*<tbody>\s*'
            r'<tr>\s*<td>possible outcomes are:</td>\s*</tr>\s*'
            r'<tr>\s*<td>[\u2022\ufffd] RPNs not returned - This is the number of employee RPNs that were not returned</td>\s*</tr>\s*'
            r'<tr>\s*<td>[\u2022\ufffd] Validation errors [\u2013\u2014\ufffd-] This is the number of validation errors in the request</td>\s*</tr>\s*'
            r'</tbody>\s*</table>',
            re.DOTALL
        )
        html, n = re.subn(pat, _BULLET_LIST_NEW.format(intro=intro), html)
        if n:
            changes.append(f'Fix {label}: Converted section 3.3 summary bullet table to ul/li ({intro[:30]}...)')

    # ------------------------------------------------------------------
    # Fix 2b/2f: Replace split RPN response file paragraph-tables with p
    # ------------------------------------------------------------------
    _RPN_RESPONSE_P = (
        '<p>An RPN response file is automatically downloaded for the user in their selected '
        'file format which details the outcome of the RPN request. The user can then input '
        'this file to their payroll software in order to complete the next stage of their '
        'payroll process.</p>'
    )
    rpn_pat = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*'
        r'<th[^>]*>An RPN response file is automatically downloaded for the user in their selected file format which</th>\s*'
        r'</tr>\s*</thead>\s*<tbody>\s*'
        r'<tr>\s*<td>details the outcome of the RPN request\. The user can then input this file to their payroll software in</td>\s*</tr>\s*'
        r'<tr>\s*<td>order to complete the next stage of their payroll process\.</td>\s*</tr>\s*'
        r'(?:<tr>\s*<td></td>\s*</tr>\s*)*'
        r'</tbody>\s*</table>',
        re.DOTALL
    )
    html, n = re.subn(rpn_pat, _RPN_RESPONSE_P, html)
    if n:
        changes.append(f'Fix 2b/2f: Converted {n} RPN response file paragraph-table(s) to p')

    # ------------------------------------------------------------------
    # Fix 2c: Replace split "other summary screen" intro paragraph-table
    # ------------------------------------------------------------------
    other_pat = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>(?:</th>|)</th>?\s*</tr>\s*</thead>\s*<tbody>\s*'
        r'<tr>\s*<td>The other summary screen the user may get is if they have completed the online form to request RPNs</td>\s*</tr>\s*'
        r'<tr>\s*<td>for new employees or requested RPNs for a specific subset of existing employees:</td>\s*</tr>\s*'
        r'(?:<tr>\s*<td></td>\s*</tr>\s*)*'
        r'</tbody>\s*</table>',
        re.DOTALL
    )
    html, n = re.subn(
        other_pat,
        '<p>The other summary screen the user may get is if they have completed the online form '
        'to request RPNs for new employees or requested RPNs for a specific subset of existing employees:</p>',
        html
    )
    if n:
        changes.append('Fix 2c: Converted section 3.3 second summary intro paragraph-table to p')

    # Fix 2d: Empty 2-column table (split TOC artifact)
    empty2col_pat = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*></th>\s*<th[^>]*></th>\s*</tr>\s*</thead>\s*'
        r'<tbody>\s*<tr>\s*<td></td>\s*<td></td>\s*</tr>\s*</tbody>\s*</table>',
        re.DOTALL
    )
    html, n = re.subn(empty2col_pat, '', html)
    if n:
        changes.append('Fix 2d: Removed empty 2-column split-TOC artifact table')

    # ------------------------------------------------------------------
    # Fix 2: Remove duplicate cover page headings
    # ------------------------------------------------------------------
    pattern2 = re.compile(
        r'<h2[^>]*id="overview_of_ros_payroll_reporting"[^>]*>.*?</h2>\s*'
        r'<h2[^>]*id="paye_modernisation"[^>]*>.*?</h2>\s*',
        re.DOTALL
    )
    html, count2 = re.subn(pattern2, '', html)
    if count2 > 0:
        changes.append(f"Fix 2: Removed {count2} duplicate cover page heading(s)")

    # Fix 3: Remove orphaned version string paragraph
    pattern3 = re.compile(r'<p>Version [^<]*Version Date [^<]*</p>\s*')
    html, count3 = re.subn(pattern3, '', html)
    if count3 > 0:
        changes.append(f"Fix 3: Removed orphaned version string paragraph ({count3} occurrence(s))")

    # Fix 4: Remove stray duplicate Table of Contents h3
    pattern4 = re.compile(r'<h3[^>]*id="table_of_contents"[^>]*>Table of Contents</h3>\s*')
    html, count4 = re.subn(pattern4, '', html)
    if count4 > 0:
        changes.append(f"Fix 4: Removed {count4} stray duplicate 'Table of Contents' h3 heading(s)")

    # ------------------------------------------------------------------
    # Fix 5: Remove dead TOC entries for suppressed cover page headings
    # ------------------------------------------------------------------
    pattern5 = re.compile(
        r'<li><a href="#overview_of_ros_payroll_reporting">[^<]*</a></li>'
        r'|<li><a href="#paye_modernisation">[^<]*</a></li>'
    )
    html, count5 = re.subn(pattern5, '', html)
    if count5 > 0:
        changes.append(f"Fix 5: Removed {count5} dead cover-page TOC entry/entries")

    # ------------------------------------------------------------------
    # Fix 6: Promote version history heading from h4 to h2.pmod
    # ------------------------------------------------------------------
    html, count6 = re.subn(
        r'<h4 id="version_history">Version History</h4>',
        '<h2 class="pmod" id="version_history">Version History</h2>',
        html
    )
    if count6 > 0:
        changes.append(f"Fix 6: Promoted version history heading to h2.pmod")

    # ------------------------------------------------------------------
    # Fix 8: Merge split section 4.1 heading
    # ------------------------------------------------------------------
    html, count8 = re.subn(
        r'<h2 class="pmod" id="4\.1">4\.1</h2>\s*'
        r'<h2 class="pmod" id="submit_payroll_[\u2013-]_upload_payroll_file">Submit Payroll [\u2013-] Upload Payroll File</h2>',
        '<h2 class="pmod" id="4.1_submit_payroll_\u2013_upload_payroll_file">4.1 Submit Payroll \u2013 Upload Payroll File</h2>',
        html
    )
    if count8 > 0:
        changes.append("Fix 8: Merged split section 4.1 heading into single h2")
    else:
        changes.append("Fix 8: WARNING - split 4.1 heading pattern not found")

    # ------------------------------------------------------------------
    # Fix 9: Merge split section 4.2.2 heading
    # ------------------------------------------------------------------
    html, count9 = re.subn(
        r'<h3 class="pmod" id="4\.2\.2_payroll_submission_[\u2013-]_acknowledgement_screen_[\u2013-]_status:_complete_with">'
        r'4\.2\.2 Payroll Submission [\u2013-] Acknowledgement Screen [\u2013-] Status: Complete with</h3>\s*'
        r'<h3 class="pmod" id="warnings_and/or_errors">Warnings and/or Errors</h3>',
        '<h3 class="pmod" id="4.2.2_payroll_submission_\u2013_acknowledgement_screen_\u2013_status:_complete_with_warnings_and_errors">'
        '4.2.2 Payroll Submission \u2013 Acknowledgement Screen \u2013 Status: Complete with Warnings and/or Errors</h3>',
        html
    )
    if count9 > 0:
        changes.append("Fix 9: Merged split section 4.2.2 heading into single h3")
    else:
        changes.append("Fix 9: WARNING - split 4.2.2 heading pattern not found")

    # ------------------------------------------------------------------
    # Fix 10: Correct TOC entries for sections 4.1 and 4.2.2
    # ------------------------------------------------------------------
    html, count10a = re.subn(
        r'<li[^>]*><a href="#4\.1">4\.1</a></li>\s*'
        r'<li[^>]*><a href="#submit_payroll_[\u2013-]_upload_payroll_file">Submit Payroll [\u2013-] Upload Payroll File</a></li>',
        '<li><a href="#4.1_submit_payroll_\u2013_upload_payroll_file">4.1 Submit Payroll \u2013 Upload Payroll File</a></li>',
        html
    )
    html, count10b = re.subn(
        r'<li[^>]*><a href="#4\.2\.2_payroll_submission_[\u2013-]_acknowledgement_screen_[\u2013-]_status:_complete_with">'
        r'4\.2\.2 Payroll Submission [\u2013-] Acknowledgement Screen [\u2013-] Status: Complete with</a></li>\s*'
        r'<li[^>]*><a href="#warnings_and/or_errors">Warnings and/or Errors</a></li>',
        '<li><a href="#4.2.2_payroll_submission_\u2013_acknowledgement_screen_\u2013_status:_complete_with_warnings_and_errors">'
        '4.2.2 Payroll Submission \u2013 Acknowledgement Screen \u2013 Status: Complete with Warnings and/or Errors</a></li>',
        html
    )
    total10 = count10a + count10b
    if total10 > 0:
        changes.append(f"Fix 10: Corrected {total10} TOC entry/entries for sections 4.1 and/or 4.2.2")
    else:
        changes.append("Fix 10: WARNING - TOC entry pattern(s) for 4.1/4.2.2 not found")

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
