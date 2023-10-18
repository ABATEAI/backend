#!/usr/bin/env python3

import google.generativeai as palm
import os
import tomllib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from square.client import Client

description = """
ABATE AI API reduces to increase via the Google PaLM and Square APIs
"""

# See https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(
    title="ABATEAI",
    description=description,
    summary="ABATE AI Backend Python API",
    version="0.0.2",
    contact={
        "name": "ABATE AI",
        "url": "https://abateai.com/api/contact",
        "email": "abateai.hackathon@gmail.com",
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
palm_api_key = ""

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

            if "GOOGLE_DEV" in cfg:
                palm_api_key = cfg["GOOGLE_DEV"]["PALM_API_KEY"]
            else:
                raise RuntimeError("[index.py] GOOGLE_DEV not in config.toml")
        except RuntimeError:
            print("[index.py] Error: Unable to read DEV configuration")
        except tomllib.TOMLDecodeError:
            print("[index.py] Error: config.toml is invalid")
        finally:
            if (
                not square_access_token
                or not square_environment
                or not square_location_id
                or not palm_api_key
            ):
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

if not palm_api_key:
    if "PALM_API_KEY" in os.environ:
        palm_api_key = os.environ["PALM_API_KEY"]
    else:
        raise RuntimeError("[index.py] Unable to access PALM_API_KEY")


palm.configure(api_key=palm_api_key)
square_client = Client(access_token=square_access_token, environment=square_environment)


@app.get("/api/contact")
async def contact():
    return {"name": "Jeffry Lew", "GitHub": "https://github.com/jeffrylew"}


@app.get("/api/google")
async def hello_google():
    return {"message": "Hello Google"}


@app.get("/api/square")
async def hello_square():
    return {"status": "success", "message": "Hello Square"}


@app.get("/api/square/location")
async def get_location():
    # Referenced
    # - https://developer.squareup.com/docs/sdks/python/quick-start
    # - https://github.com/square/connect-api-examples/blob/master
    #   /connect-examples/v2/python_payment/main.py
    result = square_client.locations.retrieve_location(location_id=square_location_id)

    if result.is_success():
        return result.body
    else:
        return result.errors


@app.get("/api/square/list_catalog")
async def get_list_catalog():
    """Get all objects from catalog of main type ITEM, ITEM_OPTION, CATEGORY"""

    # Referenced
    # - https://developer.squareup.com/docs/catalog-api/retrieve-catalog-objects
    result = square_client.catalog.list_catalog()

    if result.is_success():
        return result.body
    else:
        return result.errors


@app.get("/api/square/catalog_objects")
async def get_catalog_objects():
    """Get catalog items with object_ids and related objects with type IMAGE"""

    # Referenced
    # - https://developer.squareup.com/explorer/square/catalog-api
    #   /batch-retrieve-catalog-objects
    result = square_client.catalog.batch_retrieve_catalog_objects(
        body={
            "object_ids": [
                "I5QQC4YOLNMYVZND75LRXRDE",
                "TIQ4SQUZNQ4NNCVAJOLOAACG",
                "CFIRRK6YQKM3SVGCGCBCZXHQ",
                "QFKYKEHRLE4M7VVNFCYPFQTM",
                "ZYZIRJRRLNCRLGDZCDIR3YWR",
                "I3YN42OW5HWKPBDGHQMRQUB7",
                "RWJ4KNA2A4JYNHW4J7DDXWFX",
                "ETA5ZHNWBGJJF6237YGDBTU3",
                "26OLJ6AWTE3D4BPRT7AJFE4L",
                "QA2VV4SGFW7QQCWDGPBCXB6P",
                "GAWGBZLSMM5CTOIB4DPAEYPJ",
                "ZGU6HONP33W55ULW4IJKGCDB",
                "MN64RZJZQC3H6AF4VSOSNLGN",
                "WKSGU6KEK3U7PE3VZ42FD76Z",
                "QOGEUQQ2NVLIVKCMEYRDI7RC",
                "OTDQYQUMGRCTDERRWEBFEPJG",
                "VHDYW7JO3SHX4AXO3M4GYAVX",
                "L3MNZU5UVEMAIVTQR2BJR7FF",
                "SO4DQXCQ3XZBWWZF3CMH7YBJ",
                "47E7RO5Q25VWKTED4XTPNQ72",
                "FU4XUWVLOZUU5XLTOKAIO3TI",
                "CWRVJDCTEK6L4X7TMSUHEGUB",
                "3QKF4LOA54QCY2422T2WNOVD",
                "4LOUBTQZT6IATTSTWIJQEUW4",
                "B377XDOQR7AZVBZW5TI4I3L6",
                "V7UF5ZNSFRTVPL66D4Z37X4E",
                "4E77G6M4D664ALW37VNPAP5K",
                "XXOCCUKY33UG4LCEMYA6ETXB",
                "SQRLCH2DEQKTXYMD6IQYJ7MY",
                "JXYNKKUX5GFATHIYNZFGTO2P",
                "5HPCLW3JYWH7MVFHRK3JDG3G",
                "2E2727SDOEFX7L3CDGML2HNS",
            ],
            "include_deleted_objects": False,
            "include_related_objects": True,
        }
    )

    if result.is_success():
        return result.body
    else:
        return result.errors


@app.get("/api/square/categories")
async def get_catalog_categories():
    """Get catalog objs of type CATEGORY (Chicken, Classic, Supreme, Veggie)"""

    # Referenced
    # - https://developer.squareup.com/explorer/square/catalog-api
    #   /search-catalog-objects
    result = square_client.catalog.search_catalog_objects(
        body={
            "object_types": [
                "CATEGORY",
            ],
            "include_deleted_objects": False,
            "include_related_objects": True,
        }
    )

    if result.is_success():
        return result.body
    else:
        return result.errors


@app.get("/api/square/images")
async def get_catalog_images():
    """Get catalog objects with type IMAGE"""

    # Referenced
    # - https://developer.squareup.com/explorer/square/catalog-api
    #   /search-catalog-objects
    result = square_client.catalog.search_catalog_objects(
        body={
            "object_types": [
                "IMAGE",
            ],
            "include_deleted_objects": False,
            "include_related_objects": True,
        }
    )

    if result.is_success():
        return result.body
    else:
        return result.errors


@app.get("/api/square/sizes")
async def get_catalog_sizes():
    """Get catalog objects with type ITEM_OPTION (they specify pizza sizes)"""

    # Referenced
    # - https://developer.squareup.com/explorer/square/catalog-api
    #   /search-catalog-objects
    result = square_client.catalog.search_catalog_objects(
        body={
            "object_types": [
                "ITEM_OPTION",
            ],
            "include_deleted_objects": False,
            "include_related_objects": True,
        }
    )

    if result.is_success():
        return result.body
    else:
        return result.errors


@app.get("/api/google/keep/{item_name}")
async def get_persuasive_message(item_name: str):
    """Get persuasive message from MakerSuite to avoid removing cart item"""

    prompt = f"""
    A customer is about to remove {item_name.replace("_", " ")} from her online
    shopping cart. Persuade her to keep it in plain text.
    """
    completion = palm.generate_text(
        model="models/text-bison-001",
        prompt=prompt,
        temperature=0.7,
        max_output_tokens=150,
    )

    return completion.result
