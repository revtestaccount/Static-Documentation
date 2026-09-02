"""
log_session.py
===============
Reusable tool to append a new dated entry to SESSION_LOG.md, and optionally
bump the "Last updated" date stamp in MIGRATION_STATUS.md / PROJECT_ASSESSMENT.md
at the same time.

Unlike tools/update_docs.py (a one-off hardcoded script tied to a single
session's specific before/after text edits), this script is meant to be run
at the end of *every* significant session/push — e.g. a new document
successfully migrated, a fix script corrected, a bug found and resolved.

Usage
-----
Edit tools/session_config.json with this session's details, then run:

    python tools/log_session.py
    python tools/log_session.py --bump-dates

The script itself never needs editing between sessions — only the JSON
config file does.

This will:
1. Prepend a new "## Session: YYYY-MM-DD" entry to SESSION_LOG.md, directly
   under the header/instructions block, above all previous entries
   (reverse-chronological order is preserved).
2. Optionally bump the "> **Last updated:** YYYY-MM-DD" line in
   MIGRATION_STATUS.md and PROJECT_ASSESSMENT.md to today's date, if
   --bump-dates is passed.
3. Reset tools/session_config.json back to an empty template afterwards
   (unless --no-reset is passed), so stale content from this session is
   never accidentally carried into the next run.

tools/session_config.json fields
---------------------------------
task            : one-line summary of what this session set out to do
findings        : list of strings — root causes / discoveries (optional)
fixed           : list of strings — what was fixed/completed, prefixed with
                  status where useful (e.g. "PIT3 ... — done")
outstanding     : list of strings — what remains open (optional)
files_touched   : list of strings — file paths touched this session
status          : closing one/two-line summary of session state

'date' is NOT read from the config file — it is always set to today's date
automatically when the script runs. Any list field can be empty — sections
with no content are omitted from the generated entry rather than rendered
empty.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(r"O:\git\Static-Documentation")
SESSION_LOG_PATH = ROOT / "SESSION_LOG.md"
SESSION_CONFIG_PATH = ROOT / "tools" / "session_config.json"

REQUIRED_FIELDS = ["task", "status"]
OPTIONAL_LIST_FIELDS = ["findings", "fixed", "outstanding", "files_touched"]


def load_session_config() -> dict:
    if not SESSION_CONFIG_PATH.exists():
        print(f"ERROR: config file not found: {SESSION_CONFIG_PATH}")
        print("Create it with at least 'task' and 'status' fields before running this script.")
        sys.exit(1)

    try:
        with open(SESSION_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: {SESSION_CONFIG_PATH} is not valid JSON: {e}")
        sys.exit(1)

    missing = [field for field in REQUIRED_FIELDS if not config.get(field)]
    if missing:
        print(f"ERROR: {SESSION_CONFIG_PATH} is missing required field(s): {', '.join(missing)}")
        sys.exit(1)

    session = {"date": date.today().isoformat()}
    session["task"] = config["task"]
    session["status"] = config["status"]
    for field in OPTIONAL_LIST_FIELDS:
        session[field] = config.get(field, [])

    return session


# ============================================================================
# Script logic — should not normally need editing
# ============================================================================


def build_entry(session: dict) -> str:
    lines = [f"## Session: {session['date']}", ""]

    lines.append(f"**Task:** {session['task']}")
    lines.append("")

    if session.get("findings"):
        lines.append("**Findings:**")
        for f in session["findings"]:
            lines.append(f"- {f}")
        lines.append("")

    if session.get("fixed"):
        lines.append("**Fixed:**")
        for f in session["fixed"]:
            lines.append(f"- ✅ {f}")
        lines.append("")

    if session.get("outstanding"):
        lines.append("**Outstanding / next steps:**")
        for o in session["outstanding"]:
            lines.append(f"- ⚪ {o}")
        lines.append("")

    if session.get("files_touched"):
        lines.append("**Files touched this session:**")
        for f in session["files_touched"]:
            lines.append(f"- `{f}`")
        lines.append("")

    lines.append(f"**Status: {session['status']}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def prepend_session_entry(session: dict) -> None:
    text = SESSION_LOG_PATH.read_text(encoding="utf-8")

    # Find the end of the header/instructions block — the first "---" divider —
    # and insert the new entry immediately after it, above all prior entries.
    marker = "---\n"
    idx = text.find(marker)
    if idx == -1:
        print(f"ERROR: could not find '---' divider in {SESSION_LOG_PATH}")
        sys.exit(1)

    insert_at = idx + len(marker)
    # Skip a single following blank line if present, to avoid a double gap
    rest = text[insert_at:]
    rest = rest.lstrip("\n")

    new_entry = "\n" + build_entry(session)
    new_text = text[:insert_at] + new_entry + "\n" + rest

    SESSION_LOG_PATH.write_text(new_text, encoding="utf-8")
    print(f"OK: SESSION_LOG.md updated with entry for {session['date']}")


SESSION_CONFIG_TEMPLATE = {
    "task": "",
    "findings": [],
    "fixed": [],
    "outstanding": [],
    "files_touched": [],
    "status": ""
}


def reset_session_config() -> None:
    with open(SESSION_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(SESSION_CONFIG_TEMPLATE, f, indent=2)
        f.write("\n")
    print(f"OK: {SESSION_CONFIG_PATH} reset to empty template")


def bump_last_updated_dates(today: str) -> None:
    for filename in ("MIGRATION_STATUS.md", "PROJECT_ASSESSMENT.md"):
        path = ROOT / filename
        if not path.exists():
            print(f"  SKIP: {filename} not found")
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = re.subn(
            r"> \*\*Last updated:\*\* \d{4}-\d{2}-\d{2}",
            f"> **Last updated:** {today}",
            text,
        )
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"  OK: {filename} — 'Last updated' bumped to {today}")
        else:
            print(f"  WARNING: {filename} — 'Last updated' line not found, not changed")


if __name__ == "__main__":
    session = load_session_config()
    prepend_session_entry(session)

    if "--bump-dates" in sys.argv:
        print("\nBumping 'Last updated' dates:")
        bump_last_updated_dates(session["date"])

    if "--no-reset" not in sys.argv:
        reset_session_config()

    print("\nDone.")
