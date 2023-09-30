from sapphire.common.api.schemas import BaseResponse


class JWTTokensResponse(BaseResponse):
    access_token: str
    refresh_token: str
