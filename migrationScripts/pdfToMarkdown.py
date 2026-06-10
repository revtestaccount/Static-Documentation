import os
import sys
import re
import hashlib
import argparse
import fitz  # PyMuPDF
from collections import Counter

# pdfplumber is optional — provides better table extraction
# Install via: pip install pdfplumber
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    pdfplumber = None
    PDFPLUMBER_AVAILABLE = False
    print("Warning: pdfplumber not available. Tables will use basic tab detection.")
    print("         Install with: pip install pdfplumber")

from extractImagesFromPdf import extract_images_from_pdf

# *** Run Command ***
# python pdfToMarkdown.py <pdf_path> [--output <dir>]
#
# Examples:
#   python pdfToMarkdown.py source.pdf
#   python pdfToMarkdown.py source.pdf --output content/PIT3/guide/

# ---------------------------------------------------------------------------
# 1. FONT SIZE ANALYSIS
# ---------------------------------------------------------------------------

def get_font_metrics(doc):
    """
    Scan the whole document to find:
      - title_text : the document title string
      - title_size : font size of the title
      - body_size  : most common font size across the document

    On page 1, collect all spans with font size >= 1.3x body size.
    The title is the one with the largest font. If sizes tie, prefer
    the one furthest down the page (highest y%).
    """
    all_sizes = []
    for page in doc:
        try:
            blocks = page.get_text("dict")["blocks"]
        except Exception:
            continue
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    all_sizes.append(round(span["size"], 1))
    if not all_sizes:
        return "", 18.0, 11.0

    body_size = Counter(all_sizes).most_common(1)[0][0]

    title_text = ""
    title_size = 0.0
    try:
        p1_blocks = doc[0].get_text("dict")["blocks"]
        page_h    = doc[0].rect.height
        candidates = []  # (y_pct, size, text)
        for block in p1_blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span["size"], 1)
                    text = span["text"].strip()
                    if not text:
                        continue
                    if size >= body_size * 1.3:
                        y_pct = span["bbox"][1] / page_h * 100
                        candidates.append((y_pct, size, text))
        if candidates:
            # Sort by y% descending — the document title sits lowest on the cover page.
            # Branding/logo text is typically higher up (smaller y%) than the actual title.
            candidates.sort(key=lambda x: x[0], reverse=True)
            _, title_size, title_text = candidates[0]
    except Exception:
        pass

    return title_text, title_size, body_size


def get_heading_level(span_size, body_size, title_size, title_emitted):
    """
    Map a font size to a Markdown heading level.
      - Title size, first occurrence only -> # h1
      - >= 1.3x body                      -> ## h2
      - >= 1.1x body                      -> ### h3
      - otherwise                         -> None (body text)
    """
    if not title_emitted and round(span_size, 1) == round(title_size, 1):
        return 1
    ratio = span_size / body_size
    if ratio >= 1.3:
        return 2
    elif ratio >= 1.1:
        return 3
    return None


# ---------------------------------------------------------------------------
# 2. REPEATING HEADER/FOOTER DETECTION
# ---------------------------------------------------------------------------

def get_repeating_lines(doc, min_repeat=3, header_zone=12.0, footer_zone=88.0):
    """
    Return a set of text lines that:
      - appear on min_repeat or more pages, AND
      - have an average y-position in the header zone (top 12%) or
        footer zone (bottom 88%+) of the page.

    This prevents content lines that happen to repeat (e.g. table column
    headers like 'GET' or 'Query Parameters') from being suppressed.
    """
    line_positions = {}  # text -> list of y% positions across pages
    for page in doc:
        ph = page.rect.height
        if ph == 0:
            continue
        seen = set()
        try:
            blocks = page.get_text("dict")["blocks"]
        except Exception:
            continue
        for block in blocks:
            for line in block.get("lines", []):
                line_text = "".join(
                    s["text"] for s in line.get("spans", [])
                ).strip()
                if line_text and len(line_text) > 2 and line_text not in seen:
                    y_pct = line["bbox"][1] / ph * 100
                    line_positions.setdefault(line_text, []).append(y_pct)
                    seen.add(line_text)

    suppressed = set()
    for text, positions in line_positions.items():
        if len(positions) < min_repeat:
            continue
        avg_y = sum(positions) / len(positions)
        if avg_y < header_zone or avg_y > footer_zone:
            suppressed.add(text)
    return suppressed


