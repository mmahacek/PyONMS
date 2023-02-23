# models.event.py


from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Union

from pyonms.models.node import ServiceType
from pyonms.utils import convert_time


class Severity(Enum):
    """Severity Levels"""

    INDETERMINATE = 1
    "Indeterminate"
    CLEARED = 2
    "Cleared"
    NORMAL = 3
    "Normal"
    WARNING = 4
    "Warning"
    MINOR = 5
    "Minor"
    MAJOR = 6
    "Major"
    CRITICAL = 7
    "Critical"


@dataclass
class EventParameter:
    name: str
    value: Union[int, str]
    type: str = "string"

    def _to_dict(self) -> dict:
        payload = {"parmName": self.name, "value": self.value}
        return payload

    def __hash__(self):
        return hash((self.name))


@dataclass(repr=False)
class Event:
    uei: str
    id: int = None
    label: str = None
    time: datetime = None
    source: str = None
    createTime: datetime = None
    description: str = None
    logMessage: str = None
    severity: Severity = None
    log: bool = None
    display: bool = None
    location: str = None
    nodeId: int = None
    nodeLabel: str = None
    ipAddress: str = None
    operatorInstructions: str = None
    host: str = None
    snmp: str = None
    snmpHost: str = None
    ifIndex: int = None
    parameters: List[Union[EventParameter, None]] = field(default_factory=list)
    serviceType: ServiceType = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.time, int):
            self.time = convert_time(self.time)
        if isinstance(self.createTime, int):
            self.createTime = convert_time(self.createTime)
        if isinstance(self.severity, str):
            self.severity = Severity[self.severity]
        if self.display == "Y":
            self.display = True
        elif self.display == "N":
            self.display = False
        if self.log == "Y":
            self.log = True
        elif self.log == "N":
            self.log = False
        self.parameters = [EventParameter(**parameter) for parameter in self.parameters]
        if self.serviceType and isinstance(self.serviceType, dict):
            self.serviceType = ServiceType(**self.serviceType)

    def __repr__(self) -> str:
        return f"Event(id={self.id}, uei={self.uei})"

    def _to_dict(self) -> dict:
        payload = {}
        for attr in dir(self):
            if attr[0] != "_" and getattr(self, attr):
                payload[attr.lower()] = getattr(self, attr)
        if isinstance(payload.get("severity"), Severity):
            payload["severity"] = self.severity.name
        if self.parameters:
            del payload["parameters"]
            payload["parms"] = []
            for parameter in self.parameters:
                payload["parms"].append(parameter._to_dict())
        return payload
