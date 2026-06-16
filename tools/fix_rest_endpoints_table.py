"""
fix_rest_endpoints_table.py
===========================
Replaces the broken section 2.1 REST Endpoints tables in the
rest_web_service_integration_guide.html for a given PIT environment.

The pipeline splits the table across multiple HTML tables due to PDF
page breaks. This script replaces them with a single clean hand-authored
table and removes the misplaced ERN/Monthly ERR rows that appear after
section 2.1.1.

Usage:
    python fix_rest_endpoints_table.py --pit PIT3
    python fix_rest_endpoints_table.py --pit PIT4
"""

import argparse
import os
import re

# ---------------------------------------------------------------------------
# Clean hand-authored section 2.1 REST Endpoints table
# ---------------------------------------------------------------------------

CLEAN_TABLE = """<table class="table" tabindex="0">
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


def fix_html(html: str) -> tuple[str, list[str]]:
    """
    Apply all fixes to the HTML and return (fixed_html, list_of_changes).
    """
    changes = []

    # ------------------------------------------------------------------
    # Fix 1: Replace all broken tables between the section 2.1 heading
    # and the "*Agent Tain" footnote with a single clean table.
    # The pipeline splits this across 2 tables due to PDF page breaks.
    # ------------------------------------------------------------------
    pattern_section_21 = re.compile(
        r'(<h3[^>]*id="2\.1\._rest_endpoints"[^>]*>.*?</h3>\s*'  # h3 heading
        r'<p>The PAYE Modernisation web service endpoints are detailed below\.</p>\s*)'  # intro paragraph
        r'((?:<table[\s\S]*?</table>\s*)+)'  # one or more broken tables
        r'(<p>\*Agent Tain)',  # footnote paragraph (anchor for end)
        re.DOTALL
    )

    def replace_section_21(m):
        changes.append("Replaced broken section 2.1 REST Endpoints tables with clean table")
        return m.group(1) + CLEAN_TABLE + "\n" + m.group(3)

    html, count = re.subn(pattern_section_21, replace_section_21, html)
    if count == 0:
        changes.append("WARNING: section 2.1 table pattern not found - manual review required")

    # ------------------------------------------------------------------
    # Fix 2: Remove the misplaced ERN / Monthly ERR table that the
    # pipeline places after section 2.1.1 content.
    # These rows are now included in the clean table above.
    # ------------------------------------------------------------------
    pattern_ern_table = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>\* Look Up ERN web service</th>'
        r'[\s\S]*?</table>',
        re.DOTALL
    )

    html, count2 = re.subn(pattern_ern_table, '', html)
    if count2 > 0:
        changes.append(f"Removed {count2} misplaced ERN/Monthly ERR table(s) after section 2.1.1")
    else:
        changes.append("NOTE: no misplaced ERN table found after 2.1.1 (may already be clean)")

    # ------------------------------------------------------------------
    # Fix 3: Remove the orphaned "1.0 Release Candidate 2" table that
    # splits out of the version history table.
    # ------------------------------------------------------------------
    pattern_rc2_table = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>1\.0 Release</th>\s*</tr>\s*</thead>\s*'
        r'<tbody>\s*<tr>\s*<td>Candidate 2</td>\s*</tr>\s*</tbody>\s*</table>',
        re.DOTALL
    )
    html, count_rc2 = re.subn(pattern_rc2_table, '', html)
    if count_rc2 > 0:
        changes.append("Removed orphaned '1.0 Release Candidate 2' table")
    else:
        changes.append("NOTE: orphaned RC2 table not found (may already be clean)")

    # ------------------------------------------------------------------
    # Fix 4: Remove the version history continuation table that spills
    # into the Document context section (ERR Milestone rows).
    # Detected by the presence of a table between the Document context
    # heading/paragraph and section 1.
    # ------------------------------------------------------------------
    pattern_version_continuation = re.compile(
        r'(<h3[^>]*id="document_context"[^>]*>.*?</h3>\s*<p>.*?</p>\s*)'
        r'(<table[^>]*>[\s\S]*?</table>\s*)',
        re.DOTALL
    )

    def remove_version_continuation(m):
        changes.append("Removed version history continuation table from Document context section")
        return m.group(1)

    html, count_vc = re.subn(pattern_version_continuation, remove_version_continuation, html)
    if count_vc == 0:
        changes.append("NOTE: version history continuation table not found (may already be clean)")

    # ------------------------------------------------------------------
    # Fix 5: Replace the HTTP request example table in section 2.1.1
    # ------------------------------------------------------------------
    # with a proper <pre><code> block.
    # The pipeline incorrectly treats this code example as a table.
    # ------------------------------------------------------------------
    pattern_http_example = re.compile(
        r'<table[^>]*>\s*<thead>\s*<tr>\s*'
        r'<th[^>]*>POST v1/rest/rpn/[^<]+</th>'
        r'[\s\S]*?</table>',
        re.DOTALL
    )

    HTTP_EXAMPLE = """<pre tabindex="0"><code>POST v1/rest/rpn/0000001W/2019/1/1?agentTain=11221w&amp;softwareUsed=SoftwareXYZ&amp;softwareVersion=1.0 HTTP/1.1
