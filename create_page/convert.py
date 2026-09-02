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
        link["href"] = "javascript:void(0)"
        link["onclick"] = "document.getElementById('" + str(tag.get("id")) + "').scrollIntoView()"
        link.string = tag.get_text(separator=" ", strip=True)
        item.append(link)
        new_html.find(id="toc").append(item)

# -- Rewrite image paths if --content-path supplied ------------------------------
# Relative paths like ./rest_web_service.../images/image_1.png must be prefixed
# with the content subfolder path so they resolve correctly from the project root.
if args.content_path:
    prefix = args.content_path.rstrip("/") + "/"
    for img in new_html.find_all("img"):
        src = img.get("src", "")
        if src and not src.startswith(("http", "/", "content/")):
            img["src"] = prefix + src.lstrip("./")

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

with open(output_path, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(str(new_html))

print(f"Done. HTML written to '{output_path}'")
