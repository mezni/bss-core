from dataclasses import dataclass

import uuid


@dataclass(frozen=True)
class RequestContext:
    request_id: str

    @classmethod
    def create(cls) -> "RequestContext":
        return cls(
            request_id=str(uuid.uuid4())
        )