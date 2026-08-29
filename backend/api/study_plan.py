from fastapi import APIRouter
from backend.models.storage import storage
from backend.services.priority_engine import priority_engine
from backend.services.study_planner import study_planner_service
router=APIRouter(prefix="/api/study-plan",tags=["Study Plan"])
@router.get("/{subject_id}")
async def get_study_plan(subject_id:str,days_left:int=7,daily_hours:float=3.0):
    subject=next((s for s in storage.get_subjects() if s["id"]==subject_id),{"name":subject_id})
    history=storage.get_quiz_history(subject_id)
    weak=[]
    # Existing history stores scores; detailed topic mastery is calculated from quiz attempts when available.
    plan=study_planner_service.generate_study_plan(subject_id,subject["name"],priority_engine.calculate_topic_priorities(storage.get_questions(subject_id)),weak,days_left,daily_hours)
    storage.save_study_plan(subject_id,plan); return plan
