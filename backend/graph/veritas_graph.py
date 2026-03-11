from langgraph.graph import StateGraph

from backend.agents.claim_agent import extract_claims_agent
from backend.processing.claim_validator import validate_claim
from backend.ai_engine import analyze_claim


class VeritasState(dict):
    text: str
    claims: list
    valid_claims: list
    results: list


def claim_node(state):

    claims = extract_claims_agent(state["text"])

    state["claims"] = claims

    return state


def validator_node(state):

    valid = []

    for claim in state["claims"]:

        result = validate_claim(claim)

        if result["is_factual"]:
            valid.append(claim)

    state["valid_claims"] = valid

    return state


def factcheck_node(state):

    results = []

    for claim in state["valid_claims"]:

        results.append(analyze_claim(claim))

    state["results"] = results

    return state


graph = StateGraph(VeritasState)

graph.add_node("extract_claims", claim_node)
graph.add_node("validate_claims", validator_node)
graph.add_node("factcheck", factcheck_node)

graph.set_entry_point("extract_claims")

graph.add_edge("extract_claims", "validate_claims")
graph.add_edge("validate_claims", "factcheck")

veritas_graph = graph.compile()