# ---------------------------------------------------------------------------
# 3. VISUAL TOC DETECTION
# ---------------------------------------------------------------------------

def is_toc_line(line):
    """
    Return True if a line looks like a visual TOC entry (dot leaders).
    e.g. "Introduction ..................... 5"
    """
    return bool(re.search(r'\.{4,}', line)) or bool(re.search(r'\s{3,}\d+\s*$', line))


def is_toc_block(lines):
    """
    Return True if a block of lines is predominantly a visual TOC
    (majority of lines are TOC-like, or starts with 'Contents'/'Table of Contents').
    """
    if not lines:
        return False
    header = lines[0].strip().lower()
    if header in ('contents', 'table of contents'):
        return True
    toc_line_count = sum(1 for l in lines if is_toc_line(l))
    return toc_line_count >= len(lines) * 0.5


# ---------------------------------------------------------------------------
# 4. PAGE NUMBER DETECTION
# ---------------------------------------------------------------------------

def is_page_number(line):
    """ Return True if a line is just a bare page number. """
    return bool(re.match(r'^\s*\d{1,3}\s*$', line))


# ---------------------------------------------------------------------------
# 5. CODE BLOCK DETECTION
# ---------------------------------------------------------------------------

# Patterns that suggest a line is part of a code/pre block
CODE_PATTERNS = [
    r'^(GET|POST|PUT|DELETE|PATCH)\s+https?://',   # HTTP method + URL
    r'^(GET|POST|PUT|DELETE|PATCH)\s+/',            # HTTP method + path
    r'^\s*(Host|Date|Content-Type|Digest|Signature|Authorization|X-HTTP):\s',  # HTTP headers
    r'^\s*\{.*\}\s*$',                              # JSON object line
    r'^\s*"[a-zA-Z_]+":\s',                         # JSON key-value
    r'HTTP/[12]\.[01]',                              # HTTP version
    r'^\s*(//|#)\s',                                 # code comment
    r'[a-zA-Z]+\.[a-zA-Z]+\(',                      # method call
    r'^\(request-target\):',                        # HTTP signature request-target
    r'^host:\s',                                     # HTTP signature host line
    r'^date:\s',                                     # HTTP signature date line
    r'^content-type:\s',                             # HTTP signature content-type line
    r'^algorithm=',                                  # HTTP signature algorithm component
    r'^headers=',                                    # HTTP signature headers component
    r'^signature=',                                  # HTTP signature signature component
]
CODE_RE = [re.compile(p) for p in CODE_PATTERNS]

def looks_like_code(line):
    return any(r.search(line) for r in CODE_RE)

def apply_code_blocks(lines):
    """
    Wrap consecutive code-like lines in fenced code blocks.
    """
    result = []
    in_code = False
    for line in lines:
        if looks_like_code(line):
            if not in_code:
                result.append("```")
                in_code = True
            result.append(line)
        else:
            if in_code:
                result.append("```")
                in_code = False
            result.append(line)
    if in_code:
        result.append("```")
    return result


# ---------------------------------------------------------------------------
# 6. PARAGRAPH JOINING
# ---------------------------------------------------------------------------

SENTENCE_END = re.compile(r'[.!?:]\s*$')
# Matches markdown unordered list (- or *) and numbered list (1. 2) etc.
LIST_PREFIX  = re.compile(r'^\s*[-\*]\s|^\s*[?\-\*\d]+[\.\)]\s')

def join_paragraphs(lines):
    """
    Join lines that are part of the same flowing paragraph.
    A line break is preserved when:
      - The current line ends with sentence-ending punctuation
      - The next line starts a heading (#), list item, or is blank
      - The current line is a heading
    Otherwise lines are joined with a space.
    """
    result = []
    buffer = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buffer:
                result.append(buffer)
                buffer = ""
            result.append("")
            continue
        is_heading = stripped.startswith("#")
        is_list    = bool(LIST_PREFIX.match(stripped))
        if is_heading or is_list:
            if buffer:
                result.append(buffer)
                buffer = ""
            result.append(stripped)
            continue
        if buffer:
            if SENTENCE_END.search(buffer) or is_heading:
                result.append(buffer)
                buffer = stripped
            else:
                buffer += " " + stripped
        else:
            buffer = stripped
    if buffer:
        result.append(buffer)
    return result


