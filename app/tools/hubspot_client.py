from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from app.core.config import get_settings


settings = get_settings()


class HubSpotClient:
    def __init__(self):
        self.client = HubSpot(access_token=settings.hubspot_api_token)

    def get_contact(self, contact_id: str):
        """Fetch a contact from HubSpot"""
        return self.client.crm.contacts.basic_api.get_by_id(contact_id)

    def update_contact_ai_fields(self, contact_id: str, properties: dict):
        """Update AI_ fields only"""
        contact_input = SimplePublicObjectInput(properties=properties)

        return self.client.crm.contacts.basic_api.update(
            contact_id,
            simple_public_object_input=contact_input,
        )