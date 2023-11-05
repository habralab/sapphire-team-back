from typing import Type

from pydantic import BaseModel

from sapphire.common.utils.empty import Empty


class SkillsFiltersRequest(BaseModel):
    query_text: str | Type[Empty] = Empty
