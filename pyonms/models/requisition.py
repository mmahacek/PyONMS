# models.requisition.py

from dataclasses import dataclass  # , field
from typing import Union

# from pyonms.utils import convert_time


@dataclass
class Requisition:
    foreign_source: str
    date_stamp: str
    last_import: str
    node: Union[dict, list]
