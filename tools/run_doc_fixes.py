"""
run_doc_fixes.py
================
Single entry point for all post-pipeline document fixes.

Every PDF that the migration pipeline cannot fully auto-correct has a
corresponding fix registered in doc_fixes_registry.json. This script
reads that registry and runs the appropriate fix function(s).

Usage
-----
    # Fix one document for one environment
    python run_doc_fixes.py --doc rest_integration_guide --pit PIT3
    python run_doc_fixes.py --doc ros_payroll_reporting --pit PIT3

    # Fix all registered documents for one environment
    python run_doc_fixes.py --all --pit PIT3

    # Fix all registered documents for both environments
    python run_doc_fixes.py --all --pit ALL

    # List all registered documents and their fixes
    python run_doc_fixes.py --list

Adding a new document fix
-------------------------
1. Add an entry to doc_fixes_registry.json
2. Add the corresponding fix_<key>() function in this file
3. Register it in the FIX_REGISTRY dict at the bottom of this file

Every fix function must have this signature:
    def fix_<key>(html: str, env: str) -> tuple[str, list[str]]
    Returns: (fixed_html, list_of_change_messages)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR   = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
REGISTRY_PATH = SCRIPT_DIR / "doc_fixes_registry.json"

# ---------------------------------------------------------------------------
# HOSTS per environment — used by fixes that need environment-specific URLs
# ---------------------------------------------------------------------------

HOSTS = {
    "PIT3": "softwaretest.ros.ie",
    "PIT4": "softwaretestnextversion.ros.ie",
}

# ===========================================================================
# FIX FUNCTIONS
# ===========================================================================

# ---------------------------------------------------------------------------
# rest_integration_guide
# Fixes: broken section 2.1 table, misplaced ERN table, orphaned RC2 table,
#        version history continuation table, HTTP example code block,
#        broken section 4.1.3 headers table
# ---------------------------------------------------------------------------

REST_CLEAN_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Description</th>
<th scope="col">HTTP Method</th>
<th scope="col">Endpoint URL</th>
<th scope="col">Additional Information</th>
<th scope="col">Links</th>
</tr>
</thead>
<tbody>
<tr>
<td>* Look Up RPN By Employer and optionally filter by date last updated and/or employee id's web service</td>
<td>GET</td>
<td>https://www.ros.ie/paye-employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)<br>employeeIDs (optional)<br>dateLastUpdated (optional)</td>
<td>lookUpRPNByEmployer</td>
</tr>
<tr>
<td>Lookup RPN by Employee web service</td>
<td>GET</td>
<td>https://www.ros.ie/paye-employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}/{employeeId}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>lookUpRPNByEmployee</td>
</tr>
<tr>
<td>New RPN web service</td>
<td>POST</td>
<td>https://www.ros.ie/paye-employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>createNewRPN</td>
</tr>
<tr>
<td>Payroll Submission web service</td>
<td>POST</td>
<td>https://www.ros.ie/paye-employers/v1/rest/payroll/{employerRegistrationNumber}/{taxYear}/{payrollRunReference}/{submissionID}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>createPayrollSubmission</td>
</tr>
<tr>
<td>Check Payroll Submission web service</td>
<td>GET</td>
<td>https://www.ros.ie/paye-employers/v1/rest/payroll/{employerRegistrationNumber}/{taxYear}/{payrollRunReference}/{submissionID}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>checkPayrollSubmissionComplete</td>
</tr>
<tr>
<td>Check Payroll Run web service</td>
<td>GET</td>
<td>https://www.ros.ie/paye-employers/v1/rest/payroll/{employerRegistrationNumber}/{taxYear}/{payrollRunReference}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>checkPayrollRunComplete</td>
</tr>
<tr>
<td>Enhanced Reporting Submission web service</td>
<td>POST</td>
<td>https://www.ros.ie/paye-employers/v1/rest/enhanced_reporting/{employerRegistrationNumber}/{taxYear}/{enhancedReportingRunReference}/{submissionID}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>submitEmployerReportingSubmission</td>
</tr>
<tr>
<td>Check ERR Run web service</td>
<td>GET</td>
<td>https://www.ros.ie/paye-employers/v1/rest/enhanced_reporting/{employerRegistrationNumber}/{taxYear}/{runReference}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>checkEnhancedReportingRequirementsRun</td>
</tr>
<tr>
<td>Check ERR Submission web service</td>
<td>GET</td>
<td>https://www.ros.ie/paye-employers/v1/rest/enhanced_reporting/{employerRegistrationNumber}/{taxYear}/{runReference}/{submissionID}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>checkEnhancedReportingRequirementsSubmission</td>
</tr>
<tr>
<td>* Look Up ERN web service</td>
<td>GET</td>
<td>https://www.ros.ie/paye-employers/v1/rest/ern/{employerRegistrationNumber}/{taxYear}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)<br>PPSNs</td>
<td>lookUpERN</td>
</tr>
<tr>
<td>Monthly ERR Report web service</td>
<td>GET</td>
<td>https://www.ros.ie/paye-employers/v1/rest/enhanced-reporting/reports/monthly/{employerRegistrationNumber}/{taxYear}/{month}</td>
<td>Query Parameters<br>softwareUsed<br>softwareVersion<br>AgentTain (optional*)</td>
<td>requestMonthlyErrReport</td>
</tr>
</tbody>
</table>"""

REST_HTTP_EXAMPLE = """<pre tabindex="0"><code>POST v1/rest/rpn/0000001W/2019/1/1?agentTain=11221w&amp;softwareUsed=SoftwareXYZ&amp;softwareVersion=1.0 HTTP/1.1
Host: www.ros.ie
Date: Wed Oct 04 16:35:51 BST 2017
Content-Type: application/x-www-form-urlencoded
X-HTTP-Method-Override: GET
Digest: 1fNNQYeUZW2laoZkOF4ssnkkzFJ83MRsz4H+fIpLrIvkBH0Zdy2G85OQSYGoHRqvyL6jVn8xJW0pW91/AYV6FEpw==
Signature: keyId="MIIEmTCCA4GgAwIBAgIRAOzckV67HlvuS0..." //truncated

// Request Body
employeeIDs={employmentID-1}&amp;employeeIDs={employmentID-2}&amp;employeeIDs={employmentID-3}</code></pre>"""

REST_HEADERS_TABLE = """\g<1>
<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Value</th>
<th scope="col">Mandatory</th>
</tr>
</thead>
<tbody>
<tr><td>* (request-target)</td><td>Yes</td></tr>
<tr><td>host</td><td>Yes</td></tr>
<tr><td>date</td><td>Yes</td></tr>
<tr><td>** x-date</td><td>Yes, if date header cannot be added</td></tr>
<tr><td>*** digest</td><td>Yes, if HTTP method is POST</td></tr>
<tr><td>**** content-type</td><td>No</td></tr>
<tr><td>content-length</td><td>No</td></tr>
<tr><td>x-http-method-override</td><td>If HTTP method is POST, HTTP header 'X-HTTP-Method-Override' exists and 'Content-Type=application/x-www-form-urlencoded'.</td></tr>
</tbody>
</table>
<p>* The &#39;(request-target)&#39; header field value is comprised of the lowercase HTTP method, an ASCII space, and the request path.</p>
<pre tabindex="0"><code>(request-target): post /paye-employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}?softwareUsed=XYZ&amp;softwareVersion=1.0</code></pre>
<p>** The &#39;x-date&#39; field should ONLY be used if a Date HTTP header cannot be added programmatically.</p>
<p>*** The &#39;Digest&#39; HTTP header is created from the POST body hashed with SHA-512 and base64 encoded.</p>
<p>**** Content-Type is required as a HTTP header if HTTP Method Type is POST.</p>
<p>All other header field values are created by concatenating the lowercase header field name, an ASCII colon, an ASCII space, and the header field value. See sample below.</p>"""


def fix_rest_integration_guide(html: str, env: str) -> tuple[str, list[str]]:
    changes = []

    # Fix 1: Replace broken section 2.1 tables
    pat21 = re.compile(
        r'(<h3[^>]*id="2\.1\._rest_endpoints"[^>]*>.*?</h3>\s*'
        r'<p>The PAYE Modernisation web service endpoints are detailed below\.</p>\s*)'
        r'((?:<table[\s\S]*?</table>\s*)+)'
        r'(<p>\*Agent Tain)',
        re.DOTALL
    )
    html, n = re.subn(pat21, lambda m: m.group(1) + REST_CLEAN_TABLE + "\n" + m.group(3), html)
    changes.append(f"Fix 1: {'Replaced' if n else 'WARNING: not found —'} section 2.1 REST endpoints table")

    # Fix 2: Remove misplaced ERN/ERR table after 2.1.1
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>\* Look Up ERN web service</th>[\s\S]*?</table>', re.DOTALL),
        '', html
    )
    if n:
        changes.append(f"Fix 2: Removed {n} misplaced ERN/Monthly ERR table(s)")

    # Fix 3: Remove orphaned RC2 table
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>1\.0 Release</th>\s*</tr>\s*</thead>\s*<tbody>\s*<tr>\s*<td>Candidate 2</td>\s*</tr>\s*</tbody>\s*</table>', re.DOTALL),
        '', html
    )
    if n:
        changes.append("Fix 3: Removed orphaned '1.0 Release Candidate 2' table")

    # Fix 4: Remove version history continuation table from Document context section
    html, n = re.subn(
        re.compile(r'(<h3[^>]*id="document_context"[^>]*>.*?</h3>\s*<p>.*?</p>\s*)(<table[^>]*>[\s\S]*?</table>\s*)', re.DOTALL),
        r'\1', html
    )
    if n:
        changes.append("Fix 4: Removed version history continuation table from Document context section")

    # Fix 5: Replace HTTP request example table with code block
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>POST v1/rest/rpn/[^<]+</th>[\s\S]*?</table>', re.DOTALL),
        REST_HTTP_EXAMPLE, html
    )
    changes.append(f"Fix 5: {'Replaced' if n else 'WARNING: not found —'} HTTP request example table with code block")

    # Fix 6: Replace broken section 4.1.3 headers table
    html, n = re.subn(
        re.compile(
            r'(<p>Allowable values in the headers field are outlined in the table below\.</p>\s*)'
            r'(<p>[\s\S]*?See sample below\.</p>\s*)'
            r'<table[^>]*>[\s\S]*?</table>',
            re.DOTALL
        ),
        REST_HEADERS_TABLE, html
    )
    changes.append(f"Fix 6: {'Replaced' if n else 'WARNING: not found —'} section 4.1.3 headers table")

    return html, changes


