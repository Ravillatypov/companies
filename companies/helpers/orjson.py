from typing import Any

from orjson import orjson
from starlette.responses import JSONResponse

# flake8: noqa


class OrjsonResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)
