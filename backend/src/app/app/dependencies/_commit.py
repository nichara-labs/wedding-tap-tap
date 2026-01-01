from typing import Annotated

from fastapi import Depends

from app.settings import CommitDetails, get_commit_info

CommitInfoDep = Annotated[CommitDetails, Depends(get_commit_info)]
