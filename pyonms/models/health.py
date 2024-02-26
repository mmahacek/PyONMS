# models.health.py

"Health models"

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Response:
    "Health status Response message"
    description: str
    status: str
    success: Optional[bool] = None
    message: Optional[str] = None

    def __post_init__(self):
        if self.status == "Success":
            self.success = True
        else:
            pass


@dataclass(repr=False)
class Health:
    "Health status class"
    healthy: Optional[bool] = None
    responses: List[Response] = field(default_factory=list)

    def __post_init__(self):
        responses = []
        for response in self.responses:
            responses.append(Response(**response))
        self.responses = responses

    def __repr__(self):
        return f"Health(healthy={self.healthy})"
