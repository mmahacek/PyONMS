# models.foreign_source.py

"Foreign Source Definition models"

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from pyonms.utils import convert_time


@dataclass
class Parameter:
    "Policy/Detector parameters"
    key: str
    value: str

    def __post_init__(self):
        self.key = str(self.key)
        self.value = str(self.value)

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        return {"key": self.key, "value": self.value}

    _to_dict = to_dict


@dataclass
class Detector:
    "Detector class"
    name: str
    class_type: str
    parameter: List[Optional[Parameter]] = field(default_factory=list)

    def __post_init__(self):
        parameter = []
        for param in self.parameter:
            if isinstance(param, dict):
                parameter.append(Parameter(**param))
            elif isinstance(param, Parameter):
                parameter.append(param)
        self.parameter = parameter

    def __repr__(self):
        return (
            f"Detector(name={self.name}, class_type={self.class_type.split('.')[-1]})"
        )

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        payload: Dict[str, Any] = {"name": self.name, "class": self.class_type}
        payload["parameter"] = []
        for parameter in self.parameter:
            if isinstance(parameter, Parameter):
                payload["parameter"].append(parameter.to_dict())
        return payload

    _to_dict = to_dict


@dataclass(repr=False)
class Policy:
    "Policy class"
    name: str
    class_type: str
    parameter: List[Optional[Parameter]] = field(default_factory=list)

    def __post_init__(self):
        parameter = []
        for param in self.parameter:
            if isinstance(param, dict):
                parameter.append(Parameter(**param))
            elif isinstance(param, Parameter):
                parameter.append(param)
        self.parameter = parameter

    def __repr__(self):
        return f"Policy(name={self.name}, class_type={self.class_type.split('.')[-1]})"

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        payload: Dict[str, Any] = {"name": self.name, "class": self.class_type}
        payload["parameter"] = []
        for parameter in self.parameter:
            if isinstance(parameter, Parameter):
                payload["parameter"].append(parameter.to_dict())
        return payload

    _to_dict = to_dict


@dataclass(repr=False)
class ForeignSource:
    "Foreign Source definition class"
    name: str
    date_stamp: Optional[datetime] = None
    scan_interval: Optional[str] = "1d"
    detectors: Dict[str, Detector] = field(default_factory=dict)
    policies: Dict[str, Policy] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.date_stamp, int):
            self.date_stamp = convert_time(self.date_stamp)
        detectors = {}
        for detector in self.detectors:
            if isinstance(detector, dict):
                new_detector = Detector(**detector)
                detectors[new_detector.name] = new_detector
            elif isinstance(detector, Detector):
                detectors[detector.name] = detector
        self.detectors = detectors
        policies = {}
        for policy in self.policies:
            if isinstance(policy, dict):
                new_policy = Policy(**policy)
                policies[new_policy.name] = new_policy
            elif isinstance(policy, Policy):
                policies[policy.name] = policy
        self.policies = policies

    def __repr__(self):
        return f"ForeignSource(name={self.name})"

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        payload: Dict[str, Any] = {
            "name": self.name,
            "scan-interval": self.scan_interval,
        }
        if self.date_stamp:
            payload["date-stamp"] = self.date_stamp
        payload["detectors"] = [
            detector.to_dict() for detector in self.detectors.values()
        ]
        payload["policies"] = [
            policies.to_dict() for policies in self.policies.values()
        ]
        return payload

    _to_dict = to_dict

    def add_detector(self, detector: Detector, merge: bool = True):
        """Add a detector to the foreign source

        Args:
            detector (`Detector`): Detector to add.
            merge (bool, optional): Merge non-null attributes with existing detector in requisition.
                Set to `False` to overwrite entire detector record.
                Defaults to `True`.

        Raises:
            `NotImplementedError`: If `merge` not set to `False`
        """  # noqa
        if merge:
            raise NotImplementedError
        else:
            self.detectors[detector.name] = detector

    def remove_detector(self, name: str):
        """Remove a detector from the foreign source

        Args:
            name (str): Name of the Detector to remove.
        """  # noqa
        if name in self.detectors:
            del self.detectors[name]

    def add_policy(self, policy: Policy, merge: bool = True):
        """Add a policy to the foreign source

        Args:
            policy (`Policy`): Policy to add.
            merge (bool, optional): Merge non-null attributes with existing policy in requisition.
                Set to `False` to overwrite entire policy record.
                Defaults to `True`.

        Raises:
            `NotImplementedError`: If `merge` not set to `False`
        """  # noqa
        if merge:
            raise NotImplementedError
        else:
            self.policies[policy.name] = policy

    def remove_policy(self, name: str):
        """Remove a policy from the foreign source

        Args:
            name (str): Name of the Policy to remove.
        """  # noqa
        if name in self.policies:
            del self.policies[name]
