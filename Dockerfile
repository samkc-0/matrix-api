ARG UV_TAG=0.9.8-python3.12-bookworm-slim
# builder
FROM ghcr.io/astral-sh/uv:${UV_TAG} AS builder
LABEL org.opencontainers.image.title="fastapi microservice" \
      org.opencontainers.image.description="fast api microservice boilerplate" \
      org.opencontainers.image.source="https://github.com/samkc-0/fastapi-microservice" \
      org.opencontainers.image.version="1.0.0" 
WORKDIR /srv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY app/ /srv/

# dev image with tools, shell, hot reload
FROM ghcr.io/astral-sh/uv:${UV_TAG} AS dev
WORKDIR /srv
COPY --from=builder /srv /srv
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl less procps \
    && rm -rf /var/lib/apt/lists/* \
    && uv sync --frozen --group dev
ENV PYTHONUNBUFFERED=1
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# prod image with minimal runtime
FROM gcr.io/distroless/base-debian12 AS prod
WORKDIR /srv
USER 65532:65532
COPY --from=builder /srv /srv
ENV PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=1 PYTHONPYCACHEPREFIX=/tmp
EXPOSE 8000
ENTRYPOINT ["/srv/.venv/bin/uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "8000"]