# ---------------------------------------------------------------------------
# ros_payroll_reporting
# Fixes: version history table, cover page headings, split headings 4.1/4.2.2
# ---------------------------------------------------------------------------

ROS_CLEAN_VERSION_TABLE = """<h4 id="version_history">Version History</h4>
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
<tr><td>0.1</td><td>05/04/2018</td><td>All</td><td>Document published.</td></tr>
<tr><td rowspan="2"><strong>1.0 Release Candidate 2</strong></td><td>24/05/2018</td><td></td><td>Version updated to 1.0 Release Candidate 2</td></tr>
<tr><td>29/04/2019</td><td>2</td><td>Added image of view payroll submission feature</td></tr>
<tr><td></td><td></td><td>5</td><td>Added section describing the view payroll functionality</td></tr>
<tr><td></td><td>02/09/2019</td><td>3.2.1</td><td>Specified that RPNs for the following year can be looked up at any time in the PIT next version environment</td></tr>
<tr><td></td><td></td><td>3.2.1</td><td>Specified that employment ID is not required for specific employee RPN lookup in PIT next version</td></tr>
<tr><td></td><td>01/11/2019</td><td>3.3</td><td>Updated returned RPN screen to show Cessation Date field for PIT next version.</td></tr>
<tr><td></td><td>02/03/2020</td><td>3.2.1</td><td>Employment ID not required for either environment</td></tr>
</tbody>
</table>"""


