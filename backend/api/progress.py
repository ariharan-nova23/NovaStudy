from fastapi import APIRouter
from backend.models.storage import storage
from backend.services.priority_engine import priority_engine
router=APIRouter(prefix="/api/progress",tags=["Progress"])
@router.get("/{subject_id}")
async def get_progress(subject_id:str):
    history=storage.get_quiz_history(subject_id); priorities=priority_engine.calculate_topic_priorities(storage.get_questions(subject_id))
    avg=round(sum((h.get("score",0)/max(1,h.get("total",100))*100) for h in history)/len(history),1) if history else 0
    mastery=[{"topic":p["topic"],"mastery_before":0,"mastery_now":avg,"delta":f"{avg:.0f}%"} for p in priorities[:8]]
    return {"subject_id":subject_id,"total_quizzes_taken":len(history),"recent_scores":history[-8:],"topic_mastery":mastery,"overall_readiness":avg}
