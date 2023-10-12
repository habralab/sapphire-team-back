import pathlib

import yaml
from pydantic import BaseModel


class Template(BaseModel):
    type: str
    subject: str
    body: str

    def __new__(cls, name: str):
        filename = f"{name}.yaml"
        filepath = pathlib.Path(__file__).parent / filename
        with open(filepath, "rt") as template_file:
            data = yaml.safe_load(template_file)

        return super().__new__(**data)    
