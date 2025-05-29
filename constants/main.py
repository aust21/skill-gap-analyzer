def prompt(job_title, resume_text):
    prompt = f"""
    You are a career assistant AI.

    You will be given:
    - A job title: "{job_title}"
    - A resume: {resume_text}

    Your tasks:
    1. Extract the trending skills found in the resume for {job_title}.
    2. Identify trending skills in the given job title.
    3. Compare both and provide:
       - Skills in common (strong points)
       - Missing critical skills
       - Tools/technologies the user should learn
       - top 5 trending skills demand (out of 100) for example ["python 23", "java 87", "html 32", "react 89", "typescript 88"]
       - Career improvement suggestions
       - A short summary of the resume's strengths
       - Overall match of job title and resume skills (out of 100)
       - Technical skill score (out of 100)
       - Soft skill score (out of 100)
       - Domain knowledge (out of 100)
       - Score of tools mentioned in the resume (out of 100)

    Respond with a valid JSON only. Do not include any explanation or text outside the JSON.
    This is the response format:
    {{
      "resume_skills": [],
      "trending_skills": [],
      "trending_skills_demand":[],
      "strong_points": [],
      "missing_critical_skills": [],
      "tools_to_learn": [],
      "certification_suggestions": [],
      "resume_strength": "",
      "career_insights": "",
      "recommendations": [],
      "overall_match":"",
      "technical_skill_score":"",
      "soft_skill_score":"",
      "domain_knowledge":"",
      "tool_score":""
    }}
    """
    return prompt