def fix_ros_payroll_reporting(html: str, env: str) -> tuple[str, list[str]]:
    changes = []

    # Fix 1: Replace broken version history table
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)*<th[^>]*>Version History</th>[\s\S]*?</table>', re.DOTALL),
        ROS_CLEAN_VERSION_TABLE, html
    )
    changes.append(f"Fix 1: {'Replaced' if n else 'WARNING: not found —'} broken version history table")

    # Fix 2a/2e: Section 3.3 bullet tables -> ul/li
    bullet_new = (
        '<p>{intro} The three possible outcomes are:</p>\n<ul>\n'
        '<li>RPNs not returned \u2013 This is the number of employee RPNs that were not returned</li>\n'
        '<li>Validation errors \u2013 This is the number of validation errors in the request</li>\n'
        '</ul>'
    )
    for intro, label in [
        ('This screen makes the user aware of how many RPNs on their request were successful.', '2a'),
        ('This screen will make the user aware of how many RPNs on their request were successful.', '2e'),
    ]:
        html, n = re.subn(
            re.compile(
                r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>' + re.escape(intro) + r' The three</th>\s*</tr>\s*</thead>\s*<tbody>\s*'
                r'<tr>\s*<td>possible outcomes are:</td>\s*</tr>\s*'
                r'<tr>\s*<td>[\u2022\ufffd] RPNs not returned - This is the number of employee RPNs that were not returned</td>\s*</tr>\s*'
                r'<tr>\s*<td>[\u2022\ufffd] Validation errors [\u2013\u2014\ufffd-] This is the number of validation errors in the request</td>\s*</tr>\s*'
                r'</tbody>\s*</table>', re.DOTALL
            ),
            bullet_new.format(intro=intro), html
        )
        if n:
            changes.append(f'Fix {label}: Converted section 3.3 bullet table to ul/li')

    # Fix 2b/2f: RPN response paragraph-tables -> <p>
    html, n = re.subn(
        re.compile(
            r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>An RPN response file is automatically downloaded for the user in their selected file format which</th>\s*</tr>\s*</thead>\s*<tbody>\s*'
            r'<tr>\s*<td>details the outcome of the RPN request\. The user can then input this file to their payroll software in</td>\s*</tr>\s*'
            r'<tr>\s*<td>order to complete the next stage of their payroll process\.</td>\s*</tr>\s*'
            r'(?:<tr>\s*<td></td>\s*</tr>\s*)*</tbody>\s*</table>', re.DOTALL
        ),
        '<p>An RPN response file is automatically downloaded for the user in their selected file format which details the outcome of the RPN request. The user can then input this file to their payroll software in order to complete the next stage of their payroll process.</p>',
        html
    )
    if n:
        changes.append(f'Fix 2b/2f: Converted {n} RPN response paragraph-table(s) to <p>')

    # Fix 2c: remaining section 3.3 paragraph-tables -> <p>
    # Handles both the empty-header variant and any residual split table
    for _pat in [
        re.compile(
            r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>(?:</th>|)</th>?\s*</tr>\s*</thead>\s*<tbody>\s*'
            r'<tr>\s*<td>The other summary screen the user may get is if they have completed the online form to request RPNs</td>\s*</tr>\s*'
            r'<tr>\s*<td>for new employees or requested RPNs for a specific subset of existing employees:</td>\s*</tr>\s*'
            r'(?:<tr>\s*<td></td>\s*</tr>\s*)*</tbody>\s*</table>', re.DOTALL),
        re.compile(
            r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*></th>\s*</tr>\s*</thead>\s*<tbody>\s*'
            r'<tr>\s*<td>The other summary screen[^<]*</td>\s*</tr>\s*'
            r'(?:<tr>\s*<td>[^<]*</td>\s*</tr>\s*)*</tbody>\s*</table>', re.DOTALL),
    ]:
        html, n = re.subn(
            _pat,
            '<p>The other summary screen the user may get is if they have completed the online form to request RPNs for new employees or requested RPNs for a specific subset of existing employees:</p>',
            html
        )
        if n:
            changes.append('Fix 2c: Converted section 3.3 summary intro paragraph-table to <p>')
            break

    # Fix 2d: Empty 2-column table (split TOC artifact)
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*></th>\s*<th[^>]*></th>\s*</tr>\s*</thead>\s*<tbody>\s*<tr>\s*<td></td>\s*<td></td>\s*</tr>\s*</tbody>\s*</table>', re.DOTALL),
        '', html
    )
    if n:
        changes.append('Fix 2d: Removed empty 2-column split-TOC artifact table')

    # Fix 2: Remove duplicate cover page headings
    html, n = re.subn(
        re.compile(r'<h2[^>]*id="overview_of_ros_payroll_reporting"[^>]*>.*?</h2>\s*<h2[^>]*id="paye_modernisation"[^>]*>.*?</h2>\s*', re.DOTALL),
        '', html
    )
    if n:
        changes.append(f"Fix 2: Removed {n} duplicate cover page heading(s)")

    # Fix 3: Remove orphaned version string paragraph
    html, n = re.subn(re.compile(r'<p>Version [^<]*Version Date [^<]*</p>\s*'), '', html)
    if n:
        changes.append(f"Fix 3: Removed {n} orphaned version string paragraph(s)")

    # Fix 4: Remove stray duplicate TOC h3
    html, n = re.subn(re.compile(r'<h3[^>]*id="table_of_contents"[^>]*>Table of Contents</h3>\s*'), '', html)
    if n:
        changes.append(f"Fix 4: Removed {n} stray 'Table of Contents' h3 heading(s)")

    # Fix 5: Remove dead cover-page TOC entries
    html, n = re.subn(
        re.compile(r'<li><a href="#overview_of_ros_payroll_reporting">[^<]*</a></li>|<li><a href="#paye_modernisation">[^<]*</a></li>'),
        '', html
    )
    if n:
        changes.append(f"Fix 5: Removed {n} dead cover-page TOC entry/entries")

    # Fix 6: Promote version history h4 -> h2.pmod
    html, n = re.subn(
        r'<h4 id="version_history">Version History</h4>',
        '<h2 class="pmod" id="version_history">Version History</h2>', html
    )
    if n:
        changes.append("Fix 6: Promoted version history heading to h2.pmod")

    # Fix 8: Merge split section 4.1 heading
    html, n = re.subn(
        re.compile(r'<h2 class="pmod" id="4\.1">4\.1</h2>\s*<h2 class="pmod" id="submit_payroll_[\u2013-]_upload_payroll_file">Submit Payroll [\u2013-] Upload Payroll File</h2>'),
        '<h2 class="pmod" id="4.1_submit_payroll_\u2013_upload_payroll_file">4.1 Submit Payroll \u2013 Upload Payroll File</h2>', html
    )
    changes.append(f"Fix 8: {'Merged' if n else 'WARNING: not found —'} split section 4.1 heading")

    # Fix 9: Merge split section 4.2.2 heading
    html, n = re.subn(
        re.compile(
            r'<h3 class="pmod" id="4\.2\.2_payroll_submission_[\u2013-]_acknowledgement_screen_[\u2013-]_status:_complete_with">'
            r'4\.2\.2 Payroll Submission [\u2013-] Acknowledgement Screen [\u2013-] Status: Complete with</h3>\s*'
            r'<h3 class="pmod" id="warnings_and/or_errors">Warnings and/or Errors</h3>'
        ),
        '<h3 class="pmod" id="4.2.2_payroll_submission_\u2013_acknowledgement_screen_\u2013_status:_complete_with_warnings_and_errors">'
        '4.2.2 Payroll Submission \u2013 Acknowledgement Screen \u2013 Status: Complete with Warnings and/or Errors</h3>',
        html
    )
    changes.append(f"Fix 9: {'Merged' if n else 'WARNING: not found —'} split section 4.2.2 heading")

    # Fix 10: Correct TOC entries for 4.1 and 4.2.2
    html, n10a = re.subn(
        re.compile(r'<li[^>]*><a href="#4\.1">4\.1</a></li>\s*<li[^>]*><a href="#submit_payroll_[\u2013-]_upload_payroll_file">Submit Payroll [\u2013-] Upload Payroll File</a></li>'),
        '<li><a href="#4.1_submit_payroll_\u2013_upload_payroll_file">4.1 Submit Payroll \u2013 Upload Payroll File</a></li>', html
    )
    html, n10b = re.subn(
        re.compile(
            r'<li[^>]*><a href="#4\.2\.2_payroll_submission_[\u2013-]_acknowledgement_screen_[\u2013-]_status:_complete_with">'
            r'4\.2\.2 Payroll Submission [\u2013-] Acknowledgement Screen [\u2013-] Status: Complete with</a></li>\s*'
            r'<li[^>]*><a href="#warnings_and/or_errors">Warnings and/or Errors</a></li>'
        ),
        '<li><a href="#4.2.2_payroll_submission_\u2013_acknowledgement_screen_\u2013_status:_complete_with_warnings_and_errors">'
        '4.2.2 Payroll Submission \u2013 Acknowledgement Screen \u2013 Status: Complete with Warnings and/or Errors</a></li>',
        html
    )
    changes.append(f"Fix 10: Corrected {n10a + n10b} TOC entry/entries for sections 4.1 and/or 4.2.2")

        # Fix 12a: In some environments Figure 10 has no dedicated image asset and
    # reuses figure_7.png (per CSV analysis, originally observed on PIT3/PIT4
    # shared behaviour). Guarded by file-existence so a future environment
    # with its own genuine figure_10.png is not overwritten with a duplicate.
    # Bug fixed 2026-06-26: the src path was a broken string literal
    # ('...' + env + '...' written INSIDE single quotes, never interpolated) —
    # now a proper f-string.
    _img_dir_12a = PROJECT_ROOT / 'content' / env / 'screens' / 'overview_of_ros_payroll_reporting' / 'images'
    if (_img_dir_12a / 'figure_10.png').exists():
        changes.append('Fix 12a: figure_10.png exists on disk for this environment - genuine image present, skipped figure_7 reuse insert')
    elif not re.search(r'figure_7\.png"/></p>\s*<p class="figure-caption">Figure 10', html):
        html, n12a = re.subn(
            r'(<p class="figure-caption">Figure 10 [^<]+</p>)',
            f'<p><img alt="Image" src="content/{env}/screens/overview_of_ros_payroll_reporting/images/figure_7.png"/></p>\n\\g<1>',
            html
        )
        if n12a:
            changes.append('Fix 12a: Inserted figure_7 (reused) before Figure 10 caption')
        else:
            changes.append('Fix 12a: WARNING - Figure 10 caption not found')
    else:
        changes.append('Fix 12a: figure_7 already present before Figure 10 - skipped')

    # Fix 12b: Figure 12 caption was not extracted from PDF text — insert both
    # image and caption between the Figure 11 caption and the Figure 13 caption.
    # Only insert Figure 12 block if not already present after Figure 11
    _fig12_present = 'figure_12.png"/></p>' in html
    if not _fig12_present:
        FIG12_INSERT = (
            '<p><img alt="Image" src="content/" + env + "/screens/overview_of_ros_payroll_reporting/images/figure_12.png"/></p>\n'
            '<p class="figure-caption">Figure 12 Request RPNs Summary screen (Detailed)</p>\n'
        )
        html, n12b = re.subn(
            r'(<p class="figure-caption">Figure 11 [^<]+</p>)',
            '\g<1>\n' + FIG12_INSERT,
            html
        )
        if n12b:
            changes.append('Fix 12b: Inserted figure_12 image and caption after Figure 11')
        else:
            changes.append('Fix 12b: WARNING - Figure 11 caption not found')
    else:
        # figure_12 already in HTML — remove any duplicate block
        html = re.sub(
            re.compile(
                r'(<p class="figure-caption">Figure 12[^<]*</p>)\s*'
                r'<p><img[^>]*figure_12\.png[^/]*/></p>\s*'
                r'<p class="figure-caption">Figure 12[^<]*</p>',
                re.DOTALL
            ),
            r'\1',
            html
        )
        changes.append('Fix 12b: figure_12 already present - removed duplicate if any')

        # Fix 12c: In some environments Figure 25 has no dedicated image asset and
    # reuses figure_15.png (per CSV analysis, originally observed on PIT3).
    # This is NOT universal — PIT4 has its own genuine figure_25.png. Guarded
    # by file-existence so the reuse is only applied when figure_25.png
    # genuinely does not exist on disk for this environment.
    # Bug fixed 2026-06-26: same broken string-literal defect as Fix 12a
    # above, plus this was incorrectly applied unconditionally to PIT4,
    # producing a duplicate/wrong image before the Figure 25 caption.
    _img_dir_12c = PROJECT_ROOT / 'content' / env / 'screens' / 'overview_of_ros_payroll_reporting' / 'images'
    if (_img_dir_12c / 'figure_25.png').exists():
        changes.append('Fix 12c: figure_25.png exists on disk for this environment - genuine image present, skipped figure_15 reuse insert')
    elif not re.search(r'figure_15\.png"/></p>\s*<p class="figure-caption">Figure 25', html):
        html, n12c = re.subn(
            r'(<p class="figure-caption">Figure 25 [^<]+</p>)',
            f'<p><img alt="Image" src="content/{env}/screens/overview_of_ros_payroll_reporting/images/figure_15.png"/></p>\n\\g<1>',
            html
        )
        if n12c:
            changes.append('Fix 12c: Inserted figure_15 (reused) before Figure 25 caption')
        else:
            changes.append('Fix 12c: WARNING - Figure 25 caption not found')
    else:
        changes.append('Fix 12c: figure_15 already present before Figure 25 - skipped')


    # Fix 13a: Add missing hyperlink on 'here' in the Access section.
    # URL is environment-specific (PIT3/PIT4) via the HOSTS dict.
    _ACCESS_URLS = {
        "PIT3": "https://softwaretest.ros.ie/oidc/login/noCertsFound?lang=en&amp;client_id=payeselfservice_rp",
        "PIT4": "https://softwaretestnextversion.ros.ie/oidc/login/noCertsFound?lang=en&amp;client_id=payeselfservice_rp",
    }
    _access_url = _ACCESS_URLS.get(env, _ACCESS_URLS['PIT3'])
    _access_link = '<a href="' + _access_url + '" target="_blank" rel="noopener noreferrer">here</a>'
    html, n13a = re.subn(
        r'screens are accessed here ,',
        'screens are accessed ' + _access_link + ',',
        html
    )
    if n13a:
        changes.append('Fix 13a: Added ' + env + ' hyperlink on "here" in Access section')
    else:
        changes.append('Fix 13a: WARNING - Access "here" text not found')

    # Fix 13b: Join split paragraph in section 3.1
    # '...Separate files</p><p>must be uploaded...' -> single joined <p>
    html, n13b = re.subn(
        re.compile(
            r'<p>(Upon selecting[^<]+Separate files)</p>\s*'
            r'<p>(must be uploaded for existing or new employees\.[^<]+)</p>',
            re.DOTALL
        ),
        lambda m: '<p>' + m.group(1) + ' ' + m.group(2) + '</p>',
        html
    )
    if n13b:
        changes.append('Fix 13b: Joined split paragraph in section 3.1')
    else:
        changes.append('Fix 13b: WARNING - split paragraph not found')

    # Fix 13c: Move section 3.3 explanatory text to between Figure 11 and
    # Figure 12. Pipeline placed it after Figure 12 caption.
    # Step 1: Remove misplaced block after Figure 12 caption
    html, n13c_a = re.subn(
        re.compile(
            r'(<p class="figure-caption">Figure 12[^<]*</p>)\s*'
            r'<p>This screen makes the user aware[\s\S]*?'
            r'(?=<p>This screen will make the user aware)',
            re.DOTALL
        ),
        lambda m: m.group(1) + '\n',
        html
    )
    # Step 2: Insert correct block between Figure 11 caption and Figure 12 image
    _block33 = (
        '<p>This screen makes the user aware of how many RPNs on their request were successful.'
        ' The three possible outcomes are:</p>\n'
        '<ul>\n'
        '<li>RPNs returned \u2013 This is the number of employee RPNs that were successfully returned</li>\n'
        '<li>RPNs not returned \u2013 This is the number of employee RPNs that were not returned</li>\n'
        '<li>Validation errors \u2013 This is the number of validation errors in the request</li>\n'
        '</ul>\n'
        '<p>An RPN response file is automatically downloaded for the user in their selected file'
        ' format which details the outcome of the RPN request. The user can then input this file'
        ' to their payroll software in order to complete the next stage of their payroll process.</p>\n'
        '<p>The other summary screen the user may get is if they have completed the online form to'
        ' request RPNs for new employees or requested RPNs for a specific subset of existing'
        ' employees:</p>\n'
    )
    html, n13c_b = re.subn(
        re.compile(
            r'(<p class="figure-caption">Figure 11[^<]*</p>)\s*'
            r'(<p><img[^>]*figure_12\.png[^/]*/></p>)',
            re.DOTALL
        ),
        lambda m: m.group(1) + '\n' + _block33 + m.group(2),
        html
    )
    # Step 3: Convert any remaining paragraph-table for 'other summary screen'
    html = re.sub(
        re.compile(
            r'<table[^>]*>[\s\S]*?<td>The other summary screen the user may get[^<]*</td>'
            r'[\s\S]*?</table>',
            re.DOTALL
        ),
        '<p>The other summary screen the user may get is if they have completed the online form'
        ' to request RPNs for new employees or requested RPNs for a specific subset of existing employees:</p>',
        html
    )
    if n13c_a or n13c_b:
        changes.append('Fix 13c: Moved section 3.3 text block between Figure 11 and Figure 12')
    else:
        changes.append('Fix 13c: WARNING - section 3.3 reorder patterns not found')

    # Fix 14: Join split paragraph at 'system verifies' / 'password is correct'
    # Occurs in section 3.2.1 — PDF page break splits one sentence across two <p> tags
    html, n14 = re.subn(
        re.compile(
            r'<p>([^<]+the system verifies)</p>\s*<p>(that the password is correct[^<]+)</p>',
            re.DOTALL
        ),
        lambda m: '<p>' + m.group(1) + ' ' + m.group(2) + '</p>',
        html
    )
    if n14:
        changes.append(f'Fix 14: Joined {n14} split paragraph(s) - system verifies / password is correct')
    else:
        changes.append('Fix 14: WARNING - split paragraph not found')

    # Fix 11: Image placement fixes
    #   11a: Insert image_1 before orphaned Figure 1 caption
    #   11b: Extract img tags from inside malformed figure-caption <p>s
    #   11c: Delete stale images 31-60 from previous pipeline run
    # ------------------------------------------------------------------
    img_base = f'content/{env}/screens/overview_of_ros_payroll_reporting/images'

    def img_tag(n):
        return f'<p><img alt="Image" src="{img_base}/image_{n}.png"/></p>\n'

    # Fix 11a: Renumber images — the pipeline always extracts image_1.png
    # as the cover page branding strip (page 1, 686x220px). All actual
    # content screenshots are extracted as image_2..image_N, making every
    # figure render one position too high. Fix: detect the cover strip by
    # its dimensions, delete it, rename image_2->image_1 etc, update HTML.
    # Idempotent: if image_1 is already a real screenshot (width > 800px)
    # the renaming is skipped.
    img_dir = PROJECT_ROOT / 'content' / env / 'screens' / 'overview_of_ros_payroll_reporting' / 'images'
    cover = img_dir / 'image_1.png'
    if cover.exists():
        # Detect cover branding strip by file size (no PIL dependency).
        # Cover strip is always ~19KB; real screenshots are always 29KB+.
        if cover.stat().st_size < 25_000:
            cover.unlink()
            # Rename image_N -> image_(N-1) for N = 2..60 (reverse to avoid collisions)
            _renamed = 0
            for _n in range(2, 61):
                _src = img_dir / f'image_{_n}.png'
                _dst = img_dir / f'image_{_n-1}.png'
                if _src.exists():
                    _src.replace(_dst)
                    _renamed += 1
            # Update HTML src references image_N -> image_(N-1) in ONE regex
            # pass to avoid cascading replacements (sequential replace would
            # rename image_2->image_1, then image_1 again, etc.)
            def _decrement_img(m):
                return f'image_{int(m.group(1)) - 1}.png'
            html, _updates = re.subn(
                r'image_([2-9]\d*|[1-9]\d+)\.png',
                _decrement_img,
                html
            )
            changes.append(f'Fix 11a: Removed cover branding strip, renamed {_renamed} images, updated {_updates} HTML references')
        else:
            changes.append('Fix 11a: image_1 is already a content screenshot (correct numbering) - skipped')
    else:
        changes.append('Fix 11a: image_1.png not found - skipped')

    # Fix 11b: extract img tags embedded inside figure-caption paragraphs
    # Pattern: <p class="figure-caption"><img .../> \n Figure N: text</p>
    def extract_img_from_caption(m):
        img_src    = m.group(1)
        cap_text   = m.group(2).strip()
        return f'<p><img alt="Image" src="{img_src}"/></p>\n<p class="figure-caption">{cap_text}</p>'

    html, n11b = re.subn(
        re.compile(
            r'<p class="figure-caption"><img alt="Image" src="([^"]+)"/>\s*\n?(Figure [^<]+)</p>',
            re.DOTALL
        ),
        extract_img_from_caption,
        html
    )
    if n11b:
        changes.append(f'Fix 11b: Extracted {n11b} img tag(s) from inside figure-caption paragraphs')

    # Fix 11c: delete stale images from previous pipeline run
    # After Fix 11a renaming, real images are image_1..image_29.
    # Anything from image_30 upward is a stale duplicate.
    _stale_count = 0
    if img_dir.is_dir():
        for _i in range(30, 61):
            _stale = img_dir / f'image_{_i}.png'
            if _stale.exists():
                _stale.unlink()
                _stale_count += 1
    if _stale_count:
        changes.append(f'Fix 11c: Deleted {_stale_count} stale image(s) from image_30 upward')

    return html, changes




