from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QuestionSchema(BaseModel):
    id: str
    question: str
    year: int
    marks: int
    unit: str
    topic: str
    subtopic: str
    question_type: str
    difficulty: str
    confidence: float = 1.0
    needs_review: bool = False

class SyllabusTopic(BaseModel):
    name: str
    subtopics: List[str] = []

class SyllabusUnit(BaseModel):
    unit: str
    title: str
    topics: List[SyllabusTopic] = []

class SyllabusSchema(BaseModel):
    subject_id: str
    subject_name: str
    units: List[SyllabusUnit] = []

class ModelPaperConfig(BaseModel):
    subject_id: str
    total_marks: int = 100
    duration_minutes: int = 180
    difficulty_mode: str = "Balanced"
    num_questions: int = 10
    num_previous_papers_considered: int = 4

class QuizConfig(BaseModel):
    subject_id: str
    quiz_mode: str = "Quick Quiz"
    num_questions: int = 10
    difficulty: str = "Adaptive"
    target_topic: Optional[str] = None
    target_unit: Optional[str] = None

class QuizSubmission(BaseModel):
    quiz_id: str
    subject_id: str
    answers: Dict[str, int]

class MockExamSubmission(BaseModel):
    exam_id: str
    subject_id: str
    answers: Dict[str, Any]
    time_taken_seconds: int

class TutorQuery(BaseModel):
    subject_id: str
    query: str
    context_topic: Optional[str] = None
    question_id: Optional[str] = None
