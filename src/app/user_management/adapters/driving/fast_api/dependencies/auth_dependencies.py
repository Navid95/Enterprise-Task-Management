from fastapi import Request


def get_authentication_service(request: Request):
    return request.app.container.get_auth_service()
