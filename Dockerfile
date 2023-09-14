# Use an official Python runtime as a parent image
FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN ls

FROM base AS python-deps

RUN pip install pipenv
RUN apt-get update && apt-get install libgl1 -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

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

