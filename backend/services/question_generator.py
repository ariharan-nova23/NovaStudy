import uuid, random, json
from backend.services.ai_service import ai_service
from backend.services.priority_engine import priority_engine

class QuestionGeneratorService:
    @staticmethod
    def generate_model_paper(subject_name, questions, syllabus, total_marks=100, duration_minutes=180, difficulty_mode="Balanced", num_questions=10, num_previous_papers=4):
        priorities=priority_engine.calculate_topic_priorities(questions)
        context=json.dumps({"syllabus":syllabus,"priorities":priorities[:12],"past_questions":questions[-60:]},ensure_ascii=False)
        if ai_service.enabled:
            prompt=f'''Create a NEW model exam paper for {subject_name}. Use ONLY the supplied syllabus and historical questions as evidence. Do not claim it predicts exact questions. Strategy: {difficulty_mode}. Total marks: {total_marks}. Duration: {duration_minutes} minutes. Return JSON only with keys instructions and sections; each section has section_name,total_section_marks,questions; each question has id,question,marks,unit,topic,difficulty,type. Make the marks sum exactly to {total_marks}. Prefer concept-level novelty instead of copying historical wording. DATA: {context}'''
            result=ai_service.ask_json(prompt)
            if result and result.get("sections"):
                paper={"paper_id":f"model_{uuid.uuid4().hex[:8]}","subject_name":subject_name,"total_marks":total_marks,"duration_minutes":duration_minutes,"difficulty_mode":difficulty_mode,"instructions":result.get("instructions",[]),"sections":result["sections"]}
                return paper
        return QuestionGeneratorService._fallback(subject_name,questions,priorities,total_marks,duration_minutes,difficulty_mode,num_questions)

    @staticmethod
    def _fallback(subject_name,questions,priorities,total_marks,duration,difficulty_mode,num_questions):
        pool=questions[:]
        if difficulty_mode=="High-Priority Topics":
            top={p["topic"] for p in priorities[:5]}; pool=[q for q in pool if q.get("topic") in top] or pool
        elif difficulty_mode=="Hard Practice": pool=[q for q in pool if q.get("difficulty")=="Hard"] or pool
        elif difficulty_mode=="Surprise Practice": pool=sorted(pool,key=lambda q:q.get("topic",""))
        else: pool=sorted(pool,key=lambda q:(-next((p["priority_score"] for p in priorities if p["topic"]==q.get("topic")),0),-q.get("marks",0)))
        chosen=[]; seen=set()
        for q in pool:
            topic=q.get("topic")
            if topic in seen and len(chosen)<4: continue
            chosen.append(q); seen.add(topic)
            if len(chosen)>=num_questions: break
        if not chosen: chosen=pool[:num_questions]
        # Scale to requested total while keeping realistic buckets.
        raw=[5 if q.get("marks",0)<=5 else 10 if q.get("marks",0)<=10 else 20 for q in chosen]
        if sum(raw) != total_marks:
            # create 3 sections and distribute target marks deterministically
            base=max(1,total_marks//max(1,len(chosen))); raw=[base]*len(chosen); raw[-1]+=total_marks-sum(raw)
        sections=[]
        for i,(q,m) in enumerate(zip(chosen,raw)):
            item={"id":f"mp_{uuid.uuid4().hex[:7]}","question":f"Practice variant: {q['question']}","marks":m,"unit":q.get("unit",""),"topic":q.get("topic",""),"difficulty":q.get("difficulty","Medium"),"type":q.get("question_type","Explanation")}
            sec=0 if m<=5 else 1 if m<=10 else 2
            while len(sections)<=sec: sections.append({"section_name":f"Section {chr(65+len(sections))}","total_section_marks":0,"questions":[]})
            sections[sec]["questions"].append(item); sections[sec]["total_section_marks"]+=m
        return {"paper_id":f"model_{uuid.uuid4().hex[:8]}","subject_name":subject_name,"total_marks":total_marks,"duration_minutes":duration,"difficulty_mode":difficulty_mode,
                "instructions":["Answer all questions unless internal choice is specified.","Base answers on the supplied syllabus."],"sections":[s for s in sections if s["questions"]]}
question_generator_service=QuestionGeneratorService()
