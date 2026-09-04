from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from backend.services.pdf_parser import pdf_parser_service
from backend.services.ocr_service import ocr_service
from backend.services.question_extractor import question_extractor_service
from backend.models.storage import storage


router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"]
)


@router.post("/paper")
async def upload_question_paper(
    file: UploadFile = File(...),
    subject_id: str = Form("dsa"),
    year: int = Form(2025),
    paper_title: Optional[str] = Form(None),
    upload_type: str = Form("question_paper")
):

    if upload_type not in ["question_paper", "study_material"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid upload type."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        raw = pdf_parser_service.extract_text_from_pdf(content)
    else:
        raw = ocr_service.process_image(content)

    if not raw.strip() and filename.endswith(".pdf"):
        raw = ocr_service.process_pdf_pages(content)

    if not raw.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract text. Install OCR dependencies for scanned documents or upload a text PDF."
        )

    syllabus = storage.get_syllabus(subject_id) or {}

    qs = question_extractor_service.extract_questions_from_text(
        raw,
        year,
        syllabus
    )

    if not qs:
        raise HTTPException(
            status_code=422,
            detail="No questions were detected in this document."
        )

    storage.add_questions(
        subject_id,
        qs
    )

    title = (
        paper_title
        or file.filename
        or (
            "Study Material"
            if upload_type == "study_material"
            else "Question Paper"
        )
    )

    paper = storage.add_paper(
        subject_id,
        year,
        title,
        file.filename or title,
        len(qs)
    )

    return {
        "status": "success",
        "upload_type": upload_type,
        "paper_id": paper["id"],
        "subject_id": subject_id,
        "year": year,
        "title": paper["title"],
        "extracted_questions_count": len(qs),
        "questions": qs
    }


@router.post("/syllabus")
async def upload_syllabus(
    file: UploadFile = File(...),
    subject_id: str = Form("dsa")
):

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded syllabus file is empty."
        )

    raw = pdf_parser_service.extract_text_from_pdf(content)

    if not raw.strip():
        raw = ocr_service.process_pdf_pages(content)

    if not raw.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract syllabus text."
        )

    return {
        "status": "received",
        "subject_id": subject_id,
        "message": "Syllabus text extracted. Structured syllabus mapping should be reviewed before replacing the stored syllabus."
    }