from claim_extractor import extract_claims
import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def analyze_claim(claim):

    prompt = f"""
You are a fact-checking AI.

Analyze the credibility of this claim.

Return ONLY JSON:

{{
 "claim": "{claim}",
 "credibility_score": number between 0 and 100,
 "summary": "short explanation"
}}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()

    output = result.get("response", "")

    json_match = re.search(r'\{.*\}', output, re.DOTALL)

    if json_match:
        return json.loads(json_match.group())

    return {
        "claim": claim,
        "credibility_score": 50,
        "summary": output
    }


def analyze_text(text):

    extracted = extract_claims(text)

    claims = extracted.get("claims", [])

    results = []

    for claim in claims:
        analysis = analyze_claim(claim)
        results.append(analysis)

    return {
        "claims_analyzed": len(results),
        "results": results
    }