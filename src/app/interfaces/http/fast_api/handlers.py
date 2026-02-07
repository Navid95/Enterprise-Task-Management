from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.app.core.exceptions import DomainError
from src.app.interfaces.http.fast_api.api_exception import APIException, exc_mapper


def register_api_exception_handler(app: FastAPI):
        @app.exception_handler(DomainError)
        async def handler(request: Request, exc: DomainError):
            api_exc = exc_mapper(exc)
            return JSONResponse(
                status_code=api_exc.status_code,
                content=api_exc.detail
            )


