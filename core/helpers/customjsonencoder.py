from json import JSONEncoder
import uuid
from typing import Any


class CustomJSONEncoder(JSONEncoder):

    def default(self, value: Any) -> Any:
        if isinstance(value, uuid.UUID):
            return str(value)
        return super(CustomJSONEncoder, self).default(value)
