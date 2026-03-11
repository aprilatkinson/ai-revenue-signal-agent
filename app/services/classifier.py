from openai import OpenAI

from app.core.config import get_settings
from app.schemas.lead_qualification import LeadQualificationResult


settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


SYSTEM_PROMPT = """
You are a B2B SaaS lead qualification assistant.

Classify the lead into strict CRM fields.

Return valid JSON only with these keys:
intent
persona
buying_stage
urgency
fit_score
route_recommendation
risk_flag
qualification_rationale
sdr_opener
confidence

Allowed values:

intent:
- Sales Inquiry
- Pricing
- Integration
- Security / Compliance
- Support
- Low Intent / Other

persona:
- Executive Buyer
- Business Buyer
- Technical Buyer
- End User
- Unknown

buying_stage:
- Early Research
- Evaluation
- Ready to Buy
- Unknown

urgency:
- Low
- Medium
- High

route_recommendation:
- Route to SDR
- Route to Solutions
- Nurture
- Manual Review
- Disqualify

risk_flag:
- None
- Possible Competitor
- Student / Research
- Support Request
- Low Confidence

Rules:
- fit_score must be 0 to 100
- confidence must be 0.0 to 1.0
- Be conservative
- If uncertain, use Unknown and Low Confidence
"""


def classify_lead(contact_properties: dict) -> LeadQualificationResult:
    inquiry = (
        contact_properties.get("message")
        or contact_properties.get("hs_content_membership_notes")
        or ""
    )

    lead_context = {
        "firstname": contact_properties.get("firstname", ""),
        "lastname": contact_properties.get("lastname", ""),
        "email": contact_properties.get("email", ""),
        "jobtitle": contact_properties.get("jobtitle", ""),
        "company": contact_properties.get("company", ""),
        "website": contact_properties.get("website", ""),
        "message": inquiry,
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Classify this lead:\n{lead_context}",
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    return LeadQualificationResult.model_validate_json(content)