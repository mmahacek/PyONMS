# models.node.py

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pyonms.utils import convert_time


class LabelSource(Enum):
    USER = "U"
    NETBIOS = "N"
    HOSTNAME = "H"
    SYSNAME = "S"
    ADDRESS = "A"
    UNKNOWN = " "


class NodeType(Enum):
    ACTIVE = "A"
    DELETED = "D"
    UNKNOWN = " "


class Managed(Enum):
    MANAGED = "M"
    UNMANAGED = "U"


class PrimaryType(Enum):
    PRIMARY = "P"
    SECONDARY = "S"
    NOT_ELIGIBLE = "N"


@dataclass(repr=False)
class AssetRecord:
    id: int
    slot: Optional[str] = None
    port: Optional[str] = None
    region: Optional[str] = None
    comment: Optional[str] = None
    password: Optional[str] = None
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    vendor: Optional[str] = None
    modelNumber: Optional[str] = None
    circuitId: Optional[str] = None
    assetNumber: Optional[str] = None
    operatingSystem: Optional[str] = None
    rack: Optional[str] = None
    division: Optional[str] = None
    department: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[str] = None
    room: Optional[str] = None
    vendorPhone: Optional[str] = None
    vendorFax: Optional[str] = None
    vendorAssetNumber: Optional[str] = None
    lastModifiedBy: Optional[str] = None
    lastModifiedDate: Optional[Union[datetime, int]] = None
    dateInstalled: Optional[str] = None
    lease: Optional[str] = None
    leaseExpires: Optional[str] = None
    supportPhone: Optional[str] = None
    maintcontract: Optional[str] = None
    maintContractNumber: Optional[str] = None
    maintContractExpiration: Optional[str] = None
    displayCategory: Optional[str] = None
    notifyCategory: Optional[str] = None
    pollerCategory: Optional[str] = None
    thresholdCategory: Optional[str] = None
    managedObjectType: Optional[str] = None
    managedObjectInstance: Optional[str] = None
    enable: Optional[str] = None
    connection: Optional[str] = None
    autoenable: Optional[str] = None
    cpu: Optional[str] = None
    ram: Optional[str] = None
    snmpcommunity: Optional[str] = None
    rackunitheight: Optional[str] = None
    admin: Optional[str] = None
    additionalhardware: Optional[str] = None
    inputpower: Optional[str] = None
    numpowersupplies: Optional[str] = None
    hdd6: Optional[str] = None
    hdd5: Optional[str] = None
    hdd4: Optional[str] = None
    hdd3: Optional[str] = None
    hdd2: Optional[str] = None
    hdd1: Optional[str] = None
    storagectrl: Optional[str] = None
    description: Optional[str] = None
    username: Optional[str] = None
    serialNumber: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[int] = None
    longitude: Optional[int] = None

    def __post_init__(self):
        if isinstance(self.lastModifiedDate, int):
            self.lastModifiedDate = convert_time(self.lastModifiedDate)

    def __repr__(self):
        return f"AssetRecord(id={self.id})"


@dataclass
class ServiceType:
    id: int
    name: str


@dataclass(repr=False)
class Service:
    id: int
    notify: str
    status: str
    qualifier: str
    down: bool
    source: str
    serviceType: ServiceType
    ipInterfaceId: int
    statusLong: str
    lastFail: datetime
    lastGood: datetime

    def __post_init__(self):
        if isinstance(self.serviceType, dict):
            self.serviceType = ServiceType(**self.serviceType)
        if isinstance(self.lastFail, int):
            self.lastFail = convert_time(self.lastFail)
        if isinstance(self.lastGood, int):
            self.lastGood = convert_time(self.lastGood)

    def __repr__(self):
        return f"Service(id={self.id}, serviceType={self.serviceType.name}, down={self.down})"


@dataclass(repr=False)
class SnmpInterface:
    id: int
    hasFlows: bool
    hasIngressFlows: bool
    hasEgressFlows: bool
    lastIngressFlow: datetime
    lastEgressFlow: datetime
    ifType: int
    lastCapsdPoll: datetime
    ifAlias: str
    ifIndex: int
    ifDescr: str
    ifName: str
    physAddr: str
    ifSpeed: int
    ifAdminStatus: int
    ifOperStatus: int
    lastSnmpPoll: datetime
    collectionUserSpecified: bool
    collectFlag: str
    pollFlag: str
    collect: bool
    poll: bool

    def __post_init__(self):
        if isinstance(self.lastIngressFlow, int):
            self.lastIngressFlow = convert_time(self.lastIngressFlow)
        if isinstance(self.lastEgressFlow, int):
            self.lastEgressFlow = convert_time(self.lastEgressFlow)
        if isinstance(self.lastCapsdPoll, int):
            self.lastCapsdPoll = convert_time(self.lastCapsdPoll)
        if isinstance(self.lastSnmpPoll, int):
            self.lastSnmpPoll = convert_time(self.lastSnmpPoll)

    def __repr__(self):
        return f"SnmpInterface(id={self.id}, ifAlias={self.ifAlias})"


