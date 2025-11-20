"""
Simple script to extract images embedded in one or more PDFs using PyMuPDF (fitz).
Usage:
    python extract_pdf_images.py Simplified_Project_Proposal.pdf GazePointer_Journal.pdf

Outputs images to ./extracted_images/<pdf-stem>/ as PNG (or native) files.
"""
import sys
import os
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) not installed. Install with: pip install pymupdf")
    sys.exit(1)


def extract_images(pdf_path: str, base_out_dir: str = "extracted_images"):
    pdf = Path(pdf_path)
    if not pdf.exists():
        raise FileNotFoundError(pdf_path)

    out_dir = Path(base_out_dir) / pdf.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf))
    count = 0
    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)
        if image_list:
            print(f"[{pdf.name}] Found {len(image_list)} images on page {page_index+1}")
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image.get("ext", "png")
            out_path = out_dir / f"page{page_index+1}_img{img_index}.{image_ext}"
            with open(out_path, "wb") as f:
                f.write(image_bytes)
            print(f"Saved image: {out_path}")
            count += 1

    print(f"Extraction complete. {count} images saved to {out_dir}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_images.py <pdf-file> [<pdf-file> ...]")
        sys.exit(1)
    for pdf_path in sys.argv[1:]:
        extract_images(pdf_path)
