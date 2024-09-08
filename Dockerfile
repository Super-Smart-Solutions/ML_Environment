# Use an official Python runtime as a parent image
FROM python:3.9.18 as prod

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
COPY pyproject.toml poetry.lock ./app/src

# Install dependencies using Poetry
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main

# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*



# Copying actual application
COPY . /app/src/
RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main


# Copy the rest of the application code
COPY . .

# Define environment variable
ENV NAME=production

# Run the FastAPI app with uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
