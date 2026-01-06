import re

import outlines
from outlines import Generator
from ollama import Client

from app.prompts import DEFAULT_MODEL_NAME, PROMPT_JD_KEYWORDS
from schemas.jd_keywords import JdKeywords


KEEP_HEADERS = ["about the job", "what you will do", "what you will bring"]
STOP_HEADERS = [
    "benefits",
    "equal opportunity",
    "eeo",
    "pay transparency",
    "the salary range"
]


def normalize_jd(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def slice_core_sections(jd: str) -> str:
    lines = jd.split("\n")
    out: list[str] = []
    capturing = False

    def norm(s: str) -> str:
        return re.sub(r"[^a-z0-9 ]+", "", s.strip().lower())

    for line in lines:
        h = norm(line)

        if any(stop in h for stop in STOP_HEADERS):
            capturing = False

        if any(keep in h for keep in KEEP_HEADERS):
            capturing = True

        if capturing:
            out.append(line)

    return "\n".join(out).strip() or jd


# Init once (keep these module-level so you don’t re-init on every call)
_ollama = Client()
_model = outlines.from_ollama(_ollama, DEFAULT_MODEL_NAME)
_gen = Generator(model=_model, output_type=JdKeywords)


def extract_jd_keywords(jd_text: str) -> JdKeywords:
    normalized = normalize_jd(jd_text)
    core = slice_core_sections(normalized)
    prompt = PROMPT_JD_KEYWORDS.replace("{{JD_TEXT}}", core)

    raw_json = _gen(prompt)
    return JdKeywords.model_validate_json(raw_json)


def resolve_job_description(jd_text: str | None) -> dict | None:
    if not jd_text or not jd_text.strip():
        return None

    normalized = normalize_jd(jd_text.strip())
    keywords = extract_jd_keywords(normalized)

    return {
        "source": "inline",
        "value": normalized,
        "chars": len(normalized),
        "keywords": keywords.model_dump(),
    }
