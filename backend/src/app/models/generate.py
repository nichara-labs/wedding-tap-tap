from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class GenerateExistingChatRequest(BaseModel):
    type_: Literal["existing"]
    content: str

    parent_message_id: UUID = Field(
        description="The message for which to generate the reply for."
    )

    chat_id: UUID


class GenerateNewChatRequest(BaseModel):
    type_: Literal["new"]
    chat_id: UUID
