from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.core.pipeline import process_pdf
from app.core.job_description import resolve_job_description


app = FastAPI(title="Resume Parser API", version="0.1")


# Where API uploads + outputs go
OUTPUT_DIR = Path("outputs")
UPLOADS_DIR = OUTPUT_DIR / "uploads"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health() -> dict:
    return {"ok": True}


def _save_upload_pdf(file: UploadFile) -> Path:
    # Basic validation (client might send anything)
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()

    if not (filename.endswith(".pdf") or content_type == "application/pdf"):
        raise HTTPException(status_code=400, detail="Upload must be a PDF")

    out_path = UPLOADS_DIR / f"{uuid4().hex}.pdf"

    try:
        # Read the whole thing once (fine for resumes)
        data = file.file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read upload: {e}")

    if not data or len(data) < 200:  # sanity check
        raise HTTPException(status_code=400, detail="Uploaded file looks empty or too small")

    out_path.write_bytes(data)
    return out_path


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read output JSON: {e}")


@app.post("/parse")
def parse_resume_api(
    file: UploadFile = File(...),
    debug: bool = Form(False),
) -> JSONResponse:
    pdf_path = _save_upload_pdf(file)

    # No JD on /parse
    success, final_path = process_pdf(
        pdf_path=pdf_path,
        output_dir=OUTPUT_DIR,
        debug=debug,
        job_description=None,
    )

    payload = _load_json(final_path)
    status = 200 if success else 400
    return JSONResponse(status_code=status, content=payload)


@app.post("/match")
def match_resume_api(
    file: UploadFile = File(...),
    jd_text: str | None = Form(None),
    debug: bool = Form(False),
) -> JSONResponse:
    pdf_path = _save_upload_pdf(file)

    job_description = resolve_job_description(jd_text)

    success, final_path = process_pdf(
        pdf_path=pdf_path,
        output_dir=OUTPUT_DIR,
        debug=debug,
        job_description=job_description,
    )

    payload = _load_json(final_path)
    status = 200 if success else 400
    return JSONResponse(status_code=status, content=payload)
