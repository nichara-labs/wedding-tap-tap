from typing import Annotated

from fastapi import Depends
from openai import AsyncOpenAI

from ._state import AppStateDep


async def _llm(app_state: AppStateDep) -> AsyncOpenAI:
    return app_state.llm


LlmDep = Annotated[AsyncOpenAI, Depends(_llm)]
