from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.app.container import Container
from src.app.infrastructure.persistence.db.session import init_engine, close_engine
from src.app.user_management.adapters.driving.fast_api.controllers.user_controller import (
    user_v1,
)
from src.app.interfaces.http.fast_api.handlers import register_api_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    init_engine()
    app.container = Container()
    yield
    # shutdown
    await close_engine()


app = FastAPI(lifespan=lifespan)
app.include_router(user_v1)
register_api_exception_handler(app)
