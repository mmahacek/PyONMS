# models.business_service.py

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional

import pyonms.models.exceptions


class Severity(Enum):
    INDETERMINATE = "Indeterminate"
    NORMAL = "Normal"
    WARNING = "Warning"
    MINOR = "Minor"
    MAJOR = "Major"
    CRITICAL = "Critical"


MAP_FUNCTIONS = ["Identity", "Increase", "Decrease", "Ignore", "SetTo"]
REDUCE_FUNCTIONS = [
    "HighestSeverity",
    "HighestSeverityAbove",
    "Threshold",
    "ExponentialPropagation",
]


@dataclass
class Attribute:
    key: str
    value: str

    def to_dict(self):
        return {"key": self.key, "value": self.value}


@dataclass(repr=False)
class MapFunction:
    type: str = "Identity"
    status: Severity = None
    properties: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.type not in MAP_FUNCTIONS:
            raise pyonms.models.exceptions.InvalidValueError(
                name="MapFunction", value="self.type", valid=MAP_FUNCTIONS
            )
        if self.type == "SetTo" and self.status:
            self.properties["status"] = self.status.value
        elif self.type == "SetTo" and not self.status and not self.properties:
            self.properties["status"] = Severity.INDETERMINATE.value

    def __repr__(self):
        if self.properties:
            return f"MapFunction(type={self.type}, properties={self.properties})"
        else:
            return f"MapFunction(type={self.type})"

    def to_dict(self):
        return {"type": self.type, "properties": self.properties}


@dataclass(repr=False)
class ReduceFunction:
    type: str = "HighestSeverity"
    threshold: float = 0.5
    above: Severity = Severity.INDETERMINATE
    base: float = 2
    properties: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.type not in REDUCE_FUNCTIONS:
            raise pyonms.models.exceptions.InvalidValueError(
                name="ReduceFunction", value=self.type, valid=REDUCE_FUNCTIONS
            )
        if self.type == "ExponentialPropagation" and not self.properties:
            self.properties["base"] = self.base
        elif self.type == "Threshold":
            if not self.properties:
                self.properties["threshold"] = self.threshold
            if self.threshold > 1:
                raise pyonms.models.exceptions.InvalidValueError(
                    name="Threshold", value=self.threshold, valid="decimal between 0-1"
                )
        elif self.type == "HighestSeverityAbove" and not self.properties:
            self.properties["threshold"] = self.above

    def __repr__(self):
        if self.type == "HighestSeverity":
            return f"ReduceFunction(type={self.type})"
        else:
            return f"ReduceFunction(type={self.type}, properties={self.properties})"

    def to_dict(self):
        return {"type": self.type, "properties": self.properties}


def _base_attributes():
    return {"attribute": []}


def _reduce_function():
    return ReduceFunction(type="HighestSeverity")


def _map_function():
    return MapFunction(type="Identity")


@dataclass(repr=False)
class IPService:
    service_name: str
    node_label: str
    ip_address: str
    id: int = None
    location: str = None

    def __repr__(self):
        return f"IPService(id={self.id}, node={self.node_label}, ip_address={self.ip_address}, service_name={self.service_name})"

    def __hash__(self):
        return hash((self.id))

    def to_dict(self):
        payload = {
            "service-name": self.service_name,
            "node-label": self.node_label,
            "ip-address": self.ip_address,
        }
        if self.id:
            payload["id"] = self.id
        if self.location:
            payload["location"] = self.location
        return payload


@dataclass(repr=False)
class ChildEdgeRequest:
    child_id: int = None
    weight: int = 1
    map_function: MapFunction = field(default_factory=_map_function)

    def __post_init__(self):
        if isinstance(self.map_function, dict):
            self.map_function = MapFunction(**self.map_function)

    def __repr__(self):
        return f"ChildEdgeRequest(child_id={self.child_id})"

    def __hash__(self):
        return hash((self.child_id))

    def to_dict(self):
        payload = {
            "map-function": self.map_function.to_dict(),
            "weight": self.weight,
            "child-id": self.child_id,
        }
        return payload


@dataclass(repr=False)
class ChildEdge:
    id: int
    location: str
    operational_status: str
    child_id: int = None
    weight: int = 1
    map_function: MapFunction = field(default_factory=_map_function)
    reduction_keys: list = field(default_factory=list)

    def __repr__(self):
        return f"ChildEdge(id={self.id}, child_id={self.child_id})"

    def __hash__(self):
        return hash((self.id))

    def to_dict(self):
        payload = {
            "id": self.id,
            "location": self.location,
            "operational-status": self.operational_status,
            "map-function": self.map_function,
            "weight": self.weight,
            "ip-service-id": self.ip_service_id,
        }
        return payload

    def request(self) -> ChildEdgeRequest:
        return ChildEdgeRequest(
            child_id=self.child_id,
            weight=self.weight,
            map_function=self.map_function,
        )


