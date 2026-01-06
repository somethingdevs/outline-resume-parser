import pymupdf
import outlines
from outlines import Generator
from ollama import Client

from app.llm.prompts import PROMPT_TEMPLATE, DEFAULT_MODEL_NAME
from schemas.resume import Resume

ollama_client = Client()
model = outlines.from_ollama(ollama_client, DEFAULT_MODEL_NAME)


def extract_pdf_text(path: str) -> str:
    with pymupdf.open(path) as doc:
        return "\n\n".join(page.get_text() for page in doc)


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    return text



def parse_resume(text: str) -> tuple[Resume, str, str]:
    prompt = PROMPT_TEMPLATE.replace("{{RESUME_TEXT}}", text)

    if "{{RESUME_TEXT}}" in prompt:
        raise ValueError("PROMPT_TEMPLATE placeholder {{RESUME_TEXT}} was not replaced.")

    resume_gen = Generator(model=model, output_type=Resume)
    raw_json = resume_gen(prompt)

    resume = Resume.model_validate_json(raw_json)

    # print(resume.model_dump())
    return resume, raw_json, prompt
