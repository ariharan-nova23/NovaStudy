from fastapi import APIRouter
from backend.models.storage import storage
from backend.services.pattern_analyzer import pattern_analyzer_service
from backend.services.similarity_engine import similarity_engine

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])

@router.get("/questions/{subject_id}")
async def get_subject_questions(subject_id: str):
    questions = storage.get_questions(subject_id)
    return {
        "subject_id": subject_id,
        "total_questions": len(questions),
        "questions": questions
    }

@router.get("/patterns/{subject_id}")
async def get_pattern_analysis(subject_id: str):
    questions = storage.get_questions(subject_id)
    patterns = pattern_analyzer_service.analyze_patterns(questions)
    
    # Calculate paper count from distinct years
    years = set(q.get("year") for q in questions if q.get("year"))
    total_papers = len(years) if years else 4

    return {
        "subject_id": subject_id,
        "total_papers": total_papers,
        "total_questions": len(questions),
        "unit_distribution": patterns["unit_distribution"],
        "marks_distribution": patterns["marks_distribution"],
        "question_type_distribution": patterns["question_type_distribution"],
        "difficulty_distribution": patterns["difficulty_distribution"]
    }

@router.get("/repeated/{subject_id}")
async def get_repeated_questions(subject_id: str):
    questions = storage.get_questions(subject_id)
    repeated_groups = similarity_engine.detect_repeated_questions(questions)
    return {
        "subject_id": subject_id,
        "total_groups": len(repeated_groups),
        "repeated_groups": repeated_groups
    }
