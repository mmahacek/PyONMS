# portal.models.py

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pyonms.models.exceptions import InvalidValueError

from pyonms.utils import convert_time

APPLIANCE_TYPE = ["HARDWARE", "VIRTUAL"]
BROKER_TYPE = ["JMS", "KAFKA"]
MINION_STATUS = ["UP", "DOWN", "GRACE_PERIOD", "UNKNOWN"]
ONMS_STATUS = ["UP", "DOWN", "GRACE_PERIOD", "UNKNOWN"]


@dataclass
class PortalBrokerConfig:
    type: str

    def __post_init__(self):
        if self.type not in BROKER_TYPE:
            raise InvalidValueError(
                name="brokerType", value=self.type, valid=BROKER_TYPE
            )


@dataclass
class PortalBrokerKafka(PortalBrokerConfig):
    bootstrapServers: List[str] = field(default_factory=list)

    def to_dict(self):
        payload = {"type": self.type, "bootstrapServers": self.bootstrapServers}
        return payload


@dataclass
class PortalBrokerJms(PortalBrokerConfig):
    url: str
    user: str
    password: str

    def to_dict(self):
        payload = {
            "type": self.type,
            "url": self.url,
            "user": self.user,
            "password": self.password,
        }
        return payload


@dataclass
class PortalHttpConfig:
    url: str
    user: str
    password: str

    def to_dict(self):
        payload = {"url": self.url, "user": self.user, "password": self.password}
        return payload


@dataclass
class PortalInstance:
    id: str
    name: str


@dataclass
class PortalInstanceCreate:
    name: str

    def to_dict(self):
        payload = {"name": self.name}
        return payload


@dataclass(repr=False)
class PortalFeatureProfile:
    id: str
    name: str
    onmsInstance: PortalInstance

    def __post_init__(self):
        if isinstance(self.onmsInstance, dict):
            self.onmsInstance = PortalInstance(**self.onmsInstance)

    def __repr__(self):
        return f"PortalFeatureProfile(id='{self.id}', name='{self.name}', onmsInstance={self.onmsInstance.name})"


@dataclass(repr=False)
class PortalConnectivityProfile:
    id: str
    name: str
    onmsInstance: PortalInstance

    def __post_init__(self):
        if isinstance(self.onmsInstance, dict):
            self.onmsInstance = PortalInstance(**self.onmsInstance)

    def __repr__(self):
        return f"PortalConnectivityProfile(id='{self.id}', name='{self.name}', onmsInstance={self.onmsInstance.name})"


@dataclass
class PortalConnectivityProfileCreate:
    name: str
    onmsInstance: PortalInstance
    httpConfig: PortalHttpConfig
    brokerConfig: Union[PortalBrokerJms, PortalBrokerKafka]

    def to_dict(self):
        payload = {
            "name": self.name,
            "httpConfig": self.httpConfig.to_dict(),
            "brokerConfig": self.brokerConfig.to_dict(),
        }
        if isinstance(self.onmsInstance, str):
            payload["onmsInstanceId"] = self.onmsInstance
        elif isinstance(self.onmsInstance, PortalInstance):
            payload["onmsInstanceId"] = self.onmsInstance.id
        return payload


@dataclass
class PortalLocation:
    id: str
    name: str
    onmsInstanceId: PortalInstance
    connectivityProfileId: PortalConnectivityProfile
    minionFeatureProfileId: PortalFeatureProfile = None


@dataclass
class PortalLocationCreate:
    name: str
    onmsInstance: PortalInstance
    connectivityProfile: PortalConnectivityProfile
    minionFeatureProfile: PortalFeatureProfile = None

    def to_dict(self):
        payload = {"name": self.name}
        if isinstance(self.onmsInstance, str):
            payload["onmsInstanceId"] = self.onmsInstance
        elif isinstance(self.onmsInstance, PortalInstance):
            payload["onmsInstanceId"] = self.onmsInstance.id
        if isinstance(self.connectivityProfile, str):
            payload["connectivityProfileId"] = self.connectivityProfile
        elif isinstance(self.connectivityProfile, PortalConnectivityProfile):
            payload["connectivityProfileId"] = self.connectivityProfile.id
        if self.minionFeatureProfile:
            if isinstance(self.minionFeatureProfile, str):
                payload["minionFeatureProfileId"] = self.minionFeatureProfile
            elif isinstance(self.minionFeatureProfile, PortalFeatureProfile):
                payload["minionFeatureProfileID"] = self.minionFeatureProfile.id
        return payload


@dataclass
class PortalMinionProfile:
    id: str
    name: str
    processEnvConfigId: str


@dataclass
class PortalMinion:
    locationId: Union[str, PortalLocation]
    minionProfileId: Optional[Union[str, PortalMinionProfile]] = None

    def to_dict(self):
        payload = {}
        if isinstance(self.locationId, str):
            payload["locationId"] = self.locationId
        elif isinstance(self.locationId, PortalLocation):
            payload["locationId"] = self.locationId.id
        if isinstance(self.minionProfileId, str):
            payload["minionProfileId"] = self.minionProfileId
        elif isinstance(self.minionProfileId, PortalMinionProfile):
            payload["minionProfileId"] = self.minionProfileId.id
        return payload


@dataclass
class PortalSubscription:
    id: str
    count: int
    expiry: datetime
    state: str

    def __post_init__(self):
        if isinstance(self.expiry, int):
            self.expiry = convert_time(self.expiry)


@dataclass(repr=False)
class PortalAppliance:
    id: str
    label: str
    type: str
    applianceProfileId: str
    minion: PortalMinion
    subscriptionId: PortalSubscription
    geoLocationLabel: str = None
    latitude: float = None
    longitude: float = None

    def __post_init__(self):
        if self.type not in APPLIANCE_TYPE:
            raise InvalidValueError(name="type", value=self.type, valid=APPLIANCE_TYPE)
        if isinstance(self.minion, dict):
            self.minion = PortalMinion(**self.minion)

    def __repr__(self):
        return f"PortalAppliance(label={self.label}, id={self.id}"

    def to_dict(self):
        payload = {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            "geoLocationLabel": self.geoLocationLabel,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "applianceProfileId": self.applianceProfileId,
            "minion": self.minion.to_dict(),
            "subscriptionId": self.subscriptionId,
        }
        return payload


@dataclass
class PortalApplianceProfile:
    id: str
    name: str


@dataclass
class PortalApplianceStatus:
    connected: bool
    minionStatus: str
    onmsStatus: str

    def __post_init__(self):
        if self.minionStatus not in MINION_STATUS:
            raise InvalidValueError(
                name="minionStatus", value=self.minionStatus, valid=MINION_STATUS
            )
        if self.onmsStatus not in ONMS_STATUS:
            raise InvalidValueError(
                name="onmsStatus", value=self.onmsStatus, valid=ONMS_STATUS
            )


@dataclass
class PortalIpInfo:
    interfaceName: str
    ipAddresses: list = field(default_factory=list)


@dataclass
class PortalAppliancePlatformInfo:
    hostname: str
    ipInfo: PortalIpInfo

    def __post_init__(self):
        if isinstance(self.ipInfo, dict):
            self.ipInfo = PortalIpInfo(**self.ipInfo)
