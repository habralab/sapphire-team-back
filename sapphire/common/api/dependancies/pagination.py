from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def pag_params(page: int = 1, per_page: int = 10):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="page_number must be greater than or equal to 1.",
        )

    if per_page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="per_page must be greater than or equal to 1.",
        )

    return {"page": page, "per_page": per_page}