import subprocess, os
os.chdir("O:/git/Static-Documentation")
msg = """Migrate PIT Self Service Application Guide (PIT3 + PIT4)

Content:
- Run pipeline on PITSelfServiceGuide.pdf for PIT3 and PIT4
- Copy all screen PDFs, CSVs, ZIPs, JSONs from source project
- Fix all broken links in self-service.html (PIT3 + PIT4)
- Update sitemap.json routes to point to new HTML pages
- Fix duplicate h2 headings and broken version history table
- Fix section 4.1 Edit Employee content (was broken into table)
- Fix section 9 appendix - clean REST/SOAP endpoints with links
- Remove empty TABLE OF CONTENTS heading (PIT4)
- Apply PIT4 hostname substitution (softwaretestnextversion.ros.ie)

CSS:
- Override Bootstrap --bs-table-bg and --bs-table-color on thead tr
  so Revenue Green header colour is not overridden by Bootstrap
- Recompile styles.css

package.json:
- Fix build:scss and watch:scss to use explicit Node path

Tools:
- Add tools/fix_selfservice_appendix.py
- Add tools/fix_selfservice_coverpage.py"""

subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", msg], check=True)
subprocess.run(["git", "push", "origin", "dev_contentMigration"], check=True)
print("Done")
