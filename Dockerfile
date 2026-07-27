# AI-Brain-Framework Dockerfile
# Multi-stage build for minimal image size

FROM python:3.11-slim AS builder

WORKDIR /build
COPY pyproject.toml ./
COPY framework/ ./framework/
COPY tools/ ./tools/

RUN pip install --no-cache-dir build \
    && python -m build --wheel

FROM python:3.11-slim

LABEL maintainer="AI-Brain-Framework Team"
LABEL version="1.0.0"
LABEL description="Professional framework with digital brain"

WORKDIR /app

COPY --from=builder /build/dist/*.whl ./
RUN pip install --no-cache-dir *.whl && rm *.whl

COPY examples/ ./examples/

USER nobody
EXPOSE 8000 8001 8002 8003

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["python", "-m", "tools.cli", "--help"]