# ---------------------------------------------------------------------------
# 7. CONSECUTIVE TABLE MERGING
# ---------------------------------------------------------------------------

def merge_consecutive_tables(md_text):
    """
    Post-process markdown to merge consecutive tables that have the same
    number of columns. Handles tables that span PDF page breaks and get
    emitted as separate markdown tables by pdfplumber.
    """
    def count_cols(row):
        return len(row.strip().strip('|').split('|'))

    def is_table_row(line):
        return line.strip().startswith('|')

    def is_separator_row(line):
        return bool(re.match(r'^\s*\|[\s\-|:]+\|\s*$', line))

    lines = md_text.split('\n')
    result = []
    i = 0

    while i < len(lines):
        if not is_table_row(lines[i]):
            result.append(lines[i])
            i += 1
            continue

        # Collect current table block
        table = []
        while i < len(lines) and is_table_row(lines[i]):
            table.append(lines[i])
            i += 1

        # Look ahead past blank lines for another table
        j = i
        while j < len(lines) and lines[j].strip() == '':
            j += 1

        # If next non-blank content is also a table, check column compatibility
        if j < len(lines) and is_table_row(lines[j]):
            next_table = []
            k = j
            while k < len(lines) and is_table_row(lines[k]):
                next_table.append(lines[k])
                k += 1

            current_cols = count_cols(table[0]) if table else 0
            next_cols    = count_cols(next_table[0]) if next_table else 0

            if current_cols == next_cols and current_cols > 0:
                # Merge: drop the header row and separator from the continuation table
                rows_to_merge = [
                    row for idx, row in enumerate(next_table)
                    if idx != 0 and not is_separator_row(row)
                ]
                table.extend(rows_to_merge)
                i = k  # advance past the merged table
                print(f"  [merge_tables] merged two {current_cols}-column tables")

        result.extend(table)
        result.append('')  # blank line after table

    return '\n'.join(result)


# ---------------------------------------------------------------------------
# 8. TABLE EXTRACTION (pdfplumber)
# ---------------------------------------------------------------------------

def extract_tables_from_page(plumber_page):
    """
    Extract tables from a page using pdfplumber and return them as a dict:
      { bbox_tuple: markdown_table_string }
    so we can replace the raw text in those regions with the Markdown table.
    """
    tables = {}
    try:
        for table in plumber_page.extract_tables():
            if not table:
                continue
            rows = []
            for i, row in enumerate(table):
                cells = [str(c).strip().replace("\n", " ") if c else "" for c in row]
                rows.append("| " + " | ".join(cells) + " |")
                if i == 0:
                    rows.append("|" + "|".join(["---"] * len(cells)) + "|")
            tables[id(table)] = "\n".join(rows)
    except Exception:
        pass
    return tables


# ---------------------------------------------------------------------------
# 9. MAIN PAGE TEXT EXTRACTION
# ---------------------------------------------------------------------------

