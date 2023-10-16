from typing import Annotated

from fastapi import Depends, Query
from pydantic import conint


async def pagination(

        page: conint(ge=1) = Query(1, description="Page number"),
        per_page: conint(ge=1) = Query(10, description="Number of items per page"),

    ) -> dict:

    return {"page": page, "per_page": per_page}
