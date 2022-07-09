FROM python:3.10-alpine

EXPOSE 8000
WORKDIR /app
CMD ["uvicorn", "cli:app", "--host", "0.0.0.0", "--port", "8000"]
RUN apk add --update --no-cache libgcc  && rm -rf /root && mkdir /root

COPY pyproject.toml .

RUN apk add --update --no-cache --virtual .tmp-build-deps  \
    build-base      \
    python3-dev     \
    libffi-dev      \
    coreutils       \
    openssl-dev     \
    gcc             \
    g++             \
    musl-dev        \
    rust            \
    cargo           \
    patchelf                                       && \
    pip install --no-cache-dir -U pip poetry       && \
    poetry config virtualenvs.create false --local && \
    poetry env use system                          && \
    poetry install --no-dev                        && \
    apk del .tmp-build-deps                        && \
    rm -rf /root

COPY companies /app

ARG VERSION='dev'
ENV VERSION=$VERSION
