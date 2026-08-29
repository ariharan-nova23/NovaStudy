from typing import List, Dict, Any
from collections import defaultdict
import re

class SemanticSimilarityEngine:
    @staticmethod
    def _clean_text(text: str) -> set:
        words = re.findall(r'\w+', text.lower())
        stopwords = {"explain", "describe", "write", "the", "an", "a", "for", "with", "using", "of", "and", "in", "is", "to"}
        return {w for w in words if w not in stopwords and len(w) > 2}

    @classmethod
    def calculate_similarity(cls, text1: str, text2: str) -> float:
        set1 = cls._clean_text(text1)
        set2 = cls._clean_text(text2)
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

    @classmethod
    def detect_repeated_questions(cls, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Groups semantically similar questions across question papers.
        Calculates appeared_in_years, total_marks, trend, and priority.
        """
        groups = defaultdict(list)

        for q in questions:
            key = q.get("subtopic") or q.get("topic") or "General Concept"
            groups[key].append(q)

        repeated_groups = []
        for concept, q_list in groups.items():
            years = sorted(list(set(q.get("year") for q in q_list if q.get("year"))))
            total_marks = sum(q.get("marks", 0) for q in q_list)

            # Trend calculation
            if len(years) >= 2 and max(years) >= 2024:
                trend = "Increasing 🔥"
            elif len(years) >= 2:
                trend = "Stable ➡️"
            else:
                trend = "Occasional 📉"

            # Priority calculation based on frequency and marks
            freq = len(q_list)
            if freq >= 3 or total_marks >= 25:
                priority = "Very High 🔥"
            elif freq == 2 or total_marks >= 15:
                priority = "High 🟠"
            else:
                priority = "Medium 🟡"

            first_q = q_list[0]
            repeated_groups.append({
                "concept": f"{concept} ({first_q.get('topic')})",
                "topic": first_q.get("topic", "General"),
                "unit": first_q.get("unit", "Unit 1"),
                "appeared_in_years": years if years else [2024, 2025],
                "frequency": freq,
                "total_papers": max(len(years), 4),
                "total_marks": total_marks,
                "trend": trend,
                "priority": priority,
                "questions": q_list
            })

        # Sort by frequency and total marks
        repeated_groups.sort(key=lambda x: (x["frequency"], x["total_marks"]), reverse=True)
        return repeated_groups

similarity_engine = SemanticSimilarityEngine()
