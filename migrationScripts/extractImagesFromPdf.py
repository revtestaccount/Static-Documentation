import os
import sys
import fitz

# *** Run Command ***
# python extractImagesFromPdf.py <pdf_path> [output_dir]
#
# Examples:
#   python extractImagesFromPdf.py source.pdf
#   python extractImagesFromPdf.py source.pdf content/PIT3/guide/
#
# Can also be imported and called from pdfToMarkdown.py:
#   from extractImagesFromPdf import extract_images_from_pdf


def extract_images_from_pdf(pdf_filename, output_dir=None):
    """
    Extract all images from a PDF into a subfolder named after the document.

    Folder structure created:
        <output_dir>/<document_name>/images/image_1.png
                                            image_2.png ...

    Args:
        pdf_filename (str): Path to the source PDF file.
        output_dir (str):   Directory to write output into.
                            Defaults to the same directory as the PDF.

    Returns:
        str: Path to the images directory that was created.
    """
    file_name_ext = os.path.basename(pdf_filename)
    file_name = os.path.splitext(file_name_ext)[0]

    base_dir = output_dir if output_dir else os.path.dirname(pdf_filename)
    image_directory = os.path.join(base_dir, file_name, "images")

    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
        print(f"Created image directory: {image_directory}")

    doc = fitz.open(pdf_filename)
    image_counter = 1

    for page_num in range(len(doc)):
        page = doc[page_num]
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            image_name = f"image_{image_counter}.png"
            image_path = os.path.join(image_directory, image_name)

            with open(image_path, "wb") as image_file:
                image_file.write(image_data)

            print(f"Saved image {image_counter} from page {page_num + 1}: {image_path}")
            image_counter += 1

    print(f"All images extracted to '{image_directory}'")
    return image_directory


# ── Entry point when run directly ─────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extractImagesFromPdf.py <pdf_path> [output_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    extract_images_from_pdf(pdf_path, out_dir)