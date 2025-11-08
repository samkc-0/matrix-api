ARG UV_TAG=0.9.8-python3.12-bookworm-slim

# builder
FROM ghcr.io/astral-sh/uv:${UV_TAG} AS builder
WORKDIR /srv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY app/ /srv/

# dev image with tools, shell, hot reload
FROM ghcr.io/astral-sh/uv:${UV_TAG} AS dev
WORKDIR /srv
COPY --from=builder /srv /srv
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl less procps && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED=1
CMD ["uv", "run", "python", "-m", "main"]

# prod image with minimal runtime
FROM gcr.io/distroless/base-debian12 AS prod
WORKDIR /srv
USER 65532:65532
COPY --from=builder /srv /srv
ENV PYTHONUNBUFFERED=1 PYTHONOPTIMIZE=1
# Optional: make FS read-only at runtime (enable if your app doesn’t write)
# (K8s/Compose can enforce readOnlyRootFilesystem too.)
ENTRYPOINT ["/srv/.venv/bin/python","-m","main"]
