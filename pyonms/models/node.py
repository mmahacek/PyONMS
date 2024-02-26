# models.node.py

"""Node models"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pyonms.utils import check_ip_address, convert_time


class LabelSource(Enum):
    """Source from how the `nodeLabel` was populated"""

    USER = "U"
    "User specified"
    NETBIOS = "N"
    "Netbios"
    HOSTNAME = "H"
    "Hostname"
    SYSNAME = "S"
    "System name"
    ADDRESS = "A"
    "Address"
    UNKNOWN = " "
    "Unknown"


class NodeType(Enum):
    """Node status"""

    ACTIVE = "A"
    "Active"
    DELETED = "D"
    "Deleted"
    UNKNOWN = " "
    "Unknown"


class ManagedIP(Enum):
    """IP management status"""

    MANAGED = "M"
    "Managed"
    UNMANAGED = "U"
    "Unmanaged"
    DELETED = "D"
    "Deleted"
    ALIAS = "A"
    "Alias"
    FORCE_UNMANAGED = "F"
    "Force Unmanaged"
    NOT_POLLED = "N"
    "Not Polled"
    REMOTELY_MONITORED = "X"
    "Remotely Monitored"


class ServiceStatus(Enum):
    """Service management status"""

    MANAGED = "A"
    UNMANAGED = "U"
    DELETED = "D"
    FORCE_UNMANAGED = "F"
    NOT_MONITORED = "N"
    RESCAN_TO_RESUME = "R"
    RESCAN_TO_SUSPEND = "S"
    REMOTELY_MONITORED = "X"


class PrimaryType(Enum):
    """IP interface primary status"""

    PRIMARY = "P"
    "SNMP Primary"
    SECONDARY = "S"
    "SNMP Secondary"
    NOT_ELIGIBLE = "N"
    "No SNMP"

    @classmethod
    def list(cls):
        """List possible enum values"""
        return list(map(lambda c: c.value, cls))


@dataclass
class Metadata:
    """Metadata record"""

    context: str
    key: str
    value: str

    def __hash__(self):
        return hash((self.context, self.key, self.value))

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        payload = {"context": self.context, "key": self.key, "value": self.value}
        return payload

    _to_dict = to_dict


@dataclass(repr=False)
class AssetRecord:
    """Asset record"""

    id: Optional[int] = None
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

    def __hash__(self):
        return hash((self.id))

    def to_dict(self) -> dict:
        "Convert object to a `dict`"
        payload = {}
        for item in dir(self):
            if item[0] != "_" and getattr(self, item):
                payload[item] = getattr(self, item)
        return payload

    _to_dict = to_dict


@dataclass
class ServiceType:
    """Service type"""

    id: int
    name: str

    def __hash__(self):
        return hash((self.id))


@dataclass(repr=False)
class Service:
    """Monitored Service object"""

    id: Optional[int] = None
    notify: Optional[str] = None
    status: Optional[Union[ServiceStatus, str]] = None
    qualifier: Optional[str] = None
    down: Optional[bool] = None
    source: Optional[str] = None
    serviceType: Optional[ServiceType] = None
    ipInterfaceId: Optional[int] = None
    statusLong: Optional[str] = None
    lastFail: Optional[datetime] = None
    lastGood: Optional[datetime] = None
    metadata: List[Metadata] = field(default_factory=list)
    applications: List[str] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.serviceType, dict):
            self.serviceType = ServiceType(**self.serviceType)
        if isinstance(self.status, str):
            self.status = ServiceStatus(self.status)
        if isinstance(self.lastFail, int):
            self.lastFail = convert_time(self.lastFail)
        if isinstance(self.lastGood, int):
            self.lastGood = convert_time(self.lastGood)

    def __repr__(self):
        return f"Service(id={self.id}, serviceType={self.serviceType.name}, down={self.down})"

    def __hash__(self):
        return hash((self.id))


@dataclass(repr=False)
class SnmpInterface:
    """SNMP Interface object"""

    id: Optional[int] = None
    hasFlows: Optional[bool] = None
    hasIngressFlows: Optional[bool] = None
    hasEgressFlows: Optional[bool] = None
    lastIngressFlow: Optional[datetime] = None
    lastEgressFlow: Optional[datetime] = None
    ifType: Optional[int] = None
    lastCapsdPoll: Optional[datetime] = None
    ifAlias: Optional[str] = None
    ifIndex: Optional[int] = None
    ifDescr: Optional[str] = None
    ifName: Optional[str] = None
    physAddr: Optional[str] = None
    ifSpeed: Optional[int] = None
    ifAdminStatus: Optional[int] = None
    ifOperStatus: Optional[int] = None
    lastSnmpPoll: Optional[datetime] = None
    collectionUserSpecified: Optional[bool] = None
    collectFlag: Optional[str] = None
    pollFlag: Optional[str] = None
    collect: Optional[bool] = None
    poll: Optional[bool] = None
    collectionPolicySpecified: Optional[bool] = None
    nodeId: Optional[int] = None

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

    def __hash__(self):
        return hash((self.id))


@dataclass(repr=False)
class IPInterface:
    """IP Interface Object"""

    id: Optional[Union[int, str]] = None
    hostName: Optional[str] = None
    isDown: Optional[bool] = None
    nodeId: Optional[int] = None
    ifIndex: Optional[int] = None
    lastEgressFlow: Optional[Union[datetime, int]] = None
    lastIngressFlow: Optional[Union[datetime, int]] = None
    ipAddress: Optional[str] = None
    snmpPrimary: Optional[Union[PrimaryType, str]] = None
    isManaged: Optional[Union[ManagedIP, str]] = None
    monitoredServiceCount: Optional[int] = None
    lastCapsdPoll: Optional[Union[datetime, int]] = None
    snmpInterface: Union[SnmpInterface, dict] = field(default_factory=dict)
    services: List[Service] = field(default_factory=list)
    metadata: List[Metadata] = field(default_factory=list)

    def __post_init__(self):
        check_ip_address(self.ipAddress, raise_error=True)
        if isinstance(self.id, str):
            self.id = int(self.id)
        if isinstance(self.lastCapsdPoll, int):
            self.lastCapsdPoll = convert_time(self.lastCapsdPoll)
        if isinstance(self.lastEgressFlow, int):
            self.lastEgressFlow = convert_time(self.lastEgressFlow)
        if isinstance(self.lastIngressFlow, int):
            self.lastIngressFlow = convert_time(self.lastIngressFlow)
        if isinstance(self.isManaged, str):
            self.isManaged = ManagedIP(self.isManaged)
        if isinstance(self.snmpPrimary, str):
            self.snmpPrimary = PrimaryType(self.snmpPrimary)
        if self.snmpInterface and isinstance(self.snmpInterface, dict):
            self.snmpInterface = SnmpInterface(**self.snmpInterface)

    def __repr__(self):
        return f"IPInterface(id={self.id}, ipAddress={self.ipAddress})"

    def __hash__(self):
        return hash((self.id))


@dataclass
class HardwareInventory:
    """Hardware Inventory Record"""

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
    """Node Object"""

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
    collectionPolicySpecified: Optional[bool] = None
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
        if self.assetRecord and isinstance(self.assetRecord, dict):
            self.assetRecord = AssetRecord(**self.assetRecord)
        if self.categories:
            self.categories = [id["name"] for id in self.categories]

    def __repr__(self):
        return f"Node(id={self.id}, label={self.label})"

    def __hash__(self):
        return hash((self.id))
