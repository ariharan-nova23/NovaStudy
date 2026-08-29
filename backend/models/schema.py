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
    question_type: str  # Definition, Explanation, Comparison, Numerical, Derivation, Algorithm, Programming, Diagram, Application, Case study
    difficulty: str     # Easy, Medium, Hard
    confidence: float = 1.0
    needs_review: bool = False

class SyllabusSubtopic(BaseModel):
    name: str

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

class QuestionPaperUploadResponse(BaseModel):
    paper_id: str
    subject_id: str
    year: int
    title: str
    extracted_questions_count: int
    questions: List[QuestionSchema]

class PatternAnalysisResponse(BaseModel):
    subject_id: str
    total_papers: int
    total_questions: int
    unit_distribution: Dict[str, float]
    marks_distribution: Dict[str, int]
    question_type_distribution: Dict[str, int]
    difficulty_distribution: Dict[str, int]

class RepeatedQuestionGroup(BaseModel):
    concept: str
    topic: str
    unit: str
    appeared_in_years: List[int]
    frequency: int
    total_papers: int
    total_marks: int
    trend: str  # Increasing, Stable, Decreasing
    priority: str  # Very High, High, Medium, Low
    questions: List[QuestionSchema]

class TopicPriorityScore(BaseModel):
    topic: str
    unit: str
    priority_score: int
    priority_label: str  # Critical, High, Medium, Low
    frequency_score: float
    marks_weight: float
    trend: str
    rationale: str

class PredictionResponse(BaseModel):
    subject_id: str
    important_topics: List[TopicPriorityScore]
    likely_question_types: Dict[str, str]
    frequently_repeated_concepts: List[RepeatedQuestionGroup]
    disclaimer: str

class ModelPaperConfig(BaseModel):
    subject_id: str
    total_marks: int = 100
    duration_minutes: int = 180
    difficulty_mode: str = "Balanced"  # Balanced, High-Priority Topics, University Pattern, Hard Practice, Surprise Practice
    num_questions: int = 10
    num_previous_papers_considered: int = 4

class ModelPaperValidationItem(BaseModel):
    check_name: str
    passed: bool
    details: str

class ModelQuestionPaper(BaseModel):
    paper_id: str
    subject_name: str
    total_marks: int
    duration_minutes: int
    difficulty_mode: str
    validation_status: bool
    validation_checks: List[ModelPaperValidationItem]
    sections: List[Dict[str, Any]]
    instructions: List[str]

class QuizConfig(BaseModel):
    subject_id: str
    quiz_mode: str  # Quick Quiz, Topic Quiz, Unit Quiz, Important Topics Quiz, Previous Paper Quiz, Adaptive Quiz, Full Mock Quiz
    num_questions: int = 10
    difficulty: str = "Adaptive"  # Easy, Medium, Hard, Adaptive
    target_topic: Optional[str] = None
    target_unit: Optional[str] = None

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer_index: int
    explanation: str
    hint: Optional[str] = None
    topic: str
    unit: str
    difficulty: str
    marks: int = 1

class QuizSubmission(BaseModel):
    quiz_id: str
    subject_id: str
    answers: Dict[str, int]  # question_id -> selected_option_index

class QuizResult(BaseModel):
    quiz_id: str
    score: int
    total_questions: int
    percentage: float
    accuracy: float
    strong_areas: List[str]
    weak_areas: List[str]
    topics_to_revise: List[str]
    question_evaluations: List[Dict[str, Any]]

class MockExamSubmission(BaseModel):
    exam_id: str
    subject_id: str
    answers: Dict[str, Any]  # question_id -> option or text response
    time_taken_seconds: int

class StudyPlanDay(BaseModel):
    day: int
    date_str: str
    focus_topic: str
    unit: str
    tasks: List[str]
    completed_tasks: List[str] = []
    estimated_hours: float

class StudyPlan(BaseModel):
    subject_id: str
    subject_name: str
    days_left: int
    daily_hours: float
    total_days: int
    schedule: List[StudyPlanDay]
    completion_percentage: float

class TutorQuery(BaseModel):
    subject_id: str
    query: str
    context_topic: Optional[str] = None
    question_id: Optional[str] = None

class TutorResponse(BaseModel):
    answer: str
    related_topics: List[str]
    suggested_questions: List[str]
