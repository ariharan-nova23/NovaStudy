import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config import APP_NAME, VERSION
from backend.models.storage import storage
from backend.api import upload, analysis, predictions, quiz, mock_exam, study_plan, progress, tutor, dashboard

app=FastAPI(title=APP_NAME,version=VERSION,description="NovaStudy AI exam analysis and study platform")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(upload.router); app.include_router(analysis.router); app.include_router(predictions.router); app.include_router(quiz.router); app.include_router(mock_exam.router); app.include_router(study_plan.router); app.include_router(progress.router); app.include_router(tutor.router); app.include_router(dashboard.router)
@app.get("/api/health")
async def health(): return {"status":"ok","app":APP_NAME,"version":VERSION}
@app.get("/api/subjects")
async def subjects(): return storage.get_subjects()

frontend=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","frontend"))
app.mount("/",StaticFiles(directory=frontend,html=True),name="frontend")
