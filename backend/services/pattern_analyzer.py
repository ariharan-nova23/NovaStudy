from typing import List, Dict, Any
from collections import Counter

class PatternAnalyzerService:
    @staticmethod
    def analyze_patterns(questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_q = len(questions)
        if total_q == 0:
            return {
                "unit_distribution": {},
                "marks_distribution": {},
                "question_type_distribution": {},
                "difficulty_distribution": {}
            }

        unit_counter = Counter(q.get("unit", "Unit 1") for q in questions)
        marks_counter = Counter(f"{q.get('marks', 10)} Marks" for q in questions)
        type_counter = Counter(q.get("question_type", "Explanation") for q in questions)
        diff_counter = Counter(q.get("difficulty", "Medium") for q in questions)

        unit_dist = {u: round((count / total_q) * 100, 1) for u, count in unit_counter.items()}
        marks_dist = dict(marks_counter)
        type_dist = dict(type_counter)
        diff_dist = dict(diff_counter)

        return {
            "unit_distribution": unit_dist,
            "marks_distribution": marks_dist,
            "question_type_distribution": type_dist,
            "difficulty_distribution": diff_dist
        }

pattern_analyzer_service = PatternAnalyzerService()
