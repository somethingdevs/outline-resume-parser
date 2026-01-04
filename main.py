import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pymupdf

from app.debug import write_text, write_json
from app.parser import extract_pdf_text, clean_text, parse_resume
from app.prompts import DEFAULT_MODEL_NAME
from schemas.meta import Meta
from schemas.resume import Resume


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



def collect_pdf_paths(input_path: Path) -> list[Path]:
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            raise ValueError(f"Input file must be a PDF: {input_path}")
        return [input_path]

    if input_path.is_dir():
        pdfs = sorted(input_path.glob("*.pdf"))
        if not pdfs:
            raise FileNotFoundError(f"No PDF files found in directory: {input_path}")
        return pdfs

    raise FileNotFoundError(f"Input path not found or unsupported: {input_path}")


def process_pdf(pdf_path: Path, output_dir: Path, debug: bool) -> tuple[bool, Path]:
    """
    Process a single PDF and write outputs:
      - always: .cleaned.txt and .final.json
      - if debug: .prompt.txt and .raw.txt

    Returns:
      (success, final_json_path)
    """
    base = output_dir / pdf_path.stem

    raw_text = ""
    cleaned_text = ""
    prompt = ""
    raw_json = ""
    resume: Resume | None = None
    success = False
    error: dict | None = None

    meta = Meta(
        source_file=str(pdf_path),
        model=DEFAULT_MODEL_NAME,
        timestamp=datetime.now(timezone.utc).isoformat(),
        chars_extracted=0,
        pages=0,
        schema_version="0.1",
    )

    try:
        meta.pages = get_pdf_page_count(pdf_path)

        raw_text = extract_pdf_text(str(pdf_path))
        cleaned_text = clean_text(raw_text)
        meta.chars_extracted = len(cleaned_text)

        if len(cleaned_text) < 200:
            raise ValueError("Extracted text is too short; PDF may be image-based or extraction failed.")

        resume, raw_json, prompt = parse_resume(cleaned_text)
        success = True

    except Exception as e:
        error = {"type": type(e).__name__, "message": str(e)}

    finally:
        # Always save cleaned text + final json
        if cleaned_text:
            write_text(f"{base}.cleaned", cleaned_text)

        if debug:
            if prompt:
                write_text(f"{base}.prompt", prompt)
            if raw_json:
                write_text(f"{base}.raw", raw_json)

        output = build_output(resume=resume, meta=meta, success=success, error=error)
        write_json(f"{base}.final", output)

    final_path = Path(f"{base}.final.json")
    return success, final_path

def main() -> None:
    parser = argparse.ArgumentParser(description="Schema-safe resume parser (Outlines + Ollama).")
    parser.add_argument("--input", required=True, help="Path to a resume PDF OR a directory of PDFs")
    parser.add_argument("--output-dir", default="outputs", help="Directory to write JSON output")
    parser.add_argument("--print", action="store_true", help="Print output JSON to stdout (single-file only)")
    parser.add_argument("--debug", action="store_true", help="Save prompt/raw artifacts (PII risk)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = collect_pdf_paths(input_path)

    ok = 0
    fail = 0
    last_output: dict | None = None

    for pdf_path in pdfs:
        success, final_path = process_pdf(pdf_path, output_dir, debug=args.debug)
        if success:
            ok += 1
        else:
            fail += 1

        # If user asked for --print, only do it when a single file was passed
        if args.print and len(pdfs) == 1:
            # read back the final json we just wrote (keeps printing consistent)
            with final_path.open("r", encoding="utf-8") as f:
                last_output = json.load(f)

    print(f"Done. success={ok} failed={fail} wrote={output_dir}")

    if args.print and len(pdfs) == 1 and last_output is not None:
        print(json.dumps(last_output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()