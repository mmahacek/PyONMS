# models.info.py

"Info endpoint models"

from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class ServiceStatus:
    "Service status"
    name: str
    status: str


@dataclass
class TicketerConfig:
    "Ticketing configuration"
    enabled: bool
    plugin: Optional[str] = None


@dataclass
class DateFormat:
    "Date and timezone information"
    zoneId: str
    datetimeformat: str


@dataclass(repr=False)
class Version:
    "Version response class"
    version_string: str
    major: Optional[int] = None
    minor: Optional[int] = None
    patch: Optional[int] = None
    dev: Optional[bool] = None

    def __post_init__(self):
        version_number = self.version_string.split(".")
        self.major = int(version_number[0])
        self.minor = int(version_number[1])
        if "-" in version_number[2]:
            patch_version = version_number[2].split("-")
            self.patch = int(patch_version[0])
            self.dev = patch_version[1]
        else:
            self.patch = int(version_number[2])

    def __repr__(self):
        return f"Version({self.version_string})"


@dataclass(repr=False)
class Info:
    "Information response class"
    displayVersion: Optional[str] = None
    version: Optional[Union[str, Version]] = None
    packageName: Optional[str] = None
    packageDescription: Optional[str] = None
    ticketerConfig: Optional[TicketerConfig] = None
    datetimeformatConfig: Optional[Union[str, DateFormat]] = None
    services: List[ServiceStatus] = field(default_factory=list)
    enabled_services: List[str] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.version, str):
            self.version = Version(version_string=self.version)
        if isinstance(self.displayVersion, str):
            self.displayVersion = Version(version_string=self.displayVersion)
        if isinstance(self.ticketerConfig, dict):
            self.ticketerConfig = TicketerConfig(**self.ticketerConfig)
        if isinstance(self.datetimeformatConfig, dict):
            self.datetimeformatConfig = DateFormat(**self.datetimeformatConfig)
        if isinstance(self.services, dict):
            services = []
            for service, status in self.services:
                services.append(ServiceStatus(name=service, status=status))
            self.services = services
        self.enabled_services = [service.name.lower() for service in self.services]

    def __repr__(self):
        running_count = len(
            [service for service in self.services if service.status == "running"]
        )
        text = f"Info(version={self.displayVersion},"
        text += f" running_services={running_count}/{len(self.services)})"
        return text
