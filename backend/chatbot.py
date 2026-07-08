from backend.llm_engine import call_qwen

def chat_with_resume(resume_text, analysis, question):

    prompt = f"""
You are an intelligent Resume Review Assistant.

Use BOTH the resume and the ATS analysis to answer.

Resume:
{resume_text}

ATS Analysis:
{analysis}

Question:
{question}

Answer:
"""

    answer = call_qwen(prompt)

    if answer is None:
        return "⚠ The AI service is currently busy. Please try your question again in a few seconds."

    return answer