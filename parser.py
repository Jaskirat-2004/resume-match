"""
PARSER FOR RESUME
"""
# =======================================================================================
import pdfplumber
import io
import re
import unicodedata
# =======================================================================================

class ResumeParseError(Exception):
    pass

# =======================================================================================

def pdf_to_text(data:bytes) -> str:

    parts=[]
    buffer = io.BytesIO(data)
    with pdfplumber.open(buffer) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                parts.append(page_text)

    full_text = "\n".join(parts)

    if not full_text:
        raise ResumeParseError("Resume is Scanned or image cannot scan pdf")
    
    return full_text

# =======================================================================================

def normalise(text: str) -> str:
    # NFKC normalisation
    cleaned = unicodedata.normalize("NFKC", text)
    # De-hyphenate -> multi-\ntenant becomes multitenant
    cleaned = re.sub(r"-\n(\w)", r"\1", cleaned)
    # Remove whitespaces
    cleaned = re.sub(r"[ \t]+", r" ", cleaned)
    cleaned = re.sub(r"\n{3,}", r"\n", cleaned)

    return cleaned.strip()

# =======================================================================================
# TEST

if __name__ == "__main__":
    # IMPORT
    from pathlib import Path

    good = Path("sample_resume.pdf").read_bytes()
    text = pdf_to_text(good)
    cleaned = normalise(text)
    print(cleaned)

