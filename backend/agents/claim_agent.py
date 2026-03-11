from langchain_ollama import OllamaLLM
import re

# Initialize LLM
llm = OllamaLLM(model="llama3")


def extract_claims_agent(text):
    """
    Extract factual claims from text using LLM.
    The model is forced to copy sentences exactly without rewriting them.
    """

    prompt = f"""
You are a claim extraction system.

Your task is to identify factual claims in the text.

IMPORTANT RULES:
- Do NOT rewrite sentences
- Do NOT paraphrase
- Do NOT correct misinformation
- Copy the sentence EXACTLY as written in the text
- Return ONLY the claims

Return each claim on a new line.

Text:
{text}
"""

    try:

        response = llm.invoke(prompt)

        claims = []

        for line in response.split("\n"):

            claim = line.strip()

            if not claim:
                continue

            # remove numbering like "1. " or "- "
            claim = re.sub(r"^[0-9]+\.\s*", "", claim)
            claim = re.sub(r"^[-•]\s*", "", claim)

            if len(claim) > 3:
                claims.append(claim)

        return claims

    except Exception as e:

        print("Claim extraction error:", e)

        return []