"""
fix_links.py
Scans all content HTML files for broken download hrefs (zip, json, xlsx, pdf, etc.)
and rewrites them to the correct content/ path where the file now exists.
"""
import os
import re
from pathlib import Path

repo       = Path(__file__).resolve().parent.parent
content_dir = repo / "content"

# Build a filename -> list-of-content-relative-paths index
index = {}
for f in content_dir.rglob("*"):
    if f.is_file():
        key = f.name.lower()
        index.setdefault(key, [])
        index[key].append("content/" + f.relative_to(content_dir).as_posix())

html_files = [
    f for f in content_dir.rglob("*.html")
    if f.name != "demodocument.html"
]

pattern = re.compile(
    r'href="([^"#][^"]*\.(zip|json|xlsx|pdf|wsdl|xsd|csv|pptx))"',
    re.IGNORECASE,
)

total_fixed  = 0
files_changed = 0

for html_file in sorted(html_files):
    text     = html_file.read_text(encoding="utf-8")
    original = text

    def replacer(m):
        global total_fixed
        href = m.group(1)
        if href.startswith("http"):
            return m.group(0)
        resolved = (repo / href).resolve()
        if resolved.exists():
            return m.group(0)               # already correct
        fname = Path(href).name
        candidates = index.get(fname.lower(), [])
        if not candidates:
            return m.group(0)               # file not migrated yet — leave alone
        fixed = candidates[0]
        total_fixed += 1
        return f'href="{fixed}"'

    text = pattern.sub(replacer, text)

    if text != original:
        html_file.write_text(text, encoding="utf-8")
        files_changed += 1
        print(f"  Updated: {html_file.relative_to(repo)}")

print(f"\nFiles changed : {files_changed}")
print(f"Hrefs fixed   : {total_fixed}")
