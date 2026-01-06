import argparse
from pathlib import Path


def parse_args() -> dict:
    parser = argparse.ArgumentParser(description="Schema-safe resume parser (Outlines + Ollama).")
    parser.add_argument("--input", required=True, help="Path to a resume PDF OR a directory of PDFs")
    parser.add_argument("--output-dir", default="outputs", help="Directory to write JSON output")
    parser.add_argument("--print", action="store_true", help="Print output JSON to stdout (single-file only)")
    parser.add_argument("--debug", action="store_true", help="Save prompt/raw artifacts (PII risk)")
    parser.add_argument("--jd-text", help="Inline job description text (paste directly)")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    return {
        "input_path": input_path,
        "output_dir": output_dir,
        "print": args.print,
        "debug": args.debug,
        "jd_text": args.jd_text,
    }
