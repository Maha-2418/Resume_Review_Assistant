from urllib import response
import time
import requests
import os
from dotenv import load_dotenv
load_dotenv()
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemma-4-26b-a4b-it:free"

def call_qwen(prompt):

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert ATS Resume Reviewer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    for _ in range(3):

        try:

            response = requests.post(
                API_URL,
                json=payload,
                headers=headers,
                timeout=90
            )

            data = response.json()

            print(data)

            # OpenRouter returned an error
            if "error" in data:

                print("OpenRouter Error:", data["error"])

                time.sleep(5)

                continue

            if "choices" in data:

                return data["choices"][0]["message"]["content"]

        except Exception as e:

            print(e)

            time.sleep(5)

    return None