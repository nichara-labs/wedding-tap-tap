import asyncio
import contextlib
from collections.abc import AsyncIterable, Callable, Sequence
from functools import partial
from math import ceil
from typing import Annotated, Any, cast
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessageParam
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import (
    DbSessionDep,
    LlmDep,
    RequiresPositiveLorestoneBalanceDep,
    SessionDataDep,
    SettingsDep,
)
from app.db.repositories import (
    LorestoneTransactionRepo,
    MessageRepo,
)
from app.db.repositories.chat import ChatRepo
from app.db.repositories.story import StoryRepo
from app.db.schema import LorestoneTransaction, Message
from app.models import (
    DeltaEvent,
    GenerateExistingChatRequest,
    GenerateNewChatRequest,
)
from app.settings import Settings
from app.utils import uuid_to_int_64

router = APIRouter(prefix=get_route_prefix(), tags=["generate"])

_log = get_logger(__name__)


@router.post("/title")
async def generate_title(
    chat_id: UUID,
    db: DbSessionDep,
    llm: LlmDep,
    session: SessionDataDep,
    settings: SettingsDep,
) -> None:
    """Generate the title for a given chat, using the first non-system message, and updates the chat title."""
    chats = ChatRepo(db)

    chat = await chats.get_by_field_or_raise(  # Will error if user doesn't own the chat
        lambda c: [c.id == chat_id, c.user_id == session.user_id]
    )

    lock_int = uuid_to_int_64(chat.id, "generate_title")
    lock = await db.execute(func.pg_try_advisory_xact_lock(lock_int))
    if not lock.scalar_one():
        _log.warning("Existing lock is being held", lock_id=lock_int)
        raise HTTPException(
            429, "An existing title generation for this chat is in progress"
        )

    if chat.title:
        raise HTTPException(400, "Chat already has a title")

    message = await MessageRepo(db).get_first_message_by_type_or_raise(
        chat_id=chat_id, user_id=session.user_id
    )

    if message.content.strip() == "":
        # Blank first message, so use generic title
        title = f"Chat {str(chat_id)[-6:]}"
    else:
        title = await _generate_title(
            llm, model=settings.llm.title_model, content=message.content
        )

    chat.title = title
    await chats.create_or_update(chat)


@router.post("/message")
async def generate_message(
    req: Annotated[
        GenerateExistingChatRequest | GenerateNewChatRequest,
        Body(discriminator="type_"),
    ],
    db: DbSessionDep,
    llm: LlmDep,
    session: SessionDataDep,
    settings: SettingsDep,
    _: RequiresPositiveLorestoneBalanceDep,
) -> StreamingResponse:
    """
    Generate a message for a chat.
    Will stream and then create the message instance in the chat, saving to the DB.
    """
    # Will fail if user does not own the chat
    chat = await ChatRepo(db).get_by_field_or_raise(
        lambda c: [c.id == req.chat_id, c.user_id == session.user_id]
    )
    lock_int = uuid_to_int_64(chat.id, "generate_message")
    lock = await db.execute(func.pg_try_advisory_xact_lock(lock_int))
    if not lock.scalar_one():
        _log.warning("Existing lock is being held", lock_id=lock_int)
        raise HTTPException(429, "An existing message generation is in progress")

    chain = await _fetch_message_chain(req, session.user_id, settings, db)

    # While it would be nice to be able to separate this into separate blocks,
    # since finalizers can only be run *after* the StreamingResponse is completed,
    # we have to put our functions as callbacks into the passed AsyncIterable.
    return StreamingResponse(
        _stream_with_finalizers(
            llm,
            settings.llm.model,
            chain,
            finalizers=[
                partial(
                    _save_message_and_transaction,
                    req,
                    session.user_id,
                    db,
                    settings.llm.lorestone_value,
                ),
            ],
        )
    )


async def _fetch_message_chain(
    req: GenerateExistingChatRequest | GenerateNewChatRequest,
    user_id: UUID,
    settings: Settings,
    db: AsyncSession,
) -> Sequence[ChatCompletionMessageParam]:
    story = await StoryRepo(db).get_by_chat_id(req.chat_id)
    system_prompt: ChatCompletionMessageParam = {
        "role": "system",
        "content": settings.llm.system_prompt + "\n" + story.prompt,
    }

    messages = await MessageRepo(db).get_by_field_multiple(
        lambda m: [m.chat_id == req.chat_id, m.user_id == user_id]
    )

    # New Chat
    if isinstance(req, GenerateNewChatRequest):
        if messages:
            raise HTTPException(400, "This is an existing chat")

        return [system_prompt]

    # Existing chat
    leaf = next(m for m in messages if m.id == req.parent_message_id)
    message_tree = MessageRepo.root_to_leaf(leaf, messages)
    existing_messages = cast(
        "list[ChatCompletionMessageParam]",
        [{"role": m.role, "content": m.content} for m in message_tree],
    )
    return [system_prompt, *existing_messages, {"role": "user", "content": req.content}]


