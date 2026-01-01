from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.db.schema import Story


class StoryCreateRequest(BaseModel):
    title: str
    description: str = Field(
        description="Short description of the story, for users to read"
    )
    prompt: str = Field(description="Used by the LLM for generation of the story.")


class StoryModel(BaseModel):
    """Prompt is not included in the model returned to the user."""

    id: UUID
    title: str
    description: str
    user_name: str | None
    is_self: bool
    """Whether the story was created by the user of user_name or not."""
    created_at: datetime

    @classmethod
    def from_story(cls, story: Story, current_user_id: UUID | None) -> StoryModel:
        is_self = bool(story.user and current_user_id == story.user.id)
        return cls(
            id=story.id,
            title=story.title,
            description=story.description,
            user_name=story.user.name if story.user else None,
            is_self=is_self,
            created_at=story.created_at,
        )


class StoryWithPromptModel(StoryModel):
    """Includes the prompt."""

    prompt: str

    @classmethod
    def from_story(cls, story: Story, current_user_id: UUID | None) -> StoryModel:
        is_self = bool(story.user and current_user_id == story.user.id)
        return cls(
            id=story.id,
            title=story.title,
            description=story.description,
            user_name=story.user.name if story.user else None,
            is_self=is_self,
            created_at=story.created_at,
            prompt=story.prompt,
        )


class GenreCreateRequest(BaseModel):
    name: str
    description: str


class GenreModel(BaseModel):
    id: UUID
    name: str
    description: str
