from datetime import datetime,timedelta
class StudyPlannerService:
    @staticmethod
    def generate_study_plan(subject_id,subject_name,priorities,weak_topics=None,days_left=7,daily_hours=3.0):
        weak=set(weak_topics or []); ranked=priorities[:]
        ranked.sort(key=lambda p:(0 if p.get("topic") in weak else 1,-p.get("priority_score",0)))
        topics=ranked or [{"topic":"General Revision","unit":"All Units","priority_score":0}]
        schedule=[]; n=max(1,min(14,days_left)); start=datetime.now()
        for i in range(n):
            p=topics[i%len(topics)]; topic=p["topic"]; unit=p.get("unit","")
            tasks=[f"Study {topic} concepts",f"Practice questions from {topic}",f"Take a short quiz on {topic}"]
            schedule.append({"day":i+1,"date_str":(start+timedelta(days=i)).strftime("%b %d, %Y"),"focus_topic":topic,"unit":unit,"tasks":tasks,"completed_tasks":[],"estimated_hours":daily_hours})
        return {"subject_id":subject_id,"subject_name":subject_name,"days_left":days_left,"daily_hours":daily_hours,"total_days":n,"schedule":schedule,"completion_percentage":0}
study_planner_service=StudyPlannerService()
