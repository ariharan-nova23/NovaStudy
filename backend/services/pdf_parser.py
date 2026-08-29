import io
try:
    import pypdf
except ImportError:
    pypdf = None

class PDFParserService:
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        if not pypdf:
            return ""
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        parts = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip(): parts.append(text)
        return "\n".join(parts)

pdf_parser_service = PDFParserService()
