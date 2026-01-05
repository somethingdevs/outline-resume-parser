from pydantic import BaseModel, Field

class MatchItem(BaseModel):
    phrase: str
    verdict: str = Field(description="matched|partial|missing")
    evidence: list[str] = Field(default_factory=list)

class MatchBucket(BaseModel):
    matched: list[MatchItem] = Field(default_factory=list)
    partial: list[MatchItem] = Field(default_factory=list)
    missing: list[MatchItem] = Field(default_factory=list)

class MatchReport(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    must_have_score: int = Field(ge=0, le=100)
    good_to_have_score: int = Field(ge=0, le=100)
    notes: list[str] = Field(default_factory=list)

    must_have: MatchBucket = Field(default_factory=MatchBucket)
    good_to_have: MatchBucket = Field(default_factory=MatchBucket)
    responsibilities: MatchBucket = Field(default_factory=MatchBucket)
    soft_skills: MatchBucket = Field(default_factory=MatchBucket)
    domain: MatchBucket = Field(default_factory=MatchBucket)