async def _stream_with_finalizers(  # noqa: C901
    llm: AsyncOpenAI,
    model: str,
    chain: Sequence[ChatCompletionMessageParam],
    finalizers: Sequence[Callable[[CompletionUsage | None, str], Any]],
) -> AsyncIterable[str]:
    """Stream the LLM response, then call finalizer function(s) with usage data and the complete LLM response."""
    queue = asyncio.Queue[str]()
    tasks: set[asyncio.Task[Any]] = set()
    try:
        stream = await llm.chat.completions.create(
            model=model,
            messages=chain,
            stream=True,
            stream_options={"include_usage": True},
        )

        usage = None
        assistant_response = []

        async def _ping() -> None:
            """Periodically send SSE comments to keep the stream alive and allow us to detect client disconnects/avoid connection timeouts."""
            while True:
                await queue.put(":ping\n\n")
                await asyncio.sleep(1)

        async def _stream_chunks() -> None:
            nonlocal usage
            async for chunk in stream:
                if chunk.usage:
                    usage = chunk.usage
                content = chunk.choices[0].delta.content
                if content is None or content == "":
                    continue
                assistant_response.append(content)
                await queue.put(DeltaEvent(type_="delta", v=content).serialize_event())
            queue.shutdown()

        tasks.add(asyncio.create_task(_ping()))
        tasks.add(asyncio.create_task(_stream_chunks()))

        with contextlib.suppress(asyncio.QueueShutDown):
            while event := await queue.get():
                yield event

        async with asyncio.TaskGroup() as tg:
            for f in finalizers:
                tg.create_task(f(usage, "".join(assistant_response)))
    except asyncio.CancelledError:  # Client disconnect
        _log.warning("Client disconnected from stream")
    finally:
        queue.shutdown()
        for task in tasks:
            task.cancel()


async def _generate_title(
    llm: AsyncOpenAI,
    model: str,
    content: str,
) -> str:
    _content = f"""Generate a concise, 3-5 word title with an emoji summarizing the content in the content's primary language.
### Guidelines:
- The title should clearly represent the main theme or subject of the content.
- Use emojis that enhance understanding of the topic, but avoid quotation marks or special formatting.
- Write the title in the content's primary language.
- Prioritize accuracy over excessive creativity; keep it clear and simple.
- Your entire response must consist solely of the title, without any introductory or concluding text.
- Do not use any markdown code fences or other encapsulating text.
- Ensure no conversational text, affirmations, or explanations precede or follow the title.
### Output:
your concise title here
### Examples:
- 📉 Stock Market Trends
- 🍪 Perfect Chocolate Chip Recipe
- Evolution of Music Streaming
- Remote Work Productivity Tips
- Artificial Intelligence in Healthcare
- 🎮 Video Game Development Insight
### Content:
<content>
${content}
</content>"""
    resp = await llm.chat.completions.create(
        model=model, messages=[{"role": "user", "content": _content}]
    )
    title = resp.choices[0].message.content
    if title is None or title.strip() == "":
        error = "Failed to generate chat title: LLM returned empty response"
        _log.error(error, content=content, model=model)
        raise HTTPException(500, error)
    return title


async def _save_message_and_transaction(  # noqa: PLR0913
    req: GenerateExistingChatRequest | GenerateNewChatRequest,
    user_id: UUID,
    db: AsyncSession,
    lorestone_value: float,
    usage: CompletionUsage | None,
    assistant_response: str,
) -> None:
    message_repo = MessageRepo(db)
    user_message = None
    if isinstance(req, GenerateExistingChatRequest):
        # Save the user's messages
        user_message = await message_repo.create_or_update(
            Message(
                content=req.content or "",
                chat_id=req.chat_id,
                role="user",
                user_id=user_id,
                parent_id=req.parent_message_id,
            )
        )
    assistant_message = await MessageRepo(db).create_or_update(
        Message(
            content="".join(assistant_response),
            chat_id=req.chat_id,
            role="assistant",
            user_id=user_id,
            parent_id=user_message.id if user_message else None,
        )
    )

    if not usage:
        _log.error("No usage data returned from LLM")
        return
    await _save_lorestone_transaction(
        db, user_id, assistant_message, usage, lorestone_value
    )


async def _save_lorestone_transaction(
    db: AsyncSession,
    user_id: UUID,
    assistant_message: Message,
    usage: CompletionUsage,
    lorestone_value: float,
) -> None:
    cost = float(usage.model_dump().get("cost", 0))
    lorestone_cost = ceil(cost / lorestone_value)

    txn = LorestoneTransactionRepo(db)
    current_balance = await txn.get_current_balance(user_id)
    balance_after_transaction = current_balance - lorestone_cost
    await txn.create_or_update(
        LorestoneTransaction(
            user_id=user_id,
            balance_before_transaction=current_balance,
            amount=-lorestone_cost,
            category="story_generation",
            balance_after_transaction=balance_after_transaction,
            additional_info=usage.model_dump_json(),
            message_id=assistant_message.id,
        )
    )
