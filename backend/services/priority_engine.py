from collections import defaultdict
class TopicPriorityEngine:
    @staticmethod
    def calculate_topic_priorities(questions):
        stats=defaultdict(lambda:{"count":0,"marks":0,"years":set(),"unit":""})
        for q in questions:
            s=stats[q.get("topic","General")]; s["count"]+=1; s["marks"]+=q.get("marks",0); s["unit"]=q.get("unit",s["unit"]); s["years"].add(q.get("year"))
        if not stats:return []
        maxc=max(x["count"] for x in stats.values()) or 1; maxm=max(x["marks"] for x in stats.values()) or 1; latest=max((q.get("year",0) for q in questions),default=0)
        out=[]
        for topic,s in stats.items():
            freq=s["count"]/maxc*100; marks=s["marks"]/maxm*100; rec=100 if latest in s["years"] else (80 if latest-1 in s["years"] else 60)
            score=round(.4*freq+.3*marks+.2*rec+.1*min(100,len(s["years"])*25))
            label="Critical" if score>=90 else "High" if score>=75 else "Medium" if score>=50 else "Low"
            years=sorted(s["years"])
            out.append({"topic":topic,"unit":s["unit"],"priority_score":score,"priority_label":label,"frequency_score":round(freq,1),"marks_weight":round(marks,1),
                        "trend":"Increasing" if latest in s["years"] and len(years)>1 else "Stable","rationale":f"Appeared {s['count']} times across {len(years)} paper year(s) and carried {s['marks']} marks."})
        return sorted(out,key=lambda x:x["priority_score"],reverse=True)
priority_engine=TopicPriorityEngine()
