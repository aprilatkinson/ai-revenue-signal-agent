from fastapi import FastAPI, Request
from pydantic import BaseModel
from pprint import pprint

from app.services.qualification_pipeline import qualify_contact

app = FastAPI(title="Revenue Signal Agent")


class QualificationRequest(BaseModel):
    contact_id: str


@app.get("/")
def root():
    return {"status": "Revenue Signal Agent running"}


@app.post("/qualify")
def qualify(req: QualificationRequest):
    result = qualify_contact(req.contact_id)
    return {
        "status": "success",
        "contact_id": req.contact_id,
        "result": result.model_dump(),
    }


@app.post("/webhooks/hubspot")
async def hubspot_webhook(request: Request):
    payload = await request.json()

    print("\n=== RAW HUBSPOT WEBHOOK PAYLOAD ===")
    pprint(payload)

    results = []

    events = payload if isinstance(payload, list) else [payload]

    for event in events:
        object_id = event.get("objectId") or event.get("object_id")
        subscription_type = event.get("subscriptionType") or event.get("subscription_type")

        if object_id:
            try:
                result = qualify_contact(str(object_id))
                results.append(
                    {
                        "contact_id": str(object_id),
                        "subscription_type": subscription_type,
                        "status": "qualified",
                        "result": result.model_dump(),
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "contact_id": str(object_id),
                        "subscription_type": subscription_type,
                        "status": "error",
                        "error": str(e),
                    }
                )
        else:
            results.append(
                {
                    "status": "ignored",
                    "reason": "No objectId in payload",
                    "event": event,
                }
            )

    print("=== WEBHOOK RESULTS ===")
    pprint(results)
    print()

    return {"received": len(events), "results": results}

from fastapi import Body
from app.services.classifier import classify_lead


@app.post("/classify-demo")
def classify_demo(payload: dict = Body(...)):
    """
    Simple endpoint for demo/testing.
    Accepts raw lead data and returns AI classification.
    """

    result = classify_lead(payload)

    return {
        "input": payload,
        "classification": result.model_dump()
    }