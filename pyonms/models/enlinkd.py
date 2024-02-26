# models.enlinkd.py

"Enlinkd Models"

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

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
    bridgeRemote: Optional[str] = None
    bridgeRemoteUrl: Optional[str] = None
    bridgeRemotePort: Optional[str] = None
    bridgeRemotePortUrl: Optional[str] = None
    bridgeRemoteNodeId: Optional[int] = None
    bridgeRemoteMAC: Optional[str] = None
    bridgeRemoteIfIndex: Optional[int] = None
    bridgeRemoteIP: Optional[str] = None

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
    bridgeLocalPort: Optional[str] = None
    bridgeLocalPortUrl: Optional[str] = None
    bridgeInfo: Optional[str] = None
    bridgeLinkCreateTime: Optional[Union[str, datetime]] = None
    bridgeLinkLastPollTime: Optional[Union[str, datetime]] = None
    BridgeLinkRemoteNodes: List[Optional[BridgeLinkRemoteNode]] = field(
        default_factory=list
    )
    linkType = LinkType.BRIDGE
    bridgeLocalNodeId: Optional[int] = None
    bridgeLocalMAC: Optional[str] = None
    bridgeLocalIfIndex: Optional[int] = None

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
    cdpLocalPort: Optional[str] = None
    cdpLocalPortUrl: Optional[str] = None
    cdpCacheDevice: Optional[str] = None
    cdpCacheDeviceUrl: Optional[str] = None
    cdpCacheDevicePort: Optional[str] = None
    cdpCacheDevicePortUrl: Optional[str] = None
    cdpCachePlatform: Optional[str] = None
    cdpCreateTime: Optional[Union[str, datetime]] = None
    cdpLastPollTime: Optional[Union[str, datetime]] = None
    linkType = LinkType.CDP
    cdpLocalNodeId: Optional[int] = None
    cdpCacheDeviceNodeId: Optional[int] = None
    cdpLocalIfIndex: Optional[int] = None
    cdpCacheDeviceIfIndex: Optional[int] = None
    cdpCacheDeviceIP: Optional[str] = None

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
    isisCircIfIndex: Optional[int] = None
    isisCircAdminState: Optional[str] = None
    isisISAdjNeighSysID: Optional[str] = None
    isisISAdjNeighSysType: Optional[str] = None
    isisISAdjNeighSysUrl: Optional[str] = None
    isisISAdjNeighSNPAAddress: Optional[str] = None
    isisISAdjNeighPort: Optional[str] = None
    isisISAdjState: Optional[str] = None
    isisISAdjNbrExtendedCircID: Optional[int] = None
    isisISAdjUrl: Optional[str] = None
    isisLinkCreateTime: Optional[Union[str, datetime]] = None
    isisLinkLastPollTime: Optional[Union[str, datetime]] = None
    linkType = LinkType.ISIS
    isisLocalNodeId: Optional[int] = None
    isisRemNodeId: Optional[int] = None
    isisLocalMAC: Optional[str] = None
    isisRemMAC: Optional[str] = None
    isisLocalIfIndex: Optional[int] = None
    isisRemIfIndex: Optional[int] = None

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
    lldpLocalPort: Optional[str] = None
    lldpLocalPortUrl: Optional[str] = None
    lldpRemChassisId: Optional[str] = None
    lldpRemChassisIdUrl: Optional[str] = None
    lldpRemInfo: Optional[str] = None
    ldpRemPort: Optional[str] = None
    lldpCreateTime: Optional[Union[str, datetime]] = None
    lldpLastPollTime: Optional[Union[str, datetime]] = None
    linkType = LinkType.LLDP
    lldpLocalNodeId: Optional[int] = None
    lldpRemNodeId: Optional[int] = None
    lldpLocalMAC: Optional[str] = None
    lldpRemMAC: Optional[str] = None
    lldpLocalIfIndex: Optional[int] = None
    lldpRemIfIndex: Optional[int] = None

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
    ospfLocalPort: Optional[str] = None
    ospfLocalPortUrl: Optional[str] = None
    ospfRemRouterId: Optional[str] = None
    ospfRemRouterUrl: Optional[str] = None
    ospfRemPort: Optional[str] = None
    ospfRemPortUrl: Optional[str] = None
    ospfLinkInfo: Optional[str] = None
    ospfLinkCreateTime: Optional[Union[str, datetime]] = None
    ospfLinkLastPollTime: Optional[Union[str, datetime]] = None
    linkType = LinkType.OSPF
    ospfLocalNodeId: Optional[int] = None
    ospfRemNodeId: Optional[int] = None
    ospfLocalMAC: Optional[str] = None
    ospfRemMAC: Optional[str] = None
    ospfLocalIfIndex: Optional[int] = None
    ospfRemIfIndex: Optional[int] = None

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
    baseBridgeAddress: Optional[str] = None
    baseNumPorts: Optional[int] = None
    baseType: Optional[str] = None
    stpProtocolSpecification: Optional[str] = None
    stpPriority: Optional[str] = None
    stpDesignatedRoot: Optional[str] = None
    stpRootCost: Optional[int] = None
    stpRootPort: Optional[int] = None
    vlan: Optional[str] = None
    vlanname: Optional[str] = None
    bridgeNodeCreateTime: Optional[Union[str, datetime]] = None
    bridgeNodeLastPollTime: Optional[Union[str, datetime]] = None
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
    cdpGlobalRun: Optional[str] = None
    cdpGlobalDeviceId: Optional[str] = None
    cdpGlobalDeviceIdFormat: Optional[str] = None
    cdpCreateTime: Optional[Union[str, datetime]] = None
    cdpLastPollTime: Optional[Union[str, datetime]] = None
    linkType = LinkType.CDP

    def __post_init__(self):
        if isinstance(self.cdpCreateTime, str):
            self.cdpCreateTime = utils.convert_link_time(self.cdpLastPollTime)
        if isinstance(self.cdpLastPollTime, str):
            self.cdpLastPollTime = utils.convert_link_time(self.cdpLastPollTime)