@dataclass(repr=False)
class IPServiceEdgeRequest:
    friendly_name: str
    ip_service_id: int = None
    weight: int = 1
    map_function: MapFunction = field(default_factory=_map_function)

    def __post_init__(self):
        if len(self.friendly_name) > 30:
            raise pyonms.models.exceptions.StringLengthError(
                30, value=self.friendly_name
            )
        if isinstance(self.map_function, dict):
            self.map_function = MapFunction(**self.map_function)

    def __repr__(self):
        return f"IPServiceEdgeRequest(friendly_name={self.friendly_name})"

    def __hash__(self):
        return hash((self.ip_service_id))

    def to_dict(self):
        payload = {
            "friendly-name": self.friendly_name,
            "map-function": self.map_function.to_dict(),
            "weight": self.weight,
            "ip-service-id": self.ip_service_id,
        }
        return payload


@dataclass(repr=False)
class IPServiceEdge:
    id: int
    location: str
    operational_status: str
    friendly_name: str
    ip_service_id: int = None
    weight: int = 1
    map_function: MapFunction = field(default_factory=_map_function)
    reduction_keys: list = field(default_factory=list)
    ip_service: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.ip_service:
            self.ip_service["service_name"] = self.ip_service.get("service-name")
            del self.ip_service["service-name"]
            self.ip_service["node_label"] = self.ip_service.get("node-label")
            del self.ip_service["node-label"]
            self.ip_service["ip_address"] = self.ip_service.get("ip-address")
            del self.ip_service["ip-address"]
            self.ip_service = IPService(**self.ip_service)
            self.ip_service_id = self.ip_service.id
        if self.map_function:
            self.map_function = MapFunction(**self.map_function)

    def __repr__(self):
        return f"IPServiceEdge(id={self.id}, friendly_name={self.friendly_name})"

    def __hash__(self):
        return hash((self.id))

    def to_dict(self):
        payload = {
            "id": self.id,
            "location": self.location,
            "operational-status": self.operational_status,
            "friendly-name": self.friendly_name,
            "map-function": self.map_function.to_dict(),
            "weight": self.weight,
            "ip-service-id": self.ip_service_id,
        }
        return payload

    def request(self) -> IPServiceEdgeRequest:
        return IPServiceEdgeRequest(
            friendly_name=self.friendly_name,
            ip_service_id=self.ip_service_id,
            weight=self.weight,
            map_function=self.map_function,
        )


@dataclass(repr=False)
class BusinessServiceRequest:
    name: str
    attributes: List[Optional[Attribute]] = field(default_factory=list)
    reduce_function: ReduceFunction = field(default_factory=_reduce_function)
    ip_service_edges: List[Optional[IPServiceEdgeRequest]] = field(default_factory=list)
    reduction_key_edges: List[Optional[str]] = field(default_factory=list)
    child_edges: List[Optional[ChildEdgeRequest]] = field(default_factory=list)
    application_edges: List[Optional[str]] = field(default_factory=list)
    parent_services: List[Optional[str]] = field(default_factory=list)

    def __repr__(self):
        return f"BusinessServiceRequest(name={self.name})"

    def to_dict(self):
        payload = {
            "name": self.name,
            "attributes": {"attribute": []},
            "reduce-function": self.reduce_function.to_dict(),
        }
        for attribute in self.attributes:
            payload["attributes"]["attribute"].append(attribute.to_dict())
            self.attributes = self.attributes
        if self.reduction_key_edges:
            payload["reduction-key-edges"] = self.reduction_key_edges
        if self.ip_service_edges:
            payload["ip-service-edges"] = [
                edge.to_dict() for edge in self.ip_service_edges
            ]
        if self.child_edges:
            payload["child-edges"] = [edge.to_dict() for edge in self.child_edges]
        if self.application_edges:
            payload["application-edges"] = self.application_edges
        if self.parent_services:
            payload["parent-services"] = self.parent_services
        return payload

    def add_attribute(self, attribute: Attribute):
        if attribute.key in [param.key for param in self.attributes]:
            self.attributes.remove(
                [param for param in self.attributes if param.key == attribute.key][0]
            )
        self.attributes.append(attribute)

    def update_edge(
        self, ip_edge: IPServiceEdgeRequest = None, child_edge: ChildEdgeRequest = None
    ):
        if isinstance(ip_edge, IPServiceEdgeRequest):
            if ip_edge.ip_service_id in [
                edge.ip_service_id for edge in self.ip_service_edges
            ]:
                self.ip_service_edges.remove(
                    [
                        edge
                        for edge in self.ip_service_edges
                        if edge.ip_service_id == ip_edge.ip_service_id
                    ][0]
                )
            self.ip_service_edges.append(ip_edge)
        if isinstance(child_edge, ChildEdgeRequest):
            if child_edge.child_id in [edge.child_id for edge in self.child_edges]:
                self.child_edges.remove(
                    [
                        edge
                        for edge in self.child_edges
                        if edge.child_id == child_edge.child_id
                    ][0]
                )
            self.child_edges.append(child_edge)


