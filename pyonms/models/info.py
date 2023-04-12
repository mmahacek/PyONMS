# models.info.py

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Service:
    name: str
    status: str


@dataclass
class TicketerConfig:
    enabled: bool
    plugin: Optional[str] = None


@dataclass
class DateFormat:
    zoneId: str
    datetimeformat: str


@dataclass(repr=False)
class Version:
    version_string: str
    major: int = None
    minor: int = None
    patch: int = None
    dev: bool = None

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
    displayVersion: str
    version: str
    packageName: str
    packageDescription: str
    ticketerConfig: TicketerConfig
    datetimeformatConfig: DateFormat
    services: List[Service]

    def __post_init__(self):
        if isinstance(self.version, str):
            self.version = Version(version_string=self.version)
        if isinstance(self.displayVersion, str):
            self.displayVersion = Version(version_string=self.displayVersion)
        if isinstance(self.ticketerConfig, dict):
            self.ticketerConfig = TicketerConfig(**self.ticketerConfig)
        if isinstance(self.datetimeformatConfig, dict):
            self.datetimeformatConfig = DateFormat(**self.datetimeformatConfig)
        services = []
        for service, status in self.services.items():
            services.append(Service(name=service, status=status))
        self.services = services

    def __repr__(self):
        text = f"Info(version={self.displayVersion},"
        text += f" running_services={len([service for service in self.services if service.status == 'running'])}/{len(self.services)})"
        return text