@dataclass(repr=False)
class IPInterface:
    id: Union[int, str]
    hostName: Optional[str]
    isDown: bool
    nodeId: int
    ifIndex: int
    lastEgressFlow: Union[datetime, int]
    lastIngressFlow: Union[datetime, int]
    monitoredServiceCount: Optional[int]
    ipAddress: str
    snmpPrimary: Union[PrimaryType, str]
    isManaged: Union[Managed, str]
    lastCapsdPoll: Union[datetime, int]
    snmpInterface: Optional[Union[SnmpInterface, dict]] = field(default_factory=dict)
    services: List[Optional[Service]] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = int(self.id)
        if isinstance(self.lastCapsdPoll, int):
            self.lastCapsdPoll = convert_time(self.lastCapsdPoll)
        if isinstance(self.lastEgressFlow, int):
            self.lastEgressFlow = convert_time(self.lastEgressFlow)
        if isinstance(self.lastIngressFlow, int):
            self.lastIngressFlow = convert_time(self.lastIngressFlow)
        if isinstance(self.isManaged, str):
            self.isManaged = Managed(self.isManaged)
        if isinstance(self.snmpPrimary, str):
            self.snmpPrimary = PrimaryType(self.snmpPrimary)
        if isinstance(self.snmpInterface, dict):
            self.snmpInterface = SnmpInterface(**self.snmpInterface)

    def __repr__(self):
        return f"IPInterface(id={self.id}, ipAddress={self.ipAddress})"


@dataclass
class Metadata:
    context: str
    key: str
    value: str


@dataclass
class HardwareInventory:
    nodeId: Optional[int] = None
    entPhysicalIndex: Optional[int] = None
    entPhysicalName: Optional[str] = None
    entPhysicalDescr: Optional[str] = None
    entPhysicalVendorType: Optional[str] = None
    entPhysicalHardwareRev: Optional[str] = None
    entPhysicalFirmwareRev: Optional[str] = None
    entPhysicalSoftwareRev: Optional[str] = None
    entPhysicalSerialNum: Optional[str] = None
    entPhysicalMfgName: Optional[str] = None
    entPhysicalModelName: Optional[str] = None
    entPhysicalAlias: Optional[str] = None
    entPhysicalAssetID: Optional[str] = None
    entPhysicalIsFRU: Optional[str] = None
    entPhysicalUris: Optional[str] = None
    entityId: Optional[int] = None
    parentPhysicalIndex: Optional[str] = None
    hwEntityAliases: list = field(default_factory=list)
    children: list = field(default_factory=list)
    vendorAttributes: list = field(default_factory=list)

    def __post_init__(self):
        if self.entityId:
            self.entityId = int(self.entityId)


@dataclass(repr=False)
class Node:
    id: int
    type: Optional[Union[NodeType, str]] = None
    label: Optional[str] = None
    location: Optional[str] = None
    createTime: Optional[Union[datetime, int]] = None
    labelSource: Optional[Union[LabelSource, str]] = None
    foreignId: Optional[str] = None
    foreignSource: Optional[str] = None
    lastIngressFlow: Optional[Union[datetime, int]] = None
    lastEgressFlow: Optional[Union[datetime, int]] = None
    lastCapsdPoll: Optional[Union[datetime, int]] = None
    sysObjectId: Optional[str] = None
    sysName: Optional[str] = None
    sysLocation: Optional[str] = None
    sysContact: Optional[str] = None
    sysDescription: Optional[str] = None
    assetRecord: Optional[Union[AssetRecord, dict]] = field(default_factory=dict)
    categories: List[Optional[Union[str, dict]]] = field(default_factory=list)
    snmpInterfaces: List[Optional[SnmpInterface]] = field(default_factory=list)
    ipInterfaces: List[Optional[IPInterface]] = field(default_factory=list)
    metadata: List[Optional[Metadata]] = field(default_factory=list)
    hardwareInventory: Optional[Union[HardwareInventory, dict]] = field(
        default_factory=dict
    )

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = int(self.id)
        if isinstance(self.createTime, int):
            self.createTime = convert_time(self.createTime)
        if isinstance(self.lastIngressFlow, int):
            self.lastIngressFlow = convert_time(self.lastIngressFlow)
        if isinstance(self.lastEgressFlow, int):
            self.lastEgressFlow = convert_time(self.lastEgressFlow)
        if isinstance(self.lastCapsdPoll, int):
            self.lastCapsdPoll = convert_time(self.lastCapsdPoll)
        if isinstance(self.labelSource, str):
            self.labelSource = LabelSource(self.labelSource)
        if isinstance(self.type, str):
            self.type = NodeType(self.type)
        if isinstance(self.assetRecord, dict):
            self.assetRecord = AssetRecord(**self.assetRecord)
        if self.categories:
            self.categories = [id["name"] for id in self.categories]

    def __repr__(self):
        return f"Node(id={self.id}, label={self.label})"
