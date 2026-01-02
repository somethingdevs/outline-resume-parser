import re
import pymupdf
import outlines
from outlines import Generator
from ollama import Client

from app.prompts import PROMPT_TEMPLATE, DEFAULT_MODEL_NAME
from schemas.resume import Resume

ollama_client = Client()
model = outlines.from_ollama(ollama_client, DEFAULT_MODEL_NAME)
resume_gen = Generator(model=model, output_type=Resume)

def extract_pdf_text(path: str) -> str:
    with pymupdf.open(path) as doc:
        return "\n\n".join(page.get_text() for page in doc)


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove form-feed / page-break characters
    text = text.replace("\x0c", "")

    # Strip leading/trailing whitespace
    text = text.strip()

    # Remove trailing whitespace on each line
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    # Collapse 3+ newlines into max 2 newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse multiple spaces/tabs into a single space (but keep newlines)
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text



def parse_resume(text: str) -> Resume:
    prompt = PROMPT_TEMPLATE.replace("{{RESUME_TEXT}}", text)

    if "{{RESUME_TEXT}}" in prompt:
        print("ERROR PLACEHOLDER!")
    raw_json = resume_gen(prompt)
    resume = Resume.model_validate_json(raw_json)
    # print(resume.model_dump())
    # print(raw_json)
    return resume
