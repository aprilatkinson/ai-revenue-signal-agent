# AI Revenue Signal Agent

AI-powered lead qualification agent that automatically analyzes inbound contacts, classifies intent, and routes them to the correct sales workflow.
The system integrates with HubSpot via webhooks and enriches contacts with AI-generated qualification insights such as intent, persona, buying stage, urgency, and recommended routing.
This enables revenue teams to prioritize high-value leads and automate early-stage qualification.

## Problem

Sales teams receive many inbound leads, but most CRM systems simply store the data without understanding the actual buying signal.
Typical problems:
- Leads enter CRM without context
- Sales teams waste time reviewing low-intent inquiries
- Technical buyers are not routed to the correct teams
- Qualification happens manually and inconsistently
Without automation, valuable signals are often missed.

## Solution
The AI Revenue Signal Agent automatically analyzes inbound contacts and enriches CRM records with structured qualification insights.
When a contact is created in HubSpot:
- HubSpot sends a webhook event
- The agent retrieves the contact data
- An AI classifier analyzes the message and profile
- The lead is categorized by intent and persona
- The CRM record is updated with AI insights
- Sales teams can immediately act on qualified leads
- This transforms a CRM from a passive database into an intelligent revenue signal system.

Example AI Output
Example classification result:
Intent: Integration
Persona: Technical Buyer
Buying Stage: Evaluation
Urgency: Medium
Fit Score: 85
Route Recommendation: Route to Solutions
Confidence: 0.8

Generated SDR message:
Hi Elena, I see you're leading the engineering organization at Acme Payments
and are evaluating platforms for expansion. I'd love to discuss how our
solution can support your integration requirements.

## Architecture
HubSpot Contact Created
        │
        ▼
HubSpot Webhook
        │
        ▼
FastAPI Endpoint
/webhooks/hubspot
        │
        ▼
Qualification Pipeline
        │
        ├─ Fetch Contact (HubSpot API)
        │
        ├─ AI Classification
        │
        ├─ Build CRM Fields
        │
        └─ Write Results Back to HubSpot
## Tech Stack
Backend API
- FastAPI
-  Uvicorn
AI Layer
- OpenAI
- LangGraph (agent pipeline orchestration)
CRM Integration
- HubSpot API Client
Infrastructure
- Python 3.11
- Pydantic
- HTTPX

## Example Workflow
Step 1 — New Contact
A user submits a form or creates a contact in HubSpot.

Step 2 — Webhook Trigger
HubSpot sends an event to:

POST /webhooks/hubspot

Step 3 — AI Qualification
The agent classifies the lead using the message and contact data.

Step 4 — CRM Enrichment
The following fields are automatically written to the contact record:
- AI Intent
- AI Persona
- AI Buying Stage
- AI Fit Score
- AI Route Recommendation
- AI Confidence

## Demo Endpoint
For testing the classifier directly:
POST /classify-demo

## Example request:
curl -X POST http://127.0.0.1:8002/classify-demo \
-H "Content-Type: application/json" \
-d '{
"firstname":"Elena",
"jobtitle":"VP Engineering",
"company":"Acme Payments",
"message":"We are evaluating platforms for European expansion..."
}'
Local Development

Clone the repository
git clone https://github.com/aprilatkinson/ai-revenue-signal-agent.git
cd ai-revenue-signal-agent
Create environment
python -m venv venv
source venv/bin/activate
Install dependencies
pip install -r requirements.txt
Run the API
uvicorn app.main:app --reload --port 8002
Future Expansion

## This project is designed to evolve into a production-ready revenue intelligence system.

Planned improvements:
- Observability
- Add tracing and monitoring of AI decisions.
- langfuse==2.21.3

Benefits:
- Track model performance
- Debug AI decisions
- Monitor prompt quality

Database Layer
Persist lead analysis results and pipeline runs.
- asyncpg==0.29.0
- sqlalchemy[asyncio]==2.0.30
- alembic==1.13.1

Possible features:
- AI audit logs
- lead scoring history
- pipeline analytics
- performance benchmarking

Background Processing
Scale processing using distributed workers.
Potential stack:
- Celery
- Redis

Benefits:
- process large lead volumes
- queue AI jobs
- retry failed workflows

Advanced AI Routing

Future versions may include:
- multi-agent qualification
- intent clustering
- deal prediction
- automated SDR assistance

Author

April Atkinson
AI Systems Builder | Agentic Workflows | GTM Sales & Marketing Automation with Governance

GitHub
https://github.com/aprilatkinson
