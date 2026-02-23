from fastapi import FastAPI
from src.app.container import Container
from src.app.infrastructure.persistence.db.session import init_engine, close_engine
from src.app.user_management.adapters.driving.fast_api.controllers.user_controller import (
    user_v1,
)
from src.app.interfaces.http.fast_api.handlers import register_api_exception_handler

container = Container()
app = FastAPI()
app.container = container


@app.on_event("startup")
async def on_startup():
    init_engine()


@app.on_event("shutdown")
async def on_shutdown():
    await close_engine()


app.include_router(user_v1)
register_api_exception_handler(app)