# ---------------------------------------------------------------------------
# ros_payroll_message_guide
# Fixes: 4 fragmented/mis-columned tables (Version History, Document
# References, JSON Message Data Items, Reference/Document Link) and 3
# orphaned single-column fragment tables produced when pdfplumber split a
# wrapped first-column cell into its own extra table.
# ---------------------------------------------------------------------------

MSGGUIDE_VERSION_HISTORY_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Version</th>
<th scope="col">Change Date</th>
<th scope="col">Section</th>
<th scope="col">Change Description</th>
</tr>
</thead>
<tbody>
<tr><td>1.0</td><td></td><td>All</td><td>Document published.</td></tr>
<tr><td>1.0 Release Candidate 2</td><td>24/05/2018</td><td></td><td>Version updated to 1.0 Release Candidate 2</td></tr>
</tbody>
</table>"""

MSGGUIDE_DOCUMENT_REFERENCES_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Reference</th>
<th scope="col">Document Link</th>
</tr>
</thead>
<tbody>
<tr><td>1. Documents Homepage</td><td><a href="https://revenue-ie.github.io/paye-employers-documentation/" target="_blank" rel="noopener noreferrer">https://revenue-ie.github.io/paye-employers-documentation/</a></td></tr>
</tbody>
</table>"""

MSGGUIDE_DATA_ITEMS_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Name</th>
<th scope="col">Description</th>
<th scope="col">Applicable Message</th>
</tr>
</thead>
<tbody>
<tr><td>Request type</td><td>Specifies the service to be called. Supported values : "lookupRPN", "createRPN", "payrollSubmission"</td><td>All</td></tr>
<tr><td>Employer Registration Number</td><td>The registration of the employer (up to 9 chars). Must be valid Employer Registered number. Format is 7 digits (including leading zeros) followed by either 1 or 2 letters</td><td>All</td></tr>
<tr><td>Tax Year</td><td>Tax Year to which the submission or request relates</td><td>All</td></tr>
<tr><td>Date Last Updated</td><td>Date to lookup for RPNs updated on or since</td><td>Look up RPN</td></tr>
<tr><td>Software Used</td><td>References to third party software used to make RPN request / payroll submission</td><td>All</td></tr>
<tr><td>Software Version</td><td>Version of software used to make request RPN request/ submission</td><td>All</td></tr>
<tr><td>Agent TAIN</td><td>Used to identify the agent submitting on behalf of the employer and to ensure that an agent link exists for this employer agent relationship for the period that the payroll submission relates to.</td><td>To be included if the RPN request or Payroll submission is being performed by an agent on behalf of an Employer</td></tr>
<tr><td>Payroll Run Reference</td><td>Used to identify the Payroll event that the submission refers to e.g. ‘Site 1 Week 1’.</td><td>Payroll Submission</td></tr>
<tr><td>Submission ID</td><td>Unique submission identifier. Must be unique for submissions under a given employer's PAYE registration number. For batch submissions, all submissions should have the same SubmissionID and should have the BatchID and BatchCount populated.</td><td>Payroll Submission</td></tr>
<tr><td>Employee IDs</td><td>Employee's PPS Number and Employee's Employment ID(Unique identifier for each distinct employment for an employee) are joined using a hyphen (eg.'1234567T-1').</td><td>Look up RPN – To be included if request is for specific Employees</td></tr>
<tr><td>Request Body</td><td>For Payroll submissions, this contains the Employee level details. For Create RPNs (NewRPN), this contains the Employee level details.</td><td>Payroll Submission, Create RPN (NewRPN)</td></tr>
</tbody>
</table>"""

MSGGUIDE_SCHEMA_REFERENCE_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Reference</th>
<th scope="col">Document Link</th>
</tr>
</thead>
<tbody>
<tr><td>JSON Envelope Schema</td><td><a href="https://revenue-ie.github.io/paye-employers-documentation//Screens/ROS_Payroll_Reporting_JSON_Envelope_schema.json" target="_blank" rel="noopener noreferrer">ROS_Payroll_Reporting_JSON_Envelope_schema.json</a></td></tr>
<tr><td>JSON Create RPN (Request body)</td><td><a href="https://revenue-ie.github.io/paye-employers-documentation/rest/paye-employers-rest-api.json" target="_blank" rel="noopener noreferrer">paye-employers-rest-api.json</a></td></tr>
<tr><td>JSON Payroll Submission (Request body)</td><td><a href="https://revenue-ie.github.io/paye-employers-documentation/rest/paye-employers-rest-api.json" target="_blank" rel="noopener noreferrer">paye-employers-rest-api.json</a></td></tr>
<tr><td>XML Look up RPNs</td><td><a href="https://revenue-ie.github.io/paye-employers-documentation/soap/v1/rpn/rpn-schema.xsd" target="_blank" rel="noopener noreferrer">rpn-schema.xsd</a></td></tr>
<tr><td>XML Create RPNs for new employees (New RPNs)</td><td><a href="https://revenue-ie.github.io/paye-employers-documentation/soap/v1/rpn/rpn-schema.xsd" target="_blank" rel="noopener noreferrer">rpn-schema.xsd</a></td></tr>
<tr><td>XML Payroll submission</td><td><a href="https://revenue-ie.github.io/paye-employers-documentation/soap/v1/payroll/payroll-schema.xsd" target="_blank" rel="noopener noreferrer">payroll-schema.xsd</a></td></tr>
</tbody>
</table>"""


