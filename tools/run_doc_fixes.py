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

    # Fix 2c: "other summary screen" paragraph-table -> <p>
    html, n = re.subn(
        re.compile(
            r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>(?:</th>|)</th>?\s*</tr>\s*</thead>\s*<tbody>\s*'
            r'<tr>\s*<td>The other summary screen the user may get is if they have completed the online form to request RPNs</td>\s*</tr>\s*'
            r'<tr>\s*<td>for new employees or requested RPNs for a specific subset of existing employees:</td>\s*</tr>\s*'
            r'(?:<tr>\s*<td></td>\s*</tr>\s*)*</tbody>\s*</table>', re.DOTALL
        ),
        '<p>The other summary screen the user may get is if they have completed the online form to request RPNs for new employees or requested RPNs for a specific subset of existing employees:</p>',
        html
    )
    if n:
        changes.append('Fix 2c: Converted section 3.3 summary intro paragraph-table to <p>')

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


# ===========================================================================
# FIX REGISTRY — maps fix key -> function
# ===========================================================================

FIX_REGISTRY = {
    "rest_integration_guide": fix_rest_integration_guide,
    "ros_payroll_reporting":   fix_ros_payroll_reporting,
    "selfservice_coverpage":   fix_selfservice_coverpage,
    "selfservice_appendix":    fix_selfservice_appendix,
    "helpdesk_guide":          fix_helpdesk_guide,
}

# ===========================================================================
# RUNNER
# ===========================================================================

def load_registry() -> list[dict]:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["documents"]


def get_html_path(doc: dict, env: str) -> Path:
    return PROJECT_ROOT / "content" / env / doc["content_path"] / doc["html_filename"]


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
