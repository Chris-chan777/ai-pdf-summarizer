import fitz


def extract_text_from_pdf(pdf_path):
    """Extract and return text from every page of a PDF file."""
    try:
        with fitz.open(pdf_path) as document:
            if document.needs_pass:
                return "PDF 文件无法解析，请确认文件未损坏或未加密。"

            extracted_text = "\n".join(
                page.get_text() for page in document
            ).strip()
    except Exception:
        return "PDF 文件无法解析，请确认文件未损坏或未加密。"

    return extracted_text or "未提取到文本内容"
