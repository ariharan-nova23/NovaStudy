from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.config import APP_NAME, VERSION
from backend.models.storage import storage
from backend.api import upload, analysis, predictions, quiz, mock_exam, study_plan, progress, tutor

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="AI Exam Analyzer & Smart Study Platform REST API Engine"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(upload.router)
app.include_router(analysis.router)
app.include_router(predictions.router)
app.include_router(quiz.router)
app.include_router(mock_exam.router)
app.include_router(study_plan.router)
app.include_router(progress.router)
app.include_router(tutor.router)

@app.get("/api/subjects")
async def get_subjects():
    return storage.get_subjects()

@app.get("/api/dashboard/{subject_id}")
async def get_dashboard_summary(subject_id: str):
    questions = storage.get_questions(subject_id)
    syllabi = storage.get_syllabi()
    history = storage.get_quiz_history(subject_id)

    years = set(q.get("year") for q in questions if q.get("year"))
    total_papers = len(years) if years else 4

    latest_quiz_score = f"{history[-1]['score']}/{history[-1]['total']}" if history else "8/10"

    return {
        "subject_id": subject_id,
        "subject_name": "Data Structures & Algorithms" if subject_id == "dsa" else "Operating Systems",
        "exam_days": 12 if subject_id == "dsa" else 18,
        "preparation_percentage": 68 if subject_id == "dsa" else 55,
        "total_papers_analyzed": total_papers,
        "total_questions_analyzed": len(questions),
        "priority_topics": [
            {"name": "Graphs & BFS/DFS", "priority": "94%", "badge": "Critical 🔥"},
            {"name": "Trees & AVL Rotations", "priority": "89%", "badge": "High 🟠"},
            {"name": "Sorting Algorithms", "priority": "82%", "badge": "High 🟠"}
        ],
        "latest_quiz_score": latest_quiz_score,
        "recommendation": "Revise BFS and DFS graph traversals and practice AVL tree rotation step-by-step questions."
    }

# Mount Frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
