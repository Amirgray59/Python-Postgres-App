from typing import Dict
from app.domain.models import ItemResponse
import uuid

FakeDB = Dict[str, ItemResponse]


def get_db() -> FakeDB:
    return {}
