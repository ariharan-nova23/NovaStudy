from collections import Counter
class PatternAnalyzerService:
    @staticmethod
    def analyze_patterns(questions):
        n=len(questions)
        if not n: return {"unit_distribution":{},"marks_distribution":{},"question_type_distribution":{},"difficulty_distribution":{}}
        units=Counter(q.get("unit","Unknown") for q in questions)
        marks=Counter(f"{q.get('marks',0)} Marks" for q in questions)
        types=Counter(q.get("question_type","Unknown") for q in questions)
        diffs=Counter(q.get("difficulty","Unknown") for q in questions)
        return {"unit_distribution":{k:round(v/n*100,1) for k,v in units.items()},"marks_distribution":dict(marks),
                "question_type_distribution":dict(types),"difficulty_distribution":dict(diffs)}
pattern_analyzer_service=PatternAnalyzerService()
