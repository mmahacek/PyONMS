# models.foreign_source.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from pyonms.models import exceptions
from pyonms.utils import convert_time


@dataclass
class Parameter:
    key: str
    value: str

    def __post_init__(self):
        self.key = str(self.key)
        self.value = str(self.value)

    def _to_dict(self) -> dict:
        return {"key": self.key, "value": self.value}


@dataclass
class Detector:
    name: str
    class_type: str
    parameters: List[Optional[Parameter]] = field(default_factory=list)

    def __post_init__(self):
        parameters = []
        for param in self.parameters:
            if isinstance(param, dict):
                parameters.append(Parameter(**param))
            elif isinstance(param, Parameter):
                parameters.append(param)
        self.parameters = parameters

    def __repr__(self):
        return (
            f"Detector(name={self.name}, class_type={self.class_type.split('.')[-1]})"
        )

    def _to_dict(self) -> dict:
        payload = {"name": self.name, "class": self.class_type}
        payload["parameter"] = [parameter._to_dict() for parameter in self.parameters]
        return payload


@dataclass(repr=False)
class Policy:
    name: str
    class_type: str
    parameters: List[Optional[Parameter]] = field(default_factory=list)

    def __post_init__(self):
        parameters = []
        for param in self.parameters:
            if isinstance(param, dict):
                parameters.append(Parameter(**param))
            elif isinstance(param, Parameter):
                parameters.append(param)
        self.parameters = parameters

    def __repr__(self):
        return f"Policy(name={self.name}, class_type={self.class_type.split('.')[-1]})"

    def _to_dict(self) -> dict:
        payload = {"name": self.name, "class": self.class_type}
        payload["parameter"] = [parameter._to_dict() for parameter in self.parameters]
        return payload


@dataclass(repr=False)
class ForeignSource:
    name: str
    date_stamp: Optional[datetime] = None
    scan_interval: str = "1d"
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

    def _to_dict(self) -> dict:
        payload = {"name": self.name, "scan-interval": self.scan_interval}
        if self.date_stamp:
            payload["date-stamp"] = self.date_stamp
        payload["detectors"] = [
            detector._to_dict() for detector in self.detectors.values()
        ]
        payload["policies"] = [
            policies._to_dict() for policies in self.policies.values()
        ]
        return payload

    def add_detector(self, detector: Detector, merge: bool = True):
        """Add a detector to the foreign source

        Args:
            node (`Detector`): Detector to add.
            merge (bool, optional): Merge non-null attributes with existing detector in requisition. Set to `False` to overwrite entire detector record. Defaults to `True`.

        Raises:
            pyonms.models.exceptions.MethodNotImplemented: If `merge` not set to `False`
        """  # noqa
        if merge:
            raise exceptions.MethodNotImplemented
        else:
            self.detectors[detector.name] = detector

    def remove_detector(self, name: str):
        if name in self.detectors.keys():
            del self.detectors[name]
        else:
            raise exceptions.InvalidValueError(name="Detector name", value=name)

    def add_policy(self, policy: Policy, merge: bool = True):
        """Add a policy to the foreign source

        Args:
            node (`Policy`): Policy to add.
            merge (bool, optional): Merge non-null attributes with existing policy in requisition. Set to `False` to overwrite entire policy record. Defaults to `True`.

        Raises:
            pyonms.models.exceptions.MethodNotImplemented: If `merge` not set to `False`
        """  # noqa
        if merge:
            raise exceptions.MethodNotImplemented
        else:
            self.policies[policy.name] = policy

    def remove_policy(self, name: str):
        if name in self.policies.keys():
            del self.policies[name]
        else:
            raise exceptions.InvalidValueError(name="Policy name", value=name)
