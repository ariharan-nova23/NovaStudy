import io

class OCRService:
    @staticmethod
    def process_image(file_bytes: bytes) -> str:
        try:
            from PIL import Image
            import pytesseract
            image = Image.open(io.BytesIO(file_bytes))
            return pytesseract.image_to_string(image)
        except Exception:
            return ""

    @staticmethod
    def process_pdf_pages(file_bytes: bytes) -> str:
        try:
            import fitz
            from PIL import Image
            import pytesseract
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            parts = []
            for page in doc:
                pix = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                parts.append(pytesseract.image_to_string(img))
            return "\n".join(parts)
        except Exception:
            return ""

ocr_service = OCRService()
