"""
fix_mojibake.py
Fixes UTF-8 mojibake in authored HTML files caused by double-encoding
of Windows-1252 smart quotes and dashes as Latin-1.

Mojibake occurs when a Windows-1252 encoded byte sequence was read as
Latin-1 and then stored as UTF-8, producing sequences like:
    â€™  instead of  '  (U+2019 RIGHT SINGLE QUOTATION MARK)
    â€œ  instead of  "  (U+201C LEFT DOUBLE QUOTATION MARK)
    â€  instead of  "  (U+201D RIGHT DOUBLE QUOTATION MARK)
    â€"  instead of  –  (U+2013 EN DASH)
    â€"  instead of  —  (U+2014 EM DASH)

The fix: re-encode from latin-1 back to bytes, then decode as cp1252.

Run from the project root:
    python tools/fix_mojibake.py
"""

import os
import glob

# Files to fix — only authored HTML, never topic*.html (those are legitimately UTF-8)
TARGET_FILES = [
    "index.html",
    "content/shared/home.html",
    "content/shared/pit-guides.html",
    "content/pit/payepithelpdeskuserguide.html",
    "content/pit/pitselfserviceguide.html",
]

def fix_mojibake(text: str) -> str:
    """
    Detect and fix mojibake by re-encoding latin-1 -> bytes -> cp1252 -> str.
    Only modifies text that contains the characteristic mojibake patterns.
    """
    # Quick check: if none of the marker bytes are present, skip
    if 'â€' not in text and '\x92' not in text and '\x93' not in text:
        return text

    try:
        # Re-encode the string as latin-1 bytes (reverses the bad UTF-8 read),
        # then decode those bytes as cp1252 (Windows-1252) to get the true characters
        fixed = text.encode('latin-1', errors='replace').decode('cp1252', errors='replace')
        return fixed
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def process_file(filepath: str) -> bool:
    """Read, fix, and write a single file. Returns True if file was changed."""
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        original = f.read()

    fixed = fix_mojibake(original)

    if fixed == original:
        print(f"  OK (no changes): {filepath}")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)

    print(f"  FIXED: {filepath}")
    return True


def main():
    # Run from project root
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    print(f"Working directory: {root}\n")

    changed = 0
    for rel_path in TARGET_FILES:
        if process_file(rel_path):
            changed += 1

    print(f"\nDone. {changed}/{len(TARGET_FILES)} files updated.")


if __name__ == "__main__":
    main()
