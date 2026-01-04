import json
from pathlib import Path

from app.cli import parse_args
from app.job_description import resolve_job_description
from app.pipeline import collect_pdf_paths, process_pdf


def main() -> None:
    args = parse_args()

    job_description = resolve_job_description(args["jd_text"])

    input_path: Path = args["input_path"]
    output_dir: Path = args["output_dir"]
    debug: bool = args["debug"]
    should_print: bool = args["print"]

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = collect_pdf_paths(input_path)

    ok = 0
    fail = 0
    last_output: dict | None = None

    for pdf_path in pdfs:
        success, final_path = process_pdf(
            pdf_path=pdf_path,
            output_dir=output_dir,
            debug=debug,
            job_description=job_description,
        )

        if success:
            ok += 1
        else:
            fail += 1

        if should_print and len(pdfs) == 1:
            with final_path.open("r", encoding="utf-8") as f:
                last_output = json.load(f)

    print(f"Done. success={ok} failed={fail} wrote={output_dir}")

    if should_print and len(pdfs) == 1 and last_output is not None:
        print(json.dumps(last_output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
