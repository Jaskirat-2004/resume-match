# resume-match

Upload a resume PDF, paste a job description, get a match score and the list of keywords the job asks for that the resume does not have.

**Live:** https://resume-match-rpu4.onrender.com

Built with FastAPI. No database, no API keys, no LLM calls. Everything runs in memory.

---

## What it does

1. You upload a resume as a PDF and paste a job description as text.
2. The PDF text is extracted, normalised, and reduced to a keyword set.
3. The job description goes through the same pipeline.
4. You get back a percentage and the keywords you are missing.

The score answers one question: **what fraction of the job description's keywords appear in the resume.** It is deliberately divided by the job description, not by the resume or by the union of both, because the question being asked is "am I missing what they asked for" and not "how similar are these two documents". Dividing by the resume would penalise a candidate for having skills beyond the role.

---

## How it works

```
PDF bytes
   |
   |  pdf_to_text()        pdfplumber over an in-memory buffer
   v
raw text
   |
   |  normalise()          NFKC -> de-hyphenate -> collapse whitespace
   v
clean text  <-------------- the job description enters here, same path
   |
   |  extract_keywords()   lowercase -> split -> strip punctuation -> drop stopwords
   v
keyword set
   |
   |  score() / missing_keywords()
   v
percentage + missing list
```

Both documents go through the identical pipeline. If only one side were lowercased or unicode-normalised, every comparison would be quietly wrong.

---

## Design notes

Things that are not obvious from reading the code.

**The parser takes bytes, not a file path.** `pdf_to_text(data: bytes)` wraps the bytes in `io.BytesIO` and hands that to pdfplumber. Nothing is ever written to disk. This matters because the app is deployed on an instance with an ephemeral filesystem, so anything written to disk disappears on restart anyway.

**Unicode normalisation is the highest value line in the project.** PDF generators store `fl` and `fi` as single ligature codepoints, so `Airflow` in a PDF is often stored with U+FB02, making it 6 characters rather than 7. `"Airflow" in text` then returns `False` and nothing raises. A resume entirely about Airflow scores zero on Airflow, and the only symptom is a number that looks slightly low. `unicodedata.normalize("NFKC", text)` flattens those back to ASCII. NFC and NFD do not, because only the K forms handle compatibility characters.

**Punctuation is stripped asymmetrically.** `python,` and `.NET` need opposite treatment: one has trailing punctuation to remove, the other has a leading dot to keep. `+` and `#` are never stripped from either end, which is what keeps `c++` and `c#` intact.

**The routes are `def`, not `async def`.** pdfplumber is CPU-bound and blocking, and there is no async version of it. An `async def` route runs directly on the event loop, so a blocking parse inside one would stall every other request on the server. A plain `def` route is run by FastAPI in a threadpool, which keeps the event loop free. This is also why the upload is read with `resume.file.read()` rather than `await resume.read()`.

**An unreadable PDF fails loudly.** A scanned or image-only PDF has no text layer, so `extract_text()` returns `None` for every page. Rather than return an empty string and let the analyzer report a mysterious 0%, `pdf_to_text` raises `ResumeParseError`. A silent wrong answer is worse than a crash.

---

## A note on ATS

The common story is that an Applicant Tracking System scores your resume and auto-rejects you below a threshold. That is mostly a myth, and it is sold hardest by tools that only make sense if you believe it.

What an ATS actually does is parse your PDF into structured fields and let a recruiter keyword-search the pile. **So the real failure mode is parse failure, not a low score.** A resume in a two-column layout, or with contact details inside an image or a header, can end up with an unreadable email address and never appear in a search at all.

This tool simulates the keyword search half. The `ResumeParseError` path is the beginning of the other half.

---

## Project structure

```
main.py         FastAPI app and routes
parser.py       PDF extraction and text normalisation
analyzer.py     tokenising, keyword extraction, scoring
config.py       stopword lists
templates/      Jinja2 templates
```

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | the upload form |
| `/health` | GET | liveness check, returns JSON |
| `/result` | POST | runs the comparison, renders the result |

`/result` only accepts POST, so opening it directly in a browser returns 405. It is reachable only as the form's submit target.

---

## Running it locally

```bash
git clone https://github.com/Jaskirat-2004/resume-match.git
cd resume-match

python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
uvicorn main:my_app --reload
```

Then open http://127.0.0.1:8000

Python 3.13. `requirements.txt` is hand-written and lists direct dependencies only, not a `pip freeze` dump.

---

## Deploying

Runs on Render's free tier as a Web Service.

- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:my_app --host 0.0.0.0 --port $PORT`

`--host 0.0.0.0` is required because the default `127.0.0.1` only accepts connections from inside the container. `$PORT` is assigned by the platform at runtime and cannot be hardcoded.

Free instances sleep after a period of inactivity, so the first request after a quiet spell takes around 50 seconds.

---

## Known limitations

Being honest about what this does not do yet.

- **Bag of words.** Every keyword weighs the same, so `SQL` stated as a hard requirement counts exactly as much as one item in a list of acceptable degrees. Repetition in a job description is a real signal of emphasis and it is currently thrown away.
- **No skill vocabulary.** Matching runs over every word in the job description rather than over a known list of skills, so boilerplate prose dominates the score. A 200-word job description might contain 9 actual skills, and the other 191 words are noise in the denominator.
- **No synonyms.** `postgres`, `postgresql` and `psql` are three unrelated tokens. `ML` and `machine learning` do not match.
- **Multi-word skills are lost.** Splitting on whitespace destroys `machine learning`, `power bi` and `apache airflow`.
- **No semantic matching.** "Built ETL pipelines moving 90 million records" does not match "experience with large-scale data pipeline development", despite meaning the same thing. Keywords cannot see that. Embeddings can.
- **A job description pasted without spaces between sentences produces junk tokens.** Word boundaries that were never in the source text cannot be recovered.
- **`ResumeParseError` is not caught in the route yet**, so an image-only PDF currently returns a 500 rather than a readable message.

---

## Roadmap

1. Catch `ResumeParseError` and render a proper message.
2. A curated skill vocabulary, so the score reflects skills rather than vocabulary overlap.
3. `Counter` instead of `set` for the job description, so repetition weighs the score and the missing list sorts by emphasis.
4. Synonym and alias mapping, which is where a database starts to earn its place.
5. Parse-ability checks: is there an extractable email, phone, and set of section headers. This is the half of ATS behaviour that actually rejects people.
6. Semantic similarity via embeddings.

---

## Why

I kept applying to roles and having no idea whether my resume actually contained what the posting asked for. Reading them side by side does not work, you see what you expect to see.

It is also the coded version of an agent I built earlier that reviewed profiles, where the underlying flaw was that it confidently scored fields it had failed to read. Doing the parsing myself means that when something cannot be read, it says so.
