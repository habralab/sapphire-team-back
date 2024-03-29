import fastapi

from collabry.common.api.exceptions import HTTPNotAuthenticated, HTTPNotFound
from collabry.common.jwt.dependencies.rest import get_jwt_data
from collabry.common.jwt.methods import JWTMethods
from collabry.common.jwt.models import JWTData
from collabry.users import broker, cache, database

from .schemas import (
    AuthorizeRequest,
    AuthorizeResponse,
    ChangePasswordRequest,
    ResetPasswordRequest,
)
from .utils import generate_authorize_response


async def logout(response: fastapi.Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


async def check(jwt_data: JWTData | None = fastapi.Depends(get_jwt_data)) -> JWTData | None:
    return jwt_data


async def sign_up(
        request: fastapi.Request,
        response: fastapi.Response,
        data: AuthorizeRequest,
) -> AuthorizeResponse:
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    broker_service: broker.Service = request.app.service.broker
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        user = await database_service.get_user(session=session, email=data.email)
        if user is not None:
            if user.password is not None:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                    detail="User already registered",
                )
            user = await database_service.update_user(
                session=session,
                user=user,
                password=data.password,
            )
        else:
            user = await database_service.create_user(
                session=session,
                email=data.email,
                password=data.password,
            )
            await broker_service.send_registration_email(user=user)

    return generate_authorize_response(jwt_methods=jwt_methods, response=response, user=user)


async def sign_in(
        request: fastapi.Request,
        response: fastapi.Response,
        data: AuthorizeRequest,
):
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        user = await database_service.get_user(session=session, email=data.email)
        if (
                user is None or
                not database_service.check_user_password(user=user, password=data.password)
        ):
            raise HTTPNotAuthenticated()

    return generate_authorize_response(jwt_methods=jwt_methods, response=response, user=user)


async def reset_password_request(request: fastapi.Request, data: ResetPasswordRequest):
    broker_service: broker.Service = request.app.service.broker
    database_service: database.Service = request.app.service.database
    cache_service: cache.Service = request.app.service.cache

    async with database_service.transaction() as session:
        user = await database_service.get_user(session=session, email=data.email)
        if not user:
            raise HTTPNotFound()

    code = await cache_service.reset_password_set_code(email=data.email)
    await broker_service.send_reset_password_email(user=user, code=code)


async def change_password(request: fastapi.Request, data: ChangePasswordRequest):
    database_service: database.Service = request.app.service.database
    cache_service: cache.Service = request.app.service.cache

    async with database_service.transaction() as session:
        user = await database_service.get_user(session=session, email=data.email)

    if not user or not cache_service.reset_password_validate_code(email=data.email, code=data.code):
        raise HTTPNotFound()

    async with database_service.transaction() as session:
        await database_service.update_user(
            session=session,
            user=user,
            password=data.new_password,
        )
