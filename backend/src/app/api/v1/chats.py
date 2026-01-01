from uuid import UUID

from fastapi import APIRouter, HTTPException
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import (
    DbSessionDep,
    RequiresLoginDep,
    SessionDataDep,
)
from app.db.repositories import ChatRepo, MessageRepo
from app.db.schema import Chat, Message
from app.models import (
    ChatModel,
    ChatWithStoryModel,
    CreateChatRequest,
    MessageModel,
    UpdateChatRequest,
)

_log = get_logger(__name__)

router = APIRouter(
    prefix=get_route_prefix(), tags=["chats"], dependencies=[RequiresLoginDep]
)


@router.get("")
async def get_chats(
    session: SessionDataDep, db: DbSessionDep
) -> list[ChatWithStoryModel]:
    """Get all chats for the current user, sorted in reverse chronological order."""
    chat_repo = ChatRepo(db)
    chats = await chat_repo.get_by_field_multiple(
        lambda c: c.user_id == session.user_id, eager_load=[Chat.story]
    )
    return sorted(
        [ChatWithStoryModel.from_chat(chat, chat.story.title) for chat in chats],
        key=lambda c: c.created_at,
        reverse=True,
    )


@router.get("/{chat_id}")
async def get_chat(
    session: SessionDataDep, db: DbSessionDep, chat_id: UUID
) -> ChatWithStoryModel:
    """Get a chat by ID."""
    chats = ChatRepo(db)
    chat = await chats.get_for_user_or_raise(
        chat_id=chat_id, user_id=session.user_id, eager_load=[Chat.story]
    )
    return ChatWithStoryModel.from_chat(chat, chat.story.title)


@router.post("", status_code=201)
async def create_chat(
    session: SessionDataDep, db: DbSessionDep, req: CreateChatRequest
) -> ChatModel:
    """Create a new chat for a given story."""
    chats = ChatRepo(db)
    chat = await chats.create_or_update(
        Chat(user_id=session.user_id, story_id=req.story_id)
    )
    return ChatModel.from_chat(chat)


@router.put("/{chat_id}")
async def update_chat(
    chat_id: UUID, session: SessionDataDep, db: DbSessionDep, req: UpdateChatRequest
) -> ChatModel:
    """Update a chat."""
    chats = ChatRepo(db)
    chat = await chats.get_for_user_or_raise(chat_id=chat_id, user_id=session.user_id)
    chat.title = req.title
    updated_chat = await chats.create_or_update(chat)
    return ChatModel.from_chat(updated_chat)


@router.delete("/{chat_id}")
async def delete_chat(chat_id: UUID, session: SessionDataDep, db: DbSessionDep) -> None:
    """Delete a chat."""
    chats = ChatRepo(db)
    num_deleted = await chats.delete_by_field(
        lambda c: [c.id == chat_id, c.user_id == session.user_id]
    )
    if num_deleted == 0:
        raise HTTPException(404, "Chat not found")

    if num_deleted != 1:
        raise HTTPException(400, f"More than 1 chat was deleted: {num_deleted}")


@router.get("/{chat_id}/messages")
async def get_chat_messages(
    session: SessionDataDep, db: DbSessionDep, chat_id: UUID
) -> list[MessageModel]:
    """Get all messages for a chat, sorted in chronological order."""
    messages = MessageRepo(db)
    messages = await messages.get_by_field_multiple(
        lambda m: [m.chat_id == chat_id, m.user_id == session.user_id],
        eager_load=[Message.children],
    )
    return sorted(
        (MessageModel.from_message(m) for m in messages),
        key=lambda m: m.id,
    )
