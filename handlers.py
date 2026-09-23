# ================================ IMPORTS ================================
from fastapi import Request
from errors import ResumeError
# ================================ LOGGER ================================
from logging import getLogger
logger = getLogger(__name__)
# ================================ HANDLERS ================================

def register_handlers(app, templates):

    @app.exception_handler(ResumeError)
    def handle_resume_error(request: Request, exc:ResumeError):
        logger.warning("ERROR OCCURED WITH USER DATA : {%s}",type(exc).__name__)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error":exc.message, "jd":getattr(request.state,"jd","")},
            status_code=400,
        )

    @app.exception_handler(Exception)
    def handle_unexpected_error(request: Request, exc:Exception):
        logger.exception("UNDEFINED ERROR : {%s}",type(exc).__name__)
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "Something went wrong on our end. Please try again."},
            status_code=500,
        )
