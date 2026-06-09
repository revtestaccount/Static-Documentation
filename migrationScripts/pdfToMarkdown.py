import os
import sys
import re
import argparse
import fitz  # PyMuPDF
from extractImagesFromPdf import extract_images_from_pdf

# *** Run Command ***
# python pdfToMarkdown.py <pdf_path> [--output <dir>]
#
# Examples:
#   python pdfToMarkdown.py source.pdf
#   python pdfToMarkdown.py source.pdf --output content/PIT3/guide/


def get_heading_level(span_size, body_size):
    """
    Derive a Markdown heading level from font size relative to body text size.
    Returns an int (1-3) or None if the span is normal body text.
    """
    ratio = span_size / body_size
    if ratio >= 1.6:
        return 1
    elif ratio >= 1.3:
        return 2
    elif ratio >= 1.1:
        return 3
    return None


def extract_page_text(page):
    """
    Extract text from a page using font-size detection for headings.
    Uses get_text('dict') to access per-span font size metadata.
    Falls back to plain text if dict extraction fails.
    """
    try:
        blocks = page.get_text("dict")["blocks"]
    except Exception:
        return page.get_text("text")

    # Collect all font sizes to estimate body text size (most common size)
    all_sizes = []
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                all_sizes.append(round(span["size"], 1))

    if not all_sizes:
        return page.get_text("text")

    # Body size = most frequently occurring font size
    body_size = max(set(all_sizes), key=all_sizes.count)

    lines_md = []
    for block in blocks:
        for line in block.get("lines", []):
            line_text = ""
            heading_level = None
            for span in line.get("spans", []):
                text = span["text"].strip()
                if not text:
                    continue
                size = round(span["size"], 1)
                level = get_heading_level(size, body_size)
                if level and heading_level is None:
                    heading_level = level
                line_text += text + " "

            line_text = line_text.strip()
            if not line_text:
                continue

            if heading_level:
                lines_md.append(f"{'#' * heading_level} {line_text}")
            else:
                lines_md.append(line_text)

    return "\n".join(lines_md)


def extract_links(text):
    """ Convert detected URLs into clickable Markdown links """
    url_pattern = r"(https?://[^\s]+)"
    return re.sub(url_pattern, r"[\1](\1)", text)


def extract_tables(text):
    """ Format tab-separated lines as Markdown tables """
    lines = text.split("\n")
    table_text = []
    for line in lines:
        if "\t" in line:
            table_text.append("| " + " | ".join(line.split("\t")) + " |")
        else:
            table_text.append(line)
    return "\n".join(table_text)


def build_image_ref(file_name, img_counter):
    """ Build a relative Markdown image reference """
    return f"![Image {img_counter}](./{file_name}/images/image_{img_counter}.png)"


# ── Argument parsing ──────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Convert a PDF to Markdown, with images extracted into a named subfolder."
)
parser.add_argument("pdf", help="Path to the source PDF file")
parser.add_argument(
    "--output", "-o",
    help="Output directory (default: same directory as the PDF)",
    default=None
)
args = parser.parse_args()

pdf_filename = args.pdf
output_dir = args.output if args.output else os.path.dirname(os.path.abspath(pdf_filename))

if not os.path.isfile(pdf_filename):
    print(f"Error: file not found: {pdf_filename}")
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)

file_name_ext = os.path.basename(pdf_filename)
file_name = os.path.splitext(file_name_ext)[0]
md_path = os.path.join(output_dir, file_name + ".md")

print(f"Input:      {pdf_filename}")
print(f"Output dir: {output_dir}")
print(f"Markdown:   {md_path}")

# ── Extract images (calls extractImagesFromPdf.py as a module) ───────────────────
print("\nExtracting images...")
extract_images_from_pdf(pdf_filename, output_dir)

# ── Convert PDF pages to Markdown ─────────────────────────────────────────────
print("\nConverting PDF to Markdown...")
doc = fitz.open(pdf_filename)
img_counter = 1

with open(md_path, "w", encoding="utf-8") as md_file:
    for page_num in range(len(doc)):
        page = doc[page_num]

        # Extract text with font-size heading detection
        text = extract_page_text(page)
        text = extract_links(text)
        text = extract_tables(text)

        # Build image references for images on this page
        image_refs = []
        for _ in page.get_images(full=True):
            image_refs.append(build_image_ref(file_name, img_counter))
            img_counter += 1

        md_file.write(f"## Page {page_num + 1}\n\n{text}\n")
        if image_refs:
            md_file.write("\n" + "\n".join(image_refs) + "\n")
        md_file.write("\n")

print(f"\nDone. Markdown written to '{md_path}'")