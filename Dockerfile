# Use an official Python runtime as a parent image
FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install Poetry
RUN pip install poetry

# Update, install gcc, libgl1-mesa-glx, and clean up to minimize the layer size
RUN apt-get update && \
    apt-get install -y gcc libgl1-mesa-glx --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and poetry.lock files (assuming they exist)
COPY pyproject.toml .
COPY poetry.lock .

# Install python dependencies in /.venv
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-dev --no-root

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create a user and set work directory
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY --chown=appuser . .
RUN ls

# Expose streamlit port
EXPOSE 8501

# Run the application
ENTRYPOINT ["streamlit", "run", "Home.py"]
