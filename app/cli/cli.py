import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CliArgs:
    input_path: Path
    output_dir: Path
    should_print: bool
    debug: bool
    jd_text: str | None


def parse_args() -> CliArgs:
    parser = argparse.ArgumentParser(description="Schema-safe resume parser (Outlines + Ollama).")
    parser.add_argument("--input", required=True, help="Path to a resume PDF OR a directory of PDFs")
    parser.add_argument("--output-dir", default="outputs", help="Directory to write JSON output")
    parser.add_argument("--print", action="store_true", help="Print output JSON to stdout (single-file only)")
    parser.add_argument("--debug", action="store_true", help="Save prompt/raw artifacts (PII risk)")
    parser.add_argument("--jd-text", help="Inline job description text (paste directly)")

    ns = parser.parse_args()

    return CliArgs(
        input_path=Path(ns.input),
        output_dir=Path(ns.output_dir),
        should_print=bool(ns.print),
        debug=bool(ns.debug),
        jd_text=ns.jd_text,
    )
