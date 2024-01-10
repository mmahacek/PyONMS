# models.enlinkd.py

"Enlinkd Models"

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Union

from pyonms import utils


class LinkType(Enum):
    "Link type enum"
    BRIDGE = "bridge"
    CDP = "cdp"
    LLDP = "lldp"
    ISIS = "isis"
    OSPF = "ospf"
    UNKNOWN = None


@dataclass
class Link:
    "Link base class"
    pass


@dataclass
class Element:
    "Element base class"
    pass


@dataclass
class LldpLink(Link):
    "LLDP Link"
    lldpLocalPort: str = None
    lldpLocalPortUrl: str = None
    lldpRemChassisId: str = None
    lldpRemChassisIdUrl: str = None
    lldpRemInfo: str = None
    ldpRemPort: str = None
    lldpCreateTime: Union[str, datetime] = None
    lldpLastPollTime: Union[str, datetime] = None
    linkType = LinkType.LLDP
    lldpLocalNodeId: int = None
    lldpRemNodeId: int = None
    lldpLocalMAC: str = None
    lldpRemMAC: str = None
    lldpLocalIfIndex: int = None
    lldpRemIfIndex: int = None

    def __post_init__(self):
        if isinstance(self.lldpCreateTime, str):
            self.lldpCreateTime = utils.convert_link_time(self.lldpCreateTime)
        if isinstance(self.lldpLastPollTime, str):
            self.lldpLastPollTime = utils.convert_link_time(self.lldpLastPollTime)
        if self.lldpLocalPortUrl:
            if local_node := infer_node_from_url(url=self.lldpLocalPortUrl):
                self.lldpLocalNodeId = local_node
        if self.lldpRemChassisIdUrl:
            if remote_node := infer_node_from_url(url=self.lldpRemChassisIdUrl):
                self.lldpRemNodeId = remote_node
        if self.lldpLocalPort:
            if local_mac := infer_mac(self.lldpLocalPort):
                self.lldpLocalMAC = local_mac
            if local_ifindex := infer_ifindex(self.lldpLocalPort):
                self.lldpLocalIfIndex = local_ifindex
        if self.ldpRemPort:
            if remote_mac := infer_mac(self.ldpRemPort):
                self.lldpRemMAC = remote_mac
            if remote_ifindex := infer_ifindex(self.ldpRemPort):
                self.lldpRemIfIndex = remote_ifindex


@dataclass
class BridgeElement(Element):
    "Bridge Element"
    baseBridgeAddress: str = None
    baseNumPorts: int = None
    baseType: str = None
    stpProtocolSpecification: str = None
    stpPriority: str = None
    stpDesignatedRoot: str = None
    stpRootCost: int = None
    stpRootPort: int = None
    vlan: str = None
    vlanname: str = None
    bridgeNodeCreateTime: Union[str, datetime] = None
    bridgeNodeLastPollTime: Union[str, datetime] = None
    linkType = LinkType.BRIDGE

    def __post_init__(self):
        if isinstance(self.bridgeNodeCreateTime, str):
            self.bridgeNodeCreateTime = utils.convert_link_time(
                self.bridgeNodeCreateTime
            )
        if isinstance(self.bridgeNodeLastPollTime, str):
            self.bridgeNodeLastPollTime = utils.convert_link_time(
                self.bridgeNodeLastPollTime
            )


@dataclass
class CdpElement(Element):
    "CDP Element"
    cdpGlobalRun: str = None
    cdpGlobalDeviceId: str = None
    cdpGlobalDeviceIdFormat: str = None
    cdpCreateTime: Union[str, datetime] = None
    cdpLastPollTime: Union[str, datetime] = None
    linkType = LinkType.CDP

    def __post_init__(self):
        if isinstance(self.cdpCreateTime, str):
            self.cdpCreateTime = utils.convert_link_time(self.cdpLastPollTime)
        if isinstance(self.cdpLastPollTime, str):
            self.cdpLastPollTime = utils.convert_link_time(self.cdpLastPollTime)


@dataclass
class IsisElement(Element):
    "IS-IS Element"
    isisSysID: str = None
    isisSysAdminState: str = None
    isisCreateTime: Union[str, datetime] = None
    isisLastPollTime: Union[str, datetime] = None
    linkType = LinkType.ISIS

    def __post_init__(self):
        if isinstance(self.isisCreateTime, str):
            self.isisCreateTime = utils.convert_link_time(self.isisCreateTime)
        if isinstance(self.isisLastPollTime, str):
            self.isisLastPollTime = utils.convert_link_time(self.isisLastPollTime)


@dataclass
class LldpElement(Element):
    "LLDP Element"
    lldpChassisId: str = None
    lldpSysName: str = None
    lldpCreateTime: Union[str, datetime] = None
    lldpLastPollTime: Union[str, datetime] = None
    linkType = LinkType.LLDP

    def __post_init__(self):
        if isinstance(self.lldpCreateTime, str):
            self.lldpCreateTime = utils.convert_link_time(self.lldpCreateTime)
        if isinstance(self.lldpLastPollTime, str):
            self.lldpLastPollTime = utils.convert_link_time(self.lldpLastPollTime)


@dataclass
class OspfElement(Element):
    "OSPF Element"
    ospfRouterId: str = None
    ospfVersionNumber: int = None
    ospfAdminStat: str = None
    ospfCreateTime: Union[str, datetime] = None
    ospfLastPollTime: Union[str, datetime] = None
    linkType = LinkType.OSPF

    def __post_init__(self):
        if isinstance(self.ospfCreateTime, str):
            self.ospfCreateTime = utils.convert_link_time(self.ospfCreateTime)
        if isinstance(self.ospfLastPollTime, str):
            self.ospfLastPollTime = utils.convert_link_time(self.ospfLastPollTime)


@dataclass
class Topology:
    "Topology class"
    lldp_links: List[LldpLink] = field(default_factory=list)
    lldp_elements: List[LldpElement] = field(default_factory=list)
    bridge_links: List[Link] = field(default_factory=list)
    bridge_elements: List[BridgeElement] = field(default_factory=list)
    cdp_links: List[Link] = field(default_factory=list)
    cdp_elements: List[CdpElement] = field(default_factory=list)
    ospf_links: List[Link] = field(default_factory=list)
    ospf_elements: List[OspfElement] = field(default_factory=list)
    isis_links: List[Link] = field(default_factory=list)
    isis_elements: List[IsisElement] = field(default_factory=list)


def infer_node_from_url(url: str) -> int:
    "Infer node ID from url querystring"
    node = re.search(r"^.*node=(\d+).*", url)
    if node:
        return int(node.group(1))


def infer_mac(text: str) -> str:
    "Infer MAC address from string"
    mac = re.search(r"^.*\(macAddress:([0-9a-fA-F]+)\).*", text)
    if mac:
        return mac.group(1)


def infer_ifindex(text: str) -> int:
    "Infer ifIndex from string"
    ifindex = re.search(r"^.*\(ifindex:(\d+)\).*", text)
    if ifindex:
        return int(ifindex.group(1))
