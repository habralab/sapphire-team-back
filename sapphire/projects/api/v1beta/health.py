from sapphire.common.api.schemas import HealthResponse
from sapphire.common.api.schemas.enums import ResponseStatus
from sapphire.common.package import get_version


async def health() -> HealthResponse:
    return HealthResponse(
        status=ResponseStatus.OK,
        version=get_version() or "0.0.0",
        name="Projects",
    )
