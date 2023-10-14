from typing import Annotated

from fastapi import Depends
from pydantic import conint


async def pagination(page: conint(ge=1) = 1, per_page: conint(ge=1) = 10) -> dict:
    return {"page": page, "per_page": per_page}
