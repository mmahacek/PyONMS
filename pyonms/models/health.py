# models.health.py

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Response:
    description: str
    status: str
    success: bool = None
    message: Optional[str] = None

    def __post_init__(self):
        if self.status == "Success":
            self.success = True
        else:
            pass


@dataclass(repr=False)
class Health:
    healthy: bool = None
    responses: List[Response] = field(default_factory=list)

    def __post_init__(self):
        responses = []
        for response in self.responses:
            responses.append(Response(**response))
        self.responses = responses

    def __repr__(self):
        return f"Health(healthy={self.healthy})"
