import os
import fitz  # PyMuPDF
import re
import sys

#*** Run Commmand ****
#python pdfToMarkdown.py O:\paye-employers-documentation-v2\paye-employers-documentation-v2-python-scripts\PITSelfServiceGuide.pdf

print('Script Parameters', sys.argv)
firstParameter = str(sys.argv[1])
print(firstParameter)

# Define the input PDF and output Markdown filenames
pdf_filename = firstParameter
print(os.getcwd())    
exit

fileNameExtn = os.path.basename(pdf_filename)
fileName = os.path.splitext(fileNameExtn)[0]
print(fileName)
md_filename = fileName + ".md"

 
def extract_headings(text):
    """ Convert detected headings to Markdown format """
    lines = text.split("\n")
    markdown_text = []
    for line in lines:
        if line.isupper():  # Assuming headings are in uppercase
            markdown_text.append(f"## {line}")  
        else:
            markdown_text.append(line)
    return "\n".join(markdown_text)

def extract_images(page, img_counter):
    """ Extract images and reference them in Markdown """
    md_image_links = []
    for img_index, img in enumerate(page.get_images(full=True)):
        img_filename = f"image_{img_counter}.png"
        # md_image_links.append(f"![Image {img_counter}](./{img_filename})")
        currentDir = os.getcwd()
        currentDirectory = currentDir.replace("\\","/") 
        # print(currentDirectory)
        md_image_links.append(f"![Image {img_counter}]({currentDirectory}/{fileName}/images/{img_filename})")
        img_counter += 1
    return "\n".join(md_image_links), img_counter

def extract_links(text):
    """ Convert detected URLs into clickable Markdown links """
    url_pattern = r"(https?://[^\s]+)"
    return re.sub(url_pattern, r"[\1](\1)", text)

def extract_tables(text):
    """ Attempt to format tables in Markdown format """
    lines = text.split("\n")
    table_text = []
    for line in lines:
        if "\t" in line:  # Assuming tab-separated values as tables
            table_text.append("| " + " | ".join(line.split("\t")) + " |")
        else:
            table_text.append(line)
    return "\n".join(table_text)

# Open the PDF file
doc = fitz.open(pdf_filename)
img_counter = 1

# Extract text and format Markdown
with open(md_filename, "w", encoding="utf-8") as md_file:
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        # Apply transformations
        text = extract_headings(text)
        text = extract_links(text)
        text = extract_tables(text)

        # Extract and reference images
        image_refs, img_counter = extract_images(page, img_counter)

        # Write to Markdown file
        md_file.write(f"# Page {page_num + 1}\n\n{text}\n\n{image_refs}\n\n")

print(f"Markdown file '{md_filename}' has been created successfully!")