def fix_ros_payroll_message_guide(html: str, env: str) -> tuple[str, list[str]]:
    changes = []

    # Fix 1: Replace broken 'Latest Version History' table (12 cols, mostly empty)
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)*<th[^>]*>Latest Version History</th>[\s\S]*?</table>', re.DOTALL),
        MSGGUIDE_VERSION_HISTORY_TABLE, html
    )
    changes.append(f"Fix 1: {'Replaced' if n else 'WARNING: not found —'} broken 'Latest Version History' table")

    # Fix 2: Replace broken 'Document References' table (introduction section)
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)*<th[^>]*>Document References</th>[\s\S]*?</table>', re.DOTALL),
        MSGGUIDE_DOCUMENT_REFERENCES_TABLE, html
    )
    changes.append(f"Fix 2: {'Replaced' if n else 'WARNING: not found —'} broken 'Document References' table")

    # Fix 3: Replace broken 'JSON Message – Data Items' table (9 cols, heavily fragmented)
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)*<th[^>]*>Name</th>[\s\S]*?</table>', re.DOTALL),
        MSGGUIDE_DATA_ITEMS_TABLE, html
    )
    changes.append(f"Fix 3: {'Replaced' if n else 'WARNING: not found —'} broken 'JSON Message – Data Items' table")

    # Fix 4: Remove orphaned 'Employer / Registration / Number' 1-column fragment
    # table (pdfplumber split-out of the Data Items table's wrapped first cell —
    # content is already present as 'Employer Registration Number' in Fix 3's table)
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>Employer</th>\s*</tr>\s*</thead>\s*<tbody>\s*<tr>\s*<td>Registration</td>\s*</tr>\s*<tr>\s*<td>Number</td>\s*</tr>\s*</tbody>\s*</table>\s*', re.DOTALL),
        '', html
    )
    if n:
        changes.append(f"Fix 4: Removed {n} orphaned 'Employer/Registration/Number' fragment table")

    # Fix 5: Remove orphaned '(NewRPN) / contains the Employee level details.'
    # fragment table (page-break continuation of the Data Items 'Request Body'
    # row — content already merged into Fix 3's Request Body cell)
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*></th>\s*<th[^>]*>contains the Employee level details\.</th>\s*<th[^>]*></th>\s*<th[^>]*>\(NewRPN\)</th>\s*<th[^>]*></th>\s*</tr>\s*</thead>[\s\S]*?</table>\s*', re.DOTALL),
        '', html
    )
    if n:
        changes.append(f"Fix 5: Removed {n} orphaned '(NewRPN)' page-break continuation table")

        # Fix 6: Replace broken Schema Reference table (fragmented, ends up under
    # section 5 due to a pipeline heading-order bug). Each <table>...</table>
    # is matched individually (non-greedy, cannot cross a </table> boundary)
    # and only substituted if that specific table's own content contains the
    # unique 'JSON Envelope Schema' marker. A plain header-anchored regex
    # with a lazy [\s\S]*? body is NOT safe here: since Fix 2's already-
    # cleaned Document References table shares the same 'Reference' header
    # but has no closing match for 'JSON Envelope Schema' inside it, the lazy
    # quantifier would skip straight over that table's </table> and keep
    # expanding through everything until it found the real target further
    # down — silently swallowing every section in between.
    def _fix6_repl(m):
        return MSGGUIDE_SCHEMA_REFERENCE_TABLE if 'JSON Envelope Schema' in m.group(0) else m.group(0)

    html, n_candidates = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)*<th[^>]*>Reference</th>[\s\S]*?</table>', re.DOTALL),
        _fix6_repl, html
    )
    n = 1 if 'JSON Envelope Schema' in MSGGUIDE_SCHEMA_REFERENCE_TABLE and MSGGUIDE_SCHEMA_REFERENCE_TABLE in html else 0
    changes.append(f"Fix 6: {'Replaced' if n else 'WARNING: not found —'} broken Schema Reference table")

    # Fix 7: Remove orphaned 'JSON Create RPN / (Request body)' 1-column
    # fragment table (pdfplumber split-out of the Schema Reference table's
    # wrapped first cell — content already present in Fix 6's table)
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>JSON Create RPN</th>\s*</tr>\s*</thead>\s*<tbody>\s*<tr>\s*<td>\(Request body\)</td>\s*</tr>\s*<tr>\s*<td>\(Request body\)</td>\s*</tr>\s*</tbody>\s*</table>\s*', re.DOTALL),
        '', html
    )
    if n:
        changes.append(f"Fix 7: Removed {n} orphaned 'JSON Create RPN / (Request body)' fragment table")

    # Fix 8: Move the Schema Reference table from Section 5 (Digital Signature)
    # to Section 4 (Schemas), where it actually belongs — the pipeline leaves
    # section 4 empty and places this table under section 5 by mistake.
    m = re.search(
        r'(<h2 class="pmod" id="4\._schemas">4\. Schemas</h2>\s*)'
        r'(<h2 class="pmod" id="5\._digital_signature">5\. Digital Signature</h2>\s*<p>[^<]*</p>\s*)'
        r'(<table class="table" tabindex="0">\s*<thead>\s*<tr>\s*<th scope="col">Reference</th>[\s\S]*?JSON Envelope Schema[\s\S]*?</table>)',
        html, re.DOTALL
    )
    if m:
        html = html[:m.start()] + m.group(1) + m.group(3) + '\n' + m.group(2) + html[m.end():]
        changes.append("Fix 8: Moved Schema Reference table from Section 5 to Section 4")

    # Fix 9: Convert run-on bullet <li> items (JSON/XML Messages sections) into
    # separate <li> elements. The pipeline joins '• A - • B - • C' PDF bullets
    # onto a single line instead of splitting them, and merges the trailing
    # sentence into the same <li>/<ul> as the last bullet.
    html, n = re.subn(
        re.compile(
            r'<li>Look up RPNs for existing employees - Create RPNs for new employees - Make a payroll submission'
            r'(?: This JSON envelope schema is required as takes in data items for these services which are provided as part of the URL if the service is invoked from the REST API\.)?'
            r'</li>'
        ),
        lambda mm: (
            '<li>Look up RPNs for existing employees</li>\n'
            '<li>Create RPNs for new employees</li>\n'
            '<li>Make a payroll submission</li>'
            + ('</ul>\n<p>This JSON envelope schema is required as takes in data items for these services which are provided as part of the URL if the service is invoked from the REST API.</p>\n<ul>' if 'This JSON envelope schema' in mm.group(0) else '')
        ),
        html
    )
    if n:
        changes.append(f"Fix 9: Split {n} run-on bullet list item(s) into separate <li> elements")

    # Fix 9 leaves a stray trailing <ul></ul> if the JSON-envelope sentence
    # variant fired (its replacement re-opens a <ul> that the original closing
    # </ul> then immediately closes again). Collapse that empty tag pair.
    html, n = re.subn(r'<ul>\s*</ul>\s*', '', html)
    if n:
        changes.append(f"Fix 9b: Removed {n} empty <ul></ul> artifact")

    return html, changes


# ---------------------------------------------------------------------------
# selfservice_coverpage
# Fixes: duplicate h2 headings, broken version history table
# ---------------------------------------------------------------------------

