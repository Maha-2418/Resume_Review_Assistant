import json
from backend.llm_engine import call_qwen
from backend.prompts import ats_prompt

def analyze_resume(resume_text):

    response = call_qwen(ats_prompt(resume_text))

    if response is None:
        return {
            "error": "AI service is temporarily unavailable. Please try again in a few seconds."
        }

    print("\n================ RAW RESPONSE ================\n")
    print(response)
    print("\n==============================================\n")

    try:
        response = response.replace("```json", "").replace("```", "").strip()
        return json.loads(response)

    except Exception as e:
        print("JSON ERROR:", e)

        return {
            "error": "The AI returned an invalid response. Please try again."
        }