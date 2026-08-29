import io
try:
    import pypdf
except ImportError:
    pypdf = None

class PDFParserService:
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        if pypdf:
            try:
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                if text.strip():
                    return text
            except Exception as e:
                print(f"pypdf extraction failed: {e}")
        
        # Fallback text decoding if not binary or plain text
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            return "Sample Extracted Paper Text: Q1. Explain BFS traversal in Graphs. Q2. Construct AVL Tree."

pdf_parser_service = PDFParserService()