Host: www.ros.ie
Date: Wed Oct 04 16:35:51 BST 2017
Content-Type: application/x-www-form-urlencoded
X-HTTP-Method-Override: GET
Digest: 1fNNQYeUZW2laoZkOF4ssnkkzFJ83MRsz4H+fIpLrIvkBH0Zdy2G85OQSYGoHRqvyL6jVn8xJW0pW91/AYV6FEpw==
Signature: keyId="MIIEmTCCA4GgAwIBAgIRAOzckV67HlvuS0..." //truncated

// Request Body
employeeIDs={employmentID-1}&amp;employeeIDs={employmentID-2}&amp;employeeIDs={employmentID-3}</code></pre>"""

    html, count3 = re.subn(pattern_http_example, HTTP_EXAMPLE, html)
    if count3 > 0:
        changes.append(f"Replaced HTTP request example table with code block")
    else:
        changes.append("NOTE: HTTP request example table not found (may already be clean)")

    # ------------------------------------------------------------------
    # Fix 6: Replace the broken section 4.1.3 allowable headers table
    # ------------------------------------------------------------------
    # Capture: Allowable values paragraph + footnote paragraph + broken table
    # Output:  Allowable values paragraph + clean table + footnote paragraph
    pattern_413_table = re.compile(
        r'(<p>Allowable values in the headers field are outlined in the table below\.</p>\s*)'
        r'(<p>[\s\S]*?See sample below\.</p>\s*)'
        r'<table[^>]*>[\s\S]*?</table>',
        re.DOTALL
    )

    HEADERS_TABLE = """\\g<1>
<table class="table" tabindex="0">
<thead>
<tr>
<th scope="col">Value</th>
<th scope="col">Mandatory</th>
</tr>
</thead>
<tbody>
<tr>
<td>* (request-target)</td>
<td>Yes</td>
</tr>
<tr>
<td>host</td>
<td>Yes</td>
</tr>
<tr>
<td>date</td>
<td>Yes</td>
</tr>
<tr>
<td>** x-date</td>
<td>Yes, if date header cannot be added</td>
</tr>
<tr>
<td>*** digest</td>
<td>Yes, if HTTP method is POST</td>
</tr>
<tr>
<td>**** content-type</td>
<td>No</td>
</tr>
<tr>
<td>content-length</td>
<td>No</td>
</tr>
<tr>
<td>x-http-method-override</td>
<td>If HTTP method is POST, HTTP header 'X-HTTP-Method-Override' exists and 'Content-Type=application/x-www-form-urlencoded'. See Section 2.1.1 for more detail.</td>
</tr>
</tbody>
</table>
<p>* The &#39;(request-target)&#39; header field is a special header field in that its value is comprised of 2 HTTP headers. It is generated by concatenating the lowercase HTTP method, an ASCII space, and the request path headers. See below for sample:</p>
<pre tabindex="0"><code>(request-target): post /paye-employers/v1/rest/rpn/{employerRegistrationNumber}/{taxYear}?softwareUsed=XYZ&amp;softwareVersion=1.0</code></pre>
<p>** The &#39;x-date&#39; headers field value should ONLY be used in conjunction with the X-Date HTTP header if a Date HTTP header cannot be added to the HTTP request programmatically. The Date header has a limitation when using javascript in a browser to build and send a HTTP signature. The limitation is that you cannot add a &#39;Date&#39; HTTP header when executing javascript in a browser. The native xmlhttprequest object prohibits addition of a &#39;Date&#39; HTTP header. Building the signature string that will be signed with an &#39;x-date&#39; header instead of a &#39;date&#39; header removes this restriction.</p>
<p>*** The &#39;Digest&#39; HTTP header is created using the POST body/payload. The payload should be converted to a byte array, hashed using the SHA-512 algorithm and finally base64 encoded before adding it as a HTTP header.</p>
<p>**** Although Content-Type does not have to be part of the Signature string, it is required as a HTTP Header if HTTP Method Type is POST. If the request is a standard POST (i.e. not a header &#39;X-HTTP-Method-Override&#39; POST), then the Content-Type should be set to &#39;application/json&#39; or &#39;application/json;charset=UTF-8&#39;.</p>
<p>All other header field values are created by concatenating the lowercase header field name followed by an ASCII colon <code>:</code>, an ASCII space <code> </code>, and the header field value. Leading and trailing whitespace in the header field value MUST be omitted. If the header field is not the last value defined in the <code>headers</code> signature field, then append an ASCII newline <code>\n</code>. See sample below.</p>"""

    html, count6 = re.subn(pattern_413_table, HEADERS_TABLE, html)
    if count6 > 0:
        changes.append("Replaced broken section 4.1.3 headers table with clean table")
    else:
        changes.append("NOTE: section 4.1.3 headers table not found (may already be clean)")

    return html, changes


def main():
    parser = argparse.ArgumentParser(description="Fix section 2.1 REST Endpoints table")
    parser.add_argument("--pit", required=True, choices=["PIT3", "PIT4"],
                        help="PIT environment to fix")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(
        project_root, "content", args.pit, "rest",
        "rest_web_service_integration_guide.html"
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
