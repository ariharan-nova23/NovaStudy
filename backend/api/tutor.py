from fastapi import APIRouter
from backend.models.schema import TutorQuery
from backend.models.storage import storage
from backend.services.ai_service import ai_service
from backend.services.priority_engine import priority_engine
router=APIRouter(prefix="/api/tutor",tags=["AI Tutor"])
@router.post("/query")
async def process_tutor_query(q:TutorQuery):
    syllabus=storage.get_syllabus(q.subject_id) or {}; questions=storage.get_questions(q.subject_id); priorities=priority_engine.calculate_topic_priorities(questions)
    if ai_service.enabled:
        prompt=f'''You are NovaStudy's tutor. Answer the student's question using only the supplied syllabus and analyzed exam context when relevant. Be clear and student-friendly. Mention uncertainty if the source does not support a claim. STUDENT: {q.query}\nSYLLABUS: {syllabus}\nPRIORITIES: {priorities[:8]}'''
        answer=ai_service.ask(prompt) or "I couldn't generate an AI answer right now."
    else:
        top=priorities[:3]
        answer=f"AI Tutor is in fallback mode because OPENAI_API_KEY is not configured. Your analyzed high-priority topics are: {', '.join(p['topic'] for p in top)}. Configure the API key to get contextual explanations for: {q.query}"
    return {"answer":answer,"related_topics":[p["topic"] for p in priorities[:4]],"suggested_questions":[x for p in priorities[:2] for x in (f"Explain {p['topic']}", f"Give me a quiz on {p['topic']} ")]}
