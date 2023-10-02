from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/api/google")
async def hello_google():
    return {"message": "Hello Google"}


@app.get("/api/square")
async def hello_square():
    return {"status": "success", "message": "Hello Square"}
