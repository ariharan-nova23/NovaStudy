from fastapi import APIRouter
from backend.models.storage import storage
from backend.services.priority_engine import priority_engine
from backend.services.similarity_engine import similarity_engine
router=APIRouter(prefix="/api/predictions",tags=["Predictions"])
@router.get("/{subject_id}")
async def get_predictions(subject_id:str):
    q=storage.get_questions(subject_id); priorities=priority_engine.calculate_topic_priorities(q); repeated=similarity_engine.detect_repeated_questions(q)
    # Historical likelihood only; not an exact future-paper prediction.
    type_counts={}
    for x in q: type_counts[x.get('question_type','Unknown')]=type_counts.get(x.get('question_type','Unknown'),0)+1
    total=max(1,len(q)); likely={k:f"{round(v/total*100)}% historical share" for k,v in sorted(type_counts.items(),key=lambda x:x[1],reverse=True)[:6]}
    return {"subject_id":subject_id,"important_topics":priorities,"likely_question_types":likely,"frequently_repeated_concepts":repeated[:8],"disclaimer":"These are pattern-based study priorities derived from the uploaded question papers. They are not guaranteed predictions of the next exam paper."}
