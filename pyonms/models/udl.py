# models.udl.py

"User-Defined Links models"

from dataclasses import dataclass
from typing import Optional, Union

from pyonms.models.node import Node


@dataclass
class UserDefinedLink:
    "UDL class"
    node_id_a: Union[int, Node]
    node_id_z: Union[int, Node]
    component_label_a: str
    component_label_z: str
    db_id: Optional[int] = None
    link_id: Optional[str] = None
    owner: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.node_id_a, Node):
            self.node_id_a = self.node_id_a.id
        if isinstance(self.node_id_z, Node):
            self.node_id_z = self.node_id_z.id
        if not self.link_id:
            self.link_id = f"n{self.node_id_a}:{self.component_label_a}->n{self.node_id_z}:{self.component_label_z}"

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        payload = {
            "owner": self.owner,
            "node-id-a": self.node_id_a,
            "component-label-a": self.component_label_a,
            "node-id-z": self.node_id_z,
            "component-label-z": self.component_label_z,
            "link-id": self.link_id,
            "db-id": self.db_id,
        }
        return payload

    _to_dict = to_dict
