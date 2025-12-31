import pymupdf
import outlines
from outlines import Generator
from typing import Optional
from ollama import Client
from pydantic import BaseModel

def extract_pdf_text(path: str) -> str:
    with pymupdf.open(path) as doc:
        return "\n\n".join(page.get_text() for page in doc)

resume_text = extract_pdf_text("assets/Ali_M_SDE_Resume.pdf")

class Resume(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None

ollama_client = Client()
model = outlines.from_ollama(ollama_client, "ministral-3:8b")
resume_gen = Generator(model=model, output_type=Resume)

prompt = f"""
Extract the applicant's basic information from the resume text below.
Return missing fields as null.

Fields:
- name
- location
- phone
- email
- github
- linkedin
- portfolio

RESUME TEXT:
{resume_text}
"""

raw_json = resume_gen(prompt)

resume = Resume.model_validate_json(raw_json)
print(resume.model_dump())
print(raw_json)
