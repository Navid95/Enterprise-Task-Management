
from fastapi import FastAPI
from src.app.container import Container

from src.app.user_management.adapters.driving.fast_api.controllers.user_controller import (
    user_v1,
)
from src.app.interfaces.http.fast_api.handlers import register_api_exception_handler

container = Container()
app = FastAPI()
app.container = container
app.include_router(user_v1)
register_api_exception_handler(app)

