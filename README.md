# NovaStudy AI

NovaStudy is a vanilla HTML/CSS/JavaScript + FastAPI study platform that turns previous question papers and syllabus data into exam-pattern analysis, study priorities, model papers, quizzes, mock exams, progress analytics and an AI tutor.

## Run locally

```powershell
cd NovaStudy
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000

## AI mode

Copy `.env.example` to `.env` and set `OPENAI_API_KEY`. Then restart the server. The backend uses the OpenAI Responses API for contextual generation when a key is present; without a key, deterministic analysis and fallback generation remain available.

## OCR

Text PDFs are handled directly. Image uploads use Tesseract when installed. Scanned PDFs can be rendered and OCR'd when PyMuPDF + Tesseract are available.

## Important

Prediction scores are pattern-based study priorities, not guarantees of future exam questions. Historical data and uploaded syllabus are the source of truth for analysis.
