def ats_prompt(resume_text):
    return f"""
You are an expert ATS Resume Reviewer.

Analyze the resume below.

Return ONLY valid JSON.

Do NOT write explanations.

Do NOT use markdown.

Output must exactly follow this format:

{{
    "ats_score": 0,
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "grammar": [],
    "job_roles": [],
    "suggestions": []
}}

Resume:

{resume_text}
"""