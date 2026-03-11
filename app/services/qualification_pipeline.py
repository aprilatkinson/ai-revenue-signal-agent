from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from app.tools.hubspot_client import HubSpotClient
from app.services.classifier import classify_lead
from app.schemas.lead_qualification import LeadQualificationResult


CONTENT_MAP = {
    "Sales Inquiry": "sales_inquiry",
    "Pricing": "pricing",
    "Integration": "integration",
    "Security / Compliance": "security_compliance",
    "Support": "support",
    "Low Intent / Other": "low_intent_other",
}


class QualificationState(TypedDict):
    contact_id: str
    properties: Optional[dict]
    result: Optional[LeadQualificationResult]
    ai_fields: Optional[dict]
    error: Optional[str]


def fetch_contact(state: QualificationState) -> QualificationState:
    """Fetch contact properties from HubSpot."""
    try:
        hubspot = HubSpotClient()
        contact = hubspot.get_contact(state["contact_id"])
        return {**state, "properties": contact.properties}
    except Exception as e:
        return {**state, "error": f"fetch_contact failed: {str(e)}"}


def run_classifier(state: QualificationState) -> QualificationState:
    """Run AI classification on contact properties."""
    if state.get("error"):
        return state
    try:
        result = classify_lead(state["properties"])
        return {**state, "result": result}
    except Exception as e:
        return {**state, "error": f"run_classifier failed: {str(e)}"}


def build_ai_fields(state: QualificationState) -> QualificationState:
    """Map classification result to HubSpot AI field schema."""
    if state.get("error"):
        return state

    result = state["result"]

    ai_fields = {
        "ai_content": CONTENT_MAP.get(result.intent, "low_intent_other"),
        "ai_persona": result.persona,
        "ai_buying_stage": result.buying_stage,
        "ai_urgency": result.urgency,
        "ai_fit_score": result.fit_score,
        "ai_route_recommendation": result.route_recommendation,
        "ai_risk_flag": result.risk_flag,
        "ai_qualification_rationale": result.qualification_rationale,
        "ai_sdr_opener": result.sdr_opener,
        "ai_confidence": result.confidence,
    }

    return {**state, "ai_fields": ai_fields}


def write_to_crm(state: QualificationState) -> QualificationState:
    """Write AI fields back to HubSpot contact record."""
    if state.get("error"):
        return state
    try:
        hubspot = HubSpotClient()
        hubspot.update_contact_ai_fields(state["contact_id"], state["ai_fields"])
        return state
    except Exception as e:
        return {**state, "error": f"write_to_crm failed: {str(e)}"}


def route_after_fetch(state: QualificationState) -> str:
    """Skip to end if fetch failed."""
    return "end" if state.get("error") else "run_classifier"


def build_qualification_graph():
    graph = StateGraph(QualificationState)

    graph.add_node("fetch_contact", fetch_contact)
    graph.add_node("run_classifier", run_classifier)
    graph.add_node("build_ai_fields", build_ai_fields)
    graph.add_node("write_to_crm", write_to_crm)

    graph.set_entry_point("fetch_contact")

    graph.add_conditional_edges(
        "fetch_contact",
        route_after_fetch,
        {"run_classifier": "run_classifier", "end": END},
    )

    graph.add_edge("run_classifier", "build_ai_fields")
    graph.add_edge("build_ai_fields", "write_to_crm")
    graph.add_edge("write_to_crm", END)

    return graph.compile()


pipeline = build_qualification_graph()


def qualify_contact(contact_id: str) -> LeadQualificationResult:
    """
    Run the full qualification pipeline via LangGraph.
    Drop-in replacement for the previous qualify_contact function.
    """
    final_state = pipeline.invoke(
        {
            "contact_id": contact_id,
            "properties": None,
            "result": None,
            "ai_fields": None,
            "error": None,
        }
    )

    if final_state.get("error"):
        raise RuntimeError(final_state["error"])

    return final_state["result"]