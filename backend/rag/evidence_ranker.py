from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_evidence(claim, evidence_list, top_k=3):

    if not evidence_list:
        return []

    texts = [claim] + evidence_list

    embeddings = model.encode(texts)

    claim_embedding = embeddings[0]
    evidence_embeddings = embeddings[1:]

    scores = cosine_similarity(
        [claim_embedding],
        evidence_embeddings
    )[0]

    ranked = sorted(
        zip(evidence_list, scores),
        key=lambda x: x[1],
        reverse=True
    )

    top_results = [text for text, score in ranked[:top_k]]

    return top_results