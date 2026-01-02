PROMPT_TEMPLATE = """
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
- Use "Present" exactly for ongoing roles
- Project name should be the heading text; do not leave it null if present.

RESUME TEXT:
{{RESUME_TEXT}}
"""

DEFAULT_MODEL_NAME = "ministral-3:8b"