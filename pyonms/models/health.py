# models.health.py

from dataclasses import dataclass

from typing import List, Optional


@dataclass
class Response:
    description: str
    status: str
    message: Optional[str] = None


@dataclass(repr=False)
class Health:
    healthy: bool
    responses: List[Response]

    def __post_init__(self):
        responses = []
        for response in self.responses:
            responses.append(Response(**response))
        self.responses = responses

    def __repr__(self):
        return f"Health(healthy={self.healthy})"
