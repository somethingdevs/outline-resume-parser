import argparse
import json
import pymupdf

from datetime import datetime, timezone

from app.debug import write_text, write_json
from app.parser import extract_pdf_text, clean_text, parse_resume
from app.prompts import DEFAULT_MODEL_NAME
from schemas.meta import Meta
from schemas.resume import Resume
from pathlib import Path


def build_output(
    resume: Resume | None,
    meta: Meta,
    success: bool,
    error: dict | None,
) -> dict:
    return {
        "success": success,
        "error": error,
        "meta": meta.model_dump(),
        "resume": None if resume is None else resume.model_dump(),
    }

def get_pdf_page_count(path: Path) -> int:
    with pymupdf.open(path) as doc:
        return len(doc)

def main() -> None:
    parser = argparse.ArgumentParser(description="Schema-safe resume parser (Outlines + Ollama).")
    parser.add_argument("--input", required=True, help="Path to a resume PDF")
    parser.add_argument("--output-dir", default="outputs", help="Directory to write JSON output")
    parser.add_argument("--print", action="store_true", help="Print output JSON to stdout")
    parser.add_argument("--debug", action="store_true", help="Toggle saving prompt and raw")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    base = output_dir / input_path.stem

    raw_text = ""
    cleaned_text = ""
    prompt = ""
    raw_json = ""
    resume: Resume | None = None
    success = False
    error: dict | None = None

    meta = Meta(
        source_file=str(input_path),
        model=DEFAULT_MODEL_NAME,
        timestamp=datetime.now(timezone.utc).isoformat(),
        chars_extracted=0,
        pages=0,
        schema_version="0.1"
    )

    try:
        meta.pages = get_pdf_page_count(input_path)

        raw_text = extract_pdf_text(str(input_path))
        cleaned_text = clean_text(raw_text)

        meta.chars_extracted = len(cleaned_text)

        if len(cleaned_text) < 200:
            raise ValueError("Extracted text is too short; PDF may be image-based or extraction failed.")

        resume, raw_json, prompt = parse_resume(cleaned_text)

        success = True

    except Exception as e:
        error = {
            "type": type(e).__name__,
            "message": str(e)
        }

    # Write stuff to debug files wrapped in finally block so it always executes
    finally:
        if cleaned_text:
            write_text(f"{base}.cleaned", cleaned_text)

        if args.debug:
            if prompt:
                write_text(f"{base}.prompt", prompt)

            if raw_json:
                write_text(f"{base}.raw", raw_json)

        output = build_output(resume=resume, meta=meta, success=success, error=error)
        write_json(f"{base}.final", output)

    print(f"Wrote: {base}.final.json")

    if args.print:
        print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()