SS_CLEAN_VERSION_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Version</th>
<th scope="col">Date</th>
<th scope="col">Section</th>
<th scope="col">Change Description</th>
</tr>
</thead>
<tbody>
<tr><td>0.1</td><td>20/03/2018</td><td>All</td><td>Initial draft</td></tr>
<tr><td></td><td></td><td>Appendices</td><td>7.3 Known Issues section added</td></tr>
<tr><td>1.0 Release Candidate 2</td><td>25/05/2018</td><td></td><td>Version updated to 1.0 Release Candidate 2</td></tr>
<tr><td></td><td>29/06/2018</td><td>Section 7</td><td>Added</td></tr>
<tr><td></td><td>20/07/2018</td><td>Section 6.1</td><td>Added</td></tr>
<tr><td></td><td>31/07/2018</td><td>Appendix</td><td>Added Returns Reconciliations endpoints</td></tr>
<tr><td></td><td>29/04/2019</td><td>Section 6</td><td>Added customer with fada description</td></tr>
<tr><td></td><td>09/08/2019</td><td>Section 3</td><td>Added detail about new employee overview screen and the new request specific certificate button</td></tr>
<tr><td></td><td></td><td>Section 4.0</td><td>Added section on employee overview</td></tr>
<tr><td></td><td></td><td>Section 4.1</td><td>Added section on edit employee</td></tr>
<tr><td></td><td></td><td>Section 5.2</td><td>Added section on Request Specific Employee button</td></tr>
</tbody>
</table>"""


def fix_selfservice_coverpage(html: str, env: str) -> tuple[str, list[str]]:
    changes = []

    # Fix 1: Remove duplicate h2 headings and fix Audience paragraph
    html, n = re.subn(
        re.compile(
            r'<h2[^>]*id="pit_self_service_application_guide"[^>]*>.*?</h2>\s*'
            r'<h2[^>]*id="paye_modernisation"[^>]*>.*?</h2>\s*'
            r'<p>Audience (This document.*?)</p>', re.DOTALL
        ),
        lambda m: f'<p>{m.group(1)}</p>', html
    )
    changes.append(f"Fix 1: {'Removed' if n else 'NOTE: not found —'} duplicate h2 headings")

    # Fix 2: Replace broken version history table
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*></th>\s*)*<th[^>]*>Version History</th>[\s\S]*?</table>', re.DOTALL),
        SS_CLEAN_VERSION_TABLE, html
    )
    changes.append(f"Fix 2: {'Replaced' if n else 'NOTE: not found —'} broken version history table")

    return html, changes


# ---------------------------------------------------------------------------
# selfservice_appendix
# Fixes: broken appendix section with spaced-out URLs
# ---------------------------------------------------------------------------

SS_CLEAN_APPENDIX = """\
<h3 class="pmod" id="9_appendix">9 APPENDIX</h3>
<p>This appendix provides the set of REST and SOAP web service endpoints for the Payroll and RPN services available for testing in the Public Interface Testing environment.</p>
<h4 id="9.1_rest_api_endpoints">9.1 REST API Endpoints</h4>
<h4 id="9.1.1_rpn_services">9.1.1 RPN Services</h4>
<p><strong>9.1.1.1 POST &ndash; Create New RPN</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/rpn/{{employerRegistrationNumber}}/{{taxYear}}?softwareUsed={{SoftwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/rpn/{{employerRegistrationNumber}}/{{taxYear}}?softwareUsed={{SoftwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<p>Example: <a href="https://{HOST}/paye-employers/v1/rest/rpn/00001013N/2018?softwareUsed=abc&amp;softwareVersion=1.0" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/rpn/00001013N/2018?softwareUsed=abc&amp;softwareVersion=1.0</a></p>
<p><strong>9.1.1.2 GET &ndash; Look Up RPN</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/rpn/{{employerRegistrationNumber}}/{{taxYear}}?softwareUsed={{SoftwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/rpn/{{employerRegistrationNumber}}/{{taxYear}}?softwareUsed={{SoftwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<p>Example: <a href="https://{HOST}/paye-employers/v1/rest/rpn/03390656OH/2018?softwareUsed=1&amp;softwareVersion=1.0" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/rpn/03390656OH/2018?softwareUsed=1&amp;softwareVersion=1.0</a></p>
<p><strong>9.1.1.3 GET &ndash; Look Up RPN by employee</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/rpn/{{employerRegistrationNumber}}/{{taxYear}}/{{employeeId}}?softwareUsed={{SoftwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/rpn/{{employerRegistrationNumber}}/{{taxYear}}/{{employeeId}}?softwareUsed={{SoftwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<h4 id="9.1.2_payroll_services">9.1.2 Payroll Services</h4>
<p><strong>9.1.2.1 POST &ndash; Payroll Submission</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistrationNumber}}/{{taxYear}}/{{payrollRunReference}}/{{SubmissionID}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistrationNumber}}/{{taxYear}}/{{payrollRunReference}}/{{SubmissionID}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<p><strong>9.1.2.2 GET &ndash; Check Payroll Submission</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistrationNumber}}/{{taxYear}}/{{PayrollRunReference}}/{{SubmissionID}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistrationNumber}}/{{taxYear}}/{{PayrollRunReference}}/{{SubmissionID}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<p><strong>9.1.2.3 GET &ndash; Check Payroll Run</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistration}}/{{taxYear}}/{{PayrollRunReference}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistration}}/{{taxYear}}/{{PayrollRunReference}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<h3 class="pmod" id="9.2_soap_api_endpoints">9.2 SOAP API Endpoints</h3>
<h4 id="9.2.1_rpn_services">9.2.1 RPN Services</h4>
<p><a href="https://{HOST}/paye-employers/v1/soap/rpn" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/soap/rpn</a></p>
<h4 id="9.2.2_payroll_service">9.2.2 Payroll Service</h4>
<p><a href="https://{HOST}/paye-employers/v1/soap/payroll" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/soap/payroll</a></p>
<h3 class="pmod" id="9.3_known_issues">9.3 Known Issues</h3>
<h4 id="9.3.1_self_service_application_login">9.3.1 Self Service Application Login</h4>
<p>On clicking the &#39;register for ROS&#39; link on the Self Service Application login page in PIT3 a &#39;503 service unavailable&#39; page is displayed to the user.</p>
</div></body></html>"""


def fix_selfservice_appendix(html: str, env: str) -> tuple[str, list[str]]:
    changes = []
    host = HOSTS.get(env, HOSTS["PIT3"])
    replacement = SS_CLEAN_APPENDIX.replace("{HOST}", host)
    html, n = re.subn(
        re.compile(r'<h3[^>]*id="9_appendix"[^>]*>[\s\S]*$', re.DOTALL),
        replacement, html
    )
    changes.append(f"Fix 1: {'Replaced' if n else 'WARNING: not found —'} broken appendix section (host: {host})")
    return html, changes


# ---------------------------------------------------------------------------
# helpdesk_guide
# Fixes: junk page-header tables, renames output file
# Note: no --pit argument — PIT3 only, operates on a fixed path
# ---------------------------------------------------------------------------

HELPDESK_JUNK_TABLE_RE = re.compile(
    r'\n?<table[^>]*>\s*<thead>\s*<tr>\s*'
    r'<th[^>]*>\s*</th>\s*'
    r'<th[^>]*>\s*PAYE PIT Help Desk\s*.{1,3}\s*User Guide\s*</th>\s*'
    r'<th[^>]*>\s*</th>\s*'
    r'</tr>\s*</thead>\s*'
    r'<tbody>(?:\s*<tr>(?:\s*<td[^>]*>\s*</td>\s*)+</tr>\s*)+</tbody>\s*'
    r'</table>',
    re.DOTALL
)


def fix_helpdesk_guide(html: str, env: str) -> tuple[str, list[str]]:
    changes = []
    html, n = HELPDESK_JUNK_TABLE_RE.subn("", html)
    changes.append(f"Fix 1: Removed {n} junk page-header table(s)")
    return html, changes


# ---------------------------------------------------------------------------
# rpn_csv_response
# Fixes: 6-page main data table split into 4 fragments with phantom empty
# columns (Name / Column Name / Description and validation / Context should
# be 4 real columns, not 6-12 mostly-empty ones); Column Descriptions and
# Version History tables have the same phantom-column problem; technical
# camelCase column names broken by PDF word-wrap (e.g. 'employerNa me' ->
# 'employerName'); one genuine cross-page row continuation (Effective Date /
# calculation basis text) that must be merged into a single cell.
# ---------------------------------------------------------------------------

RPNCSV_COLUMN_DESCRIPTIONS_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Column</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr><td>Data Item</td><td>Name of data item</td></tr>
<tr><td>Description and Validation</td><td>Description of the data element and the validation rules that will be applied</td></tr>
<tr><td>Context</td><td>How the data element will be used by Revenue</td></tr>
</tbody>
</table>"""

RPNCSV_VERSION_HISTORY_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Version</th>
<th scope="col">Change Date</th>
<th scope="col">Element</th>
<th scope="col">Change Description</th>
</tr>
</thead>
<tbody>
<tr><td>0.10</td><td>02/02/2018</td><td>N/A</td><td>Document published</td></tr>
<tr><td>1.0 Release Candidate 2</td><td>24/05/2018</td><td></td><td>Version updated to 1.0 Release Candidate 2</td></tr>
<tr><td></td><td>02/03/2020</td><td>Employment Cessation Date</td><td>Item added</td></tr>
<tr><td></td><td>22/01/2025</td><td>State Pension (Contributory)</td><td>Item added</td></tr>
</tbody>
</table>"""

# Main data table: 4 real columns (Name / Column Name / Description and
# validation / Context). Column Name values are the exact camelCase field
# names from the source PDF with PDF-wrap spacing removed. Verified against
# the raw PDF text (pdfplumber extract_text(), pages 3-8) row by row.
#
# Two cross-page split behaviours confirmed present, handled as follows:
#   - 'Effective Date' row: genuinely continues onto the next page with
#     real content - merged into one cell here.
#   - 'Exclusion Order' row: also split across pages, but the continuation
#     has no content on the second page - no merge needed, row is complete
#     as-is.
RPNCSV_MAIN_TABLE = """<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Name</th>
<th scope="col">Column Name</th>
<th scope="col">Description and validation</th>
<th scope="col">Context</th>
</tr>
</thead>
<tbody>
<tr><td>Employer Name</td><td>employerName</td><td>Header: Employer name, max length 100 characters</td><td>Use to identify the employer and confirm that the employer name matches with Revenue records</td></tr>
<tr><td>Employer Registration number</td><td>employerRegistrationNumber</td><td>Header: Used to identify employer to which the submission relates, max length 100 characters.</td><td>Used to identify employer to which the submission relates.</td></tr>
<tr><td>Agent Tain</td><td>agentTain</td><td>Header: Tax Advisor Identification Number. Required if RPN is queried by agent on behalf of employer.</td><td></td></tr>
<tr><td>Tax Year</td><td>taxYear</td><td>Header: Used to identify the tax year to which the RPN lookup relates (YYYY)</td><td>The Tax Year RPN relates to</td></tr>
<tr><td>Total RPN count</td><td>totalRPNCount</td><td>Header: Total number of RPNs returned</td><td>The total number of RPN that are associated with the RPN request submitted.</td></tr>
<tr><td>Date time Effective</td><td>dateTimeEffective</td><td>Header: The date and time at which the RPN returned is correct/was issued (YYYY-MM-DDThh:mm:ss.sss&plusmn;hhmm). max length 28</td><td>Date &amp; time from when the RPN is effective from</td></tr>
<tr><td>RPN Number</td><td>rpnNumber</td><td>RPN: The number of the RPN issued to the employer in respect of an employee. Or value Not Found Max length 20</td><td>RPN: List of RPN that make up a valid lookup RPN response. NoRPN: EmployeePPSNs and EmploymentIDs of employees who do not currently have an RPN associated with the employer. New RPN need to be requested for these employees using the NewRPNRequest service. Used in conjunction with the Employee PPSN to uniquely identify the instruction issued.</td></tr>
<tr><td>Employee PPSN</td><td>employeePPSN</td><td>Format is 7 digits (including leading zeros) followed by either 1 or 2 letters. Max length 10</td><td>Used to identify employee to which the RPN relates.</td></tr>
<tr><td>Employment ID</td><td>employmentID</td><td>The value of this field will be the Employment ID provided to Revenue by the employer when setting up the employment. If the RPN is being triggered as a result of the employee setting up the employment via Jobs and Pension or contacting Revenue, the value of this field will not be populated. Max length 20</td><td>Used to uniquely identify each employment for the employee.</td></tr>
<tr><td>RPN Issue Date</td><td>rpnIssueDate</td><td>RPN: Date format yyyy-mm-dd. Max length 10</td><td>The date the RPN issued.</td></tr>
<tr><td>Employer Reference</td><td>employerReference</td><td>Employee internal staff identifier.</td><td>Used to uniquely identify the unique employment for the employer and employee.</td></tr>
<tr><td>First Name</td><td>firstName</td><td>First name of the employee. Max length 100 characters</td><td>Employee first name</td></tr>
<tr><td>Family Name</td><td>familyName</td><td>Family name of the employee. Max length 100 characters</td><td>Employee family name</td></tr>
<tr><td>Previous Employee PPSN</td><td>previousEmployeePPSN</td><td>Must be valid PPS number (up to 9 chars). Format is 7 digits (including leading zeros) followed by either 1 or 2 letters.</td><td>Used to identify employees previous PPS number if applicable e.g. W PPS number. Should only appear if changed since previous submission This will appear until Revenue knows that the payroll operator has updated the Employee PPSN in their own system i.e. until Revenue receives a submission with the new Employee PPSN</td></tr>
<tr><td>Effective Date</td><td>effectiveDate</td><td>First day on which the RPN specified will apply. Max length 10 &bull; If the RPN is issued before the start of the tax year in question this will be set to January 1st of the tax year. &bull; If the RPN is issued during the tax year in question the date is dependent on the calculation basis of the RPN as follows: o If the calculation basis is Cumulative the date will be set to January 1st of the year. o If the calculation basis is Week 1 the date will be set to the date the RPN issued. Date format yyyy-mm-dd Min date 2019-01-01 Date can be in the future</td><td>The instruction can be used from this date until updated again.</td></tr>
<tr><td>End Date</td><td>endDate</td><td>The date the RPN ends. Date format yyyy-mm-dd Min date 2019-01-01 Max length 10 Last date on which the RPN specified will apply. After this date a new RPN should be requested.</td><td>Applicable to Tax Basis Week 1. For Cumulative instruction the date will be the XXXX-12-31. This will appear if applicable.</td></tr>
<tr><td>Employment Cessation Date</td><td>employmentCessationDate</td><td>This is the date the employment ceased. It is a conditional data item and will only appear when the employment to which the RPN relates was ceased either by the employer or the employee during the current year. Date format yyyy-mm-dd Min date 202X-01-01</td><td>RPNs for ceased employments are required if a post cessation payment is being made. The Employment Cessation Date allows the employer/payroll operator to distinguish between RPNs for live employments and ceased employments.</td></tr>
<tr><td>Income Tax Calculation Basis</td><td>incomeTaxCalculationBasis</td><td>PAYE calculation basis used in the submission. Options allowed are Cumulative, Week1 and Emergency.</td><td>Used to indicate the correct tax basis to be applied.</td></tr>
<tr><td>Exclusion Order</td><td>exclusionOrder</td><td>Set to &ldquo;true&rdquo; if an exclusion order is on file for the employee. This field is not included if an exclusion order is not on file for the employee</td><td>Used to indicate if there is an exclusion order on file for the employee for the specified period.</td></tr>
<tr><td>Yearly Tax Credit</td><td>yearlyTaxCredits</td><td>Amount of tax credits available to the employee for the year the RPN relates to. This number will contain two decimal places. Positive number only</td><td>Net Tax Credits. Amount of tax credits available to the employee for the year the RPN relates to. Amount of tax credits available for use in the PAYE calculation. Breakdown is displayed to employee through PAYE Services.</td></tr>
<tr><td>Tax Rate 1 Percent</td><td>taxRatePercent1</td><td>The lower rate of tax for the year the RPN relates to. Positive number only</td><td>Rate to be applied for any income below Rate 1 Cut Off.</td></tr>
<tr><td>Yearly Rate 1 Cut Off</td><td>yearlyRateCutoff1</td><td>Rate 1 cut off for the year the RPN relates. Positive number only</td><td>Breakdown is displayed to employee through PAYE Services</td></tr>
<tr><td>Tax Rate 2 Percent</td><td>taxRatePercent2</td><td>The higher rate of tax for the year the RPN relates to. Positive number only.</td><td>Rate to be applied for any income above Rate 1 Cut Off</td></tr>
<tr><td>Pay for Income Tax to Date</td><td>payForIncomeTaxToDate</td><td>This will include total income liable to Income Tax to date &ndash; including previous employment income. In the case of recommencements, this includes previous pay from that employer in the same tax year. This number will contain two decimal places. This field will be populated where the Income Tax Calculation Basis is cumulative.</td><td>When multiple employments exist, RPN must include correct previous employment income. This will include only the previous Pay and Tax that should be applied.</td></tr>
<tr><td>Income Tax Deducted to Date</td><td>incomeTaxDeductedToDate</td><td>Total amount of employee&rsquo;s Income Tax deducted to date. In the case of recommencements, this includes previous tax from that employer in the same tax year. This number will contain two decimal places. This field will be populated where the Income Tax Calculation Basis is cumulative.</td><td>Total Income Tax paid to date. Taking into account any PAYE refunded through any unemployment repayment claim(s).</td></tr>
<tr><td>USC Status</td><td>uscStatus</td><td>Ordinary Exempt</td><td>Used to deduct correct amount of USC.</td></tr>
<tr><td>USC Rate 1 Percent</td><td>uscRatePercent1</td><td>USC Rate 1 Percent applicable to USC Status Ordinary in the year the RPN relates to. This number will contain two decimal places. Positive number only</td><td>Current rate 0.5%.</td></tr>
<tr><td>Yearly USC Rate 1 Cut Off</td><td>yearlyUSCRateCutoff1</td><td>Yearly USC rate 1 cut off applicable to USC Status Ordinary in the year the RPN relates to. This number will contain two decimal places. Positive number only.</td><td></td></tr>
<tr><td>USC Rate 2 Percent</td><td>uscRatePercent2</td><td>USC Rate 2 Percent applicable to USC Status Ordinary in the year the RPN relates to. This number will contain two decimal places. Positive number only.</td><td>Current rate 2.5%.</td></tr>
<tr><td>Yearly USC Rate 2 Cut Off</td><td>yearlyUSCRateCutoff2</td><td>Yearly USC rate 2 cut off applicable to USC Status Ordinary in the year the RPN relates to. This number will contain two decimal places. Positive number only</td><td></td></tr>
<tr><td>USC Rate 3 Percent</td><td>uscRatePercent3</td><td>USC Rate 3 Percent applicable to USC Status Ordinary in the year the RPN relates to. This number will contain two decimal places. Positive number only</td><td>Current rate 5%.</td></tr>
<tr><td>Yearly USC Rate 3 Cut Off</td><td>yearlyUSCRateCutoff3</td><td>Yearly USC rate 3 cut off applicable to USC Status Ordinary in the year the RPN relates to. This number will contain two decimal places. Positive number only</td><td></td></tr>
<tr><td>USC Rate 4 Percent</td><td>uscRatePercent4</td><td>Yearly USC rate 4 cut off applicable to USC Status Ordinary in the year the RPN relates to. This number will contain two decimal places. Positive number only</td><td>Current rate 8%.</td></tr>
<tr><td>Yearly USC Rate 4 Cut Off</td><td>yearlyUSCRateCutoff4</td><td>Yearly USC rate 4 applicable to USC Status Ordinary in the year the RPN relates to. This number will contain two decimal places. Positive number only</td><td></td></tr>
<tr><td>Pay for USC to Date</td><td>payForUSCToDate</td><td>Net pay subject to USC. This number will contain two decimal places. This field will be populated where the Income Tax Calculation Basis is cumulative.</td><td>This will include total income liable to USC to date &ndash; including previous employment income and any additional declared income liable to USC e.g. Rental Income. This will appear if available.</td></tr>
<tr><td>USC Deducted To Date</td><td>uscDeductedToDate</td><td>Total amount of employee&rsquo;s USC deducted to date. This number will contain two decimal places. This field will be populated where the Income Tax Calculation Basis is cumulative. Positive number only</td><td>Total USC paid to date. Taking into account any USC refunded through any unemployment repayment claim(s). This will appear if available</td></tr>
<tr><td>LPT to be Deducted</td><td>lptToDeduct</td><td>Local Property Tax amount due. Positive number only</td><td>Amount of LPT to be deducted through payroll.</td></tr>
<tr><td>State Pension (Contributory)</td><td>statePensionCont</td><td>Set to TRUE or FALSE indicating that the person is receiving their state pension. This field will be required to be TRUE on all RPNs for people that are drawing down their state contributory pension.</td><td>This field will default to false on all RPNs for people that are not drawing down their state contributory pension.</td></tr>
<tr><td>Employee is exempt from PRSI in Ireland</td><td>prsiExempt</td><td>Set to &ldquo;true&rdquo; if employee has been granted an exemption from paying PRSI in Ireland. This field is not included if employee is not exempt from paying PRSI.</td><td>This will appear only where DSP carries out a review and determines that the individual should be exempt from paying PRSI in Ireland. This must not be confused with PRSI exempt income. Will only appear where available.</td></tr>
<tr><td>PRSI Class and Subclass</td><td>prsiClass</td><td>PRSI Class and Subclass that the employee should be updated to.</td><td>This will appear only where DSP updates the class or where DSP knows the individual is on the wrong class (i.e. where a review has been carried out by DSP) Will only appear where available.</td></tr>
</tbody>
</table>"""


def fix_rpn_csv_response(html: str, env: str) -> tuple[str, list[str]]:
    changes = []

    # Fix 0: Correct section heading order/placement in the Column Descriptions
    # area. The source PDF order is: 'Column Descriptions' heading -> Column/
    # Description table -> 'Latest Version History' heading -> Version table
    # -> 'Note on ‘Conditional’ data items:' heading -> paragraph. The pipeline
    # instead hoists the 'Note on Conditional data items' heading up to sit
    # directly after 'Column Descriptions' (before either table), and drops
    # the 'Latest Version History' heading entirely. Both are corrected here:
    # the misplaced heading is removed from its wrong position, the missing
    # heading is re-inserted before the Version table (added in Fix 2 below),
    # and the paragraph + its correct heading are moved to their proper place
    # after the Version table.
    m = re.search(
        r'(<h3 class="pmod" id="column_descriptions">Column Descriptions</h3>\s*)'
        r'(<h3 class="pmod" id="note_on_[^"]*">Note on [^<]*</h3>\s*)'
        r'(<p>Where the data item is applicable[\s\S]*?is mandatory\.</p>\s*)',
        html
    )
    if m:
        html = html[:m.start()] + m.group(1) + html[m.end():]
        note_heading_and_para = m.group(2) + m.group(3)
        changes.append("Fix 0: Moved misplaced 'Note on ‘Conditional’ data items:' heading out of Column Descriptions intro")
    else:
        note_heading_and_para = None
        changes.append("Fix 0: WARNING: misplaced 'Note on Conditional data items' heading not found —")

    # Fix 1: Replace broken 'Column' / 'Description' table (Column Descriptions
    # section) - phantom empty columns collapsed to the 2 real columns.
    html, n = re.subn(
        re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)*<th[^>]*>Column</th>[\s\S]*?</table>', re.DOTALL),
        RPNCSV_COLUMN_DESCRIPTIONS_TABLE, html
    )
    changes.append(f"Fix 1: {'Replaced' if n else 'WARNING: not found —'} broken Column Descriptions table")

    # Fix 2: Replace broken 'Version' / 'Change Date' / 'Element' / 'Change
    # Description' table (Latest Version History) - phantom empty columns
    # collapsed to the 4 real columns. Also re-inserts the 'Latest Version
    # History' heading (dropped by the pipeline) directly before the table,
    # and re-inserts the 'Note on ‘Conditional’ data items:' heading plus its
    # paragraph (moved out of the intro by Fix 0) directly after the table —
    # matching the source PDF's actual section order.
    version_table_re = re.compile(r'<table[^>]*>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)*<th[^>]*>Version</th>[\s\S]*?</table>', re.DOTALL)
    n = len(version_table_re.findall(html))
    if n:
        replacement = '<h4 id="latest_version_history">Latest Version History</h4>\n' + RPNCSV_VERSION_HISTORY_TABLE
        if note_heading_and_para:
            replacement += '\n' + note_heading_and_para.rstrip()
        html = version_table_re.sub(replacement, html, count=1)
        changes.append("Fix 2: Replaced broken Version History table, restored 'Latest Version History' heading, repositioned 'Note on Conditional data items' section after it")
    else:
        changes.append("Fix 2: WARNING: not found — broken Version History table")

    # Fix 3: Replace all fragmented 'Name' / 'Column' / 'Description and
    # validation' / 'Context' table fragments (the main data table, split by
    # the pipeline into 4 separate <table> blocks across the underlying
    # 6-page PDF table) with a single clean, merged table. Every fragment
    # shares the same 'Name' header, so all of them are located; the first
    # occurrence is replaced with the clean merged table and any remaining
    # fragments are removed outright.
    fragment_re = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>Name</th>[\s\S]*?</table>\s*',
        re.DOTALL
    )
    count = len(fragment_re.findall(html))
    if count:
        first_done = [False]

        def _repl(m):
            if not first_done[0]:
                first_done[0] = True
                return RPNCSV_MAIN_TABLE + '\n'
            return ''

        html = fragment_re.sub(_repl, html)
        changes.append(f"Fix 3: Replaced {count} fragmented main data table piece(s) with 1 clean merged table")
    else:
        changes.append("Fix 3: WARNING: no main data table fragments found —")

    # Fix 4: Reformat the 'Version 1.0 Release Candidate 2 Version Date
    # 02/03/2020' intro paragraph into a two-column label/value layout
    # (Version on the left, Version Date right-aligned) matching the source
    # PDF's cover-page presentation, instead of a single run-on sentence.
    html, n = re.subn(
        re.compile(r'<p>Version ([^<]+?) Version Date (\d{2}/\d{2}/\d{4})</p>'),
        r'<div style="display:flex; justify-content:space-between; margin:0.5rem 0;">'
        r'<span><strong>Version</strong> \1</span>'
        r'<span><strong>Version Date</strong> \2</span>'
        r'</div>',
        html
    )
    if n:
        changes.append("Fix 4: Reformatted 'Version / Version Date' line into two-column layout")

    return html, changes


# ===========================================================================
# FIX REGISTRY — maps fix key -> function
# ===========================================================================

FIX_REGISTRY = {
    "rest_integration_guide":   fix_rest_integration_guide,
    "ros_payroll_reporting":     fix_ros_payroll_reporting,
    "ros_payroll_message_guide": fix_ros_payroll_message_guide,
    "selfservice_coverpage":     fix_selfservice_coverpage,
    "selfservice_appendix":      fix_selfservice_appendix,
    "helpdesk_guide":            fix_helpdesk_guide,
    "rpn_csv_response":          fix_rpn_csv_response,
}

# ===========================================================================
# RUNNER
# ===========================================================================

def load_registry() -> list[dict]:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["documents"]


def get_html_path(doc: dict, env: str) -> Path:
    # Support per-environment filenames (html_filename_pit3 / html_filename_pit4)
    # falling back to shared html_filename if no env-specific one is defined.
    env_key = f'html_filename_{env.lower()}'
    filename = doc.get(env_key) or doc.get('html_filename', '')
    return PROJECT_ROOT / 'content' / env / doc['content_path'] / filename


def run_fixes_for_doc(doc: dict, env: str) -> bool:
    """Run all registered fixes for a document in a given environment. Returns True on success."""

    # Special case: helpdesk_guide — rename spaced filename first
    if doc["key"] == "helpdesk_guide":
        spaced_src = PROJECT_ROOT / "content" / "pit" / "paye pit help desk user guide.html"
        dest = get_html_path(doc, env)
        if spaced_src.exists():
            if dest.exists():
                dest.unlink()
            spaced_src.rename(dest)
            print(f"  Renamed: {spaced_src.name} -> {dest.name}")

    html_path = get_html_path(doc, env)

    if not html_path.is_file():
        print(f"  SKIP: file not found: {html_path}")
        return False

    print(f"  Processing: {html_path.relative_to(PROJECT_ROOT)}")

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    for fix_key in doc["fixes"]:
        fix_fn = FIX_REGISTRY.get(fix_key)
        if not fix_fn:
            print(f"  WARNING: no fix function registered for key '{fix_key}'")
            continue
        html, changes = fix_fn(html, env)
        for change in changes:
            print(f"    {change}")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  OK: written")
    return True


def cmd_list(docs: list[dict]):
    print(f"\n{'Key':<30} {'Description':<45} {'Environments':<15} Fixes")
    print("-" * 110)
    for doc in docs:
        envs  = ", ".join(doc["environments"])
        fixes = ", ".join(doc["fixes"])
        notes = f"  [{doc['notes']}]" if doc.get("notes") else ""
        print(f"{doc['key']:<30} {doc['description']:<45} {envs:<15} {fixes}{notes}")
    print()


def cmd_run(docs: list[dict], doc_key: str, env: str):
    envs_to_run = [env] if env != "ALL" else ["PIT3", "PIT4"]
    matched = [d for d in docs if d["key"] == doc_key]
    if not matched:
        print(f"ERROR: no document registered with key '{doc_key}'")
        print("Run with --list to see all registered documents.")
        sys.exit(1)
    doc = matched[0]
    for e in envs_to_run:
        if e not in doc["environments"]:
            print(f"  SKIP: {doc['description']} is not registered for {e}")
            continue
        print(f"\n[{e}] {doc['description']}")
        run_fixes_for_doc(doc, e)


def cmd_all(docs: list[dict], env: str):
    envs_to_run = [env] if env != "ALL" else ["PIT3", "PIT4"]
    for e in envs_to_run:
        for doc in docs:
            if e not in doc["environments"]:
                continue
            print(f"\n[{e}] {doc['description']}")
            run_fixes_for_doc(doc, e)


# ===========================================================================
# ENTRY POINT
# ===========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Run post-pipeline HTML fixes for migrated documents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_doc_fixes.py --list
  python run_doc_fixes.py --doc rest_integration_guide --pit PIT3
  python run_doc_fixes.py --doc ros_payroll_reporting --pit ALL
  python run_doc_fixes.py --all --pit PIT3
  python run_doc_fixes.py --all --pit ALL
        """
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="List all registered documents")
    group.add_argument("--doc",  metavar="KEY",       help="Run fixes for a specific document key")
    group.add_argument("--all",  action="store_true", help="Run fixes for all registered documents")

    parser.add_argument("--pit", choices=["PIT3", "PIT4", "ALL"],
                        help="Environment to fix (required unless --list)")

    args = parser.parse_args()

    if not args.list and not args.pit:
        parser.error("--pit is required unless using --list")

    docs = load_registry()

    if args.list:
        cmd_list(docs)
    elif args.doc:
        cmd_run(docs, args.doc, args.pit)
    elif args.all:
        cmd_all(docs, args.pit)


if __name__ == "__main__":
    main()
