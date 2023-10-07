#!/usr/bin/env python3

import os
import tomllib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from square.client import Client

description = """
ABATE AI API reduces to increase via the Google Vertex AI and Square APIs
"""

# See https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title="ABATEAI",
    description=description,
    summary="ABATE AI Backend Python API",
    version="0.0.1",
    contact={
        "name": "ABATE AI",
        "url": "https://www.abateai.com/contact/",
        "email": "support@abateai.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


# Needed so FastAPI server can accept forwarded requests in production
# See https://codevoweb.com/integrate-fastapi-framework-with-nextjs-and-deploy/
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Get credentials from config.toml (development)
# or from environment variable (production)
square_access_token = ""
square_environment = ""
square_location_id = ""

# If CONFIG_TOML_FILE is defined, read configuration/credentials from it
if "CONFIG_TOML_FILE" in os.environ:
    with open(os.environ["CONFIG_TOML_FILE"], "rb") as toml_file:
        try:
            cfg = tomllib.load(toml_file)

            if "SQUARE_DEV" in cfg:
                square_access_token = cfg["SQUARE_DEV"]["SQUARE_ACCESS_TOKEN"]
                square_environment = cfg["SQUARE_DEV"]["SQUARE_ENVIRONMENT"]
                square_location_id = cfg["SQUARE_DEV"]["SQUARE_LOCATION_ID"]
            else:
                raise RuntimeError("[index.py] SQUARE_DEV not in config.toml")
        except RuntimeError:
            print("[index.py] Error: Unable to read SQUARE_DEV configuration")
        except tomllib.TOMLDecodeError:
            print("[index.py] Error: config.toml is invalid")
        finally:
            if (not square_access_token or
                not square_environment or
                not square_location_id):
                print("[index.py] Retrieving configuration another way...")

# Read configuration/credentials from environment variables
if not square_access_token:
    if "SQUARE_ACCESS_TOKEN" in os.environ:
        square_access_token = os.environ["SQUARE_ACCESS_TOKEN"]
    else:
        raise RuntimeError("[index.py] Unable to access SQUARE_ACCESS_TOKEN")

if not square_environment:
    if "SQUARE_ENVIRONMENT" in os.environ:
        square_environment = os.environ["SQUARE_ENVIRONMENT"]
    else:
        raise RuntimeError("[index.py] Unable to access SQUARE_ENVIRONMENT")
    
if not square_location_id:
    if "SQUARE_LOCATION_ID" in os.environ:
        square_location_id = os.environ["SQUARE_LOCATION_ID"]
    else:
        raise RuntimeError("[index.py] Unable to access SQUARE_LOCATION_ID")


square_client = Client(
    access_token=square_access_token,
    environment=square_environment)


@app.get("/api/google")
async def hello_google():
    return {"message": "Hello Google"}


@app.get("/api/square")
async def hello_square():
    return {"status": "success", "message": "Hello Square"}

@app.get("api/square/locations")
async def get_locations():
    # Referenced
    # - https://developer.squareup.com/docs/sdks/python/quick-start
    # - https://github.com/square/connect-api-examples/blob/master
    #   /connect-examples/v2/python_payment/main.py
    result = square_client.locations.retrieve_location(
        location_id=square_location_id)
    
    if result.is_success():
        return result.body
    else:
        return result.errors
