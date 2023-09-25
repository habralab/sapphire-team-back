from aiohttp import web
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import secrets
from config import config
from oauthlib.oauth2 import WebApplicationClient
import aiohttp
from sapphire.users.oauth_schemas.common import ErrorResponse
from  sapphire.users.oauth_schemas.oauth import TokenResponse

router = APIRouter()
state = secrets.token_urlsafe(16)
client = WebApplicationClient(config.client_id)


@router.get('/authorize', response_class=RedirectResponse)
async def redirect_to_auth(scope: list = []):
    return client.prepare_request_uri(
        uri=config.server_authorization_url,
        redirect_uri=config.callback_url,
        skope=scope,
        state=state,
    )


@router.get('/tocken')
async def oauth2(request: web.Request):
    code = request.query["code"]
    state = request.query["state"]
    if state != state:
        return ErrorResponse(message='')
    # Getting access_token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "redirect_uri": config.callback_url,
    }
    async with aiohttp.request(method="POST", url=config.server_token_url, data=data) as response:
        data = await response.json()

    # Getting info about user
    access_token = data["access_token"]
    headers = {"Authorization": f"Token {access_token}"}
    async with aiohttp.request(method="GET", url=config.user_info_token_url, headers=headers) as response:
        user_data = await response.json()

    return web.Response(text=user_data["user"]["email_normalized"])