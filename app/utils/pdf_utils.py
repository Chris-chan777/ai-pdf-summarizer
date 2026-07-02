import fitz


def extract_text_from_pdf(pdf_path):
    """Extract and return text from every page of a PDF file."""
    with fitz.open(pdf_path) as document:
        extracted_text = "\n".join(page.get_text() for page in document).strip()

    return extracted_text or "未提取到文本内容"
