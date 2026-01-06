from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse


@dataclass(frozen=True)
class CliArgs:
    input_path: Path
    output_dir: Path
    debug: bool
    should_print: bool
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
        debug=bool(ns.debug),
        should_print=bool(ns.print),
        jd_text=ns.jd_text,
    )
