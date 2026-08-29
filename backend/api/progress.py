from fastapi import APIRouter
from backend.models.storage import storage

router = APIRouter(prefix="/api/progress", tags=["Progress"])

@router.get("/{subject_id}")
async def get_progress(subject_id: str):
    history = storage.get_quiz_history(subject_id)
    
    topic_mastery = [
        {"topic": "Graphs & BFS/DFS", "mastery_before": 42, "mastery_now": 76, "delta": "+34%"},
        {"topic": "Trees & Binary Search Trees", "mastery_before": 65, "mastery_now": 89, "delta": "+24%"},
        {"topic": "Sorting Algorithms", "mastery_before": 70, "mastery_now": 82, "delta": "+12%"},
        {"topic": "Dynamic Programming", "mastery_before": 25, "mastery_now": 38, "delta": "+13%"},
        {"topic": "Stacks & Queues", "mastery_before": 58, "mastery_now": 78, "delta": "+20%"}
    ]

    return {
        "subject_id": subject_id,
        "total_quizzes_taken": len(history),
        "recent_scores": history[-5:],
        "topic_mastery": topic_mastery,
        "overall_readiness": 68
    }
