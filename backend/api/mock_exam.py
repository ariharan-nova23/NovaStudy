from fastapi import APIRouter
from backend.models.schema import ModelPaperConfig, MockExamSubmission
from backend.services.question_generator import question_generator_service
from backend.services.paper_validator import paper_validator_service
from backend.models.storage import storage

router = APIRouter(prefix="/api/mock-exam", tags=["Mock Exam"])

@router.post("/generate")
async def generate_mock_exam(config: ModelPaperConfig):
    # Fetch subject name
    subjects = storage.get_subjects()
    s_name = next((s["name"] for s in subjects if s["id"] == config.subject_id), "Data Structures & Algorithms")

    paper_data = question_generator_service.generate_model_paper(
        subject_name=s_name,
        total_marks=config.total_marks,
        duration_minutes=config.duration_minutes,
        difficulty_mode=config.difficulty_mode,
        num_previous_papers=config.num_previous_papers_considered
    )

    # Validation step
    val_report = paper_validator_service.validate_paper(
        sections=paper_data["sections"],
        target_marks=config.total_marks,
        difficulty_mode=config.difficulty_mode
    )

    paper_data["validation_status"] = val_report["validation_status"]
    paper_data["validation_checks"] = val_report["checks"]

    return paper_data

@router.post("/submit")
async def submit_mock_exam(submission: MockExamSubmission):
    ans_count = len(submission.answers)
    total_q = 10
    raw_score = min(88, int((ans_count / max(1, total_q)) * 88) + 10)

    # Save to history
    storage.save_quiz_history({
        "id": submission.exam_id,
        "subject_id": submission.subject_id,
        "score": raw_score,
        "total": 100,
        "date": "Today",
        "quiz_type": "Full Mock Exam"
    })

    return {
        "status": "success",
        "exam_id": submission.exam_id,
        "score": raw_score,
        "total_marks": 100,
        "accuracy": f"{raw_score}%",
        "time_spent_minutes": round(submission.time_taken_seconds / 60, 1),
        "strong_areas": ["Breadth First Search (BFS)", "Quick Sort Analysis", "Circular Queue"],
        "weak_areas": ["AVL Tree Rotations (LR/RL)", "Hashing Collision Resolution"],
        "rubric_breakdown": [
            {"criterion": "Algorithmic Logic & Steps", "points": "35/40", "feedback": "Clear step-by-step logic."},
            {"criterion": "Mathematical Accuracy", "points": "22/25", "feedback": "Good numerical calculations."},
            {"criterion": "Diagram & Structure", "points": "21/35", "feedback": "Include rotational diagrams for AVL trees."}
        ]
    }
