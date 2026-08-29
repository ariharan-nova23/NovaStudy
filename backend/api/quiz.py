from fastapi import APIRouter, HTTPException
from backend.models.schema import QuizConfig, QuizSubmission
from backend.services.quiz_generator import quiz_generator_service
from backend.services.evaluator import evaluator_service
from backend.models.storage import storage
router=APIRouter(prefix="/api/quiz",tags=["Quiz"])
@router.post("/generate")
async def generate_quiz(config:QuizConfig):
    quiz=quiz_generator_service.generate_quiz(config.subject_id,storage.get_questions(config.subject_id),storage.get_syllabus(config.subject_id) or {},config.quiz_mode,config.num_questions,config.difficulty,config.target_topic,config.target_unit)
    if not quiz.get("questions"): raise HTTPException(422,"No quiz questions available. Upload question papers first.")
    storage.save_quiz(quiz)
    public=[]
    for q in quiz["questions"]:
        x=dict(q); x.pop("correct_answer_index",None); public.append(x)
    return {**quiz,"questions":public}
@router.post("/submit")
async def submit_quiz(submission:QuizSubmission):
    quiz=storage.get_quiz(submission.quiz_id)
    if not quiz: raise HTTPException(404,"Quiz session not found.")
    result=evaluator_service.evaluate_quiz(quiz,submission.answers)
    storage.save_quiz_history({"id":submission.quiz_id,"subject_id":submission.subject_id,"score":result["score"],"total":result["total_questions"],"date":"Today","quiz_type":quiz.get("quiz_mode","Practice Quiz")})
    return result
