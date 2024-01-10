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
class BridgeLinkRemoteNode:
    "Bridge Link Remote Node"
    bridgeRemote: str = None
    bridgeRemoteUrl: str = None
    bridgeRemotePort: str = None
    bridgeRemotePortUrl: str = None
    bridgeRemoteNodeId: int = None
    bridgeRemoteMAC: str = None
    bridgeRemoteIfIndex: int = None
    bridgeRemoteIP: str = None

    def __post_init__(self):
        if self.bridgeRemoteUrl:
            if remote_node := infer_node_from_url(url=self.bridgeRemoteUrl):
                self.bridgeRemoteNodeId = remote_node
        if self.bridgeRemotePort:
            if remote_ifindex := infer_ifindex(text=self.bridgeRemotePort):
                self.bridgeRemoteIfIndex = remote_ifindex
            if remote_ip := infer_ip(text=self.bridgeRemotePort):
                self.bridgeRemoteIP = remote_ip
        if self.bridgeRemote:
            if remote_mac := infer_mac(text=self.bridgeRemote):
                self.bridgeRemoteMAC = remote_mac


@dataclass
class BridgeLink(Link):
    "Bridge Link"
    bridgeLocalPort: str = None
    bridgeLocalPortUrl: str = None
    bridgeInfo: str = None
    bridgeLinkCreateTime: Union[str, datetime] = None
    bridgeLinkLastPollTime: Union[str, datetime] = None
    BridgeLinkRemoteNodes: List[BridgeLinkRemoteNode] = field(default_factory=list)
    linkType = LinkType.BRIDGE
    bridgeLocalNodeId: int = None
    bridgeLocalMAC: str = None
    bridgeLocalIfIndex: int = None

    def __post_init__(self):
        if isinstance(self.bridgeLinkCreateTime, str):
            self.bridgeLinkCreateTime = utils.convert_link_time(
                self.bridgeLinkCreateTime
            )
        if isinstance(self.bridgeLinkLastPollTime, str):
            self.bridgeLinkLastPollTime = utils.convert_link_time(
                self.bridgeLinkLastPollTime
            )
        if self.BridgeLinkRemoteNodes:
            if isinstance(self.BridgeLinkRemoteNodes[0], dict):
                remotes = []
                for remote in self.BridgeLinkRemoteNodes:
                    remotes.append(BridgeLinkRemoteNode(**remote))
                self.BridgeLinkRemoteNodes = remotes
        if self.bridgeLocalPortUrl:
            if local_node := infer_node_from_url(url=self.bridgeLocalPortUrl):
                self.bridgeLocalNodeId = local_node
        if self.bridgeLocalPort:
            if local_mac := infer_mac(self.bridgeLocalPort):
                self.bridgeLocalMAC = local_mac
            if local_ifindex := infer_ifindex(self.bridgeLocalPort):
                self.bridgeLocalIfIndex = local_ifindex


@dataclass
class CdpLink(Link):
    "CDP Link"
    cdpLocalPort: str = None
    cdpLocalPortUrl: str = None
    cdpCacheDevice: str = None
    cdpCacheDeviceUrl: str = None
    cdpCacheDevicePort: str = None
    cdpCacheDevicePortUrl: str = None
    cdpCachePlatform: str = None
    cdpCreateTime: Union[str, datetime] = None
    cdpLastPollTime: Union[str, datetime] = None
    linkType = LinkType.CDP
    cdpLocalNodeId: int = None
    cdpCacheDeviceNodeId: int = None
    cdpLocalIfIndex: int = None
    cdpCacheDeviceIfIndex: int = None
    cdpCacheDeviceIP: str = None

    def __post_init__(self):
        if isinstance(self.cdpCreateTime, str):
            self.cdpCreateTime = utils.convert_link_time(self.cdpCreateTime)
        if isinstance(self.cdpLastPollTime, str):
            self.cdpLastPollTime = utils.convert_link_time(self.cdpLastPollTime)
        if self.cdpLocalPortUrl:
            if local_node := infer_node_from_url(url=self.cdpLocalPortUrl):
                self.cdpLocalNodeId = local_node
        if self.cdpCacheDeviceUrl:
            if remote_node := infer_node_from_url(url=self.cdpCacheDeviceUrl):
                self.cdpCacheDeviceNodeId = remote_node
        if self.cdpLocalPort:
            if local_ifindex := infer_ifindex(self.cdpLocalPort):
                self.cdpLocalIfIndex = local_ifindex
        if self.cdpCacheDevicePort:
            if remote_ifindex := infer_ifindex(self.cdpCacheDevicePort):
                self.cdpCacheDeviceIfIndex = remote_ifindex
            if remote_ip := infer_ip(self.cdpCacheDevicePort):
                self.cdpCacheDeviceIP = remote_ip


