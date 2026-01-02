from typing import Optional
from pydantic import BaseModel, Field


class ResumeInfo(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None

class ResumeSkills(BaseModel):
    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    cloud_tools: list[str] = Field(default_factory=list)
    dev_tools: list[str] = Field(default_factory=list)

class ResumeExperience(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    experience_bullets: list[str] = Field(default_factory=list)

class ResumeEducation(BaseModel):
    university: Optional[str] = None
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    extra_info: Optional[str] = None

class ResumeProject(BaseModel):
    project: Optional[str] = None
    technologies: list[str] = Field(default_factory=list)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    project_bullets: list[str] = Field(default_factory=list)

class ResumeCertification(BaseModel):
    certification: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    verification_id: Optional[str] = None

class Resume(BaseModel):
    info: ResumeInfo = Field(default_factory=ResumeInfo)
    experience: list[ResumeExperience] = Field(default_factory=list)
    skills: ResumeSkills = Field(default_factory=ResumeSkills)
    projects: list[ResumeProject] = Field(default_factory=list)
    education: list[ResumeEducation] = Field(default_factory=list)
    certifications: list[ResumeCertification] = Field(default_factory=list)