# dao.nodes.py

# cspell:ignore snmpinterfaces, ipinterfaces

from typing import List, Union

from pyonms.dao import Endpoint
import pyonms.models.node


class NodeAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "nodes"

    def get_node(self, id: int) -> Union[pyonms.models.node.Node, None]:
        record = self._get(uri=f"{self.url}/{id}")
        if record is not None:
            return self.process_node(record)
        else:
            return None

    def get_nodes(
        self, limit=100, batch_size=100
    ) -> List[Union[pyonms.models.node.Node, None]]:
        devices = []
        records = self.get_batch(
            url=self.url,
            endpoint="node",
            limit=limit,
            batch_size=batch_size,
        )
        if records == [None]:
            return [None]
        for record in records:
            devices.append(self.process_node(record))
        return devices

    def get_node_snmpinterfaces(
        self, node_id: int
    ) -> List[pyonms.models.node.SnmpInterface]:
        interfaces = []
        records = self._get(uri=f"{self.url}/{node_id}/snmpinterfaces")
        if records:
            for snmp_interface in records["snmpInterface"]:
                interfaces.append(pyonms.models.node.SnmpInterface(**snmp_interface))
        return interfaces

    def get_node_ip_addresses(
        self, node_id: int
    ) -> List[pyonms.models.node.IPInterface]:
        ip_addresses = []
        records = self._get(uri=f"{self.url}/{node_id}/ipinterfaces")
        if records:
            for ip_interface in records["ipInterface"]:
                ip = pyonms.models.node.IPInterface(**ip_interface)
                ip.services = self.get_node_ip_services(node_id, ip.ipAddress)
                ip_addresses.append(ip)
        return ip_addresses

    def get_node_ip_services(
        self, node_id: int, ip_address: str
    ) -> List[pyonms.models.node.Service]:
        services = []
        records = self._get(
            uri=f"{self.url}/{node_id}/ipinterfaces/{ip_address}/services"
        )
        if records:
            for service in records["service"]:
                services.append(pyonms.models.node.Service(**service))
        return services

    def get_node_metadata(self, node_id: int) -> List[pyonms.models.node.Metadata]:
        metadata = []
        records = self._get(uri=f"{self.url}/{node_id}/metadata")
        for record in records["metaData"]:
            metadata.append(pyonms.models.node.Metadata(**record))
        return metadata

    def process_node(self, data) -> pyonms.models.node.Node:
        node = pyonms.models.node.Node(**data)
        node.snmpInterfaces = self.get_node_snmpinterfaces(node.id)
        node.ipInterfaces = self.get_node_ip_addresses(node.id)
        node.metadata = self.get_node_metadata(node.id)
        return node
