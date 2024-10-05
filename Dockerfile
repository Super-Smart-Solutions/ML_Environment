# Use an official Python runtime as a parent image
FROM python:3.9.18 AS prod

RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# INSTALLING poetry
RUN pip install poetry==1.8.2

# Configuring poetry
# Disable virtual env, adding poetry to global env
# Configuring Cache
RUN poetry config virtualenvs.create false
RUN poetry config cache-dir /tmp/poetry_cache

# Set the working directory in the container
WORKDIR /app/src

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock /app/src

# Install dependencies using Poetry
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copying application
COPY . /app/src/
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

CMD ["/usr/local/bin/python", "-m", "app"]


FROM prod AS dev
#ENV NAME=development

RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --no-root --no-dev

