from enum import Enum


class ResponseStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