def extract_page_text(page, plumber_page, title_size, body_size,
                      title_emitted, repeating_lines):
    """
    Extract and clean text from one page.
    Returns (markdown_text, title_emitted).
    """
    try:
        blocks = page.get_text("dict")["blocks"]
    except Exception:
        return page.get_text("text"), title_emitted

    # -- Extract pdfplumber tables and record their bounding boxes --
    md_tables   = []  # list of markdown table strings
    table_bboxes = []  # list of (x0, y0, x1, y1) for each table
    if PDFPLUMBER_AVAILABLE and plumber_page is not None:
        try:
            for table in plumber_page.find_tables():
                bbox = table.bbox  # (x0, top, x1, bottom)
                md_rows = []
                data = table.extract()
                if not data:
                    continue
                for i, row in enumerate(data):
                    cells = [str(c).strip().replace("\n", " ") if c else "" for c in row]
                    md_rows.append("| " + " | ".join(cells) + " |")
                    if i == 0:
                        md_rows.append("|" + "|".join(["---"] * len(cells)) + "|")
                md_tables.append("\n".join(md_rows))
                table_bboxes.append(bbox)
        except Exception:
            pass

    def in_table_region(block_bbox):
        """ Return True if a fitz block overlaps with any pdfplumber table bbox. """
        bx0, by0, bx1, by1 = block_bbox
        for (tx0, ty0, tx1, ty1) in table_bboxes:
            if bx0 < tx1 and bx1 > tx0 and by0 < ty1 and by1 > ty0:
                return True
        return False

    # -- Extract text blocks --
    raw_lines = []
    title_emitted_this_call = False

    for block in blocks:
        # Skip fitz text blocks that fall inside a pdfplumber table region
        # to prevent duplicate content (raw text + table)
        block_bbox = block.get("bbox", (0, 0, 0, 0))
        if table_bboxes and in_table_region(block_bbox):
            continue

        block_lines_text = []
        for line in block.get("lines", []):
            line_text = ""
            heading_level = None
            for span in line.get("spans", []):
                text = span["text"].strip()
                if not text:
                    continue
                size = round(span["size"], 1)
                level = get_heading_level(size, body_size, title_size,
                                          title_emitted or title_emitted_this_call)
                if level == 1:
                    title_emitted_this_call = True
                if level and heading_level is None:
                    heading_level = level
                line_text += text + " "

            line_text = line_text.strip()
            if not line_text:
                continue

            # Convert PDF bullet character (•) to markdown list item
            if line_text.startswith('\u2022'):
                line_text = '- ' + line_text[1:].strip()
            elif '\u2022' in line_text:
                # Multiple bullets on one line: "• item1 • item2"
                parts = [p.strip() for p in line_text.split('\u2022') if p.strip()]
                if len(parts) > 1:
                    for part in parts:
                        block_lines_text.append('- ' + part)
                    continue

            # Convert PDF sub-bullet 'o ' (lowercase o + space) to indented list item.
            # PDFs use 'o' as a second-level bullet character (e.g. in date format lists).
            if re.match(r'^o\s+\S', line_text):
                line_text = '  - ' + line_text[1:].strip()

            # Skip bare page numbers
            if is_page_number(line_text):
                continue

            # Skip repeating headers/footers (header/footer zone only)
            if line_text in repeating_lines:
                continue

            if heading_level:
                block_lines_text.append(f"{'#' * heading_level} {line_text}")
            else:
                block_lines_text.append(line_text)

        # Detect and skip visual TOC blocks
        if is_toc_block(block_lines_text):
            continue

        raw_lines.extend(block_lines_text)
        raw_lines.append("")  # blank line between blocks

    # -- Apply code block wrapping --
    raw_lines = apply_code_blocks(raw_lines)

    # -- Join flowing paragraphs --
    raw_lines = join_paragraphs(raw_lines)

    # -- Append pdfplumber tables at end of page --
    if md_tables:
        raw_lines.append("")
        for tbl in md_tables:
            raw_lines.append(tbl)
            raw_lines.append("")

    return "\n".join(raw_lines), title_emitted or title_emitted_this_call


# ---------------------------------------------------------------------------
# 10. IMAGE DEDUPLICATION
# ---------------------------------------------------------------------------

def get_image_hash(doc, xref):
    """ Return MD5 hash of raw image bytes. """
    try:
        img = doc.extract_image(xref)
        return hashlib.md5(img["image"]).hexdigest()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# ARGUMENT PARSING
# ---------------------------------------------------------------------------

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
output_dir   = args.output if args.output else os.path.dirname(os.path.abspath(pdf_filename))

if not os.path.isfile(pdf_filename):
    print(f"Error: file not found: {pdf_filename}")
    sys.exit(1)

os.makedirs(output_dir, exist_ok=True)

file_name_ext = os.path.basename(pdf_filename)
file_name     = os.path.splitext(file_name_ext)[0]
md_path       = os.path.join(output_dir, file_name + ".md")

