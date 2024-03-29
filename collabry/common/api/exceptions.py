import fastapi


class HTTPNotAuthenticated(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )


class HTTPForbidden(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )


class HTTPNotFound(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Not found.",
        )


class HTTPInternalServerError(fastapi.HTTPException):
    def __init__(self):
        super().__init__(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
