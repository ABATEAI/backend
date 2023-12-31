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

Copy [config.toml.example](config.toml.example) and rename the copy to
`config.toml`. Populate the configuration fields with development values.
Please reach out to @jeffrylew for the specific values. Make sure `config.toml`
does not get version controlled or added to GitHub! It has been added to
[.gitignore](.gitignore), [.dockerignore](.dockerignore), and
[.gcloudignore](.gcloudignore) to avoid leaking credentials.

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

ABATE AI's API builds off the Google MakerSuite API and Square APIs.
The following links can be referenced during development.

- Square Python SDK: https://pypi.org/project/squareup/
- Square SDK Quickstart:
  https://developer.squareup.com/docs/sdks/python/quick-start
- Square Python Payment Example:
  https://github.com/square/connect-api-examples/tree/master/connect-examples/v2/python_payment
- Google Generative AI Python Client: https://pypi.org/project/google-generativeai/
- PaLM API Quickstart:
  https://developers.generativeai.google/tutorials/text_quickstart

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

### Production

Environment variables with the same names as those in
[config.toml.example](config.toml.example) need to be defined in the
production environment prior to merging any backend branches into main.

### Suggestions

Backend development suggestions can be requested by opening a new ticket at
https://github.com/ABATEAI/backend/issues.
