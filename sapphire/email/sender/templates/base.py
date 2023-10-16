import email.message
import enum
import pathlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Literal

import yaml
from pydantic import BaseModel


class BodyPartTypeEnum(str, enum.Enum):
    TEXT = "text"
    HTML = "html"


class BodyPart(BaseModel):
    def render(self, data: dict[str, Any]) -> email.message.Message:
        raise NotImplementedError


class TextBodyPart(BodyPart):
    type: Literal[BodyPartTypeEnum.TEXT.value]
    text: str
    encoding: str = "utf-8"

    def render(self, data: dict[str, Any]) -> MIMEText:
        return MIMEText(self.text.format(**data), "plain", self.encoding)


class HTMLBodyPart(BodyPart):
    type: Literal[BodyPartTypeEnum.HTML.value]
    text: str
    encoding: str = "utf-8"

    def render(self, data: dict[str, Any]) -> MIMEText:
        return MIMEText(self.text.format(**data), "html", self.encoding)


class Template(BaseModel):
    name: str
    subject: str
    body: list[TextBodyPart | HTMLBodyPart]

    def __new__(cls, name: str):
        filename = f"{name}.yaml"
        filepath = pathlib.Path(__file__).parent / filename
        with open(filepath, "rt") as template_file:
            data = yaml.safe_load(template_file)

        return super().__new__(**data)

    def render(self, recipient: str, sender: str, data: dict[str, Any]) -> MIMEMultipart:
        message = MIMEMultipart()

        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = self.subject.format(**data)
        for part in self.body:
            message.attach(part.render(data=data))

        return message
