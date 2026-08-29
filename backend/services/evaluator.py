from collections import defaultdict
class EvaluatorService:
    @staticmethod
    def evaluate_quiz(quiz, user_answers):
        questions={q["id"]:q for q in quiz.get("questions",[])}; correct=0; topics=defaultdict(lambda:{"correct":0,"total":0}); evaluations=[]
        for qid,q in questions.items():
            idx=user_answers.get(qid); ok=idx is not None and idx==q.get("correct_answer_index")
            if ok: correct+=1
            topic=q.get("topic","General"); topics[topic]["total"]+=1; topics[topic]["correct"]+=int(ok)
            evaluations.append({"question_id":qid,"question":q.get("question"),"selected_option":q.get("options",[])[idx] if idx is not None and 0<=idx<len(q.get("options",[])) else "Not answered","correct_option":q.get("options",[])[q.get("correct_answer_index",0)],"is_correct":ok,"explanation":q.get("explanation",""),"topic":topic})
        total=len(questions); pct=round(correct/max(1,total)*100,1)
        strong=[t for t,s in topics.items() if s["correct"]/s["total"]>=.75]; weak=[t for t,s in topics.items() if s["correct"]/s["total"]<.75]
        return {"quiz_id":quiz.get("quiz_id"),"score":correct,"total_questions":total,"percentage":pct,"accuracy":pct,"strong_areas":strong,"weak_areas":weak,"topics_to_revise":weak,"question_evaluations":evaluations}
evaluator_service=EvaluatorService()
