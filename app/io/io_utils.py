from pathlib import Path

import pymupdf


def get_pdf_page_count(path: Path) -> int:
    with pymupdf.open(path) as doc:
        return len(doc)