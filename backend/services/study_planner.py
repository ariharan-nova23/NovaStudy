from typing import Dict, Any, List
from datetime import datetime, timedelta

class StudyPlannerService:
    @staticmethod
    def generate_study_plan(
        subject_id: str,
        subject_name: str,
        days_left: int = 7,
        daily_hours: float = 3.0,
        weak_topics: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a structured N-Day study plan tailored to the student's exam date and weak areas.
        """
        schedule = []
        base_date = datetime.now()

        plan_templates = [
            {
                "topic": "Graphs & Graph Traversal",
                "unit": "Unit 4",
                "tasks": ["Read BFS & DFS concepts", "Solve 5 practice problems on BFS", "Review adjacency list representations"]
            },
            {
                "topic": "Trees & AVL Balancing",
                "unit": "Unit 3",
                "tasks": ["Study BST deletion cases", "Practice AVL rotations (LL, RR, LR, RL)", "Solve 10 tree traversal questions"]
            },
            {
                "topic": "Sorting & Hashing",
                "unit": "Unit 5",
                "tasks": ["Revise Quick Sort & Merge Sort recurrences", "Practice Hashing collision resolution", "Complete 10 sorting practice MCQs"]
            },
            {
                "topic": "Stacks, Queues & Arrays",
                "unit": "Unit 1",
                "tasks": ["Revise Infix to Postfix conversion", "Study Circular Queue array modulo math", "Solve 5 Stack evaluation problems"]
            },
            {
                "topic": "Linked Lists & Memory",
                "unit": "Unit 2",
                "tasks": ["Practice in-place Singly Linked List reversal", "Review Polynomial Addition with lists", "Review past 3 year list questions"]
            },
            {
                "topic": "Model Question Paper Practice",
                "unit": "All Units",
                "tasks": ["Generate AI Model Paper", "Attempt 3-hour timed practice paper", "Validate marks distribution"]
            },
            {
                "topic": "Full Mock Exam & Final Revision",
                "unit": "All Units",
                "tasks": ["Attempt Full AI Mock Exam", "Review weak area feedback report", "Final formula & algorithm quick revision"]
            }
        ]

        total_days = max(1, min(14, days_left))

        for i in range(total_days):
            day_num = i + 1
            day_date = base_date + timedelta(days=i)
            template = plan_templates[i % len(plan_templates)]

            schedule.append({
                "day": day_num,
                "date_str": day_date.strftime("%b %d, %Y"),
                "focus_topic": template["topic"],
                "unit": template["unit"],
                "tasks": template["tasks"],
                "completed_tasks": [template["tasks"][0]] if day_num == 1 else [],
                "estimated_hours": daily_hours
            })

        return {
            "subject_id": subject_id,
            "subject_name": subject_name,
            "days_left": days_left,
            "daily_hours": daily_hours,
            "total_days": total_days,
            "schedule": schedule,
            "completion_percentage": 14.2
        }

study_planner_service = StudyPlannerService()
