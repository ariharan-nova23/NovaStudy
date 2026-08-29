import re, uuid
from typing import List, Dict, Any
from backend.services.syllabus_mapper import syllabus_mapper_service
from backend.services.ai_service import ai_service

class QuestionExtractorService:
    @staticmethod
    def extract_questions_from_text(raw_text: str, paper_year: int = 2025, syllabus: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if ai_service.enabled and syllabus:
            prompt = f'''Extract all exam questions from this paper and map them only to the supplied syllabus. Return JSON only as {{"questions":[...]}}. Each question must have id, question, year, marks, unit, topic, subtopic, question_type, difficulty, confidence, needs_review. Do not invent questions.\nSYLLABUS:\n{syllabus}\nPAPER:\n{raw_text}'''
            result = ai_service.ask_json(prompt)
            if result and isinstance(result.get("questions"), list):
                return result["questions"]
        return QuestionExtractorService._heuristic(raw_text, paper_year, syllabus or {})

    @staticmethod
    def _heuristic(raw_text, year, syllabus):
        lines = [re.sub(r"\s+", " ", x.strip()) for x in raw_text.splitlines() if x.strip()]
        questions=[]; buf=[]; current_marks=2
        q_start = re.compile(r"^(?:Q(?:uestion)?\s*\d+|\d+\s*[.)]|[A-Z]\d+\s*[.)])", re.I)
        for line in lines:
            mm = re.search(r"(?:\(|\[)?\s*(\d+)\s*(?:marks?|M)\s*(?:\)|\])?", line, re.I)
            if mm: current_marks=int(mm.group(1))
            if q_start.match(line):
                if buf: questions.append(QuestionExtractorService._structure(" ".join(buf), year, current_marks, syllabus))
                buf=[line]
            elif buf: buf.append(line)
        if buf: questions.append(QuestionExtractorService._structure(" ".join(buf), year, current_marks, syllabus))
        return [q for q in questions if len(q["question"]) > 8]

    @staticmethod
    def _structure(text, year, marks, syllabus):
        low=text.lower()
        if any(x in low for x in ["differentiate", "compare", " vs "]): typ="Comparison"
        elif any(x in low for x in ["algorithm", "bfs", "dfs", "dijkstra", "kruskal", "prim"]): typ="Algorithm"
        elif any(x in low for x in ["trace", "calculate", "construct", "convert"]): typ="Numerical"
        elif any(x in low for x in ["write a", "write c", "write a c", "function", "program"]): typ="Programming"
        elif any(x in low for x in ["define", "what is"]): typ="Definition"
        elif "derive" in low: typ="Derivation"
        elif "diagram" in low: typ="Diagram"
        else: typ="Explanation"
        mapped=syllabus_mapper_service.map_question(text, syllabus) if syllabus else {"unit":"Needs Review","topic":"Needs Review","subtopic":"Unassigned","confidence":0.3,"needs_review":True}
        difficulty="Easy" if marks <= 2 else ("Medium" if marks <= 10 else "Hard")
        return {"id":f"extracted_{uuid.uuid4().hex[:8]}","question":text,"year":year,"marks":marks,
                "unit":mapped["unit"],"topic":mapped["topic"],"subtopic":mapped["subtopic"],
                "question_type":typ,"difficulty":difficulty,"confidence":mapped["confidence"],"needs_review":mapped["needs_review"]}

question_extractor_service=QuestionExtractorService()
