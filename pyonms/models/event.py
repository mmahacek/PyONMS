# models.event.py

"""Event models"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Union

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
    """Event Parameter"""

    name: str
    value: Union[int, str]
    type: str = "string"

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        payload = {"parmName": self.name, "value": self.value}
        return payload

    _to_dict = to_dict

    def __hash__(self):
        return hash((self.name))


@dataclass(repr=False)
class Event:
    """OnmsEvent Model"""

    uei: str
    id: Optional[int] = None
    label: Optional[str] = None
    time: Optional[datetime] = None
    source: Optional[str] = None
    createTime: Optional[datetime] = None
    description: Optional[str] = None
    logMessage: Optional[str] = None
    severity: Optional[Severity] = Severity.INDETERMINATE
    log: Optional[bool] = None
    display: Optional[bool] = None
    location: Optional[str] = None
    nodeId: Optional[int] = None
    nodeLabel: Optional[str] = None
    ipAddress: Optional[str] = None
    operatorInstructions: Optional[str] = None
    host: Optional[str] = None
    snmp: Optional[str] = None
    snmpHost: Optional[str] = None
    ifIndex: Optional[int] = None
    parameters: Dict[str, Union[dict, EventParameter]] = field(default_factory=dict)
    serviceType: Optional[ServiceType] = None

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
        parameters = [EventParameter(**parameter) for parameter in self.parameters]
        self.parameters = {parm.name: parm for parm in parameters}
        if self.serviceType and isinstance(self.serviceType, dict):
            self.serviceType = ServiceType(**self.serviceType)

    def __repr__(self) -> str:
        return f"Event(id={self.id}, uei={self.uei})"

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        payload = {}
        for key, value in vars(self).items():
            if key == "description":
                key = "descr"
            elif key == "operatorInstructions":
                key = "operinstruct"
            elif key == "ipAddress":
                key = "interface"
            elif key in ["logMessage", "display", "id"]:
                continue
            if value:
                payload[key.lower()] = value
        if self.severity:
            payload["severity"] = self.severity.name
        if self.parameters:
            del payload["parameters"]
            payload["parms"] = []
            for parameter in self.parameters.values():
                payload["parms"].append(parameter.to_dict())  # type: ignore
        return payload

    _to_dict = to_dict

    def set_parameter(
        self,
        name: str,
        value: str,
        type: str = "string",  # pylint: disable=redefined-builtin
    ) -> None:
        """Set or remove an `EventParameter`.

        Args:
            name (str): Name of the parameter to update.
            value (str): Value of the parameter to set.  If `None`, existing parameter will be removed.
            type (str, optional): Data type of the value. Defaults to "string".
        """
        if value:
            self.parameters[name] = EventParameter(name=name, value=value, type=type)
        else:
            if name in self.parameters:
                del self.parameters[name]
