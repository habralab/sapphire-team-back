from datetime import datetime

import fastapi


def set_cookie(
        response: fastapi.Response,
        name: str,
        value: str,
        expires: datetime,
) -> fastapi.Response:
    response.set_cookie(
        key=name,
        value=value,
        expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        path="/",
        secure=True,
        httponly=True,
        samesite="strict",
    )

    return response
