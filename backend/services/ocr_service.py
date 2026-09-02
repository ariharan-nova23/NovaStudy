import io
import os
import pytesseract
import fitz
from PIL import Image


class OCRService:

    @staticmethod
    def _configure_tesseract():
        """
        Tell pytesseract exactly where the Tesseract executable is.
        This avoids Windows PATH issues.
        """
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            raise FileNotFoundError(
                f"Tesseract not found at: {tesseract_path}"
            )

    @staticmethod
    def process_image(file_bytes: bytes) -> str:
        try:
            OCRService._configure_tesseract()

            image = Image.open(io.BytesIO(file_bytes))

            # Convert to RGB for reliable OCR
            image = image.convert("RGB")

            text = pytesseract.image_to_string(
                image,
                config="--psm 6"
            )

            return text.strip()

        except Exception as e:
            print(f"[OCR IMAGE ERROR] {type(e).__name__}: {e}")
            return ""

    @staticmethod
    def process_pdf_pages(file_bytes: bytes) -> str:
        try:
            OCRService._configure_tesseract()

            doc = fitz.open(
                stream=file_bytes,
                filetype="pdf"
            )

            parts = []

            for page_number, page in enumerate(doc, start=1):

                # Render PDF page as an image
                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2.0, 2.0),
                    alpha=False
                )

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                text = pytesseract.image_to_string(
                    image,
                    config="--psm 6"
                )

                if text.strip():
                    parts.append(
                        f"\n--- Page {page_number} ---\n{text.strip()}"
                    )

            doc.close()

            return "\n".join(parts).strip()

        except Exception as e:
            print(f"[OCR PDF ERROR] {type(e).__name__}: {e}")
            return ""


ocr_service = OCRService()