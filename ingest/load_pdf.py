from PyPDF2 import PdfReader
from langchain.schema import Document
import pytesseract
from pdf2image import convert_from_path
import camelot


def extract_page_content(pdf_path, page_num):
    """
    Extract text, tables, and OCR content from a single page.
    """
    reader = PdfReader(pdf_path)
    page = reader.pages[page_num]

    text = page.extract_text() or ""


    table_text = ""
    try:
        tables = camelot.read_pdf(
            pdf_path,
            pages=str(page_num + 1),
            flavor="stream"
        )
        for table in tables:
            table_text += table.df.to_string(index=False) + "\n"
    except Exception:
        pass

  
    ocr_text = ""
    try:
        images = convert_from_path(
            pdf_path,
            first_page=page_num + 1,
            last_page=page_num + 1
        )
        for img in images:
            ocr_text += pytesseract.image_to_string(img)
    except Exception:
        pass

    combined = "\n".join(
        part for part in [text, table_text, ocr_text] if part.strip()
    )

    return combined.strip()


def load_pdf(path: str):
    reader = PdfReader(path)
    documents = []

    for i in range(len(reader.pages)):
        content = extract_page_content(path, i)

        documents.append(
            Document(
                page_content=content if content else "[NO CONTENT FOUND]",
                metadata={"page": i}
            )
        )

    return documents
