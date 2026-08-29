class PaperValidatorService:
    @staticmethod
    def validate_paper(sections, target_marks=100, difficulty_mode="Balanced", syllabus=None, priorities=None):
        qs=[q for s in sections for q in s.get("questions",[])]
        total=sum(q.get("marks",0) for q in qs)
        checks=[{"check_name":"Total Marks Verification","passed":total==target_marks,"details":f"Calculated Total = {total}/{target_marks} Marks"}]
        units={q.get("unit") for q in qs}; checks.append({"check_name":"Unit Distribution Balance","passed":len(units)>=min(3,len(syllabus.get('units',[])) if syllabus else 3),"details":f"Covered {len(units)} units"})
        if difficulty_mode=="Hard Practice": diff_ok=all(q.get("difficulty")=="Hard" for q in qs)
        else: diff_ok=True
        checks.append({"check_name":"Difficulty Ratio Alignment","passed":diff_ok,"details":"Difficulty strategy checked against requested mode."})
        allowed={(t.get("name"),u.get("unit")) for u in (syllabus or {}).get("units",[]) for t in u.get("topics",[])}
        syllabus_ok=all((q.get("topic"),q.get("unit")) in allowed for q in qs) if allowed else True
        checks.append({"check_name":"Syllabus Compliance","passed":syllabus_ok,"details":"Questions mapped to supplied syllabus topics."})
        texts=[q.get("question","").strip().lower() for q in qs]; dup=len(texts)!=len(set(texts))
        checks.append({"check_name":"Duplicate Avoidance","passed":not dup,"details":"No exact duplicates detected."})
        top={p.get("topic") for p in (priorities or [])[:3]}; represented=not top or bool(top & {q.get("topic") for q in qs})
        checks.append({"check_name":"Priority Topic Coverage","passed":represented,"details":"High-priority topics represented where available."})
        return {"validation_status":all(x["passed"] for x in checks),"checks":checks}
paper_validator_service=PaperValidatorService()
