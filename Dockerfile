# Use an official Python runtime as a parent image
FROM python:3.10-slim as base

# Set environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

# Python dependencies stage
FROM base AS python-deps

# Install Poetry for Python dependency management
RUN pip install poetry

# Install necessary system dependencies (e.g., gcc for compiling Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Copy pyproject.toml and poetry.lock to install Python dependencies
COPY pyproject.toml poetry.lock ./

# Install Python dependencies in a virtual environment
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-dev

# Runtime stage
FROM base AS runtime

# Copy virtual environment from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Install any additional runtime dependencies, such as git
RUN apt-get update && apt-get install -y git

# Create a non-root user and set the working directory
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Copy the application files into the container
COPY --chown=appuser . .

# Expose the port that the application uses
EXPOSE 8501

# Define the command to run the application
ENTRYPOINT ["streamlit", "run", "Home.py"]

