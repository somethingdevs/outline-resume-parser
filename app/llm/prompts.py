PROMPT_TEMPLATE = """
Extract structured resume information from the text below.

Return ONLY valid JSON (no markdown, no extra text).

You MUST output this exact JSON shape (all top-level keys must exist exactly once):
{
  "info": {
    "name": null,
    "location": null,
    "phone": null,
    "email": null,
    "github": null,
    "linkedin": null,
    "portfolio": null
  },
  "skills": {
    "languages": [],
    "frameworks": [],
    "databases": [],
    "cloud_tools": [],
    "dev_tools": []
  },
  "experience": [
    {
      "company": null,
      "position": null,
      "start_date": null,
      "end_date": null,
      "experience_bullets": []
    }
  ],
  "education": [
    {
      "university": null,
      "degree": null,
      "start_date": null,
      "end_date": null,
      "extra_info": null
    }
  ],
  "projects": [
    {
      "project": null,
      "technologies": [],
      "start_date": null,
      "end_date": null,
      "project_bullets": []
    }
  ],
  "certifications": [
    {
      "certification": null,
      "start_date": null,
      "end_date": null,
      "verification_id": null
    }
  ]
}

Rules:
- Use exactly these keys and nesting. Do not add, rename, or remove keys.
- Missing scalar values must be null.
- Lists must be [] only if the resume truly has no entries for that section.
- If the resume text contains "PROFESSIONAL EXPERIENCE", experience must have at least 1 entry.
- If the resume text contains "ACADEMIC PROJECTS" or "PROJECTS", projects must have at least 1 entry.
- Use "Present" exactly for ongoing roles.
- For bullets: merge wrapped lines into the same bullet.
- For projects: "project" must be the heading text; do not leave it null if present.
- For technologies: split comma-separated items into a list of strings.
- If a line contains only "•", treat the following line(s) as the bullet text.

RESUME TEXT:
{{RESUME_TEXT}}
"""

DEFAULT_MODEL_NAME = "ministral-3:8b"

PROMPT_JD_KEYWORDS = """
You are analyzing a job description and extracting ATS-relevant information.

From the job description, you must extract and categorize information into the following groups:

1. must_have
2. good_to_have
3. responsibilities
4. soft_skills
5. domain

Each extracted item MUST include:
- a concise keyword or phrase
- a short evidence snippet copied verbatim from the job description

# EXAMPLE

JOB DESCRIPTION:
We are looking for a Python engineer with strong experience in Pydantic and LLM inference.
You will build structured output systems and mentor other engineers.

RESULT:
{
  "must_have": [
    {
      "keyword": "Python",
      "evidence": "strong experience in Python"
    },
    {
      "keyword": "Pydantic",
      "evidence": "strong experience in Pydantic"
    }
  ],
  "good_to_have": [],
  "responsibilities": [
    {
      "keyword": "build structured output systems",
      "evidence": "You will build structured output systems"
    }
  ],
  "soft_skills": [
    {
      "keyword": "mentoring",
      "evidence": "mentor other engineers"
    }
  ],
  "domain": [
    {
      "keyword": "LLM inference",
      "evidence": "LLM inference"
    }
  ]
}

# OUTPUT INSTRUCTIONS

Answer in valid JSON only. Do not include markdown or commentary.

Here are the output object definitions:

KeywordEvidence:
    keyword (str): a concise keyword or short phrase
    evidence (str): an exact snippet copied from the job description that proves the keyword

JdKeywords:
    must_have (list[KeywordEvidence]): required or strongly implied skills or knowledge
    good_to_have (list[KeywordEvidence]): preferred or “plus” qualifications
    responsibilities (list[KeywordEvidence]): tasks, duties, or ownership described in the role
    soft_skills (list[KeywordEvidence]): communication, collaboration, mentoring, leadership traits
    domain (list[KeywordEvidence]): industry, problem space, or technical domain context

Rules:
- Use exactly the keys shown above.
- Do NOT invent keywords or tools not supported by evidence.
- Every keyword MUST have evidence.
- If a category is not present in the job description, return an empty list.
- Prefer concrete technical terms (libraries, APIs, decoding methods, parsing techniques).

Return a valid JSON object of type "JdKeywords".

# OUTPUT

JOB DESCRIPTION:
{{JD_TEXT}}

RESULT:
"""

PROMPT_MATCH_REPORT = """You are an ATS reviewer.
You are given:
1) A job description keyword breakdown (must_have, good_to_have, responsibilities, soft_skills, domain)
2) A candidate resume already parsed into JSON.

Your task:
- Compare resume vs job needs.
- For each phrase in each bucket, classify it as:
  matched = clearly present in resume
  partial = related but not explicit / weak evidence
  missing = not present

Scoring rules:
- must_have_score: 0-100 (most important)
- good_to_have_score: 0-100
- overall_score: weighted = 70% must_have + 30% good_to_have (round to int)
- Do NOT give full points if evidence is weak.
- Evidence must be short quotes from resume fields (skills lists, bullets, project tech).

# EXAMPLE

JOB_KEYWORDS:
{"must_have":["Python","Pydantic"],"good_to_have":["Beam search"]}

RESUME_JSON:
{"skills":{"languages":["Python"]},"experience":[{"experience_bullets":["Used Pydantic models..."]}]}

RESULT:
{
  "overall_score": 85,
  "must_have_score": 100,
  "good_to_have_score": 0,
  "notes": ["Beam search not mentioned."],
  "must_have": {...},
  ...
}

# OUTPUT INSTRUCTIONS

Answer in valid JSON only. No extra text.

MatchReport:
  overall_score (int 0-100)
  must_have_score (int 0-100)
  good_to_have_score (int 0-100)
  notes (list[str])
  must_have / good_to_have / responsibilities / soft_skills / domain:
    matched/partial/missing lists of MatchItem

MatchItem:
  phrase (str)
  verdict (matched|partial|missing)
  evidence (list[str])  # 0-3 short snippets

Return a valid JSON of type "MatchReport".

# OUTPUT

JOB_KEYWORDS:
{{JOB_KEYWORDS}}

RESUME_JSON:
{{RESUME_JSON}}

RESULT:
"""