from fastapi import FastAPI

api = FastAPI()


@api.get("/")
def home():
    """
    Hello World API.

    Returns
    -------
    """
    return {"message": "Hello World!"}
