import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def extract_claims(text):
    """
    Extract factual claims from text without rewriting them.
    """

    prompt = f"""
You are a claim extraction system.

Your job is to extract sentences that contain factual claims.

IMPORTANT RULES:
- Do NOT rewrite the sentence
- Do NOT paraphrase
- Do NOT correct misinformation
- Return the claim EXACTLY as it appears in the text

Return ONLY JSON in this format:

{{
 "claims": [
   "exact sentence copied from the text"
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

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception("Ollama request failed")

        result = response.json()

        output = result.get("response", "").strip()

        # safer JSON extraction
        json_match = re.search(r"\{.*?\}", output, re.DOTALL)

        if json_match:

            parsed = json.loads(json_match.group())

            claims = parsed.get("claims", [])

            if not isinstance(claims, list):
                return {"claims": []}

            cleaned_claims = []

            for claim in claims:

                if isinstance(claim, str):

                    claim = claim.strip()

                    # remove quotes or trailing punctuation issues
                    claim = claim.strip('"').strip("'")

                    if len(claim) > 3:
                        cleaned_claims.append(claim)

            return {"claims": cleaned_claims}

        return {"claims": []}

    except Exception as e:

        return {
            "claims": [],
            "error": str(e)
        }