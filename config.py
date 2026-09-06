"""
CONFIG FOR RESUME PARSER
"""

# ================================ FILLER WORDS ================================

STOP_ENGLISH = {
    "a","an","the","and","or","but","if","then","than","that","this","these","those",
    "of","in","on","at","to","for","with","from","by","as","into","over","under",
    "about","against","between","during","before","after","above","below","up","down",
    "out","off","again","further","once","here","there","when","where","why","how",
    "what","who","whom","which","whose","all","any","both","each","few","more","most",
    "other","some","only","own","same","so","such","no","nor","not","too","very",
    "is","am","are","was","were","be","been","being","have","has","had","having",
    "do","does","did","doing","will","would","shall","should","can","could","may",
    "might","must","i","me","my","we","us","our","you","your","he","him","his",
    "she","her","it","its","they","them","their",
}

STOP_JD = {
    "role","position","candidate","applicant","job","company","team","join",
    "looking","seeking","ideal","successful","responsibilities","requirements",
    "required","qualifications","preferred","must","strong","excellent","good",
    "great","solid","proven","demonstrated","ability","able","skills","knowledge",
    "understanding","familiarity","experience","years","year","etc","including",
    "include","includes","related","relevant","equivalent","degree","field",
    "using","use","used","work","working","new","well","help","ensure","across",
    "within","per","via","apply","please","opportunity","environment","plus",
}

FILLER_WORDS = frozenset(STOP_ENGLISH | STOP_JD)

# ================================ WORDS ================================