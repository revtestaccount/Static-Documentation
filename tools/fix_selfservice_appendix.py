"""
fix_selfservice_appendix.py
===========================
Replaces the broken appendix section (section 9) in pitselfserviceguide.html
for PIT3 and PIT4. The pipeline extracted spaced-out URL characters from the
PDF (e.g. 'softwa r e t est.ros.ie/paye- employers/v1/r e s t /rpn/...')
which need to be replaced with clean clickable links matching the PDF layout.

Usage:
    python fix_selfservice_appendix.py --pit PIT3
    python fix_selfservice_appendix.py --pit PIT4
"""

import argparse
import os
import re

# ---------------------------------------------------------------------------
# Clean hand-authored appendix section
# Placeholder {HOST} is replaced with the correct hostname per environment
# ---------------------------------------------------------------------------
CLEAN_APPENDIX = """\
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
<p>Example: <a href="https://{HOST}/paye-employers/v1/rest/rpn/03390656OH/2018/01092485G-2?softwareUsed=1&amp;softwareVersion=1.0" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/rpn/03390656OH/2018/01092485G-2?softwareUsed=1&amp;softwareVersion=1.0</a></p>
<p><strong>9.1.1.4 GET &ndash; Look Up RPN by employer using optional filters date last updated and/or employee Ids</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/rpn/{{employerRegistrationNumber}}/{{taxYear}}?softwareUsed={{SoftwareName}}&amp;softwareVersion={{softwareVersion}}&amp;employeeIDs={{employeeId1}},{{employeeId2}}&amp;dateLastUpdated={{date}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/rpn/{{employerRegistrationNumber}}/{{taxYear}}?softwareUsed={{SoftwareName}}&amp;softwareVersion={{softwareVersion}}&amp;employeeIDs={{employeeId1}},{{employeeId2}}&amp;dateLastUpdated={{date}}</a></p>
<p>Example: <a href="https://{HOST}/paye-employers/v1/rest/rpn/03390656OH/2018?softwareUsed=1&amp;softwareVersion=1&amp;employeeIDs=00202020PA-1,7002439CA-2&amp;dateLastUpdated=2018-02-01" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/rpn/03390656OH/2018?softwareUsed=1&amp;softwareVersion=1&amp;employeeIDs=00202020PA-1,7002439CA-2&amp;dateLastUpdated=2018-02-01</a></p>
<h4 id="9.1.2_payroll_services">9.1.2 Payroll Services</h4>
<p><strong>9.1.2.1 POST &ndash; Payroll Submission</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistrationNumber}}/{{taxYear}}/{{payrollRunReference}}/{{SubmissionID}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistrationNumber}}/{{taxYear}}/{{payrollRunReference}}/{{SubmissionID}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<p>Example: <a href="https://{HOST}/paye-employers/v1/rest/payroll/00087900D/2018/PayrollRun1/Submission01?softwareUsed=abc&amp;softwareVersion=1.0" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/00087900D/2018/PayrollRun1/Submission01?softwareUsed=abc&amp;softwareVersion=1.0</a></p>
<p><strong>9.1.2.2 GET &ndash; Check Payroll Submission</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistrationNumber}}/{{taxYear}}/{{PayrollRunReference}}/{{SubmissionID}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistrationNumber}}/{{taxYear}}/{{PayrollRunReference}}/{{SubmissionID}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<p>Example: <a href="https://{HOST}/paye-employers/v1/rest/payroll/00087900D/2018/PayrollRun1/Submission01?softwareUsed=abc&amp;softwareVersion=1.0" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/00087900D/2018/PayrollRun1/Submission01?softwareUsed=abc&amp;softwareVersion=1.0</a></p>
<p><strong>9.1.2.3 GET &ndash; Check Payroll Run</strong><br>
<a href="https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistration}}/{{taxYear}}/{{PayrollRunReference}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/{{employerRegistration}}/{{taxYear}}/{{PayrollRunReference}}?softwareUsed={{softwareName}}&amp;softwareVersion={{softwareVersion}}</a></p>
<p>Example: <a href="https://{HOST}/paye-employers/v1/rest/payroll/00087900D/2018/PayrollRun1?softwareUsed=abc&amp;softwareVersion=1.0" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/payroll/00087900D/2018/PayrollRun1?softwareUsed=abc&amp;softwareVersion=1.0</a></p>
<h4 id="9.1.3_returns_reconciliations">9.1.3 Returns Reconciliations</h4>
<p><a href="https://{HOST}/paye-employers/v1/rest/returns_reconciliation/{{employerRegistration}}?softwareUsed={{softwareName}}&amp;periodStartDate={{periodStartDate}}&amp;periodEndDate={{periodEndDate}}&amp;softwareVersion={{softwareVersion}}" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/returns_reconciliation/{{employerRegistration}}?softwareUsed={{softwareName}}&amp;periodStartDate={{periodStartDate}}&amp;periodEndDate={{periodEndDate}}&amp;softwareVersion={{softwareVersion}}</a></p>
<p>Example: <a href="https://{HOST}/paye-employers/v1/rest/returns_reconciliation/03497992DH?softwareUsed=abc&amp;periodStartDate=2019-04-01&amp;periodEndDate=2019-04-30&amp;softwareVersion=1" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/rest/returns_reconciliation/03497992DH?softwareUsed=abc&amp;periodStartDate=2019-04-01&amp;periodEndDate=2019-04-30&amp;softwareVersion=1</a></p>
<h3 class="pmod" id="9.2_soap_api_endpoints">9.2 SOAP API Endpoints</h3>
<h4 id="9.2.1_rpn_services">9.2.1 RPN Services</h4>
<p><a href="https://{HOST}/paye-employers/v1/soap/rpn" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/soap/rpn</a></p>
<h4 id="9.2.2_payroll_service">9.2.2 Payroll Service</h4>
<p><a href="https://{HOST}/paye-employers/v1/soap/payroll" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/soap/payroll</a></p>
<h4 id="9.2.3_returns_reconciliations">9.2.3 Returns Reconciliations</h4>
<p><a href="https://{HOST}/paye-employers/v1/soap/returns_reconciliation" target="_blank" rel="noopener noreferrer">https://{HOST}/paye-employers/v1/soap/returns_reconciliation</a></p>
<h3 class="pmod" id="9.3_known_issues">9.3 Known Issues</h3>
<h4 id="9.3.1_self_service_application_login">9.3.1 Self Service Application Login</h4>
<p>On clicking the &#39;register for ROS&#39; link on the Self Service Application login page in PIT3 a &#39;503 service unavailable&#39; page is displayed to the user.</p>
</div></body></html>"""

HOSTS = {
    "PIT3": "softwaretest.ros.ie",
    "PIT4": "softwaretestnextversion.ros.ie",
}


def fix_html(html: str, host: str) -> tuple[str, list[str]]:
    changes = []

    # Replace everything from the section 9 heading to end of file
    pattern = re.compile(
        r'<h3[^>]*id="9_appendix"[^>]*>[\s\S]*$',
        re.DOTALL
    )

    replacement = CLEAN_APPENDIX.replace("{HOST}", host)

    html, count = re.subn(pattern, replacement, html)
    if count > 0:
        changes.append(f"Replaced broken appendix section with clean hand-authored HTML (host: {host})")
    else:
        changes.append("WARNING: appendix section pattern not found - manual review required")

    return html, changes


def main():
    parser = argparse.ArgumentParser(description="Fix appendix section in pitselfserviceguide.html")
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

    host = HOSTS[args.pit]
    fixed_html, changes = fix_html(html, host)

    for change in changes:
        print(f"  {change}")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(fixed_html)

    print(f"OK - written to {html_path}")


if __name__ == "__main__":
    main()
