
from fastapi import FastAPI
from src.app.container import Container

from src.app.user_management.adapters.driving.fast_api.controllers.user_controller import (
    user_v1,
)

container = Container()
app = FastAPI()
app.container = container
app.include_router(user_v1)


