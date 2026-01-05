from __future__ import annotations

from pydantic import BaseModel, Field


class KeywordEvidence(BaseModel):
    keyword: str
    evidence: str

class JdKeywords(BaseModel):
    must_have: list[KeywordEvidence] = Field(default_factory=list)
    good_to_have: list[KeywordEvidence] = Field(default_factory=list)
    responsibilities: list[KeywordEvidence] = Field(default_factory=list)
    soft_skills: list[KeywordEvidence] = Field(default_factory=list)
    domain: list[KeywordEvidence] = Field(default_factory=list)