@dataclass(repr=False)
class BusinessService:
    id: int
    location: str
    operational_status: str
    name: str
    attributes: List[Optional[Attribute]] = field(default_factory=list)
    reduce_function: ReduceFunction = field(default_factory=_reduce_function)
    ip_services_edges: List[Optional[IPServiceEdge]] = field(default_factory=list)
    reduction_key_edges: List[Optional[str]] = field(default_factory=list)
    child_edges: List[Optional[ChildEdge]] = field(default_factory=list)
    application_edges: List[Optional[str]] = field(default_factory=list)
    parent_services: List[Optional[str]] = field(default_factory=list)

    def __post_init__(self):  # noqa C901
        if self.attributes:
            if isinstance(self.attributes, dict):
                attributes = []
                for attribute in self.attributes.get("attribute"):
                    attributes.append(Attribute(**attribute))
                self.attributes = attributes
        if self.ip_services_edges:
            if isinstance(self.ip_services_edges[0], dict):
                ip_edges = []
                for edge in self.ip_services_edges:
                    edge["operational_status"] = edge.get("operational-status")
                    del edge["operational-status"]
                    edge["map_function"] = edge.get("map-function")
                    del edge["map-function"]
                    edge["reduction_keys"] = edge.get("reduction-keys")
                    del edge["reduction-keys"]
                    edge["ip_service"] = edge.get("ip-service")
                    del edge["ip-service"]
                    edge["friendly_name"] = edge.get("friendly-name")
                    del edge["friendly-name"]
                    ip_edges.append(IPServiceEdge(**edge))
                self.ip_services_edges = ip_edges
        if self.child_edges:
            if isinstance(self.child_edges[0], dict):
                child_edges = []
                for edge in self.child_edges:
                    edge["operational_status"] = edge.get("operational-status")
                    del edge["operational-status"]
                    edge["map_function"] = edge.get("map-function")
                    del edge["map-function"]
                    edge["reduction_keys"] = edge.get("reduction-keys")
                    del edge["reduction-keys"]
                    edge["child_id"] = edge.get("child-id")
                    del edge["child-id"]
                    child_edges.append(ChildEdge(**edge))
                self.child_edges = child_edges
        if isinstance(self.reduce_function, dict):
            self.reduce_function = ReduceFunction(**self.reduce_function)

    def __repr__(self):
        return f"BusinessService(id={self.id}, name={self.name})"

    def to_dict(self):
        payload = {
            "name": self.name,
            "id": self.id,
            "location": self.location,
            "operational-status": self.operational_status,
            "attributes": {"attribute": []},
            "reduce-function": self.reduce_function.to_dict(),
        }
        for attribute in self.attributes:
            payload["attributes"]["attribute"].append(attribute.to_dict())
        if self.reduction_key_edges:
            payload["reduction-key-edges"] = self.reduction_key_edges
        if self.ip_services_edges:
            payload["ip-services-edges"] = [
                edge.to_dict() for edge in self.ip_services_edges
            ]
        if self.child_edges:
            payload["child-edges"] = self.child_edges
        if self.application_edges:
            payload["application-edges"] = self.application_edges
        if self.parent_services:
            payload["parent-services"] = self.parent_services
        return payload

    def request(self) -> BusinessServiceRequest:
        request = BusinessServiceRequest(
            name=self.name,
            attributes=self.attributes,
            reduce_function=self.reduce_function,
            reduction_key_edges=self.reduction_key_edges,
            application_edges=self.application_edges,
        )
        if self.ip_services_edges:
            request.ip_service_edges = [
                edge.request() for edge in self.ip_services_edges
            ]
        if self.child_edges:
            request.child_edges = [edge.request() for edge in self.child_edges]
        return request
