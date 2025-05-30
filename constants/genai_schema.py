from pydantic import BaseModel


class GenAISchema(BaseModel):
    resume_skills: list[str]
    trending_skills: list[str]
    missing_critical_skills: list[str]
    tools_to_learn: list[str]
    certification_suggestions: list[str]
    resume_strength: str
    career_insights: str
    recommendations: list[str]
    overall_match: str
    technical_skill_score: str
    soft_skill_score: str
    domain_knowledge:str
    tool_score:str
    trending_skills_demand:list[str]
    top_skills_to_learn:list[str]
    skills_to_hightlight:list[str]
    emerging_technologies:list[str]
    short_term_goals:list[str]