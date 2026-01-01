from typing import Annotated

from fastapi import Depends

from app.settings import Settings, get_settings


def _get_settings() -> Settings:
    return get_settings()


SettingsDep = Annotated[Settings, Depends(_get_settings)]
