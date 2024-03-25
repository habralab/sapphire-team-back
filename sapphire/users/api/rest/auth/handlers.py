import fastapi

from sapphire.common.api.exceptions import HTTPForbidden, HTTPNotAuthenticated, HTTPNotFound
from sapphire.common.jwt.dependencies.rest import get_jwt_data
from sapphire.common.jwt.methods import JWTMethods
from sapphire.common.jwt.models import JWTData
from sapphire.users import broker, cache, database

from .schemas import AuthorizeRequest, AuthorizeResponse
from .utils import generate_authorize_response


async def logout(response: fastapi.Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


async def check(jwt_data: JWTData | None = fastapi.Depends(get_jwt_data)) -> JWTData | None:
    return jwt_data


async def sign_up(
        request: fastapi.Request,
        response: fastapi.Response,
        auth_data: AuthorizeRequest,
) -> AuthorizeResponse:
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        user = await database_service.get_user(session=session, email=auth_data.email)
        if user is not None:
            if user.password is not None:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                    detail="User already registered",
                )
            user = await database_service.update_user(
                session=session,
                user=user,
                password=auth_data.password,
            )
        else:
            user = await database_service.create_user(
                session=session,
                email=auth_data.email,
                password=auth_data.password,
            )

    return generate_authorize_response(jwt_methods=jwt_methods, response=response, user=user)


async def sign_in(
        request: fastapi.Request,
        response: fastapi.Response,
        auth_data: AuthorizeRequest,
):
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        user = await database_service.get_user(session=session, email=auth_data.email)
        if (
                user is None or
                not database_service.check_user_password(user=user, password=auth_data.password)
        ):
            raise HTTPNotAuthenticated()

    return generate_authorize_response(jwt_methods=jwt_methods, response=response, user=user)


async def change_password(
        request: fastapi.Request,
        email: str
):
    broker_service: broker.Service = request.app.service.broker
    database_service: database.Service = request.app.service.database
    cache_service: cache.Service = request.app.service.cache

    async with database_service.transaction() as session:
        user = await database_service.get_user(
            session=session,
            email=email
        )
        if not user:
            raise HTTPNotFound()

    secret_code = await cache_service.change_password_set_secret_code()  # in the future will be key
    # to get code to validate sent code with input code
    await broker_service.send_email_code(email=email, code=secret_code)

    return fastapi.Response(status_code=200)


async def reset_password(
        request: fastapi.Request,
        secret_code: str,
        email: str,
        new_password: str
):
    database_service: database.Service = request.app.service.database
    cache_service: cache.Service = request.app.service.cache

    if not cache_service.change_password_validate_code(secret_code=secret_code):
        raise HTTPForbidden()

    async with database_service.transaction() as session:
        user = await database_service.get_user(session=session, email=email)
        await database_service.update_user(
            session=session,
            user=user,
            password=new_password
        )
    return fastapi.Response(status_code=200, content="Password reset")
