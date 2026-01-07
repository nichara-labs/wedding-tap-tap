FROM python:3.14-slim@sha256:9813eecff3a08a6ac88aea5b43663c82a931fd9557f6aceaa847f0d8ce738978 AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest@sha256:515b886e8eb99bcf9278776d8ea41eb4553a794195ef5803aa7ca6258653100d /uv /uvx /bin/

# Inherited by all stages and persisted in the final image
ENV APP_DIR=/app
ENV TZ=Asia/Singapore
ENV PYTHONPATH=$APP_DIR/src
ENV UV_CACHE_DIR=/home/user/.cache/uv
ENV PYTHONUNBUFFERED=TRUE
ENV CACHE_UID=1000
ENV CACHE_GID=1000

# Speed up container start time https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv: Don't link packages to the mounted cache on the host (which will not be present in the final image). Instead, copy packages to the container
ENV UV_LINK_MODE=copy

# Ensure that the `python` command uses the venv
ENV PATH="$APP_DIR/.venv/bin:$PATH"

# Useful utilities
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    curl vim git && \
    rm -rf /var/lib/apt/lists/*

# Run the container as a non-root user
RUN useradd -ms /bin/bash --user-group -l -u "${CACHE_UID}" user

USER user

WORKDIR ${APP_DIR}

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=$UV_CACHE_DIR,uid=$CACHE_UID,gid=$CACHE_GID \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

FROM base AS deployment

# Add the rest of the project source code and install it
# Installing the project separately from its dependencies allows optimal layer caching
COPY --chown=user:user pyproject.toml uv.lock main.py $APP_DIR/
RUN --mount=type=cache,target=$UV_CACHE_DIR,uid=$CACHE_UID,gid=$CACHE_GID \
    uv sync --frozen --no-dev

# Set these variables later so that caches work
ARG COMMIT_SHA=local
ARG COMMIT_TIMESTAMP=0
ENV COMMIT_SHA=${COMMIT_SHA}
ENV COMMIT_TIMESTAMP=${COMMIT_TIMESTAMP}

CMD ["fastapi", "run"]
