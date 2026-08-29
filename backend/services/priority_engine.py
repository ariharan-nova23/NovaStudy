from typing import List, Dict, Any
from collections import defaultdict

class TopicPriorityEngine:
    @staticmethod
    def calculate_topic_priorities(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        topic_stats = defaultdict(lambda: {"count": 0, "total_marks": 0, "years": set(), "unit": "Unit 1"})

        for q in questions:
            t = q.get("topic", "General")
            topic_stats[t]["count"] += 1
            topic_stats[t]["total_marks"] += q.get("marks", 10)
            if q.get("year"):
                topic_stats[t]["years"].add(q.get("year"))
            if q.get("unit"):
                topic_stats[t]["unit"] = q.get("unit")

        results = []
        max_marks = max((s["total_marks"] for s in topic_stats.values()), default=1)
        max_count = max((s["count"] for s in topic_stats.values()), default=1)

        for topic_name, stats in topic_stats.items():
            freq_score = (stats["count"] / max_count) * 100
            marks_score = (stats["total_marks"] / max_marks) * 100
            recency_score = 90 if 2025 in stats["years"] else (75 if 2024 in stats["years"] else 60)
            
            # Weighted formula
            priority_num = int(0.35 * freq_score + 0.30 * marks_score + 0.20 * recency_score + 0.15 * 80)
            priority_num = min(98, max(35, priority_num))

            if priority_num >= 90:
                label = "Critical"
            elif priority_num >= 75:
                label = "High"
            elif priority_num >= 50:
                label = "Medium"
            else:
                label = "Low"

            years_list = sorted(list(stats["years"]))
            trend_str = "Increasing" if 2025 in years_list and len(years_list) >= 2 else "Stable"
            
            rationale = (
                f"{topic_name} received a high AI priority score ({priority_num}%) because it appeared in "
                f"{len(years_list)} recent papers ({', '.join(map(str, years_list))}) and carried a total of "
                f"{stats['total_marks']} marks across past exams."
            )

            results.append({
                "topic": topic_name,
                "unit": stats["unit"],
                "priority_score": priority_num,
                "priority_label": label,
                "frequency_score": round(freq_score, 1),
                "marks_weight": round(marks_score, 1),
                "trend": trend_str,
                "rationale": rationale
            })

        results.sort(key=lambda x: x["priority_score"], reverse=True)
        return results

priority_engine = TopicPriorityEngine()
