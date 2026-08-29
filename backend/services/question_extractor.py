import re
import uuid
from typing import List, Dict, Any

class QuestionExtractorService:
    @staticmethod
    def extract_questions_from_text(raw_text: str, paper_year: int = 2025) -> List[Dict[str, Any]]:
        """
        Converts raw question paper text into structured JSON question objects.
        """
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
        questions = []

        q_buffer = []
        current_marks = 10

        for line in lines:
            # Check for marks pattern like (10 Marks), [5M], 10 marks
            marks_match = re.search(r'\(?(\d+)\s*(?:Marks|marks|M|m)\)?', line)
            if marks_match:
                current_marks = int(marks_match.group(1))

            if re.match(r'^(?:Q\d+|Question\d+|\d+[\.\)])', line, re.IGNORECASE):
                if q_buffer:
                    full_q = " ".join(q_buffer)
                    questions.append(QuestionExtractorService._structure_question(full_q, paper_year, current_marks))
                    q_buffer = []
                q_buffer.append(line)
            else:
                if q_buffer:
                    q_buffer.append(line)

        if q_buffer:
            full_q = " ".join(q_buffer)
            questions.append(QuestionExtractorService._structure_question(full_q, paper_year, current_marks))

        # Fallback if no questions detected
        if not questions:
            questions.append(QuestionExtractorService._structure_question(
                f"Explain the core concept described in paper: {raw_text[:80]}...", paper_year, 10
            ))

        return questions

    @staticmethod
    def _structure_question(q_text: str, year: int, marks: int) -> Dict[str, Any]:
        text_lower = q_text.lower()
        
        # Determine Question Type
        if "explain" in text_lower or "describe" in text_lower:
            q_type = "Explanation"
        elif "differentiate" in text_lower or "compare" in text_lower or "vs" in text_lower:
            q_type = "Comparison"
        elif "algorithm" in text_lower or "bfs" in text_lower or "dfs" in text_lower:
            q_type = "Algorithm"
        elif "trace" in text_lower or "calculate" in text_lower or "construct" in text_lower or "convert" in text_lower:
            q_type = "Numerical"
        elif "write a" in text_lower or "function" in text_lower or "program" in text_lower:
            q_type = "Programming"
        elif "define" in text_lower or "what is" in text_lower:
            q_type = "Definition"
        elif "derive" in text_lower:
            q_type = "Derivation"
        else:
            q_type = "Application"

        # Determine Topic & Unit
        if "bfs" in text_lower or "dfs" in text_lower or "graph" in text_lower:
            unit = "Unit 4"
            topic = "Graph Traversal"
            subtopic = "BFS" if "bfs" in text_lower else "DFS"
            difficulty = "Medium"
        elif "tree" in text_lower or "avl" in text_lower or "bst" in text_lower:
            unit = "Unit 3"
            topic = "Balanced Trees" if "avl" in text_lower else "Binary Search Trees"
            subtopic = "AVL Trees & Rotations" if "avl" in text_lower else "BST"
            difficulty = "Hard" if "avl" in text_lower else "Medium"
        elif "sort" in text_lower or "quick" in text_lower or "merge" in text_lower:
            unit = "Unit 5"
            topic = "Sorting Algorithms"
            subtopic = "Quick Sort" if "quick" in text_lower else "Merge Sort"
            difficulty = "Medium"
        elif "stack" in text_lower or "queue" in text_lower:
            unit = "Unit 1"
            topic = "Stacks" if "stack" in text_lower else "Queues"
            subtopic = "Infix to Postfix" if "infix" in text_lower else "Linear Queue"
            difficulty = "Easy" if marks <= 5 else "Medium"
        else:
            unit = "Unit 2"
            topic = "Linked Lists"
            subtopic = "General"
            difficulty = "Medium"

        return {
            "id": f"extracted_{uuid.uuid4().hex[:8]}",
            "question": q_text,
            "year": year,
            "marks": marks,
            "unit": unit,
            "topic": topic,
            "subtopic": subtopic,
            "question_type": q_type,
            "difficulty": difficulty,
            "confidence": 0.92,
            "needs_review": False
        }

question_extractor_service = QuestionExtractorService()
