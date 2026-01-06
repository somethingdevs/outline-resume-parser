import json
from pathlib import Path

from app.cli.args import parse_args
from app.core.job_description import resolve_job_description
from app.core.pipeline import collect_pdf_paths, process_pdf


def run_cli() -> None:
    args = parse_args()

    job_description = resolve_job_description(args.jd_text)

    if not args.input_path.exists():
        raise FileNotFoundError(f"Input file not found: {args.input_path}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = collect_pdf_paths(args.input_path)

    ok = 0
    fail = 0
    last_output: dict | None = None

    for pdf_path in pdfs:
        success, final_path = process_pdf(
            pdf_path=pdf_path,
            output_dir=args.output_dir,
            debug=args.debug,
            job_description=job_description,
        )

        ok += 1 if success else 0
        fail += 0 if success else 1

        if args.should_print and len(pdfs) == 1:
            last_output = json.loads(final_path.read_text(encoding="utf-8"))

    print(f"Done. success={ok} failed={fail} wrote={args.output_dir}")

    if args.should_print and len(pdfs) == 1 and last_output is not None:
        print(json.dumps(last_output, indent=2, ensure_ascii=False))
