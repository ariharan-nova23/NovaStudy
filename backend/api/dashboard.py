from fastapi import APIRouter
from backend.models.storage import storage
from backend.services.priority_engine import priority_engine
router=APIRouter(prefix="/api/dashboard",tags=["Dashboard"])
@router.get("/{subject_id}")
async def get_dashboard(subject_id:str):
    subject=next((s for s in storage.get_subjects() if s["id"]==subject_id),{"id":subject_id,"name":subject_id,"exam_days":0,"preparation":0})
    q=storage.get_questions(subject_id); history=storage.get_quiz_history(subject_id); priorities=priority_engine.calculate_topic_priorities(q)
    latest=f"{history[-1]['score']}/{history[-1]['total']}" if history else "—"
    return {"subject_id":subject_id,"subject_name":subject["name"],"exam_days":subject.get("exam_days",0),"preparation_percentage":subject.get("preparation",0),
            "total_papers_analyzed":len({x.get('year') for x in q if x.get('year')}),"total_questions_analyzed":len(q),
            "priority_topics":[{"name":p["topic"],"priority":f"{p['priority_score']}%","badge":p["priority_label"]} for p in priorities[:5]],"latest_quiz_score":latest,
            "recommendation":f"Start with {priorities[0]['topic']} and then {priorities[1]['topic']}." if len(priorities)>1 else "Upload more papers to improve analysis."}
