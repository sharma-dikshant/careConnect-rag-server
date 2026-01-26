import fitz  # PyMuPDF
from io import BytesIO

class PDFParser:
    def extract_text(self, file_content: BytesIO) -> str:
        doc = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

pdf_parser = PDFParser()
