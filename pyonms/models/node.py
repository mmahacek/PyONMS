# models.node.py

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Union

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
    slot: str = None
    port: str = None
    region: str = None
    comment: str = None
    password: str = None
    category: str = None
    manufacturer: str = None
    vendor: str = None
    modelNumber: str = None
    circuitId: str = None
    assetNumber: str = None
    operatingSystem: str = None
    rack: str = None
    division: str = None
    department: str = None
    building: str = None
    floor: str = None
    room: str = None
    vendorPhone: str = None
    vendorFax: str = None
    vendorAssetNumber: str = None
    lastModifiedBy: str = None
    lastModifiedDate: int = None
    dateInstalled: str = None
    lease: str = None
    leaseExpires: str = None
    supportPhone: str = None
    maintcontract: str = None
    maintContractNumber: str = None
    maintContractExpiration: str = None
    displayCategory: str = None
    notifyCategory: str = None
    pollerCategory: str = None
    thresholdCategory: str = None
    managedObjectType: str = None
    managedObjectInstance: str = None
    enable: str = None
    connection: str = None
    autoenable: str = None
    cpu: str = None
    ram: str = None
    snmpcommunity: str = None
    rackunitheight: str = None
    admin: str = None
    additionalhardware: str = None
    inputpower: str = None
    numpowersupplies: str = None
    hdd6: str = None
    hdd5: str = None
    hdd4: str = None
    hdd3: str = None
    hdd2: str = None
    hdd1: str = None
    storagectrl: str = None
    description: str = None
    username: str = None
    serialNumber: str = None
    city: str = None

    def __post_init__(self):
        self.lastModifiedDate = convert_time(self.lastModifiedDate)

    def __repr__(self):
        return f"AssetRecord(id={self.id})"


@dataclass
class ServiceType:
    id: int
    name: str


@dataclass
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
        self.serviceType = ServiceType(**self.serviceType)
        self.lastFail = convert_time(self.lastFail)
        self.lastGood = convert_time(self.lastGood)


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
        self.lastIngressFlow = convert_time(self.lastIngressFlow)
        self.lastEgressFlow = convert_time(self.lastEgressFlow)
        self.lastCapsdPoll = convert_time(self.lastCapsdPoll)
        self.lastSnmpPoll = convert_time(self.lastSnmpPoll)

    def __repr__(self):
        return f"SnmpInterface(id={self.id}, ifAlias={self.ifAlias})"


@dataclass(repr=False)
class IPInterface:
    id: int
    hostName: str
    isDown: bool
    nodeId: int
    ifIndex: int
    lastEgressFlow: datetime
    lastIngressFlow: datetime
    monitoredServiceCount: int
    ipAddress: str
    snmpPrimary: str
    isManaged: str
    lastCapsdPoll: int = datetime
    snmpInterface: SnmpInterface = field(default_factory=dict)
    services: List[Union[Service, None]] = field(default_factory=list)

    def __post_init__(self):
        self.id = int(self.id)
        self.lastCapsdPoll = convert_time(self.lastCapsdPoll)
        self.lastEgressFlow = convert_time(self.lastEgressFlow)
        self.lastIngressFlow = convert_time(self.lastIngressFlow)
        self.isManaged = Managed(self.isManaged)
        self.snmpPrimary = PrimaryType(self.snmpPrimary)
        if self.snmpInterface:
            self.snmpInterface = SnmpInterface(**self.snmpInterface)

    def __repr__(self):
        return f"IPInterface(id={self.id}, ipAddress={self.ipAddress})"


@dataclass
class Metadata:
    context: str
    key: str
    value: str


@dataclass(repr=False)
class Node:
    id: int
    type: NodeType = None
    label: str = None
    location: str = None
    createTime: datetime = None
    labelSource: LabelSource = None
    foreignId: str = None
    foreignSource: str = None
    lastIngressFlow: datetime = None
    lastEgressFlow: datetime = None
    lastCapsdPoll: datetime = None
    sysObjectId: str = None
    sysName: str = None
    sysLocation: str = None
    sysContact: str = None
    sysDescription: str = None
    assetRecord: List[Union[AssetRecord, None]] = field(default_factory=dict)
    categories: List[Union[str, None]] = field(default_factory=list)
    snmpInterfaces: List[Union[SnmpInterface, None]] = field(default_factory=list)
    ipInterfaces: List[Union[IPInterface, None]] = field(default_factory=list)
    metadata: List[Union[Metadata, None]] = field(default_factory=list)

    def __post_init__(self):
        self.id = int(self.id)
        self.createTime = convert_time(self.createTime)
        self.lastIngressFlow = convert_time(self.lastIngressFlow)
        self.lastEgressFlow = convert_time(self.lastEgressFlow)
        self.lastCapsdPoll = convert_time(self.lastCapsdPoll)
        self.labelSource = LabelSource(self.labelSource)
        self.type = NodeType(self.type)
        if self.assetRecord:
            self.assetRecord = AssetRecord(**self.assetRecord)
        if self.categories:
            self.categories = [id["name"] for id in self.categories]

    def __repr__(self):
        return f"Node(id={self.id}, label={self.label})"
