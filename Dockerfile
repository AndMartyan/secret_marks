FROM python:3.7 as baseimage

# dependencies builder
FROM baseimage as builder

ARG PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION="ignore" \
    POETRY_VENV=/poetry

COPY pyproject.toml poetry.lock /tmp/

WORKDIR /tmp

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install --upgrade pip \
    && $POETRY_VENV/bin/pip install poetry \
    && $POETRY_VENV/bin/poetry export \
        --only=main \
        --format requirements.txt \
        --output /tmp/requirements.txt \
        --without-hashes \
        --no-interaction \
        --no-cache \
    && cat /tmp/requirements.txt \
    && python3 -m pip install \
        --prefix=/install \
        -r /tmp/requirements.txt


RUN mkdir /secret_marks

WORKDIR /secret_marks

COPY . .

RUN chmod a+x docker/*.sh
