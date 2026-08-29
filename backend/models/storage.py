import json
import os
import uuid
from datetime import date
from pathlib import Path
from typing import Dict, Any, List
from backend.config import DATA_DIR

class StorageEngine:
    def __init__(self):
        self.subjects_file = DATA_DIR / "subjects.json"
        self.questions_file = DATA_DIR / "questions.json"
        self.syllabi_file = DATA_DIR / "syllabi.json"
        self.quiz_history_file = DATA_DIR / "quiz_history.json"
        self.papers_file = DATA_DIR / "papers.json"
        self.generated_file = DATA_DIR / "generated_papers.json"
        self.quizzes_file = DATA_DIR / "quizzes.json"
        self.study_plans_file = DATA_DIR / "study_plans.json"
        self._ensure_files()

    def _ensure_files(self):
        defaults = {
            self.subjects_file: [], self.questions_file: {}, self.syllabi_file: {},
            self.quiz_history_file: [], self.papers_file: [], self.generated_file: [],
            self.quizzes_file: {}, self.study_plans_file: {}
        }
        for path, default in defaults.items():
            if not path.exists():
                self._write(path, default)

    def _read(self, path, default):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return default

    def _write(self, path, data):
        tmp = Path(str(path) + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)

    def get_subjects(self): return self._read(self.subjects_file, [])
    def get_syllabi(self): return self._read(self.syllabi_file, {})
    def get_syllabus(self, subject_id): return self.get_syllabi().get(subject_id)
    def get_questions(self, subject_id): return self._read(self.questions_file, {}).get(subject_id, [])

    def save_syllabus(self, subject_id, syllabus):
        all_syllabi = self.get_syllabi(); all_syllabi[subject_id] = syllabus
        self._write(self.syllabi_file, all_syllabi)

    def add_paper(self, subject_id, year, title, filename, question_count):
        papers = self._read(self.papers_file, [])
        paper = {"id": f"paper_{uuid.uuid4().hex[:10]}", "subject_id": subject_id, "year": year,
                 "title": title, "filename": filename, "question_count": question_count,
                 "uploaded_at": date.today().isoformat()}
        papers.append(paper); self._write(self.papers_file, papers); return paper

    def add_questions(self, subject_id, questions):
        all_q = self._read(self.questions_file, {})
        all_q.setdefault(subject_id, []).extend(questions)
        self._write(self.questions_file, all_q)

    def get_papers(self, subject_id):
        return [p for p in self._read(self.papers_file, []) if p.get("subject_id") == subject_id]

    def save_quiz(self, quiz):
        quizzes = self._read(self.quizzes_file, {}); quizzes[quiz["quiz_id"]] = quiz
        self._write(self.quizzes_file, quizzes)

    def get_quiz(self, quiz_id): return self._read(self.quizzes_file, {}).get(quiz_id)

    def save_quiz_history(self, result):
        history = self._read(self.quiz_history_file, []); history.append(result)
        self._write(self.quiz_history_file, history)

    def get_quiz_history(self, subject_id):
        return [h for h in self._read(self.quiz_history_file, []) if h.get("subject_id") == subject_id]

    def save_generated_paper(self, paper):
        papers = self._read(self.generated_file, []); papers.append(paper)
        self._write(self.generated_file, papers)

    def save_study_plan(self, subject_id, plan):
        plans = self._read(self.study_plans_file, {}); plans[subject_id] = plan
        self._write(self.study_plans_file, plans)

storage = StorageEngine()
