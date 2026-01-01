from app.db.schema import Email

from .base import BaseRepo


class EmailRepo(BaseRepo[Email]):
    @property
    def _model(self) -> type[Email]:
        return Email
