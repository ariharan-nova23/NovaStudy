from fastapi import APIRouter
from backend.models.storage import storage
from backend.services.pattern_analyzer import pattern_analyzer_service
from backend.services.similarity_engine import similarity_engine
router=APIRouter(prefix="/api/analysis",tags=["Analysis"])
@router.get("/questions/{subject_id}")
async def get_subject_questions(subject_id:str):
    q=storage.get_questions(subject_id); return {"subject_id":subject_id,"total_questions":len(q),"questions":q}
@router.get("/patterns/{subject_id}")
async def get_pattern_analysis(subject_id:str):
    q=storage.get_questions(subject_id); p=pattern_analyzer_service.analyze_patterns(q); years={x.get('year') for x in q if x.get('year')}
    return {"subject_id":subject_id,"total_papers":len(years),"total_questions":len(q),**p}
@router.get("/repeated/{subject_id}")
async def get_repeated_questions(subject_id:str):
    groups=similarity_engine.detect_repeated_questions(storage.get_questions(subject_id)); return {"subject_id":subject_id,"total_groups":len(groups),"repeated_groups":groups}
