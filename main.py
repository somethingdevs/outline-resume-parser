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

class ResumeInfo(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None

class ResumeSkills(BaseModel):
    languages: list[str] = []
    frameworks: list[str] = []
    databases: list[str] = []
    cloud_tools: list[str] = []
    dev_tools: list[str] = []

class ResumeExperience(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    experience_bullets: list[str] = []

class ResumeEducation(BaseModel):
    university: Optional[str] = None
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    extra_info: Optional[str] = None

class ResumeProjects(BaseModel):
    project: Optional[str] = None
    technologies: list[str] = []
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    project_bullets: list[str] = []

class ResumeCertifications(BaseModel):
    certification: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    verification_id: Optional[str] = None

class Resume(BaseModel):
    info: ResumeInfo
    experience: list[ResumeExperience]
    skills: ResumeSkills
    projects: list[ResumeProjects]
    education: list[ResumeEducation]
    certifications: list[ResumeCertifications]

ollama_client = Client()
model = outlines.from_ollama(ollama_client, "ministral-3:8b")
resume_gen = Generator(model=model, output_type=Resume)

prompt = f"""
Extract structured resume information from the text below.

Follow this structure exactly:

1) info:
   - name
   - location
   - phone
   - email
   - github
   - linkedin
   - portfolio

2) skills:
    - languages: (list of strings)
    - frameworks: (list of strings)
    - databases: (list of strings)
    - cloud_tools: (list of strings)
    - dev_tools: (list of strings)

3) experience:
   - list of roles, each with:
     - company
     - position
     - start_date
     - end_date
     - experience_bullets (list of strings)

4) education:
   - list of entries, each with:
     - university
     - degree
     - start_date
     - end_date
     - extra_info

5) projects:
   - list of projects, each with:
     - project
     - technologies (list of strings)
     - start_date
     - end_date
     - project_bullets (list of strings)

6) certifications:
   - list of certifications, each with:
     - certification
     - start_date
     - end_date
     - verification_id

Rules:
- Return missing values as null
- Return missing sections as empty lists
- Do not add extra fields
- Do not include explanations or commentary
- Project name should be the heading text; do not leave it null if present.

RESUME TEXT:
{resume_text}
"""


raw_json = resume_gen(prompt)

resume = Resume.model_validate_json(raw_json)
print(resume.model_dump())
print(raw_json)
