from typing import Protocol
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import ChatRepo
from app.db.schema import Chat

pytestmark = pytest.mark.anyio


class ChatFactory(Protocol):
    async def __call__(self, user_id: UUID, story_id: UUID, title: str) -> Chat: ...


@pytest.fixture
async def chat_repo(db_session: AsyncSession) -> ChatRepo:
    return ChatRepo(db_session)


@pytest.fixture
def chat_factory(chat_repo: ChatRepo) -> ChatFactory:
    async def _chat_factory(user_id: UUID, story_id: UUID, title: str) -> Chat:
        chat = await chat_repo.create_or_update(
            Chat(user_id=user_id, story_id=story_id, title=title)
        )
        await chat_repo.session.commit()
        return chat

    return _chat_factory
