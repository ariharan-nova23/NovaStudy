from collections import defaultdict
import re
class SemanticSimilarityEngine:
    STOP={"explain","describe","write","the","an","a","for","with","using","of","and","in","is","to","what"}
    @classmethod
    def _tokens(cls,text): return {w for w in re.findall(r"\w+", text.lower()) if len(w)>2 and w not in cls.STOP}
    @classmethod
    def similarity(cls,a,b):
        A,B=cls._tokens(a),cls._tokens(b)
        return len(A&B)/len(A|B) if A and B else 0
    @classmethod
    def detect_repeated_questions(cls,questions):
        groups=[]
        used=set()
        for i,q in enumerate(questions):
            if i in used: continue
            group=[q]; used.add(i)
            for j,r in enumerate(questions[i+1:],i+1):
                if cls.similarity(q.get("question",""),r.get("question","")) >= 0.45 or (q.get("subtopic") and q.get("subtopic")==r.get("subtopic")):
                    group.append(r); used.add(j)
            years=sorted({x.get("year") for x in group if x.get("year")})
            if len(group)<2: continue
            total_marks=sum(x.get("marks",0) for x in group)
            trend="Increasing" if len(years)>=2 and max(years)==max(x.get("year",0) for x in questions) else ("Stable" if len(years)>=2 else "Occasional")
            priority="Very High" if len(group)>=3 or total_marks>=25 else ("High" if len(group)==2 or total_marks>=15 else "Medium")
            groups.append({"concept":f"{q.get('subtopic') or q.get('topic')}","topic":q.get("topic","General"),"unit":q.get("unit",""),
                           "appeared_in_years":years,"frequency":len(group),"total_papers":len({x.get('year') for x in questions if x.get('year')}) or len(years),
                           "total_marks":total_marks,"trend":trend,"priority":priority,"questions":group})
        return sorted(groups,key=lambda x:(x["frequency"],x["total_marks"]),reverse=True)
similarity_engine=SemanticSimilarityEngine()
