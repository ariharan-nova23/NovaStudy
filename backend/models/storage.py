import json
import os
from typing import Dict, Any, List
from backend.config import DATA_DIR
from backend.data.sample_data import SAMPLE_SYLLABI, SAMPLE_QUESTIONS

class StorageEngine:
    def __init__(self):
        self.subjects_file = os.path.join(DATA_DIR, "subjects.json")
        self.questions_file = os.path.join(DATA_DIR, "questions.json")
        self.syllabi_file = os.path.join(DATA_DIR, "syllabi.json")
        self.quiz_history_file = os.path.join(DATA_DIR, "quiz_history.json")
        self.study_plans_file = os.path.join(DATA_DIR, "study_plans.json")
        self._ensure_initial_data()

    def _ensure_initial_data(self):
        if not os.path.exists(self.syllabi_file):
            with open(self.syllabi_file, "w") as f:
                json.dump(SAMPLE_SYLLABI, f, indent=2)

        if not os.path.exists(self.questions_file):
            with open(self.questions_file, "w") as f:
                json.dump(SAMPLE_QUESTIONS, f, indent=2)

        if not os.path.exists(self.subjects_file):
            subjects = [
                {"id": "dsa", "name": "Data Structures & Algorithms", "exam_days": 12, "preparation": 68},
                {"id": "os", "name": "Operating Systems", "exam_days": 18, "preparation": 55}
            ]
            with open(self.subjects_file, "w") as f:
                json.dump(subjects, f, indent=2)

        if not os.path.exists(self.quiz_history_file):
            sample_history = [
                {"id": "qhist_1", "subject_id": "dsa", "score": 8, "total": 10, "date": "2026-08-25", "quiz_type": "Quick Quiz"},
                {"id": "qhist_2", "subject_id": "dsa", "score": 9, "total": 10, "date": "2026-08-28", "quiz_type": "Topic Quiz - Graphs"}
            ]
            with open(self.quiz_history_file, "w") as f:
                json.dump(sample_history, f, indent=2)

    def get_subjects(self) -> List[Dict[str, Any]]:
        with open(self.subjects_file, "r") as f:
            return json.load(f)

    def get_syllabi(self) -> Dict[str, Any]:
        with open(self.syllabi_file, "r") as f:
            return json.load(f)

    def get_syllabus(self, subject_id: str) -> Dict[str, Any]:
        syllabi = self.get_syllabi()
        return syllabi.get(subject_id, syllabi.get("dsa"))

    def get_questions(self, subject_id: str) -> List[Dict[str, Any]]:
        with open(self.questions_file, "r") as f:
            all_q = json.load(f)
            return all_q.get(subject_id, all_q.get("dsa", []))

    def add_question(self, subject_id: str, question_dict: Dict[str, Any]):
        with open(self.questions_file, "r") as f:
            all_q = json.load(f)
        if subject_id not in all_q:
            all_q[subject_id] = []
        all_q[subject_id].append(question_dict)
        with open(self.questions_file, "w") as f:
            json.dump(all_q, f, indent=2)

    def save_quiz_history(self, quiz_result: Dict[str, Any]):
        with open(self.quiz_history_file, "r") as f:
            history = json.load(f)
        history.append(quiz_result)
        with open(self.quiz_history_file, "w") as f:
            json.dump(history, f, indent=2)

    def get_quiz_history(self, subject_id: str) -> List[Dict[str, Any]]:
        with open(self.quiz_history_file, "r") as f:
            history = json.load(f)
            return [h for h in history if h.get("subject_id") == subject_id]

storage = StorageEngine()
