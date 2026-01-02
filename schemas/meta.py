from typing import Optional

from pydantic import BaseModel


class Meta(BaseModel):
    source_file: str
    model: str
    timestamp: str
    chars_extracted: int = 0
    pages: int = 0
    schema_version: str = '0.1'
    prompt_version: Optional[str] = None