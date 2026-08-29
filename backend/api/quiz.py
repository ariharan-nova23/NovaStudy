from fastapi import APIRouter
from backend.models.schema import QuizConfig, QuizSubmission
from backend.services.quiz_generator import quiz_generator_service
from backend.services.evaluator import evaluator_service
from backend.models.storage import storage

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])

@router.post("/generate")
async def generate_quiz(config: QuizConfig):
    quiz_data = quiz_generator_service.generate_quiz(
        subject_id=config.subject_id,
        quiz_mode=config.quiz_mode,
        num_questions=config.num_questions,
        difficulty=config.difficulty,
        target_topic=config.target_topic
    )
    return quiz_data

@router.post("/submit")
async def submit_quiz(submission: QuizSubmission):
    result = evaluator_service.evaluate_quiz(
        quiz_id=submission.quiz_id,
        subject_id=submission.subject_id,
        user_answers=submission.answers
    )
    
    # Save into storage history
    storage.save_quiz_history({
        "id": submission.quiz_id,
        "subject_id": submission.subject_id,
        "score": result["score"],
        "total": result["total_questions"],
        "date": "Today",
        "quiz_type": "Practice Quiz"
    })

    return result
