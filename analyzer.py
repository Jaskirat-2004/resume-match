"""
ANALYSER FOR RESUME
"""
# ================================ CONFIG IMPORTS ================================
import re
from config import (ALL_SKILLS, SKILL_PHRASES, SKILL_ALIASES)
# ================================ EXTRACT KEYWORDS FUNCTION ================================

def extract_keywords(data:str) -> set:

    data = data.lower()
    # power bi -> powerbi
    sorted_phrases = sorted(SKILL_PHRASES, key=len, reverse=True)
    for phrase in sorted_phrases:
        data = data.replace(phrase,SKILL_PHRASES[phrase])
    
    all_keywords = re.split(r"[^a-z0-9+#]+", data)
    cleaned_keywords = set(SKILL_ALIASES.get(kw,kw) for kw in all_keywords if kw)

    keywords = cleaned_keywords.intersection(ALL_SKILLS)
    return keywords

# ================================ SCORE FUNCTION ================================

def score(jd_kw:set, resume_kw:set) -> float:
    if len(jd_kw)==0:
        return 0.0
    
    matched = jd_kw.intersection(resume_kw)
    score = (len(matched)/len(jd_kw))*100

    return score

# ================================ MISSING FUNCTION ================================

def missed_matched_keywords(jd_kw:set, resume_kw:set) -> list:
    # JD and Resume Intersection -> Then JD - matched
    matched = jd_kw.intersection(resume_kw)
    missed = jd_kw.difference(matched)
    return list(missed), list(matched),

# =======================================================================================
# TEST

if __name__ == "__main__":
    print(extract_keywords("role dashboards involve... power bi postgres.. psql.. java.. data ingestion hello, (hi) a - an yeah c++ c# .NET NET. .NET."))
    a = None
    if a:
        print("yes")