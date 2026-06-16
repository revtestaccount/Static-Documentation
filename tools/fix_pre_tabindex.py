"""
fix_pre_tabindex.py
===================
Ensures all <pre> elements have tabindex="0" for WCAG 2.1 keyboard
accessibility (SC 2.1.3 — scrollable content must be keyboard accessible).

Patches any <pre> tag that is missing tabindex="0" in place.
Safe to run multiple times — idempotent.

Usage:
    python fix_pre_tabindex.py <html_file> [<html_file> ...]

Example:
    python fix_pre_tabindex.py ../content/PIT3/rest/rest_web_service_integration_guide.html
"""

import re
import sys
import os


def fix_file(path: str) -> int:
    """Add tabindex="0" to all <pre> tags missing it. Returns count of fixes."""
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    fixed = re.sub(r'<pre(?!\s[^>]*tabindex)(?=[>\s])', '<pre tabindex="0"', html)
    count = html.count("<pre") - sum(1 for _ in re.finditer(r'<pre\s[^>]*tabindex', html))

    with open(path, "w", encoding="utf-8") as f:
        f.write(fixed)

    return count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_pre_tabindex.py <html_file> [<html_file> ...]")
        sys.exit(1)

    for path in sys.argv[1:]:
        if not os.path.isfile(path):
            print(f"ERROR: not found: {path}")
            continue
        count = fix_file(path)
        print(f"OK - {path}: {count} <pre> tag(s) patched")
