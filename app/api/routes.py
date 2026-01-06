from __future__ import annotations

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from app.core.pipeline import process_pdf
from app.core.job_description import resolve_job_description
from app.api.storage import OUTPUT_DIR, save_upload_pdf, load_json

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"ok": True}


@router.post("/parse")
def parse_resume_api(
    file: UploadFile = File(...),
    debug: bool = Form(False),
) -> JSONResponse:
    pdf_path = save_upload_pdf(file)

    success, final_path = process_pdf(
        pdf_path=pdf_path,
        output_dir=OUTPUT_DIR,
        debug=debug,
        job_description=None,
    )

    payload = load_json(final_path)
    return JSONResponse(status_code=(200 if success else 400), content=payload)


@router.post("/match")
def match_resume_api(
    file: UploadFile = File(...),
    jd_text: str | None = Form(None),
    debug: bool = Form(False),
) -> JSONResponse:
    pdf_path = save_upload_pdf(file)
    job_description = resolve_job_description(jd_text)

    success, final_path = process_pdf(
        pdf_path=pdf_path,
        output_dir=OUTPUT_DIR,
        debug=debug,
        job_description=job_description,
    )

    payload = load_json(final_path)
    return JSONResponse(status_code=(200 if success else 400), content=payload)
