from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import uuid
from backend.services.pdf_parser import pdf_parser_service
from backend.services.ocr_service import ocr_service
from backend.services.question_extractor import question_extractor_service
from backend.models.storage import storage

router=APIRouter(prefix="/api/upload",tags=["Upload"])
@router.post("/paper")
async def upload_question_paper(file:UploadFile=File(...),subject_id:str=Form("dsa"),year:int=Form(2025),paper_title:Optional[str]=Form(None)):
    content=await file.read()
    raw=pdf_parser_service.extract_text_from_pdf(content) if file.filename.lower().endswith('.pdf') else ocr_service.process_image(content)
    if not raw.strip() and file.filename.lower().endswith('.pdf'): raw=ocr_service.process_pdf_pages(content)
    if not raw.strip(): raise HTTPException(422,"Could not extract text. Install OCR dependencies for scanned documents or upload a text PDF.")
    syllabus=storage.get_syllabus(subject_id) or {}
    qs=question_extractor_service.extract_questions_from_text(raw,year,syllabus)
    if not qs: raise HTTPException(422,"No questions were detected in this paper.")
    storage.add_questions(subject_id,qs)
    paper=storage.add_paper(subject_id,year,paper_title or file.filename,file.filename,len(qs))
    return {"status":"success","paper_id":paper["id"],"subject_id":subject_id,"year":year,"title":paper["title"],"extracted_questions_count":len(qs),"questions":qs}

@router.post("/syllabus")
async def upload_syllabus(file:UploadFile=File(...),subject_id:str=Form("dsa")):
    content=await file.read(); raw=pdf_parser_service.extract_text_from_pdf(content)
    if not raw.strip(): raw=ocr_service.process_pdf_pages(content)
    if not raw.strip(): raise HTTPException(422,"Could not extract syllabus text.")
    # The existing syllabus JSON is the canonical structured source. We don't silently invent a structure.
    return {"status":"received","subject_id":subject_id,"message":"Syllabus text extracted. Structured syllabus mapping should be reviewed before replacing the stored syllabus."}
