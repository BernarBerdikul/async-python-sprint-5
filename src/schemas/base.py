import orjson
from pydantic import BaseModel

__all__ = ("FastORMJsonModel",)


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FastORMJsonModel(BaseModel):
    """Модель с быстрым json-сериализатором."""

    # Standard config settings.
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
