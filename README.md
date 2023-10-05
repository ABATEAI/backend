# ABATE AI backend
Backend Python API source code for abateai.com

## Quick start

### Prerequisites for Development

- [GitHub Account](https://github.com/)
- [Docker Hub Account](https://hub.docker.com/)
- [Docker Engine](https://docs.docker.com/get-docker/) and
  [Docker Compose](https://docs.docker.com/compose/install/) as standalone
  binaries OR [Docker Desktop](https://docs.docker.com/desktop/), which is
  simpler and includes Docker Engine and Docker Compose

### Installation

First, clone the repo and change directory into it with

```bash
$ git clone https://github.com/ABATEAI/backend.git
$ cd backend
```

Assuming you have installed Docker Desktop, open the application and sign in.
Then build the Docker image for the ABATE AI backend API with `docker-compose`

```bash
$ docker-compose build
```

Verify the image was created by running the following in a terminal

```bash
$ docker image ls
REPOSITORY                      TAG         IMAGE ID       CREATED        SIZE
backend-abateai_api             latest      some_hash_01   1 minute ago   1.16GB
```

### Development

ABATE AI's API builds off the Google Vertex AI API and Square APIs.
The following links can be referenced during development.

- Square Python SDK: https://pypi.org/project/squareup/
- Square SDK Quickstart:
  https://developer.squareup.com/docs/sdks/python/quick-start
- Square Python Payment Example:
  https://github.com/square/connect-api-examples/tree/master/connect-examples/v2/python_payment
- Vertex AI Python SDK: https://pypi.org/project/google-cloud-aiplatform/
- Timeseries Insights API Overview:
  https://cloud.google.com/timeseries-insights/docs/overview

The development server is started with

```bash
$ docker-compose up -d
```

You can also build and start the server with the combined command

```bash
$ docker-compose up -d --build
```

Responses from the ABATE AI API that are viewable can be seen at
`http://localhost:8000/api/<api_path>`.

Any changes to [src/index.py](src/index.py) will show up in the browser
(if viewable) after refreshing.

Once you are done with development, shut down the server with

```bash
$ docker-compose down
```

and quit Docker Desktop (don't just exit, ensure you power down the engine).

### Suggestions

Backend development suggestions can be requested by opening a new ticket at
https://github.com/ABATEAI/backend/issues.
