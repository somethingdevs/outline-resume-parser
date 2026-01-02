import argparse
import json
import pymupdf

from datetime import datetime, timezone

from app.parser import extract_pdf_text, clean_text, parse_resume
from app.prompts import DEFAULT_MODEL_NAME
from schemas.meta import Meta
from schemas.resume import Resume
from pathlib import Path


def build_output(resume: Resume, meta: Meta) -> dict:
    return {
        "meta": meta.model_dump(),
        "resume": resume.model_dump()
    }

def get_pdf_page_count(path: Path) -> int:
    with pymupdf.open(path) as doc:
        return len(doc)

def main() -> None:
    parser = argparse.ArgumentParser(description="Schema-safe resume parser (Outlines + Ollama).")
    parser.add_argument("--input", required=True, help="Path to a resume PDF")
    parser.add_argument("--output-dir", default="outputs", help="Directory to write JSON output")
    parser.add_argument("--print", action="store_true", help="Print output JSON to stdout")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_text = extract_pdf_text(str(input_path))
    cleaned_text = clean_text(raw_text)

    resume = parse_resume(cleaned_text)

    meta = Meta(
        source_file=str(input_path),
        model=DEFAULT_MODEL_NAME,
        timestamp=datetime.now(timezone.utc).isoformat(),
        chars_extracted=len(cleaned_text),
        pages=get_pdf_page_count(input_path),
        schema_version="0.1"
    )

    output = build_output(resume=resume, meta=meta)

    # Write JSON
    out_file = output_dir / f'{input_path.stem}.json'
    with out_file.open("w", encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    if args.print:
        print(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"Wrote: {out_file}")

if __name__ == "__main__":
    main()