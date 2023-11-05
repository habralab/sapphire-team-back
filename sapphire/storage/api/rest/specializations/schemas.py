from typing import Type

from pydantic import BaseModel

from sapphire.common.utils.empty import Empty


class SpicializationFiltersRequest(BaseModel):
    query_data: str | Type[Empty] = Empty
