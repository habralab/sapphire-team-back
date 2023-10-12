import fastapi


class HTTPNotAuthenticated(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )
