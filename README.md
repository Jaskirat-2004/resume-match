# resume-match

Upload a resume PDF, paste a job description, and get back a match score, the skills you have, and the skills the job asks for that your resume does not mention.

**Live:** https://resume-match.kikilabs.in

Built with FastAPI. No database, no API keys, no LLM calls, no model weights. Everything runs in memory on a 512 MB instance.

---

## What it does

1. You upload a resume as a PDF and paste a job description as text.
2. Both are extracted, unicode-normalised, and tokenised through the identical pipeline.
3. Each is reduced to the set of **known skills** it mentions, by intersecting with a curated vocabulary.
4. You get a score, a matched list, and a missing list.

The score answers one question: **what fraction of the skills this job asks for appear in the resume.** It is deliberately divided by the job description, not by the resume or the union of both, because the question is "am I missing what they asked for" and not "how similar are these documents". Dividing by the resume would penalise a candidate for having skills beyond the role.

---

## Why a vocabulary instead of a stopword list

The first version matched every word in the job description against every word in the resume, and removed common English with a growing blacklist. It scored a real Data Analyst posting at **26%**, and 54 of the "missing keywords" were words like `overviewjob`, `bachelor`, `s` and `like`.

The problem is structural. A blacklist has to enumerate everything that is *not* a skill, which is all of English and therefore never finishes.

A vocabulary inverts it. Matching intersects with a curated list of ~460 known skills, so anything that is not a skill is invisible and no blacklist is needed at all. The same posting now scores **~47-54%**, and every word in both output lists is a real skill.

---

## How it works

```
PDF bytes                          job description text
   |                                        |
   |  pdf_to_text()                         |
   v                                        |
raw text                                    |
   |                                        |
   +--------------------+-------------------+
                        |
                        |  normalise()      NFKC -> de-hyphenate -> collapse whitespace
                        v
                   clean text
                        |
                        |  lowercase
                        |  SKILL_PHRASES    "power bi" -> "powerbi"   (before splitting)
                        |  split on [^a-z0-9+#]+
                        |  & ALL_SKILLS     everything not a known skill dies here
                        v
                   skill set
                        |
                        |  score()  /  missed_matched_keywords()
                        v
            percentage + matched list + missing list
```

Both documents travel the identical path. If only one side were lowercased or unicode-normalised, every comparison would be quietly wrong.

---

## The skill vocabulary

`config.py` holds the vocabulary, organised so that adding a skill means finding its domain rather than appending to a blob.

| Name | Purpose |
|---|---|
| `SKILLS_BY_DOMAIN` | 13 domains: languages, frontend, backend, databases, data engineering, analytics & BI, ML & AI, devops & cloud, mobile, testing, security, tools, business |
| `ALL_SKILLS` | the flat frozenset that matching intersects against, derived from the domains |
| `SKILL_PHRASES` | multi-word and punctuated skills, collapsed into one token **before** splitting |
| `SKILL_ALIASES` | different spellings of one skill, `postgres` to `postgresql` |
| `DISPLAY_NAMES` | canonical token to human-readable, `powerbi` to `Power BI` |
| `ROLE_PROFILES` | 15 job roles mapped to the domains they draw on |

**The token rule that governs every entry:** the tokeniser splits on every character that is not `a-z`, `0-9`, `+` or `#`. So each entry in a domain set must be a single token made only of those characters. `c++` and `postgresql` match directly. `power bi` and `node.js` never can, and belong in `SKILL_PHRASES`, which rewrites them into `powerbi` and `nodejs` before the split happens.

`skills_for_role("Data Analyst")` returns every skill the system knows about for that role, which is what a "what does this tool understand?" page is built on.

---

## Design notes

Things that are not obvious from reading the code.

**The parser takes bytes, not a file path.** `pdf_to_text(data: bytes)` wraps the bytes in `io.BytesIO` and hands that to pdfplumber. Nothing is written to disk. This matters because the deployment target has an ephemeral filesystem, so anything written to disk disappears on restart anyway.

**Unicode normalisation is the highest value line in the project.** PDF generators store `fl` and `fi` as single ligature codepoints, so `Airflow` in a PDF is often stored with U+FB02 and is six characters rather than seven. `"Airflow" in text` then returns `False` and nothing raises. A resume entirely about Airflow scores zero on Airflow, and the only symptom is a number that looks slightly low. `unicodedata.normalize("NFKC", text)` flattens those back to ASCII. NFC and NFD do not, because only the K forms handle compatibility characters.

**Tokenising keeps `+` and `#`.** `c++` and `c#` survive the split because they are in the character class. `.net` and `node.js` degrade to `net` and `node`+`js`, which costs nothing, because the resume side degrades identically and the two still match. Consistency beats fidelity.

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
analyzer.py     tokenising, skill extraction, scoring
config.py       the skill vocabulary, phrases, aliases, role profiles
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

Runs on Render's free tier as a Web Service, behind a Cloudflare CNAME.

- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:my_app --host 0.0.0.0 --port $PORT`

`--host 0.0.0.0` is required because the default `127.0.0.1` only accepts connections from inside the container. `$PORT` is assigned by the platform at runtime and cannot be hardcoded.

Free instances sleep after a period of inactivity, so the first request after a quiet spell takes around 50 seconds.

---

## Known limitations

Being honest about what this does not do yet.

- **`SKILL_PHRASES` is defined but not yet applied in `extract_keywords`**, so multi-word skills like Power BI are currently invisible.
- **`score()` has no guard for a job description containing zero recognised skills**, which divides by zero.
- **`ResumeParseError` is not caught in the route**, so an image-only PDF returns a 500 rather than a readable message.
- **`SKILL_ALIASES` is not wired in**, so `postgres` and `postgresql` are two unrelated skills, and `reports` and `reporting` are counted separately.
- **Every skill weighs the same.** A requirement stated once counts as much as one repeated five times. Repetition in a job description is real signal and is currently discarded.
- **Required versus preferred is not distinguished.** Missing a must-have and missing a nice-to-have score identically.
- **No semantic matching.** "Built ETL pipelines moving 90 million records" does not match "experience with large-scale data pipeline development", despite meaning the same thing. Keywords cannot see that. Embeddings can.
- **The vocabulary is hand-curated**, so a skill nobody added is a skill the tool cannot see.
- **No tests.**

---

## Roadmap

1. Apply `SKILL_PHRASES` before tokenising, and guard the zero-skill divide.
2. Catch `ResumeParseError` and render a proper message.
3. Wire `SKILL_ALIASES` so spelling variants collapse to one skill.
4. `Counter` instead of `set` for the job description, so repetition weighs the score and the missing list sorts by emphasis.
5. Parse-ability checks: is there an extractable email, phone, and set of section headers. This is the half of ATS behaviour that actually rejects people.
6. Store analyses, which makes TF-IDF weighting possible and removes the last hand-curated part.
7. Semantic similarity via embeddings.

---

## Why

I kept applying to roles and having no idea whether my resume actually contained what the posting asked for. Reading them side by side does not work, you see what you expect to see.

It is also the coded version of an agent I built earlier that reviewed profiles, where the underlying flaw was that it confidently scored fields it had failed to read. Doing the parsing myself means that when something cannot be read, it says so.
