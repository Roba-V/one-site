from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    """
    Hello World API.

    Returns
    -------
    """
    return {"message": "Hello World!"}
