from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.common import constants as cst
from backend.common import messages as msg
from backend.common.core.config import config
from backend.common.core.log import logger

logger.debug(msg.D_API_CFG_LOADED % config)
logger.debug("Initialisation process completed.")
app = FastAPI(
    debug=config.DEBUG,
    title=config.API_NAME,
    summary=config.API_SUMMARY,
    version=cst.API_VERSION,
    openapi_url=f"{config.API_URL}/openapi.json",
)

# Set all CORS enabled origins
if config.API_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=[str(origin).strip("/") for origin in config.API_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/hello_world/")
async def home():
    """
    Hello World API.

    Returns
    -------
    """
    logger.info("Hello World API Processing Start")
    return {"message": "Hello World!"}
