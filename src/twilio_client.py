import json
from typing import get_args

import twilio.rest

from .conversation import Conversation, ConversationState
from .customer import Customer


class TwilioClient:
    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        phone_number: str,
        templates: dict[str, str],
    ):
        self.client = twilio.rest.Client(account_sid, auth_token)
        self.phone_number = phone_number
        self.templates = templates

    def get_customer_conversations(self, customer: Customer) -> list[Conversation]:
        try:
            conversations = []

            for c in self.client.conversations.v1.participant_conversations.list(
                address=customer.phone_number
            ):
                id = c.conversation_sid
                date_created = c.conversation_date_created
                date_updated = c.conversation_date_updated
                state = c.conversation_state

                if (
                    not id
                    or not date_created
                    or not date_updated
                    or state not in get_args(ConversationState)
                ):
                    continue

                conversations.append(
                    Conversation(
                        id,
                        customer,
                        date_created,
                        date_updated,
                        state,  # type: ignore
                    )
                )

            return conversations
        except Exception as e:
            print(
                f"Error retrieving conversations (TwilioClient.get_customer_conversations({customer=})): {e}"
            )
            return []

    def has_active_conversations(self, customer: Customer) -> bool:
        conversations = self.get_customer_conversations(customer)

        return any(map(lambda c: c.state == "active", conversations))

    def send_message(
        self, customer: Customer, template_name: str, template_variables: dict[str, str]
    ) -> None:
        if template_name not in self.templates:
            print(
                f"Error retrieving template_id (TwilioClient.send_message({customer=}, {template_name=}, template_variables={json.dumps(template_variables)})): {template_name} not in templates"
            )
            return

        template_id = self.templates.get(template_name, "")

        try:
            self.client.messages.create(
                from_=self.phone_number,
                to=customer.phone_number,
                content_sid=template_id,
                content_variables=json.dumps(template_variables),
            )
        except Exception as e:
            print(
                f"Error sending message (TwilioClient.send_message({customer=}, {template_name=}, template_variables={json.dumps(template_variables)})): {e}"
            )
