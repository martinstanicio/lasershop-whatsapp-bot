from typing import get_args

import twilio.rest

from .conversation import Conversation, ConversationState
from .customer import Customer


class TwilioClient:
    def __init__(self, account_sid: str, auth_token: str, templates: dict[str, str]):
        self.client = twilio.rest.Client(account_sid, auth_token)
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