@dataclass
class IsisElement(Element):
    "IS-IS Element"
    isisSysID: Optional[str] = None
    isisSysAdminState: Optional[str] = None
    isisCreateTime: Optional[Union[str, datetime]] = None
    isisLastPollTime: Optional[Union[str, datetime]] = None
    linkType = LinkType.ISIS

    def __post_init__(self):
        if isinstance(self.isisCreateTime, str):
            self.isisCreateTime = utils.convert_link_time(self.isisCreateTime)
        if isinstance(self.isisLastPollTime, str):
            self.isisLastPollTime = utils.convert_link_time(self.isisLastPollTime)


@dataclass
class LldpElement(Element):
    "LLDP Element"
    lldpChassisId: Optional[str] = None
    lldpSysName: Optional[str] = None
    lldpCreateTime: Optional[Union[str, datetime]] = None
    lldpLastPollTime: Optional[Union[str, datetime]] = None
    linkType = LinkType.LLDP

    def __post_init__(self):
        if isinstance(self.lldpCreateTime, str):
            self.lldpCreateTime = utils.convert_link_time(self.lldpCreateTime)
        if isinstance(self.lldpLastPollTime, str):
            self.lldpLastPollTime = utils.convert_link_time(self.lldpLastPollTime)


@dataclass
class OspfElement(Element):
    "OSPF Element"
    ospfRouterId: Optional[str] = None
    ospfVersionNumber: Optional[int] = None
    ospfAdminStat: Optional[str] = None
    ospfCreateTime: Optional[Union[str, datetime]] = None
    ospfLastPollTime: Optional[Union[str, datetime]] = None
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


def infer_ifindex(text: str) -> Optional[int]:
    "Infer ifIndex from string"
    ifindex = re.search(r"^.*\(ifindex:(\d+)\).*", text)
    if ifindex:
        return int(ifindex.group(1))
    else:
        return None


def infer_ip(text: str) -> Optional[str]:
    "Infer IP address from string"
    ip = re.search(r"^.*\((((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})\).*", text)
    if ip:
        return ip.group(1)
    else:
        return None


def infer_node_from_url(url: str) -> Optional[int]:
    "Infer node ID from url querystring"
    node = re.search(r"^.*node=(\d+).*", url)
    if node:
        return int(node.group(1))
    else:
        return None


def infer_mac(text: str) -> Optional[str]:
    "Infer MAC address from string"
    mac = re.search(r"^.*\((mac|macAddress):([0-9A-Fa-f]+)\).*", text)
    if mac:
        return mac.group(2)
    else:
        return None
