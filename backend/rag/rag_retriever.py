from backend.rag.evidence_retriever import search_evidence
from backend.rag.text_chunker import chunk_text
from backend.rag.vector_store import build_index, search_index


def retrieve_evidence(claim):
    """
    Retrieve relevant evidence for a claim using:
    Search -> Chunking -> Vector Index -> Semantic Retrieval
    """

    try:
        # Step 1: Search documents related to claim
        documents = search_evidence(claim)

        if not documents:
            return []

        # Step 2: Chunk documents
        chunks = []

        for doc in documents:
            if not doc:
                continue

            doc_chunks = chunk_text(doc)
            chunks.extend(doc_chunks)

        if not chunks:
            return []

        # Step 3: Build vector index (FAISS)
        build_index(chunks)

        # Step 4: Retrieve most relevant chunks
        results = search_index(claim)

        if not results:
            return []

        return results

    except Exception as e:
        print("RAG Retrieval Error:", e)
        return []