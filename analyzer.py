"""
ANALYSER FOR RESUME
"""
# =======================================================================================
from config import FILLER_WORDS
# =======================================================================================

def extract_keywords(data:str) -> set:
    all_keywords = set(data.lower().split())
    cleaned = set()
    for keyword in all_keywords:
        keyword = keyword.lstrip("({[-")
        keyword = keyword.rstrip(".,;:!)}]")
        if keyword:
            cleaned.add(keyword)

    keywords = cleaned.difference(FILLER_WORDS)

    return keywords

# =======================================================================================


# =======================================================================================
# TEST

if __name__ == "__main__":
    print(extract_keywords("role involve hello, (hi) a - an yeah c++ c# .NET NET. .NET."))

    a = None
    if a:
        print("yes")