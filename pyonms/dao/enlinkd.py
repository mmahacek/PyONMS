# dao.enlinkd.py

"Enlinkd Endpoint"

from typing import List, Optional

import pyonms.models.enlinkd
from pyonms.dao.base import Endpoint


class EnlinkdAPI(Endpoint):
    "Enlinkd API Endpoint"

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "enlinkd"

    def get_node_links(self, node_id: int) -> Optional[pyonms.models.enlinkd.Topology]:
        "Get all links for a given node."
        record = self._get(url=f"{self.url}/{node_id}")
        if record not in [None, {}]:
            return self._process_topology(record)
        else:
            return None

    def _process_topology(self, data: dict) -> pyonms.models.enlinkd.Topology:
        topology = pyonms.models.enlinkd.Topology()
        if data.get("bridgeLinkNodes"):
            topology.bridge_links = self._process_bridge_links(
                data=data["bridgeLinkNodes"]
            )
        if data.get("cdpLinkNodes"):
            topology.cdp_links = self._process_cdp_links(data=data["cdpLinkNodes"])
        if data.get("isisLinkNodes"):
            topology.isis_links = self._process_isis_links(data=data["isisLinkNodes"])
        if data.get("lldpLinkNodes"):
            topology.lldp_links = self._process_lldp_links(data=data["lldpLinkNodes"])
        if data.get("ospfLinkNodes"):
            topology.ospf_links = self._process_ospf_links(data=data["ospfLinkNodes"])
        if data.get("bridgeElementNodes"):
            topology.bridge_elements = self._process_bridge_elements(
                data=data["bridgeElementNodes"]
            )
        if data.get("cdpElementNode"):
            topology.cdp_elements.append(
                self._process_cdp_element(data=data["cdpElementNode"])
            )
        if data.get("isisElementNode"):
            topology.isis_elements.append(
                self._process_isis_element(data=data["isisElementNode"])
            )
        if data.get("lldpElementNode"):
            topology.lldp_elements.append(
                self._process_lldp_element(data=data["lldpElementNode"])
            )
        if data.get("ospfElementNode"):
            topology.ospf_elements.append(
                self._process_ospf_element(data=data["ospfElementNode"])
            )
        return topology

    def _process_bridge_links(
        self, data: list[dict]
    ) -> List[pyonms.models.enlinkd.BridgeLink]:
        links = []
        for link in data:
            links.append(pyonms.models.enlinkd.BridgeLink(**link))
        return links

    def _process_cdp_links(
        self, data: list[dict]
    ) -> List[pyonms.models.enlinkd.CdpLink]:
        links = []
        for link in data:
            links.append(pyonms.models.enlinkd.CdpLink(**link))
        return links

    def _process_isis_links(
        self, data: list[dict]
    ) -> List[pyonms.models.enlinkd.IsIsLink]:
        links = []
        for link in data:
            links.append(pyonms.models.enlinkd.IsIsLink(**link))
        return links

    def _process_lldp_links(
        self, data: list[dict]
    ) -> List[pyonms.models.enlinkd.LldpLink]:
        links = []
        for link in data:
            links.append(pyonms.models.enlinkd.LldpLink(**link))
        return links

    def _process_ospf_links(
        self, data: list[dict]
    ) -> List[pyonms.models.enlinkd.OspfLink]:
        links = []
        for link in data:
            links.append(pyonms.models.enlinkd.OspfLink(**link))
        return links

    def _process_bridge_elements(
        self, data: dict
    ) -> List[pyonms.models.enlinkd.BridgeElement]:
        elements = []
        for element in data:
            elements.append(pyonms.models.enlinkd.BridgeElement(**element))
        return elements

    def _process_cdp_element(self, data: dict) -> pyonms.models.enlinkd.CdpElement:
        return pyonms.models.enlinkd.CdpElement(**data)

    def _process_isis_element(self, data: dict) -> pyonms.models.enlinkd.IsisElement:
        return pyonms.models.enlinkd.IsisElement(**data)

    def _process_lldp_element(self, data: dict) -> pyonms.models.enlinkd.LldpElement:
        return pyonms.models.enlinkd.LldpElement(**data)

    def _process_ospf_element(self, data: dict) -> pyonms.models.enlinkd.OspfElement:
        return pyonms.models.enlinkd.OspfElement(**data)
