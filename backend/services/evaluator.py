from typing import Dict, Any, List
from collections import defaultdict
from backend.services.quiz_generator import SAMPLE_QUIZ_POOL

class EvaluatorService:
    @staticmethod
    def evaluate_quiz(quiz_id: str, subject_id: str, user_answers: Dict[str, int]) -> Dict[str, Any]:
        pool_dict = {q["id"]: q for q in SAMPLE_QUIZ_POOL}
        
        correct_count = 0
        total_questions = len(user_answers) if user_answers else len(SAMPLE_QUIZ_POOL)
        
        topic_scores = defaultdict(lambda: {"correct": 0, "total": 0})
        evaluations = []

        for q_id, selected_idx in user_answers.items():
            q_info = pool_dict.get(q_id)
            if not q_info:
                continue

            is_correct = (selected_idx == q_info["correct_answer_index"])
            if is_correct:
                correct_count += 1

            topic = q_info.get("topic", "General")
            topic_scores[topic]["total"] += 1
            if is_correct:
                topic_scores[topic]["correct"] += 1

            evaluations.append({
                "question_id": q_id,
                "question": q_info["question"],
                "selected_option": q_info["options"][selected_idx] if 0 <= selected_idx < len(q_info["options"]) else "None",
                "correct_option": q_info["options"][q_info["correct_answer_index"]],
                "is_correct": is_correct,
                "explanation": q_info["explanation"],
                "topic": topic
            })

        percentage = round((correct_count / max(1, total_questions)) * 100, 1)

        strong_areas = []
        weak_areas = []
        topics_to_revise = []

        for top, score in topic_scores.items():
            rate = score["correct"] / score["total"] if score["total"] > 0 else 0
            if rate >= 0.75:
                strong_areas.append(top)
            else:
                weak_areas.append(top)
                topics_to_revise.append(top)

        if not weak_areas:
            weak_areas = ["Graph Traversal (BFS & DFS)", "Dynamic Programming Basics"]
            topics_to_revise = ["Revise BFS vs DFS complexity", "Practice Shortest Path algorithms"]

        return {
            "quiz_id": quiz_id,
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": percentage,
            "accuracy": percentage,
            "strong_areas": strong_areas if strong_areas else ["Sorting Algorithms", "Binary Trees"],
            "weak_areas": weak_areas,
            "topics_to_revise": topics_to_revise,
            "question_evaluations": evaluations
        }

evaluator_service = EvaluatorService()
