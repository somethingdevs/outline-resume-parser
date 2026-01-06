from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile, HTTPException

OUTPUT_DIR = Path("outputs")
UPLOADS_DIR = OUTPUT_DIR / "uploads"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def save_upload_pdf(file: UploadFile) -> Path:
    filename = (file.filename or "").lower()
    content_type = (file.content_type or "").lower()

    if not (filename.endswith(".pdf") or content_type == "application/pdf"):
        raise HTTPException(status_code=400, detail="Upload must be a PDF")

    out_path = UPLOADS_DIR / f"{uuid4().hex}.pdf"

    try:
        data = file.file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read upload: {e}")

    if not data or len(data) < 200:
        raise HTTPException(status_code=400, detail="Uploaded file looks empty or too small")

    out_path.write_bytes(data)
    return out_path


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read output JSON: {e}")
