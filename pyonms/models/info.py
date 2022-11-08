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
class Info:
    displayVersion: str
    version: str
    packageName: str
    packageDescription: str
    ticketerConfig: TicketerConfig
    datetimeformatConfig: DateFormat
    services: List[Service]

    def __post_init__(self):
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
