# ================================ IMPORTS ================================
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# ================================ FUNCTIONS ================================
from config import (display)
from parser import (pdf_to_text, normalise)
from analyzer import (extract_keywords, score, missed_matched_keywords)
# ================================ FASTAPI APP ================================

my_app = FastAPI()
templates = Jinja2Templates(directory = "templates")
templates.env.filters["display"] = display
my_app.mount("/static", StaticFiles(directory="static"), name="static")

# ================================ HEALTH ROUTE ================================

@my_app.get("/health")
def health():
    return {"OWNER": "JASKIRAT", "PROJECT": "RESUME-MATCH"}

# ================================ ROOT ROUTE ================================

@my_app.get("/")
def root(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
    
# ================================ RESULT ROUTE ================================

@my_app.post("/result",response_class=HTMLResponse)
def result(request:Request, jd:str=Form(...), resume:UploadFile=File(...)):

    # RESUME
    resume_data = pdf_to_text(resume.file.read())
    cleaned_resume = normalise(resume_data)
    resume_keywords = extract_keywords(cleaned_resume)
    # JD
    cleaned_jd = normalise(jd)
    jd_keywords = extract_keywords(cleaned_jd)

    similarity_score = score(jd_keywords,resume_keywords)
    missed_list, matched_list = missed_matched_keywords(jd_keywords,resume_keywords)

    return templates.TemplateResponse(
        request = request,
        name = "result.html",
        context = {
            "score":similarity_score,
            "missing":missed_list,
            "matching":matched_list,
            }
    )

# =======================================================================================


