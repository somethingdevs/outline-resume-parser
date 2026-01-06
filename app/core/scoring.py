import json
import outlines
from outlines import Generator
from ollama import Client

from app.prompts import DEFAULT_MODEL_NAME, PROMPT_MATCH_REPORT
from schemas.match_report import MatchReport

_ollama = Client()
_model = outlines.from_ollama(_ollama, DEFAULT_MODEL_NAME)
_gen = Generator(model=_model, output_type=MatchReport)

def score_resume_against_jd(resume, jd_keywords: dict) -> MatchReport:
    resume_json = resume.model_dump()
    prompt = (
        PROMPT_MATCH_REPORT
        .replace("{{JOB_KEYWORDS}}", json.dumps(jd_keywords, ensure_ascii=False))
        .replace("{{RESUME_JSON}}", json.dumps(resume_json, ensure_ascii=False))
    )
    raw = _gen(prompt)
    return MatchReport.model_validate_json(raw)
