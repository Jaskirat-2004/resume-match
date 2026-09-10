# ================================ IMPORTS ================================
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# ================================ FUNCTIONS ================================
from config import (display)
from parser import (pdf_to_text, normalise)
from analyzer import (extract_keywords, score, missed_matched_keywords)
from errors import (ResumeError,FileTooLargeError)
# ================================ FASTAPI APP ================================

my_app = FastAPI()
templates = Jinja2Templates(directory = "templates")
templates.env.filters["display"] = display
my_app.mount("/static", StaticFiles(directory="static"), name="static")

# ================================ EXCEPTION HANDLER ================================

@my_app.exception_handler(ResumeError)
def handle_resume_error(request: Request, exc:ResumeError):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error":exc.message, "jd":getattr(request.state,"jd","")},
        status_code=400,
    )

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

    request.state.jd = jd

    if (resume.size)/10**6 > 5:
        raise FileTooLargeError((resume.size)/10**6)

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


