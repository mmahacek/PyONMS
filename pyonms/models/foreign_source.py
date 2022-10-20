# models.foreign_source.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from pyonms.utils import convert_time


@dataclass
class Parameter:
    key: str
    value: str

    def __post_init__(self):
        self.key = str(self.key)
        self.value = str(self.value)


@dataclass
class Detector:
    name: str
    class_type: str
    parameter: List[Optional[Parameter]] = field(default_factory=list)

    def __post_init__(self):
        parameters = []
        for param in self.parameter:
            if isinstance(param, dict):
                parameters.append(Parameter(**param))
            elif isinstance(param, Parameter):
                parameters.append(param)
        self.parameter = parameters

    def __repr__(self):
        return (
            f"Detector(name={self.name}, class_type={self.class_type.split('.')[-1]})"
        )


@dataclass(repr=False)
class Policy:
    name: str
    class_type: str
    parameter: List[Optional[Parameter]] = field(default_factory=list)

    def __post_init__(self):
        parameters = []
        for param in self.parameter:
            if isinstance(param, dict):
                parameters.append(Parameter(**param))
            elif isinstance(param, Parameter):
                parameters.append(param)
        self.parameter = parameters

    def __repr__(self):
        return f"Policy(name={self.name}, class_type={self.class_type.split('.')[-1]})"


@dataclass(repr=False)
class ForeignSource:
    name: str
    date_stamp: datetime
    scan_interval: str = "1d"
    detectors: List[Optional[Detector]] = field(default_factory=list)
    policies: List[Optional[Policy]] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.date_stamp, int):
            self.date_stamp = convert_time(self.date_stamp)
        detectors = []
        for detector in self.detectors:
            if isinstance(detector, dict):
                detectors.append(Detector(**detector))
            elif isinstance(detector, Detector):
                detectors.append(detector)
        self.detectors = detectors
        policies = []
        for policy in self.policies:
            if isinstance(policy, dict):
                policies.append(Policy(**policy))
            elif isinstance(policy, Policy):
                policies.append(policy)
        self.policies = policies

    def __repr__(self):
        return f"ForeignSource(name={self.name})"
