import spacy


# Load spaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    raise Exception("spaCy model not found. Run: python -m spacy download en_core_web_sm")


# Words that usually indicate opinions
OPINION_WORDS = [
    "i think",
    "i feel",
    "i believe",
    "i guess",
    "i suppose",
    "in my opinion",
    "seems like",
    "scary",
    "terrible",
    "awful",
    "amazing",
    "bad",
    "good"
]


def validate_claim(claim):
    """
    Determine whether a sentence is a factual claim
    that can be verified using evidence.
    """

    try:

        # Step 0 — basic validation
        if not claim or not isinstance(claim, str):
            return {
                "claim": claim,
                "is_factual": False
            }

        claim = claim.strip()

        if len(claim) < 4:
            return {
                "claim": claim,
                "is_factual": False
            }

        claim_lower = claim.lower()

        # Step 1 — detect obvious opinion statements
        for word in OPINION_WORDS:
            if word in claim_lower:
                return {
                    "claim": claim,
                    "is_factual": False
                }

        # Step 2 — ignore questions
        if claim.endswith("?"):
            return {
                "claim": claim,
                "is_factual": False
            }

        # Step 3 — NLP parsing
        doc = nlp(claim)

        subject = False
        verb = False
        obj = False

        for token in doc:

            # Detect subject
            if token.dep_ in ["nsubj", "nsubjpass"]:
                subject = True

            # Detect verbs (including auxiliary verbs like "is")
            if token.pos_ in ["VERB", "AUX"]:
                verb = True

            # Detect object or attribute
            if token.dep_ in ["dobj", "pobj", "attr"]:
                obj = True

        # Step 4 — classify factual claim
        if subject and verb:
            return {
                "claim": claim,
                "is_factual": True
            }

        return {
            "claim": claim,
            "is_factual": False
        }

    except Exception as e:

        # Safe fallback if NLP fails
        return {
            "claim": claim,
            "is_factual": True,
            "error": str(e)
        }