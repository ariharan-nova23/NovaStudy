from fastapi import APIRouter, HTTPException
from backend.models.schema import ModelPaperConfig, MockExamSubmission
from backend.services.question_generator import question_generator_service
from backend.services.paper_validator import paper_validator_service
from backend.services.ai_service import ai_service
from backend.models.storage import storage
router=APIRouter(prefix="/api/mock-exam",tags=["Mock Exam"])
@router.post("/generate")
async def generate_mock_exam(config:ModelPaperConfig):
    subjects=storage.get_subjects(); subject=next((s for s in subjects if s["id"]==config.subject_id),None)
    if not subject: raise HTTPException(404,"Subject not found")
    paper=question_generator_service.generate_model_paper(subject["name"],storage.get_questions(config.subject_id),storage.get_syllabus(config.subject_id) or {},config.total_marks,config.duration_minutes,config.difficulty_mode,config.num_questions,config.num_previous_papers_considered)
    val=paper_validator_service.validate_paper(paper["sections"],config.total_marks,config.difficulty_mode,storage.get_syllabus(config.subject_id) or {},__import__('backend.services.priority_engine',fromlist=['priority_engine']).priority_engine.calculate_topic_priorities(storage.get_questions(config.subject_id)))
    paper["validation_status"]=val["validation_status"]; paper["validation_checks"]=val["checks"]; storage.save_generated_paper(paper); return paper
@router.post("/submit")
async def submit_mock_exam(submission:MockExamSubmission):
    # Descriptive mock exams are evaluated heuristically unless an AI key is configured.
    exam=None
    if ai_service.enabled:
        prompt=f'''Evaluate a student's descriptive mock exam. Return JSON with score (0-100), accuracy string, strong_areas list, weak_areas list, rubric_breakdown list of criterion/points/feedback. QUESTIONS AND ANSWERS: {submission.answers}'''
        exam=ai_service.ask_json(prompt)
    if not exam:
        answered=sum(1 for v in submission.answers.values() if str(v).strip()); score=round(answered/max(1,len(submission.answers))*100) if submission.answers else 0
        exam={"score":score,"accuracy":f"{score}%","strong_areas":[],"weak_areas":[],"rubric_breakdown":[{"criterion":"Answer coverage","points":f"{score}/100","feedback":"Score is based on answered-question coverage in fallback mode. Configure OPENAI_API_KEY for AI rubric evaluation."}]}
    storage.save_quiz_history({"id":submission.exam_id,"subject_id":submission.subject_id,"score":exam["score"],"total":100,"date":"Today","quiz_type":"Full Mock Exam"})
    return {"status":"success","exam_id":submission.exam_id,"score":exam["score"],"total_marks":100,"accuracy":exam.get("accuracy",f"{exam['score']}%"),"time_spent_minutes":round(submission.time_taken_seconds/60,1),"strong_areas":exam.get("strong_areas",[]),"weak_areas":exam.get("weak_areas",[]),"rubric_breakdown":exam.get("rubric_breakdown",[])}
