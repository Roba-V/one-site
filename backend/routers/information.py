from fastapi import APIRouter

import backend.schemas.information as information_schema
from backend.common import constants as cst

router = APIRouter()


@router.get("/hello", response_model=information_schema.World)
async def say_world():
    return information_schema.World(message="World!")


@router.get("/version", response_model=information_schema.Version)
async def get_version():
    return information_schema.Version(version=cst.API_VERSION)
