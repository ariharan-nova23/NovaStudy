import re
import uuid
from typing import List, Dict, Any

from backend.services.ai_service import ai_service


class QuestionExtractorService:

    @staticmethod
    def extract_questions_from_text(
        raw_text: str,
        paper_year: int = 2025,
        syllabus: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:

        # AI mode when available
        if ai_service.enabled:
            syllabus_text = syllabus if syllabus else "No official syllabus available."

            prompt = f"""
You are an examination question extraction and syllabus mapping system.

Extract ONLY actual examination questions.

IMPORTANT:
- Ignore lecture notes, textbook explanations, examples, solved examples,
  headings, page numbers, advertisements, and study material.
- Do NOT treat lecture examples as exam questions.
- Do NOT invent questions.
- Preserve original question wording.
- Identify the actual subject from the content.
- If a question is not clearly an exam question, exclude it.
- Use only syllabus topics when a syllabus is supplied.
- Return JSON only.

SYLLABUS:
{syllabus_text}

QUESTION PAPER TEXT:
{raw_text}

Return:
{{
  "questions": [
    {{
      "question": "...",
      "year": {paper_year},
      "marks": 2,
      "unit": "...",
      "topic": "...",
      "subtopic": "...",
      "question_type": "...",
      "difficulty": "Easy/Medium/Hard",
      "confidence": 0.0,
      "needs_review": false
    }}
  ]
}}
"""

            result = ai_service.ask_json(prompt)

            if result and isinstance(result.get("questions"), list):
                return QuestionExtractorService._clean_questions(
                    result["questions"],
                    paper_year
                )

        # Local fallback
        return QuestionExtractorService._heuristic(
            raw_text,
            paper_year
        )

    @staticmethod
    def _clean_questions(
        questions: List[Dict[str, Any]],
        year: int
    ) -> List[Dict[str, Any]]:

        cleaned = []

        for q in questions:
            question = str(q.get("question", "")).strip()

            if not QuestionExtractorService._looks_like_question(question):
                continue

            try:
                marks = int(q.get("marks", 2))
            except Exception:
                marks = 2

            if marks <= 0 or marks > 20:
                marks = 2

            cleaned.append({
                "id": q.get(
                    "id",
                    f"extracted_{uuid.uuid4().hex[:8]}"
                ),
                "question": question,
                "year": q.get("year", year),
                "marks": marks,
                "unit": q.get("unit", "Needs Review"),
                "topic": q.get("topic", "Needs Review"),
                "subtopic": q.get("subtopic", "Unassigned"),
                "question_type": q.get(
                    "question_type",
                    "Explanation"
                ),
                "difficulty": q.get(
                    "difficulty",
                    "Medium"
                ),
                "confidence": float(
                    q.get("confidence", 0.6)
                ),
                "needs_review": bool(
                    q.get("needs_review", False)
                )
            })

        return cleaned

    @staticmethod
    def _heuristic(
        raw_text: str,
        year: int
    ) -> List[Dict[str, Any]]:

        # Clean OCR noise
        text = raw_text.replace("\x00", " ")
        text = re.sub(r"\s+", " ", text)

        # Split into possible question blocks.
        # Supports:
        # 1.
        # 1)
        # Q1
        # Q.1
        # Question 1
        pattern = re.compile(
            r"(?=(?:Question\s*)?(?:Q\.?\s*)?\d+\s*[\.)\:])",
            re.IGNORECASE
        )

        blocks = pattern.split(text)

        questions = []

        for block in blocks:
            block = block.strip()

            if len(block) < 15:
                continue

            # Remove obvious page / lecture-note material
            if QuestionExtractorService._is_non_exam_content(block):
                continue

            # Must look like an actual question
            if not QuestionExtractorService._looks_like_question(block):
                continue

            marks = QuestionExtractorService._detect_marks(block)

            structured = QuestionExtractorService._structure(
                block,
                year,
                marks
            )

            questions.append(structured)

        return questions

    @staticmethod
    def _detect_marks(text: str) -> int:

        # Look for explicit marks near the end of the question
        patterns = [
            r"\(\s*(\d+)\s*marks?\s*\)",
            r"\[\s*(\d+)\s*marks?\s*\]",
            r"(\d+)\s*marks?\s*$",
            r"[-–]\s*(\d+)\s*$"
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                marks = int(match.group(1))

                if 1 <= marks <= 20:
                    return marks

        # Safe default
        return 2

    @staticmethod
    def _looks_like_question(text: str) -> bool:

        low = text.lower().strip()

        # Reject obvious lecture/study material
        bad_phrases = [
            "lecture -",
            "lecture –",
            "lecture:",
            "quick memory trick",
            "example:",
            "example ",
            "solution:",
            "solution ",
            "consistency check:",
            "conclusion:",
            "statement name of the law",
            "chapter ",
            "contents",
            "references",
            "bibliography"
        ]

        if any(x in low for x in bad_phrases):
            return False

        # Strong question indicators
        question_words = [
            "which",
            "what",
            "find",
            "determine",
            "prove",
            "show",
            "state",
            "define",
            "construct",
            "calculate",
            "solve",
            "verify",
            "express",
            "rewrite",
            "translate",
            "establish",
            "derive",
            "explain",
            "compare",
            "differentiate"
        ]

        if any(
            re.search(r"\b" + re.escape(word) + r"\b", low)
            for word in question_words
        ):
            return True

        # Mathematical notation often survives OCR
        math_indicators = [
            "proposition",
            "truth table",
            "tautology",
            "contradiction",
            "predicate",
            "quantifier",
            "relation",
            "function",
            "permutation",
            "combination",
            "graph",
            "recurrence",
            "set",
            "subset"
        ]

        return any(x in low for x in math_indicators)

    @staticmethod
    def _is_non_exam_content(text: str) -> bool:

        low = text.lower()

        # These are strong indicators that the PDF is lecture material
        lecture_indicators = [
            "lecture -",
            "lecture –",
            "quick memory trick",
            "example 1:",
            "example 2:",
            "example:",
            "solution:",
            "consistency check:",
            "conclusion:",
            "statement name of the law",
            "logical equivalences and examples",
            "compound propositions"
        ]

        matches = sum(
            1 for x in lecture_indicators
            if x in low
        )

        # If several lecture indicators occur,
        # don't treat the block as an exam question.
        return matches >= 2

    @staticmethod
    def _structure(
        text: str,
        year: int,
        marks: int
    ) -> Dict[str, Any]:

        low = text.lower()

        # ---------------------------------------------------------
        # MATHEMATICS — LOGIC
        # ---------------------------------------------------------

        if any(x in low for x in [
            "proposition",
            "truth table",
            "tautology",
            "contradiction",
            "logical equivalence",
            "logical connective",
            "biconditional",
            "conditional statement",
            "converse",
            "contrapositive",
            "inverse"
        ]):

            topic = "Logic and Propositions"

            if any(x in low for x in [
                "quantifier",
                "predicate",
                "domain",
                "∀",
                "∃",
                "nested quantification",
                "negation"
            ]):
                topic = "Predicates and Quantifiers"
                subtopic = "Predicates, Quantifiers and Negation"

            elif any(x in low for x in [
                "truth table",
                "tautology",
                "logical equivalence"
            ]):
                subtopic = "Truth Tables and Logical Equivalence"

            elif any(x in low for x in [
                "converse",
                "contrapositive",
                "inverse",
                "conditional"
            ]):
                subtopic = "Conditional and Biconditional Statements"

            else:
                subtopic = "Propositions and Logical Connectives"

            unit = "Unit 1"

        # ---------------------------------------------------------
        # SET THEORY
        # ---------------------------------------------------------

        elif any(x in low for x in [
            "set",
            "subset",
            "union",
            "intersection",
            "cartesian product",
            "power set",
            "venn diagram"
        ]):

            unit = "Unit 1"
            topic = "Set Theory"
            subtopic = "Sets and Set Operations"

        # ---------------------------------------------------------
        # RELATIONS
        # ---------------------------------------------------------

        elif any(x in low for x in [
            "relation",
            "equivalence relation",
            "reflexive",
            "symmetric",
            "transitive",
            "antisymmetric"
        ]):

            unit = "Unit 2"
            topic = "Relations"
            subtopic = "Properties of Relations"

        # ---------------------------------------------------------
        # FUNCTIONS
        # ---------------------------------------------------------

        elif any(x in low for x in [
            "function",
            "injective",
            "surjective",
            "bijective",
            "one-to-one",
            "onto"
        ]):

            unit = "Unit 2"
            topic = "Functions"
            subtopic = "Types of Functions"

        # ---------------------------------------------------------
        # COMBINATORICS
        # ---------------------------------------------------------

        elif any(x in low for x in [
            "permutation",
            "combination",
            "binomial coefficient",
            "counting principle",
            "pigeonhole"
        ]):

            unit = "Unit 3"
            topic = "Combinatorics"
            subtopic = "Permutations, Combinations and Counting"

        # ---------------------------------------------------------
        # GRAPH THEORY
        # ---------------------------------------------------------

        elif any(x in low for x in [
            "graph",
            "vertex",
            "vertices",
            "edge",
            "degree",
            "euler",
            "hamilton",
            "connected graph"
        ]):

            unit = "Unit 4"
            topic = "Graph Theory"
            subtopic = "Graphs and Graph Properties"

        # ---------------------------------------------------------
        # RECURRENCE
        # ---------------------------------------------------------

        elif any(x in low for x in [
            "recurrence",
            "recurrence relation"
        ]):

            unit = "Unit 5"
            topic = "Recurrence Relations"
            subtopic = "Solving Recurrence Relations"

        else:
            unit = "Needs Review"
            topic = "Needs Review"
            subtopic = "Unassigned"

        # ---------------------------------------------------------
        # DIFFICULTY
        # ---------------------------------------------------------

        if marks <= 2:
            difficulty = "Easy"
        elif marks <= 10:
            difficulty = "Medium"
        else:
            difficulty = "Hard"

        # ---------------------------------------------------------
        # QUESTION TYPE
        # ---------------------------------------------------------

        if any(x in low for x in [
            "define",
            "what is",
            "state"
        ]):
            question_type = "Definition"

        elif any(x in low for x in [
            "prove",
            "show that",
            "verify",
            "disprove",
            "counterexample"
        ]):
            question_type = "Proof"

        elif any(x in low for x in [
            "derive",
            "derivation"
        ]):
            question_type = "Derivation"

        elif any(x in low for x in [
            "calculate",
            "determine",
            "solve",
            "find"
        ]):
            question_type = "Numerical"

        elif any(x in low for x in [
            "compare",
            "differentiate",
            "difference between"
        ]):
            question_type = "Comparison"

        else:
            question_type = "Explanation"

        needs_review = topic == "Needs Review"

        return {
            "id": f"extracted_{uuid.uuid4().hex[:8]}",
            "question": text,
            "year": year,
            "marks": marks,
            "unit": unit,
            "topic": topic,
            "subtopic": subtopic,
            "question_type": question_type,
            "difficulty": difficulty,
            "confidence": 0.85 if not needs_review else 0.3,
            "needs_review": needs_review
        }


question_extractor_service = QuestionExtractorService()