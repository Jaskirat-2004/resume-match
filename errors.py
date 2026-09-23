class ResumeError(Exception):
    """Base class. Anything the user can fix"""
    message = "Something went wrong with the file"

class ResumeParseError(ResumeError):
    message = "This looks like a scanned or image-only PDF.\nUpload the text version, the one Word or Overleaf exported."

class NotAPdfError(ResumeError):
    message = "This file could not be read as pdf."

class FileTooLargeError(ResumeError):
    def __init__(self, size_mb):
        self.message = f"That file is {size_mb:.1f} MB. The limit is 5 MB."
        super().__init__(self.message)
