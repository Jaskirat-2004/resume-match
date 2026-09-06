# =====================================================================
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# =====================================================================

my_app = FastAPI()
templates = Jinja2Templates(directory = "templates")

# =====================================================================

@my_app.get("/health")
def health():
    return {"OWNER": "JASKIRAT", "PROJECT": "RESUME-MATCH"}

# =====================================================================

@my_app.get("/")
def root(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

# =====================================================================

@my_app.get("/upload",response_class=HTMLResponse)
def upload(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
    )
    
# =====================================================================

@my_app.post("/result",response_class=HTMLResponse)
def result(
    request:Request,
    jd:str=Form(...),
    resume:UploadFile=File(...)
    ):
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={"jd":jd,
                 "resume":resume,}
    )

# =====================================================================


