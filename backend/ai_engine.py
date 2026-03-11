from backend.processing.claim_extractor import extract_claims
from backend.processing.claim_validator import validate_claim
from backend.rag.rag_retriever import retrieve_evidence

import requests
import json
import re


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def analyze_claim(claim):
    """
    Analyze a single claim using RAG + LLM reasoning
    """

    try:

        # Step 1 — Retrieve evidence
        evidence = retrieve_evidence(claim)

        if not evidence:
            evidence_text = "No external evidence retrieved."
        else:
            # limit evidence size to prevent prompt explosion
            evidence_text = "\n".join(evidence[:5])

        # Step 2 — Construct prompt
        prompt = f"""
You are a professional fact-checking AI.

STRICT RULES:
- Do NOT rewrite the claim
- Do NOT paraphrase the claim
- Only evaluate the credibility of the claim

Claim:
{claim}

Evidence:
{evidence_text}

Evaluate whether the claim is true or false.

Return ONLY JSON:

{{
 "credibility_score": number between 0 and 100,
 "summary": "short explanation"
}}

Scoring:
0 = completely false
50 = uncertain
100 = completely true
"""

        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }

        # Step 3 — Call Ollama
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise Exception("Ollama API request failed")

        result = response.json()

        if "response" not in result:
            raise Exception("Invalid Ollama response format")

        output = result["response"].strip()

        # Step 4 — Extract JSON safely
        json_match = re.search(r"\{.*?\}", output, re.DOTALL)

        if json_match:

            parsed = json.loads(json_match.group())

            score = parsed.get("credibility_score", 50)

            if not isinstance(score, (int, float)):
                score = 50

            score = int(score)
            score = max(0, min(score, 100))

            summary = parsed.get("summary", "")

            # Always preserve original claim
            return {
                "claim": claim,
                "credibility_score": score,
                "summary": summary
            }

        # fallback if JSON extraction fails
        return {
            "claim": claim,
            "credibility_score": 50,
            "summary": output
        }

    except Exception as e:

        return {
            "claim": claim,
            "credibility_score": 50,
            "summary": f"Error analyzing claim: {str(e)}"
        }


def analyze_text(text):
    """
    Full pipeline:
    Text → Claim Extraction → Claim Validation → Fact Checking
    """

    try:

        if not text or not isinstance(text, str):
            return {
                "claims_found": 0,
                "valid_claims": 0,
                "results": []
            }

        # Step 1 — Extract claims
        extracted = extract_claims(text)

        claims = extracted.get("claims", [])

        valid_claims = []

        # Step 2 — Validate claims
        for claim in claims:

            validation = validate_claim(claim)

            if validation.get("is_factual"):
                valid_claims.append(claim)

        results = []

        # Step 3 — Analyze each valid claim
        for claim in valid_claims:

            analysis = analyze_claim(claim)

            results.append(analysis)

        return {
            "claims_found": len(claims),
            "valid_claims": len(valid_claims),
            "results": results
        }

    except Exception as e:

        return {
            "claims_found": 0,
            "valid_claims": 0,
            "results": [],
            "error": str(e)
        }