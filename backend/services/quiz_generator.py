import uuid, random
from backend.services.ai_service import ai_service

class QuizGeneratorService:
    @staticmethod
    def generate_quiz(subject_id, questions, syllabus, quiz_mode="Quick Quiz", num_questions=10, difficulty="Adaptive", target_topic=None, target_unit=None):
        candidates=questions[:]
        if target_topic: candidates=[q for q in candidates if target_topic.lower() in q.get("topic","").lower() or target_topic.lower() in q.get("subtopic","").lower()] or candidates
        if target_unit: candidates=[q for q in candidates if q.get("unit")==target_unit] or candidates
        if difficulty in {"Easy","Medium","Hard"}: candidates=[q for q in candidates if q.get("difficulty")==difficulty] or candidates
        if quiz_mode=="Important Topics Quiz": candidates=sorted(candidates,key=lambda q:q.get("marks",0),reverse=True)
        random.shuffle(candidates); selected=candidates[:max(1,min(num_questions,len(candidates)))]
        if not ai_service.enabled:
            topics=list(dict.fromkeys(q.get("topic","General") for q in questions if q.get("topic")))
            topics=topics[:8] or ["General"]
            local=[]
            for q in selected:
                correct=q.get("topic","General")
                options=[correct]+[t for t in topics if t != correct][:3]
                while len(options)<4: options.append("Other topic")
                random.shuffle(options)
                local.append({
                    "id":f"qz_{uuid.uuid4().hex[:8]}",
                    "question":f"Which topic is most directly represented by this past-paper question?\n\n{q.get('question','')}",
                    "options":options[:4],
                    "correct_answer_index":options.index(correct),
                    "explanation":f"The uploaded question is mapped to {correct} in {q.get('unit','the syllabus') }.",
                    "hint":"Use the topic and concept named in the question.",
                    "topic":correct,"unit":q.get("unit",""),"difficulty":q.get("difficulty","Medium"),"marks":1
                })
            selected=local
        if ai_service.enabled and selected:
            prompt=f'''Create {len(selected)} multiple-choice questions for {subject_id}. Use ONLY these concepts and syllabus. Return JSON {{"questions":[...]}}. Each item: question, options (4), correct_answer_index, explanation, hint, topic, unit, difficulty, marks. Avoid copying historical wording. SOURCE QUESTIONS: {selected} SYLLABUS: {syllabus}'''
            result=ai_service.ask_json(prompt)
            if result and isinstance(result.get("questions"),list): selected=result["questions"]
        for q in selected:
            q.setdefault("id", f"qz_{uuid.uuid4().hex[:8]}")
            q.setdefault("marks", 1)
        quiz_id=f"quiz_{uuid.uuid4().hex[:8]}"
        quiz={"quiz_id":quiz_id,"subject_id":subject_id,"quiz_mode":quiz_mode,"difficulty":difficulty,"questions":selected}
        return quiz
quiz_generator_service=QuizGeneratorService()
