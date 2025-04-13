FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG USER_NAME=csicard

# Install make
RUN apt-get update && \
    apt-get install -y make && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER root
RUN useradd -ms /bin/bash ${USER_NAME}
ADD pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY --chown=${USER_NAME} . .

USER ${USER_NAME}

ENV PYTHONPATH="src"
