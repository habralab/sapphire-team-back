from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON,
        datetime: DateTime(timezone=True),
    }
