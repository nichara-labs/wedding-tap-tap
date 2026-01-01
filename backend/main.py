# This file needs to be named app.py for fastapi dev/run to work.
import subprocess

from botocore.exceptions import TokenRetrievalError

from app.entrypoint import create_app
from app.settings import get_settings

try:
    app = create_app(get_settings())
except TokenRetrievalError:
    if get_settings().app.env == "local":
        subprocess.run(["aws", "sso", "login"], check=True)  # noqa: S607
        app = create_app(get_settings())
    else:
        raise
