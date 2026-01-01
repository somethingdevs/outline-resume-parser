# Schema-Safe Resume Parser (ATS-Ready)

A web-friendly, schema-safe resume parsing engine built using **Outlines** and **local open-source LLMs (via Ollama)**.

The core idea is simple:  
**turn messy resume PDFs into reliable, structured JSON** that you can actually use — for ATS screening, job matching, and resume optimization.

This project started as a resume parser and is evolving into a lightweight **ATS analyzer + resume/JD matcher**.

---

## What this does (right now)

- Upload a resume (PDF)
- Extract text locally
- Use **schema-constrained LLM generation** to produce:
  - contact info
  - skills (categorized)
  - experience (roles + bullets)
  - education
  - projects
  - certifications
- Output is **guaranteed valid JSON** (no broken formats, no post-processing hacks)

The structured output accurately reflects real resume content (tested on production resumes).

---

## Why this exists

Traditional LLM resume parsers:
- hallucinate fields
- break JSON
- require retry logic and regex cleanup

This project avoids that by using **Outlines** to constrain generation at the token level:
- the model *cannot* emit invalid structure
- missing fields become `null`
- missing sections become empty lists

Think **contracts > prompts**.

---

## Tech stack

- **Python**
- **Outlines (v1)** — structured / constrained generation
- **Ollama** — local LLM runtime
- **Ministral-3 8B** — open-source generative model
- **Pydantic** — schema enforcement
- **PyMuPDF** — PDF text extraction

No cloud APIs. No vendor lock-in. Runs locally.

---

## Current schema (high level)

Resume
├── info
├── skills
│ ├── languages
│ ├── frameworks
│ ├── databases
│ ├── cloud_tools
│ └── dev_tools
├── experience [ ]
├── projects [ ]
├── education [ ]
└── certifications [ ]


Every field is optional. Lists default to empty.  
This makes the parser resilient across wildly different resume formats.

---

## Where this is going (planned)

### 1) Web application (next)
- Upload resume via UI
- Preview extracted sections
- Download JSON
- Basic validation warnings (missing email, empty skills, etc.)

### 2) ATS / Job Description matcher
- Upload resume + paste job description
- Output:
  - matched skills
  - missing keywords
  - overlap score (simple, explainable)
- No “AI magic score” nonsense — transparent heuristics

### 3) Resume optimizer
- Generate ATS-friendly bullets aligned to a JD
- Reorder sections based on role
- Normalize formatting automatically

### 4) vLLM backend (optional)
- Swap Ollama for vLLM to support:
  - higher throughput
  - server-based inference
  - production-style deployment

---

## Why this is useful (actually)

- Personal resume optimization
- Recruiter screening tools
- Data-driven ATS analysis
- Structured resume datasets
- Inference / LLM tooling portfolio piece

This isn’t a toy demo — it’s a foundation.

---

## Running locally (high level)

1. Install **Ollama**
2. Pull the model:
```bash
   ollama run ministral-3:8b
```
3. Create a Python virtual environment
4. Install dependencies
5. Run the parser on a PDF
## Contributions

Contributions are welcome! Here’s how you can help:

```bash
feat: The new feature youre proposing
fix: A bug fix in the project
style: Feature and updates related to UI improvements and styling
test: Everything related to testing
docs: Everything related to documentation
refactor: Regular code refactoring and maintenance
```