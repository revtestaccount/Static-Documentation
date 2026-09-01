import markdown
import argparse
import os
import sys
from bs4 import BeautifulSoup

# *** Run Command ***
# python convert.py <input.md> [--output <output.html>] [--content-path <prefix>]
#
# Examples:
#   python convert.py payepithelpdeskuserguide.md
#   python convert.py ../content/PIT3/rest/rest_web_service_integration_guide.md \
#       --output ../content/PIT3/rest/rest_web_service_integration_guide.html \
#       --content-path content/PIT3/rest/
#
# NOTE: h1 is the document title only. pdfToMarkdown.py emits # (h1) for the largest
# font on page 1. convert.py trusts this and never promotes or demotes headings.
# --content-path is required when the page is loaded via the router into index.html,
# since relative image paths must resolve from the project root, not the content folder.

parser = argparse.ArgumentParser(
    description="Convert a Markdown file to a site-ready HTML fragment with auto-generated TOC."
)
parser.add_argument("input", help="Path to the input .md file")
parser.add_argument(
    "--output", "-o",
    help="Path for the output .html file (default: same location and name as input)",
    default=None
)
parser.add_argument(
    "--content-path", "-p",
    help="Path prefix to prepend to relative image src attributes "
         "(e.g. content/PIT3/rest/). Required when the HTML will be loaded "
         "into index.html via the router.",
    default=None,
    dest="content_path"
)
parser.add_argument(
    "--stylesheet", "-s",
    help="Relative path to the stylesheet to inject into <head> "
         "(e.g. ../../../assets/css/styles.css). Calculated from output file depth.",
    default=None,
    dest="stylesheet"
)
args = parser.parse_args()

input_path = args.input
if not os.path.isfile(input_path):
    print(f"Error: file not found: {input_path}")
    sys.exit(1)

if args.output:
    output_path = args.output
else:
    output_path = os.path.splitext(input_path)[0] + ".html"

print(f"Input:  {input_path}")
print(f"Output: {output_path}")

with open(input_path, "r", encoding="utf-8") as input_file:
    text = input_file.read()
html = markdown.markdown(text, extensions=["fenced_code", "tables"])

new_html = BeautifulSoup(html, "lxml")

# -- Apply classes and IDs -------------------------------------------------------
for tag in new_html.find_all("h1"):
    tag["class"] = "document-title"
    tag["id"] = "title"

def make_id(tag):
    return tag.get_text(separator=" ", strip=True).replace(" ", "_").lower()[:80]

for tag in new_html.find_all("h2"):
    tag["class"] = "pmod"
    tag["id"] = make_id(tag)

for tag in new_html.find_all("h3"):
    tag["class"] = "pmod"
    tag["id"] = make_id(tag)

for tag in new_html.find_all("h4"):
    tag["class"] = "pmod"
    tag["id"] = make_id(tag)

for tag in new_html.find_all("table"):
    tag["class"] = "table"
    tag["tabindex"] = "0"

# -- Add scope="col" to all <th> elements inside <thead> rows -----------------
for tag in new_html.find_all("thead"):
    for th in tag.find_all("th"):
        if not th.get("scope"):
            th["scope"] = "col"

# -- Generate Table of Contents (h2, h3, h4 only - h1 title never included) -----
title_tag = new_html.find(id="title")
if title_tag:
    toc_heading = new_html.new_tag("h2")
    toc_heading.string = "Table of Contents"
    toc_heading["class"] = "pmod"
    toc_heading["id"] = "table_of_contents"
    title_tag.insert_after(toc_heading)

    toc = new_html.new_tag("ul")
    toc["id"] = "toc"
    toc_heading.insert_after(toc)

    for tag in new_html.find_all(["h2", "h3", "h4"]):
        if tag.get("id") == "table_of_contents":
            continue
        item = new_html.new_tag("li")
        if tag.name == "h3":
            item["style"] = "margin-left: 1.5rem;"
        elif tag.name == "h4":
            item["style"] = "margin-left: 3rem;"
        link = new_html.new_tag("a")
        link["href"] = "#" + str(tag.get("id"))
        link.string = tag.get_text(separator=" ", strip=True)
        item.append(link)
        toc.append(item)

