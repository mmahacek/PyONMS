# models.requisition.py

from dataclasses import dataclass, field
from typing import Union

# from pyonms.utils import convert_time


@dataclass
class Requisition:
    foreign_source: str
    date_stamp: str
    last_import: str = None
    node: Union[list, None] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.node, dict):
            self.node = [self.node]
