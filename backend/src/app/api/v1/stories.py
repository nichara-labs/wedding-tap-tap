from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter
from structlog.stdlib import get_logger

from app.api.utils import get_route_prefix
from app.app.dependencies import DbSessionDep, MaybeSessionDataDep, SessionDataDep
from app.db.repositories import StoryRepo
from app.db.schema import Story
from app.models import StoryCreateRequest, StoryModel, StoryWithPromptModel

_log = get_logger(__name__)

router = APIRouter(prefix=get_route_prefix(), tags=["stories"])


@router.post("")
async def create(
    req: StoryCreateRequest, db: DbSessionDep, session: SessionDataDep
) -> StoryModel:
    """Create a new story."""
    stories = StoryRepo(db)
    story = await stories.create_or_update(
        Story(
            title=req.title,
            description=req.description,
            prompt=req.prompt,
            user_id=session.user_id,
        ),
        eager_load=[Story.user],
    )
    return StoryModel.from_story(story, session.user_id)


@router.get("")
async def get_stories(
    db: DbSessionDep, session: MaybeSessionDataDep, *, show_deleted: bool = False
) -> list[StoryModel]:
    """Fetch all stories sorted in reverse choronological order."""
    stories = StoryRepo(db)
    all_stories = await stories.get_by_field_multiple(
        lambda s: s.deleted_at.is_not(None) if show_deleted else s.deleted_at.is_(None),
        eager_load=[Story.user],
    )
    return sorted(
        (
            StoryModel.from_story(
                s, current_user_id=session.user_id if session else None
            )
            for s in all_stories
        ),
        key=lambda s: s.created_at,
        reverse=True,
    )


@router.get("/{story_id}")
async def get_story(
    db: DbSessionDep, session: SessionDataDep, story_id: UUID
) -> StoryModel | StoryWithPromptModel:
    """Fetch a single story. If the story is owner by the user, includes the prompt."""
    story = await StoryRepo(db).get_by_field_or_raise(
        lambda s: [s.id == story_id], eager_load=[Story.user]
    )
    if story.user_id == session.user_id:
        return StoryWithPromptModel.from_story(story, current_user_id=session.user_id)
    return StoryModel.from_story(story, current_user_id=session.user_id)


@router.put("/{story_id}")
async def edit_story(
    db: DbSessionDep, session: SessionDataDep, story_id: UUID, req: StoryCreateRequest
) -> StoryModel:
    """Edit a story."""
    stories = StoryRepo(db)
    story = await stories.get_by_field_or_raise(
        lambda s: [s.id == story_id, s.user_id == session.user_id],
        eager_load=[Story.user],
    )
    story.title = req.title
    story.prompt = req.prompt
    story.description = req.description
    updated = await stories.create_or_update(story)
    return StoryModel.from_story(updated, current_user_id=session.user_id)


@router.delete("/{story_id}")
async def delete_story(
    db: DbSessionDep, session: SessionDataDep, story_id: UUID
) -> None:
    """Mark a story as deleted."""
    stories = StoryRepo(db)
    story = await stories.get_by_field_or_raise(
        lambda s: [
            s.id == story_id,
            s.user_id == session.user_id,
            s.deleted_at.is_(None),
        ]
    )
    story.deleted_at = datetime.now(tz=UTC)
    await stories.create_or_update(story)
