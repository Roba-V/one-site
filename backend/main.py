from fastapi import FastAPI

api = FastAPI()


@api.get("/")
def home():
    return {"message": "Hello World!"}