# -- Rewrite image paths if --content-path supplied ------------------------------
# Relative paths like ./rest_web_service.../images/image_1.png must be prefixed
# with the content subfolder path so they resolve correctly from the project root.
if args.content_path:
    prefix = args.content_path.rstrip("/") + "/"
    for img in new_html.find_all("img"):
        src = img.get("src", "")
        if src and not src.startswith(("http", "/", "content/")):
            img["src"] = prefix + src.lstrip("./")

# -- Convert any surviving bullet paragraphs (• text) to proper <ul><li> lists --
# Safety net: pdfToMarkdown.py converts • to markdown `- ` list items, but if any
# slip through as <p> tags they are caught here and converted to proper HTML lists.
# Strategy: find all bullet <p> tags, group consecutive ones, replace each group
# with a single <ul>. Done in two passes to avoid mutating the list while iterating.
body = new_html.find("body")
if body:
    # Pass 1: tag all bullet <p> elements
    bullet_paras = [
        p for p in body.find_all("p", recursive=False)
        if p.get_text().strip().startswith('\u2022')
    ]
    # Pass 2: group consecutive bullet <p> elements and replace with <ul>
    while bullet_paras:
        p = bullet_paras.pop(0)
        # Build the <ul> from this and any immediately following bullet <p> siblings
        ul = new_html.new_tag('ul')
        li = new_html.new_tag('li')
        li.string = p.get_text().strip().lstrip('\u2022').strip()
        ul.append(li)
        nxt = p.find_next_sibling()
        while nxt and nxt.name == 'p' and nxt.get_text().strip().startswith('\u2022'):
            li = new_html.new_tag('li')
            li.string = nxt.get_text().strip().lstrip('\u2022').strip()
            ul.append(li)
            to_remove = nxt
            nxt = nxt.find_next_sibling()
            to_remove.decompose()
            if to_remove in bullet_paras:
                bullet_paras.remove(to_remove)
        p.replace_with(ul)

# -- Apply .figure-caption class to Figure N caption paragraphs ----------------
# Captions are plain <p> elements starting with 'Figure N' — apply the class
# so they render centred italic beneath their associated image.
if body:
    import re as _re
    _fig_re = _re.compile(r'^Figure\s+\d+', _re.IGNORECASE)
    for p in body.find_all('p'):
        text = p.get_text(strip=True)
        if _fig_re.match(text):
            p['class'] = 'figure-caption'

# -- Reformat cover-page 'Version X Version Date Y' run-on paragraphs -----------
# Source PDFs commonly present Version/Version Date as two side-by-side cover-page
# fields, but the PDF extraction joins them into a single run-on <p> like:
#   'Version 1.0 Version Date 12/06/2020'
# Replace any such paragraph with a two-column label/value <div> layout matching
# the source PDF's presentation, instead of leaving it as an unreadable run-on
# sentence. Handles the common case where the value is a bare version number/date
# on either side (e.g. also 'Version 1.0 Release Candidate 2 Version Date 24/05/2018').
if body:
    import re as _re

    def _build_version_div(version_value, date_value):
        wrapper_div = new_html.new_tag('div')
        wrapper_div['style'] = 'display:flex; justify-content:space-between; margin:0.5rem 0;'
        version_span = new_html.new_tag('span')
        version_strong = new_html.new_tag('strong')
        version_strong.string = 'Version'
        version_span.append(version_strong)
        version_span.append(' ' + version_value)
        date_span = new_html.new_tag('span')
        date_strong = new_html.new_tag('strong')
        date_strong.string = 'Version Date'
        date_span.append(date_strong)
        date_span.append(' ' + date_value)
        wrapper_div.append(version_span)
        wrapper_div.append(date_span)
        return wrapper_div

        # Case 1: 'Version X Version Date Y' all in one run-on <p> - requires a
    # non-empty date value, otherwise this is really Case 2 (split across two
    # <p> tags) and must fall through to that branch instead.
    _ver_re = _re.compile(r'^Version\s+(.+?)\s+Version Date\s+(\S.*)$', _re.IGNORECASE)
    # Case 2: split across two consecutive <p> tags - first ends with
    # 'Version Date' (no value, or trailing whitespace only), second <p>
    # (or plain sibling text) is just the date value.
    _ver_split_re = _re.compile(r'^Version\s+(.+?)\s+Version Date\s*$', _re.IGNORECASE)

    for p in body.find_all('p'):
        if p.decomposed:
            continue
        text = p.get_text(separator=' ', strip=True)
        m = _ver_re.match(text)
        if m:
            p.replace_with(_build_version_div(m.group(1).strip(), m.group(2).strip()))
            continue
        m_split = _ver_split_re.match(text)
        if m_split:
            nxt = p.find_next_sibling()
            if nxt and nxt.name == 'p':
                date_value = nxt.get_text(strip=True)
                nxt.decompose()
                p.replace_with(_build_version_div(m_split.group(1).strip(), date_value))

