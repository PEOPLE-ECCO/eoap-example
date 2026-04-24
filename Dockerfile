ARG BASE_IMAGE=ghcr.io/people-ecco/ecco-algorithm-base:latest
FROM ${BASE_IMAGE}

# Algorithm base path
ARG ALGORITHM_BASE="people_ecco.src.main"
ENV ALGORITHM_BASE=${ALGORITHM_BASE}
ENV UV_PYTHON=3.12

# Install dependencies
COPY requirements.txt requirements.txt
RUN uv pip install --system -r requirements.txt

# Copy sourcecode.
COPY src/ src/
