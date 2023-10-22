from sapphire.common.api.schemas.health import HealthResponse
from sapphire.common.utils.package import get_version


async def health() -> HealthResponse:
    return HealthResponse(
        name="Messenger",
        version=get_version() or "0.0.0",
    )
