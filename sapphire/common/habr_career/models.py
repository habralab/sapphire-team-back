from pydantic import BaseModel, PositiveInt


class Skill(BaseModel):
    id: PositiveInt
    title: str


class Specialization(BaseModel):
    id: PositiveInt
    title: str


class CareerTrack(BaseModel):
    login: str
    full_name: str
    avatar: str
    skills: list[Skill]
    specializations: list[Specialization]
