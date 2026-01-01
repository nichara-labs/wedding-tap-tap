from typing import Protocol
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import StoryRepo
from app.db.schema import Story

pytestmark = pytest.mark.anyio


class StoryFactory(Protocol):
    async def __call__(
        self, user_id: UUID, title: str, description: str, prompt: str
    ) -> Story: ...


@pytest.fixture
def story_repo(db_session: AsyncSession) -> StoryRepo:
    return StoryRepo(db_session)


@pytest.fixture
def story_factory(story_repo: StoryRepo) -> StoryFactory:
    async def _story_factory(
        user_id: UUID, title: str, description: str, prompt: str
    ) -> Story:
        story = await story_repo.create_or_update(
            Story(title=title, description=description, prompt=prompt, user_id=user_id)
        )
        await story_repo.session.commit()
        return story

    return _story_factory
