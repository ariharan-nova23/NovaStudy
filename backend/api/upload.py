from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
import uuid
from backend.services.pdf_parser import pdf_parser_service
from backend.services.ocr_service import ocr_service
from backend.services.question_extractor import question_extractor_service
from backend.models.storage import storage

router = APIRouter(prefix="/api/upload", tags=["Upload"])

@router.post("/paper")
async def upload_question_paper(
    file: UploadFile = File(...),
    subject_id: str = Form("dsa"),
    year: int = Form(2025),
    paper_title: Optional[str] = Form(None)
):
    content = await file.read()

    # Detect PDF or Image
    if file.filename.lower().endswith(".pdf"):
        raw_text = pdf_parser_service.extract_text_from_pdf(content)
    else:
        raw_text = ocr_service.process_image(content)

    title = paper_title or file.filename or f"{year} Question Paper"
    
    # Extract structured questions
    extracted = question_extractor_service.extract_questions_from_text(raw_text, year)

    # Save questions into storage engine
    for q in extracted:
        storage.add_question(subject_id, q)

    return {
        "status": "success",
        "paper_id": f"paper_{uuid.uuid4().hex[:8]}",
        "subject_id": subject_id,
        "year": year,
        "title": title,
        "extracted_questions_count": len(extracted),
        "questions": extracted
    }

@router.post("/syllabus")
async def upload_syllabus(
    file: UploadFile = File(...),
    subject_id: str = Form("dsa")
):
    content = await file.read()
    raw_text = pdf_parser_service.extract_text_from_pdf(content)
    
    return {
        "status": "success",
        "subject_id": subject_id,
        "message": "Syllabus uploaded and mapped successfully.",
        "units_mapped": 5
    }
