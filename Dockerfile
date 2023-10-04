# syntax=docker/dockerfile:1

# Set base image, has Python 3.11.5 and pip 23.2.1
FROM python:3.11.5 AS builder

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set working directory in container
WORKDIR /usr/src

# Copy dependencies file to the working directory
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy local src directory content
COPY src/ ./app

# Set labels
LABEL vendor1="ABATE AI"
LABEL com.abateai.release-date="2023-10-04"
LABEL com.abateai.version="1.0.2"

# If running behind a proxy like Nginx or Traefik add --proxy-headers
CMD ["bash", "-c", "uvicorn app.index:app --host 0.0.0.0 --port ${PORT:-8000}"]

# # Following instructions are for slimming down image
# # See https://www.docker.com/blog/containerized-python-development-part-1/

# # Set base image for 1st stage
# FROM python:3.11.5 AS builder

# # Copy dependencies file
# COPY requirements.txt ./

# # Install dependencies to the local user directory (i.e. /root/.local)
# RUN pip install --no-cache-dir --user --upgrade -r requirements.txt

# # 2nd stage
# FROM python:3.11.5-slim AS runner

# # Set working directory in container
# WORKDIR /usr/src

# # Copy only the dependencies installation from the 1st stage image
# COPY --from=builder /root/.local /root/.local

# # Copy local src directory content to working directory
# COPY src/ ./app

# # Update PATH environment variable
# ENV PATH=/root/.local:$PATH

# # Use default entrypoint
# ENTRYPOINT [ "/bin/sh", "-c" ]
