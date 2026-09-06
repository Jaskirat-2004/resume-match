"""
ANALYSER FOR RESUME
"""
# ================================ CONFIG IMPORTS ================================

import re
from config import (ALL_SKILLS, SKILL_PHRASES)
# ================================ EXTRACT KEYWORDS FUNCTION ================================

def extract_keywords(data:str) -> set:
    
    all_keywords = re.split(r"[^a-z0-9+#]+", data.lower())
    cleaned_keywords = set(kw for kw in all_keywords if kw)

    keywords = cleaned_keywords.intersection(ALL_SKILLS)
    return keywords

# ================================ SCORE FUNCTION ================================

def score(jd_kw:set, resume_kw:set) -> float:
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
    print(extract_keywords("role involve... postgres.. psql.. java.. data ingestion hello, (hi) a - an yeah c++ c# .NET NET. .NET."))

    a = None
    if a:
        print("yes")