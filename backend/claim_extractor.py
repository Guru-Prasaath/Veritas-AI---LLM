import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def extract_claims(text):

    prompt = f"""
Extract the main factual claims from the following text.

Return ONLY JSON in this format:

{{
 "claims": [
   "claim 1",
   "claim 2",
   "claim 3"
 ]
}}

Text:
{text}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        result = response.json()

        output = result.get("response", "")

        json_match = re.search(r'\{.*\}', output, re.DOTALL)

        if json_match:
            return json.loads(json_match.group())

        return {"claims": []}

    except Exception as e:
        return {"error": str(e)}