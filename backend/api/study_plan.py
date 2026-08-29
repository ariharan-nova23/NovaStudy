from fastapi import APIRouter
from backend.services.study_planner import study_planner_service
from backend.models.storage import storage

router = APIRouter(prefix="/api/study-plan", tags=["Study Plan"])

@router.get("/{subject_id}")
async def get_study_plan(subject_id: str, days_left: int = 7, daily_hours: float = 3.0):
    subjects = storage.get_subjects()
    s_name = next((s["name"] for s in subjects if s["id"] == subject_id), "Data Structures & Algorithms")
    
    plan = study_planner_service.generate_study_plan(
        subject_id=subject_id,
        subject_name=s_name,
        days_left=days_left,
        daily_hours=daily_hours
    )
    return plan