# -- Add tabindex="0" to all <pre> blocks so keyboard users can scroll them -----
for tag in new_html.find_all("pre"):
    tag["tabindex"] = "0"

# -- Wrap all body content in a constrained .document-content div ---------------
body = new_html.find("body")
if body:
    wrapper = new_html.new_tag("div")
    wrapper["class"] = "document-content"
    for child in list(body.children):
        wrapper.append(child.extract())
    body.append(wrapper)

# -- Write output ----------------------------------------------------------------
os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

# lxml strips <head> from the BeautifulSoup tree, so we write the full <html>
# opening as a raw string rather than relying on BS4 DOM manipulation.
# We always inject lang="en", <meta charset>, and <title>.
doc_title = ""
title_tag = new_html.find(id="title")
if title_tag:
    doc_title = title_tag.get_text(strip=True)

html_out = str(new_html)
stylesheet_link = ""
if args.stylesheet:
    stylesheet_link = f'\n    <link rel="stylesheet" href="{args.stylesheet}" />'

head_block = (
    f'<head>\n'
    f'    <meta charset="UTF-8" />{stylesheet_link}\n'
    f'    <title>{doc_title}</title>\n'
    f'</head>\n'
)
html_out = html_out.replace("<html>", f'<html lang="en">\n{head_block}', 1)

with open(output_path, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(html_out)

print(f"Done. HTML written to '{output_path}'")

# -- Environment hostname validation ------------------------------------------
# PIT3 documents must use softwaretest.ros.ie
# PIT4 documents must use softwaretestnextversion.ros.ie
# Flag any mismatch so it can be corrected before publishing.
PIT3_HOST = "softwaretest.ros.ie"
PIT4_HOST = "softwaretestnextversion.ros.ie"

output_norm = output_path.replace("\\", "/").lower()

correct_host = ""
wrong_host   = ""

if "/pit3/" in output_norm or "/pit3" in output_norm:
    env = "PIT3"
    correct_host = PIT3_HOST
    wrong_host   = PIT4_HOST
elif "/pit4/" in output_norm or "/pit4" in output_norm:
    env = "PIT4"
    correct_host = PIT4_HOST
    wrong_host   = PIT3_HOST
else:
    env = None

if env:
    with open(output_path, "r", encoding="utf-8") as f:
        html_text = f.read()
    warnings = []
    if wrong_host in html_text:
        count = html_text.count(wrong_host)
        warnings.append(
            f"  [HOSTNAME WARNING] {env} document contains '{wrong_host}' ({count} occurrence{'s' if count > 1 else ''})."
            f"\n  Expected '{correct_host}'. Please review and correct before publishing."
        )
    if warnings:
        print("\n" + "\n".join(warnings))
    else:
        print(f"[hostname check] OK — no wrong-environment hostnames found for {env}.")
