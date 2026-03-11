from typing import Literal

from pydantic import BaseModel, Field


class LeadQualificationResult(BaseModel):
    intent: Literal[
        "Sales Inquiry",
        "Pricing",
        "Integration",
        "Security / Compliance",
        "Support",
        "Low Intent / Other",
    ]
    persona: Literal[
        "Executive Buyer",
        "Business Buyer",
        "Technical Buyer",
        "End User",
        "Unknown",
    ]
    buying_stage: Literal[
        "Early Research",
        "Evaluation",
        "Ready to Buy",
        "Unknown",
    ]
    urgency: Literal[
        "Low",
        "Medium",
        "High",
    ]
    fit_score: int = Field(ge=0, le=100)
    route_recommendation: Literal[
        "Route to SDR",
        "Route to Solutions",
        "Nurture",
        "Manual Review",
        "Disqualify",
    ]
    risk_flag: Literal[
        "None",
        "Possible Competitor",
        "Student / Research",
        "Support Request",
        "Low Confidence",
    ]
    qualification_rationale: str
    sdr_opener: str
    confidence: float = Field(ge=0.0, le=1.0)