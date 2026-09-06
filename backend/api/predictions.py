from fastapi import APIRouter

from backend.models.storage import storage
from backend.services.priority_engine import priority_engine
from backend.services.similarity_engine import similarity_engine


router = APIRouter(
    prefix="/api/predictions",
    tags=["Predictions"]
)


@router.get("/{subject_id}")
async def get_predictions(subject_id: str):

    all_questions = storage.get_questions(subject_id)

    # Only previous question papers are used for prediction.
    # Study material / practice questions are excluded.
    question_papers = [
        q for q in all_questions
        if q.get("source_type", "question_paper") == "question_paper"
    ]

    priorities = priority_engine.calculate_topic_priorities(
        question_papers
    )

    repeated = similarity_engine.detect_repeated_questions(
        question_papers
    )

    # Historical question-type distribution
    type_counts = {}

    for question in question_papers:
        question_type = question.get(
            "question_type",
            "Unknown"
        )

        type_counts[question_type] = (
            type_counts.get(question_type, 0) + 1
        )

    total = max(1, len(question_papers))

    likely = {
        question_type: f"{round(count / total * 100)}% historical share"
        for question_type, count in sorted(
            type_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )[:6]
    }

    return {
        "subject_id": subject_id,
        "important_topics": priorities,
        "likely_question_types": likely,
        "frequently_repeated_concepts": repeated[:8],
        "historical_question_count": len(question_papers),
        "study_material_count": (
            len(all_questions) - len(question_papers)
        ),
        "disclaimer": (
            "These are pattern-based study priorities derived "
            "only from uploaded previous question papers. "
            "Study materials and practice problems are excluded. "
            "They are not guaranteed predictions of the next exam paper."
        )
    }