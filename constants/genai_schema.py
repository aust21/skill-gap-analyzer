from pydantic import BaseModel


class GenAISchema(BaseModel):
    resume_skills: list[str]
    trending_skills: list[str]
    strong_points: list[str]
    missing_critical_skills: list[str]
    tools_to_learn: list[str]
    certification_suggestions: list[str]
    resume_strength: str
    career_insights: str
    recommendations: list[str]
