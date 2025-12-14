from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from .customer import Customer

ConversationState = Literal["active", "closed", "inactive"]


@dataclass
class Conversation:
    id: str
    customer: Customer
    date_created: datetime
    date_updated: datetime
    state: ConversationState