print(f"Input:      {pdf_filename}")
print(f"Output dir: {output_dir}")
print(f"Markdown:   {md_path}")

# ---------------------------------------------------------------------------
# MAIN CONVERSION
# ---------------------------------------------------------------------------

doc = fitz.open(pdf_filename)

# Font metrics
title_text, title_size, body_size = get_font_metrics(doc)
print(f"Document title:  {title_text!r}")
print(f"Title font size: {title_size}pt  |  Body font size: {body_size}pt")

# Repeating lines (headers/footers)
repeating_lines = get_repeating_lines(doc)
print(f"Repeating lines detected: {len(repeating_lines)}")
for l in sorted(repeating_lines):
    print(f"  suppress: {l!r}")

# Extract images with deduplication
print("\nExtracting images...")
image_dir = os.path.join(output_dir, file_name, "images")
os.makedirs(image_dir, exist_ok=True)
seen_hashes = set()
# Map (page_num, img_index) -> filename or None if duplicate
img_map = {}
global_counter = 1
for page_num in range(len(doc)):
    page = doc[page_num]
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        h = get_image_hash(doc, xref)
        if h and h in seen_hashes:
            img_map[(page_num, img_index)] = None  # duplicate — skip
            print(f"  page {page_num+1} img {img_index+1}: duplicate, skipped")
        else:
            if h:
                seen_hashes.add(h)
            img_name = f"image_{global_counter}.png"
            img_path = os.path.join(image_dir, img_name)
            try:
                base_image = doc.extract_image(xref)
                with open(img_path, "wb") as f:
                    f.write(base_image["image"])
                print(f"  page {page_num+1} img {img_index+1}: saved as {img_name}")
            except Exception as e:
                print(f"  page {page_num+1} img {img_index+1}: error {e}")
                img_map[(page_num, img_index)] = None
                continue
            img_map[(page_num, img_index)] = img_name
            global_counter += 1

# Convert pages to Markdown
print("\nConverting PDF to Markdown...")
title_emitted = False

def convert_pages(plumber_doc=None):
    global title_emitted
    with open(md_path, "w", encoding="utf-8") as md_file:
        # Write the document title as h1 first, before the page loop.
        # This ensures it appears once even though it is suppressed as a
        # repeating header on all subsequent pages.
        if title_text:
            md_file.write(f"# {title_text}\n\n")
            title_emitted = True
        for page_num in range(len(doc)):
            page         = doc[page_num]
            plumber_page = plumber_doc.pages[page_num] if plumber_doc else None

            text, title_emitted = extract_page_text(
                page, plumber_page, title_size, body_size,
                title_emitted, repeating_lines
            )

            # Join split URLs — PDFs sometimes break long URLs across lines.
            # A line ending with a URL fragment (no space, starts next line with
            # a path segment) gets joined before linkification.
            text = re.sub(r'(https?://[^\s]+)\s*\n\s*([^\s\[\]<>"{}|^`#%]+)', r'\1\2', text)

            # Convert URLs to Markdown links
            text = re.sub(r'(https?://[^\s\)\]]+)', r'[\1](\1)', text)

            # Build image references for this page (skip duplicates)
            image_refs = []
            for img_index, _ in enumerate(page.get_images(full=True)):
                img_name = img_map.get((page_num, img_index))
                if img_name:
                    image_refs.append(
                        f"![Image](./{file_name}/images/{img_name})"
                    )

            # Skip page 1 images entirely — these are cover page branding/logos.
            # The SVG branding block added by migration_pipeline.py replaces them.
            if page_num == 0:
                image_refs = []

            if text.strip():
                md_file.write(text.strip() + "\n\n")
            if image_refs:
                md_file.write("\n".join(image_refs) + "\n\n")

    # Post-process: merge consecutive tables split across PDF page breaks
    print("\nMerging consecutive tables...")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    md_content = merge_consecutive_tables(md_content)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


if PDFPLUMBER_AVAILABLE:
    with pdfplumber.open(pdf_filename) as plumber_doc:
        convert_pages(plumber_doc)
else:
    convert_pages(None)

print(f"\nDone. Markdown written to '{md_path}'")
