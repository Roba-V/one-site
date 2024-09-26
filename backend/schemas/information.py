from pydantic import BaseModel


class World(BaseModel):
    message: str


class Version(BaseModel):
    version: str
