from fastapi import FastAPI

from backend.common import constants as cst
from backend.common import messages as msg
from backend.common.core.config import config
from backend.common.core.extensions import init_app, lifespan
from backend.routers import authentication, information, user

app = FastAPI(
    debug=config.DEBUG,
    title=config.API_NAME,
    summary=config.API_SUMMARY,
    version=cst.API_VERSION,
    openapi_url=f"{config.API_URL}/openapi.json",
    lifespan=lifespan,
)

init_app(app)

app.include_router(authentication.router, tags=[msg.MSG_LOGIN])
app.include_router(user.router, prefix=cst.PATH_USER, tags=[msg.MSG_USER])
app.include_router(information.router, tags=[msg.MSG_OTHER])
