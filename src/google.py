from fastapi import FastAPI

gapp = FastAPI()


@gapp.get("/api/google")
async def hello_google():
    return {"message": "Hello Google"}