@dataclass
class IsIsLink(Link):
    "IS-IS Link"
    isisCircIfIndex: int = None
    isisCircAdminState: str = None
    isisISAdjNeighSysID: str = None
    isisISAdjNeighSysType: str = None
    isisISAdjNeighSysUrl: str = None
    isisISAdjNeighSNPAAddress: str = None
    isisISAdjNeighPort: str = None
    isisISAdjState: str = None
    isisISAdjNbrExtendedCircID: int = None
    isisISAdjUrl: str = None
    isisLinkCreateTime: Union[str, datetime] = None
    isisLinkLastPollTime: Union[str, datetime] = None
    linkType = LinkType.ISIS
    isisLocalNodeId: int = None
    isisRemNodeId: int = None
    isisLocalMAC: str = None
    isisRemMAC: str = None
    isisLocalIfIndex: int = None
    isisRemIfIndex: int = None

    def __post_init__(self):
        if isinstance(self.isisLinkCreateTime, str):
            self.isisLinkCreateTime = utils.convert_link_time(self.isisLinkCreateTime)
        if isinstance(self.isisLinkLastPollTime, str):
            self.isisLinkLastPollTime = utils.convert_link_time(
                self.isisLinkLastPollTime
            )


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
class OspfLink(Link):
    "OSPF Link"
    ospfLocalPort: str = None
    ospfLocalPortUrl: str = None
    ospfRemRouterId: str = None
    ospfRemRouterUrl: str = None
    ospfRemPort: str = None
    ospfRemPortUrl: str = None
    ospfLinkInfo: str = None
    ospfLinkCreateTime: Union[str, datetime] = None
    ospfLinkLastPollTime: Union[str, datetime] = None
    linkType = LinkType.OSPF
    ospfLocalNodeId: int = None
    ospfRemNodeId: int = None
    ospfLocalMAC: str = None
    ospfRemMAC: str = None
    ospfLocalIfIndex: int = None
    ospfRemIfIndex: int = None

    def __post_init__(self):
        if isinstance(self.ospfLinkCreateTime, str):
            self.ospfLinkCreateTime = utils.convert_link_time(self.ospfLinkCreateTime)
        if isinstance(self.ospfLinkLastPollTime, str):
            self.ospfLinkLastPollTime = utils.convert_link_time(
                self.ospfLinkLastPollTime
            )


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
    bridge_links: List[BridgeLink] = field(default_factory=list)
    bridge_elements: List[BridgeElement] = field(default_factory=list)
    cdp_links: List[CdpLink] = field(default_factory=list)
    cdp_elements: List[CdpElement] = field(default_factory=list)
    isis_links: List[IsIsLink] = field(default_factory=list)
    isis_elements: List[IsisElement] = field(default_factory=list)
    lldp_links: List[LldpLink] = field(default_factory=list)
    lldp_elements: List[LldpElement] = field(default_factory=list)
    ospf_links: List[OspfLink] = field(default_factory=list)
    ospf_elements: List[OspfElement] = field(default_factory=list)


def infer_ifindex(text: str) -> int:
    "Infer ifIndex from string"
    ifindex = re.search(r"^.*\(ifindex:(\d+)\).*", text)
    if ifindex:
        return int(ifindex.group(1))


def infer_ip(text: str) -> str:
    "Infer IP address from string"
    ip = re.search(r"^.*\((((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})\).*", text)
    if ip:
        return ip.group(1)


def infer_node_from_url(url: str) -> int:
    "Infer node ID from url querystring"
    node = re.search(r"^.*node=(\d+).*", url)
    if node:
        return int(node.group(1))


def infer_mac(text: str) -> str:
    "Infer MAC address from string"
    mac = re.search(r"^.*\((mac|macAddress):([0-9A-Fa-f]+)\).*", text)
    if mac:
        return mac.group(2)
