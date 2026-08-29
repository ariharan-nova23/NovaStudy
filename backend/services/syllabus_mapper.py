from typing import Dict, Any, List

class SyllabusMapperService:
    @staticmethod
    def map_question(question_text: str, syllabus: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps a question to syllabus unit, topic, and subtopic based on keyword alignment.
        If mapping is ambiguous (confidence < 0.6), marks as 'Needs Review'.
        """
        text_lower = question_text.lower()
        best_match = None
        highest_score = 0

        for unit_item in syllabus.get("units", []):
            unit_name = unit_item.get("unit", "Unit 1")
            for topic_item in unit_item.get("topics", []):
                topic_name = topic_item.get("name", "")
                subtopics = topic_item.get("subtopics", [])

                score = 0
                for word in topic_name.lower().split():
                    if len(word) > 3 and word in text_lower:
                        score += 2

                for sub in subtopics:
                    for sub_word in sub.lower().split():
                        if len(sub_word) > 3 and sub_word in text_lower:
                            score += 3

                if score > highest_score:
                    highest_score = score
                    best_match = {
                        "unit": unit_name,
                        "topic": topic_name,
                        "subtopic": subtopics[0] if subtopics else topic_name,
                        "confidence": min(1.0, 0.4 + score * 0.15),
                        "needs_review": False
                    }

        if not best_match or highest_score == 0:
            return {
                "unit": "Unit 1 (Unassigned)",
                "topic": "Needs Review",
                "subtopic": "Unassigned",
                "confidence": 0.35,
                "needs_review": True
            }

        return best_match

syllabus_mapper_service = SyllabusMapperService()
