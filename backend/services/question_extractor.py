import re
import uuid
from typing import List, Dict, Any

from backend.services.syllabus_mapper import syllabus_mapper_service
from backend.services.ai_service import ai_service


class QuestionExtractorService:

    @staticmethod
    def extract_questions_from_text(
        raw_text: str,
        paper_year: int = 2025,
        syllabus: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:

        # ---------------------------------------------------------
        # MODE 1:
        # Syllabus exists → use AI to map questions to syllabus
        # ---------------------------------------------------------
        if ai_service.enabled and syllabus:

            prompt = f"""
Extract all exam questions from this question paper.

Map every question ONLY to the supplied syllabus.

Return JSON only in this format:

{{
  "questions": [
    {{
      "id": "unique_id",
      "question": "full question",
      "year": {paper_year},
      "marks": 2,
      "unit": "Unit 1",
      "topic": "Topic name",
      "subtopic": "Subtopic name",
      "question_type": "Numerical",
      "difficulty": "Easy",
      "confidence": 0.95,
      "needs_review": false
    }}
  ]
}}

Rules:

1. Extract only questions actually present in the paper.
2. Do not invent questions.
3. Do not invent syllabus topics.
4. Use the supplied syllabus for unit/topic/subtopic mapping.
5. If a question cannot confidently be mapped, set needs_review to true.
6. Preserve the original question wording as much as possible.
7. Estimate marks only when marks are visible or clearly inferable.
8. Return valid JSON only.

SYLLABUS:
{syllabus}

QUESTION PAPER:
{raw_text}
"""

            result = ai_service.ask_json(prompt)

            if result and isinstance(
                result.get("questions"),
                list
            ):
                return QuestionExtractorService._clean_questions(
                    result["questions"],
                    paper_year
                )


        # ---------------------------------------------------------
        # MODE 2:
        # No syllabus → AI discovers topics from the questions
        # ---------------------------------------------------------
        if ai_service.enabled and not syllabus:

            prompt = f"""
Analyze this exam question paper and extract every question.

There is NO syllabus available.

Therefore, discover the academic topics and subtopics directly
from the questions.

Return JSON only in this format:

{{
  "questions": [
    {{
      "id": "unique_id",
      "question": "full question",
      "year": {paper_year},
      "marks": 2,
      "unit": "Unit 1",
      "topic": "Discovered topic",
      "subtopic": "Discovered subtopic",
      "question_type": "Numerical",
      "difficulty": "Easy",
      "confidence": 0.90,
      "needs_review": false
    }}
  ]
}}

Rules:

1. Extract ONLY questions that actually appear in the paper.
2. Do NOT invent questions.
3. Do NOT invent an official syllabus.
4. Topics must be discovered from the actual question content.
5. Use meaningful academic topic names.
6. Group questions dealing with the same concept under the
   same topic/subtopic whenever appropriate.
7. If the paper clearly contains unit information, preserve it.
8. If unit information is not available, use:
   "Unit 1", "Unit 2", etc. only when supported by the paper.
9. If the unit cannot be determined, use:
   "Unknown Unit"
10. Do not assume that the subject is DSA.
11. The subject must be inferred from the actual question content.
12. If confidence is low, set needs_review to true.
13. question_type should describe the actual type of question.
14. difficulty should be Easy, Medium, or Hard.
15. Return valid JSON only.

QUESTION PAPER:
{raw_text}
"""

            result = ai_service.ask_json(prompt)

            if result and isinstance(
                result.get("questions"),
                list
            ):
                return QuestionExtractorService._clean_questions(
                    result["questions"],
                    paper_year
                )


        # ---------------------------------------------------------
        # MODE 3:
        # No AI → fallback heuristic extraction
        # ---------------------------------------------------------
        return QuestionExtractorService._heuristic(
            raw_text,
            paper_year,
            syllabus or {}
        )


    # =============================================================
    # CLEAN AI RESULTS
    # =============================================================

    @staticmethod
    def _clean_questions(
        questions: List[Dict[str, Any]],
        paper_year: int
    ) -> List[Dict[str, Any]]:

        cleaned = []

        for question in questions:

            if not isinstance(question, dict):
                continue

            text = str(
                question.get("question", "")
            ).strip()

            if len(text) <= 8:
                continue


            # Make sure every question has an ID
            question_id = question.get("id")

            if not question_id:
                question_id = (
                    f"extracted_"
                    f"{uuid.uuid4().hex[:8]}"
                )


            # Marks
            try:
                marks = int(
                    question.get(
                        "marks",
                        2
                    )
                )
            except (TypeError, ValueError):
                marks = 2


            # Difficulty
            difficulty = str(
                question.get(
                    "difficulty",
                    "Medium"
                )
            ).strip()

            if difficulty not in [
                "Easy",
                "Medium",
                "Hard"
            ]:
                difficulty = "Medium"


            # Confidence
            try:
                confidence = float(
                    question.get(
                        "confidence",
                        0.7
                    )
                )
            except (TypeError, ValueError):
                confidence = 0.7

            confidence = max(
                0.0,
                min(1.0, confidence)
            )


            # Topic information
            unit = str(
                question.get(
                    "unit",
                    "Unknown Unit"
                )
            ).strip()

            topic = str(
                question.get(
                    "topic",
                    "Unknown Topic"
                )
            ).strip()

            subtopic = str(
                question.get(
                    "subtopic",
                    "Unassigned"
                )
            ).strip()


            question_type = str(
                question.get(
                    "question_type",
                    "Explanation"
                )
            ).strip()


            needs_review = bool(
                question.get(
                    "needs_review",
                    confidence < 0.6
                )
            )


            cleaned.append({

                "id": question_id,

                "question": text,

                "year": question.get(
                    "year",
                    paper_year
                ),

                "marks": marks,

                "unit": unit,

                "topic": topic,

                "subtopic": subtopic,

                "question_type": question_type,

                "difficulty": difficulty,

                "confidence": confidence,

                "needs_review": needs_review
            })


        return cleaned


    # =============================================================
    # HEURISTIC EXTRACTION
    # =============================================================

    @staticmethod
    def _heuristic(
        raw_text,
        year,
        syllabus
    ):

        lines = [
            re.sub(
                r"\s+",
                " ",
                x.strip()
            )
            for x in raw_text.splitlines()
            if x.strip()
        ]


        questions = []
        buf = []
        current_marks = 2


        q_start = re.compile(
            r"^(?:"
            r"Q(?:uestion)?\s*\d+"
            r"|\d+\s*[.)]"
            r"|[A-Z]\d+\s*[.)]"
            r")",
            re.I
        )


        for line in lines:

            mm = re.search(
                r"(?:\(|\[)?\s*"
                r"(\d+)"
                r"\s*(?:marks?|M)"
                r"\s*(?:\)|\])?",
                line,
                re.I
            )


            if mm:
                current_marks = int(
                    mm.group(1)
                )


            if q_start.match(line):

                if buf:

                    questions.append(
                        QuestionExtractorService._structure(
                            " ".join(buf),
                            year,
                            current_marks,
                            syllabus
                        )
                    )

                buf = [line]

            elif buf:

                buf.append(line)


        if buf:

            questions.append(
                QuestionExtractorService._structure(
                    " ".join(buf),
                    year,
                    current_marks,
                    syllabus
                )
            )


        return [
            q
            for q in questions
            if len(q["question"]) > 8
        ]


    # =============================================================
    # STRUCTURE INDIVIDUAL QUESTION
    # =============================================================

    @staticmethod
    def _structure(
        text,
        year,
        marks,
        syllabus
    ):

        low = text.lower()


        # ---------------------------------------------------------
        # Question type
        # ---------------------------------------------------------

        if any(
            x in low
            for x in [
                "differentiate",
                "compare",
                " vs ",
                "difference between"
            ]
        ):

            typ = "Comparison"


        elif any(
            x in low
            for x in [
                "algorithm",
                "bfs",
                "dfs",
                "dijkstra",
                "kruskal",
                "prim"
            ]
        ):

            typ = "Algorithm"


        elif any(
            x in low
            for x in [
                "trace",
                "calculate",
                "construct",
                "convert",
                "find",
                "solve",
                "evaluate"
            ]
        ):

            typ = "Numerical"


        elif any(
            x in low
            for x in [
                "write a",
                "write c",
                "write a c",
                "function",
                "program"
            ]
        ):

            typ = "Programming"


        elif any(
            x in low
            for x in [
                "define",
                "what is",
                "state"
            ]
        ):

            typ = "Definition"


        elif any(
            x in low
            for x in [
                "derive",
                "prove",
                "show that"
            ]
        ):

            typ = "Derivation"


        elif "diagram" in low:

            typ = "Diagram"


        else:

            typ = "Explanation"


        # ---------------------------------------------------------
        # Topic mapping
        # ---------------------------------------------------------

        if syllabus:

            mapped = (
                syllabus_mapper_service
                .map_question(
                    text,
                    syllabus
                )
            )

        else:

            mapped = {
                "unit": "Unknown Unit",
                "topic": "Unknown Topic",
                "subtopic": "Unassigned",
                "confidence": 0.3,
                "needs_review": True
            }


        # ---------------------------------------------------------
        # Difficulty
        # ---------------------------------------------------------

        if marks <= 2:

            difficulty = "Easy"

        elif marks <= 10:

            difficulty = "Medium"

        else:

            difficulty = "Hard"


        return {

            "id":
                f"extracted_"
                f"{uuid.uuid4().hex[:8]}",

            "question":
                text,

            "year":
                year,

            "marks":
                marks,

            "unit":
                mapped["unit"],

            "topic":
                mapped["topic"],

            "subtopic":
                mapped["subtopic"],

            "question_type":
                typ,

            "difficulty":
                difficulty,

            "confidence":
                mapped["confidence"],

            "needs_review":
                mapped["needs_review"]
        }


question_extractor_service = (
    QuestionExtractorService()
)