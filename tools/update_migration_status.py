"""
update_migration_status.py
Compares meaningful source assets in O:/git/paye-employers-documentation
against what has been migrated to content/ in this repo, and rewrites
MIGRATION_STATUS.md with the current state.

Usage (from repo root):
    python tools/update_migration_status.py

Requirements: Python 3.8+, no external dependencies.
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

REPO_ROOT   = Path(__file__).resolve().parent.parent
SOURCE_ROOT = Path(r"O:\git\paye-employers-documentation")
CONTENT_DIR = REPO_ROOT / "content"
OUTPUT_FILE = REPO_ROOT / "MIGRATION_STATUS.md"

# Extensions that represent real content assets worth tracking individually
TRACKED_EXTENSIONS = {
    ".html", ".json", ".wsdl", ".xsd",
    ".pdf", ".xlsx", ".zip", ".pptx", ".csv",
}

# Directories whose contents are migrated as a complete bulk unit —
# not tracked file-by-file (avoids listing ~2000 topic*.html lines).
SKIP_DIRS = {
    "soap-schema-reference",
}

# Filename patterns to exclude from individual tracking
SKIP_FILENAME_PATTERNS = [
    re.compile(r"^topic\d+\.(html|png)$", re.IGNORECASE),
    re.compile(r"^mso[0-9A-F]+\.tmp$",    re.IGNORECASE),
]


# ── Helpers ────────────────────────────────────────────────────────────────────

def should_skip(rel_path: Path) -> bool:
    for part in rel_path.parts:
        if part in SKIP_DIRS:
            return True
    for pattern in SKIP_FILENAME_PATTERNS:
        if pattern.match(rel_path.name):
            return True
    return False


def collect_source_assets(version: str) -> list:
    """
    Walk SOURCE_ROOT/<version> with directory pruning so we never descend
    into the huge soap-schema-reference trees (~1000+ files each).
    """
    base = SOURCE_ROOT / version
    if not base.exists():
        return []
    assets = []

















    for dirpath, dirnames, filenames in os.walk(base):
        # Prune SKIP_DIRS in-place so os.walk never descends into them
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in sorted(filenames):
            ext = Path(filename).suffix.lower()
            if ext not in TRACKED_EXTENSIONS:
                continue
            full = Path(dirpath) / filename
            rel  = full.relative_to(SOURCE_ROOT)
            if should_skip(rel):
                continue
            parts    = rel.parts  # e.g. ('PIT3', 'guide', 'file.pdf')
            category = parts[1].replace("-", " ").replace("_", " ").title() if len(parts) >= 2 else "Root"
            assets.append({
                "source_rel": rel.as_posix(),
                "filename":   filename,
                "category":   category,
                "version":    version,
            })
    return sorted(assets, key=lambda a: a["source_rel"])


# Build a flat index of content/ files once, keyed by (name.lower(), ext.lower())
# so lookups are O(1) instead of repeated rglob calls.
_CONTENT_INDEX: dict = {}

def _build_content_index():
    global _CONTENT_INDEX
    if _CONTENT_INDEX:
        return
    for path in CONTENT_DIR.rglob("*"):
        if path.is_file():
            key = (path.name.lower(), path.suffix.lower())
            _CONTENT_INDEX.setdefault(key, [])
            _CONTENT_INDEX[key].append(path)


def find_in_content(source_rel: str):
    """Return (found: bool, migrated_path: str)."""
    _build_content_index()
    filename = Path(source_rel).name


    ext      = Path(source_rel).suffix.lower()
    matches  = _CONTENT_INDEX.get((filename.lower(), ext), [])
    if matches:
        return True, matches[0].relative_to(REPO_ROOT).as_posix()
    return False, ""





def check_bulk_unit(content_subdir: str):
    """
    Check a bulk-migrated directory by counting files in the REPO content/ side only.
    We don't re-scan the source (too slow); instead we just verify the target exists
    and has files.
    """
    tgt = CONTENT_DIR / content_subdir


    if not tgt.exists():
        return "❌", "directory not present in content/"
    tgt_count = sum(1 for f in tgt.rglob("*") if f.is_file())
    if tgt_count == 0:




        return "❌", "directory exists but contains no files"
    return "✅", f"{tgt_count} files present"


# ── Section builders ───────────────────────────────────────────────────────────

def build_summary(pit3: list, pit4: list) -> str:
    all_assets = pit3 + pit4
    total    = len(all_assets)
    migrated = sum(1 for a in all_assets if find_in_content(a["source_rel"])[0])
    pct      = round(migrated / total * 100) if total else 0
    bar      = "█" * (pct // 5) + "░" * (20 - pct // 5)
    return (
        "## Summary\n\n"
        f"**Progress:** {migrated} / {total} tracked assets migrated  \n"
        f"`{bar}` {pct}%\n"
    )


def build_pit_guides() -> str:
    pages = [
        ("payepithelpdeskuserguide.html", "PAYE PIT Help Desk User Guide"),
        ("pitselfserviceguide.html",      "PIT Self-Service Guide"),
    ]
    rows = []
    for filename, label in pages:
        exists = (CONTENT_DIR / "pit" / filename).exists()
        emoji  = "✅" if exists else "❌"
        path   = f"`content/pit/{filename}`" if exists else "—"
        rows.append(f"| {label} | {emoji} | {path} |")
    return (
        "## PIT Guides (HTML Pages)\n\n"
        "| Page | Status | Content Path |\n"
        "|------|--------|-------------- |\n"
        + "\n".join(rows) + "\n"
    )


def build_bulk_units() -> str:
    units = [






        ("PIT3 SOAP schema reference (topic*.html + images)", "PIT3/soap/soap-schema-reference"),
        ("PIT4 SOAP schema reference (topic*.html + images)", "PIT4/soap/soap-schema-reference"),
        ("PIT3 SOAP v1 schemas & WSDLs",                     "PIT3/soap/v1"),
        ("PIT4 SOAP v1 schemas & WSDLs",                     "PIT4/soap/v1"),
        ("PIT3 REST API reference",                           "PIT3/rest"),
        ("PIT4 REST API reference",                           "PIT4/rest"),
    ]
    rows = []


    for label, tgt in units:
        emoji, detail = check_bulk_unit(tgt)
        rows.append(f"| {label} | {emoji} | {detail} |")
    return (
        "## Bulk-Migrated Units\n\n"
        "> These directories are migrated as complete units, not tracked file-by-file.\n\n"
        "| Unit | Status | Detail |\n"
        "|------|--------|--------|\n"
        + "\n".join(rows) + "\n"
    )


def build_version_section(version: str, assets: list) -> str:
    # Group by category
    by_cat: dict = {}
    for a in assets:
        by_cat.setdefault(a["category"], []).append(a)

    lines = [f"## {version}\n"]
    for cat, items in sorted(by_cat.items()):
        lines.append(f"### {cat}\n")
        lines.append("| File | Status | Migrated Path |")
        lines.append("|------|--------|---------------|")
        for item in items:
            found, path = find_in_content(item["source_rel"])
            emoji  = "✅" if found else "❌"
            target = f"`{path}`" if found else "—"
            lines.append(f"| `{item['filename']}` | {emoji} | {target} |")
        lines.append("")
    return "\n".join(lines)


def build_not_yet_migrated(pit3: list, pit4: list) -> str:
    missing = [a for a in pit3 + pit4 if not find_in_content(a["source_rel"])[0]]
    if not missing:
        return "## Not Yet Migrated\n\n_All tracked assets have been migrated._ ✅\n"
    rows = [f"| {a['version']} | {a['category']} | `{a['filename']}` |" for a in missing]
    return (
        "## Not Yet Migrated\n\n"
        "| Version | Category | File |\n"
        "|---------|----------|------|\n"
        + "\n".join(rows) + "\n"
    )


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("Scanning source assets...")
    pit3 = collect_source_assets("PIT3")
    pit4 = collect_source_assets("PIT4")
    print(f"  PIT3: {len(pit3)} tracked files")
    print(f"  PIT4: {len(pit4)} tracked files")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    md = "\n".join([
        "# Migration Status\n",
        f"> Auto-generated by `tools/update_migration_status.py`  \n"
        f"> Last updated: **{now}**\n",
        "---\n",
        build_summary(pit3, pit4),
        "---\n",
        build_pit_guides(),
        build_bulk_units(),
        build_version_section("PIT3", pit3),
        build_version_section("PIT4", pit4),
        build_not_yet_migrated(pit3, pit4),
    ])

    OUTPUT_FILE.write_text(md, encoding="utf-8")
    print(f"\nWritten: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
