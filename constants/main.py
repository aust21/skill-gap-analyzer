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
       - Missing critical skills
       - Tools/technologies the user should learn
       - Maximum of 10 trending skills demand (out of 100) for example ["python 23", "java 87", "html 32", "react 89", "typescript 88"].
       - Career improvement suggestions
       - A short summary of the resume's strengths
       - Overall match of job title and resume skills (out of 100)
       - Technical skill score (out of 100)
       - Soft skill score (out of 100)
       - Domain knowledge (out of 100)
       - Score of tools mentioned in the resume (out of 100)
       - Top 3 skills to learn and priority (out of 100) for example ["aws 40", "docker 90", "django 99"]. Respond only with 3 skills to learn and not more or less.
       - Top 3 skills to highlighted from the resume and priority (out of 100) for example ["python 90", "pandas 90", "numpy 99"]. Respond only with 3 skills to learn and not more or less.
       - Top 3 skills emerging technologies and priority (out of 100) for example ["cloud computing 90", "natural language coding 90", "blazor 99"]. Respond only with 3 skills to learn and not more or less.
       - Top 2 short term goals. the skills should be in this format: ["Learn docker:Learn containerization fundamentals to address the top skill gap in your profile.", "Build a Cloud-Based Project:Create a small project using AWS or Azure to demonstrate your cloud computing abilities."]. Respond only with 2 short term goals and not more or less.

    Respond with a valid JSON only. Do not include any explanation or text outside the JSON.
    This is the response format:
    {{
      "resume_skills": [],
      "trending_skills": [],
      "trending_skills_demand":[],
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
      "tool_score":"",
      "top_skills_to_learn":[],
      "skills_to_hightlight":[],
      "emerging_technologies":[],
      "short_term_goals":[]
    }}
    """
    return prompt