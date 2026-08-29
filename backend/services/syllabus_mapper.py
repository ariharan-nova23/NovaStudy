from typing import Dict, Any
import re

class SyllabusMapperService:
    @staticmethod
    def map_question(question_text: str, syllabus: Dict[str, Any]) -> Dict[str, Any]:
        text = question_text.lower()
        best = None; best_score = 0
        aliases = {
            "breadth first search (bfs)": ["bfs", "breadth first search"],
            "depth first search (dfs)": ["dfs", "depth first search"],
            "avl trees & rotations": ["avl", "rotation", "ll", "rr", "lr", "rl"],
            "binary search trees": ["bst", "binary search tree"],
            "dijkstra's algorithm": ["dijkstra"],
            "kruskal's algorithm": ["kruskal"],
            "prim's algorithm": ["prim"],
            "quick sort": ["quick sort", "quicksort"],
            "merge sort": ["merge sort", "mergesort"],
            "infix to postfix": ["infix", "postfix"],
            "circular queue": ["circular queue"],
            "reversal": ["reverse", "reversal"],
            "collision resolution": ["collision", "chaining", "linear probing", "open addressing"],
        }
        for unit in syllabus.get("units", []):
            for topic in unit.get("topics", []):
                score = 0; matched = []
                for phrase in [topic.get("name", "")] + topic.get("subtopics", []):
                    phrase_low=phrase.lower()
                    alias_hits=sum(1 for alias in aliases.get(phrase_low, []) if alias in text)
                    words=[w for w in re.findall(r"[a-z0-9]+", phrase_low) if len(w)>3 and w not in {"algorithm","algorithms","tree","trees","graph","graphs","list","lists","system","systems","management"}]
                    hits=sum(1 for w in words if w in text)
                    if alias_hits or hits:
                        score += alias_hits * 8 + hits * (3 if phrase != topic.get("name") else 2)
                        matched.append(phrase)
                if score > best_score:
                    best_score = score
                    best = {"unit": unit.get("unit", ""), "topic": topic.get("name", ""),
                            "subtopic": matched[0] if matched else topic.get("name", ""),
                            "confidence": min(0.98, 0.35 + score * 0.12), "needs_review": False}
        if not best:
            return {"unit": "Unassigned", "topic": "Needs Review", "subtopic": "Unassigned", "confidence": 0.3, "needs_review": True}
        if best["confidence"] < 0.6: best["needs_review"] = True
        return best

syllabus_mapper_service = SyllabusMapperService()
