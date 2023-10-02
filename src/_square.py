from fastapi import FastAPI

sapp = FastAPI()


@sapp.get("/api/square")
async def hello_square():
    return {"message": "Hello Square"}
