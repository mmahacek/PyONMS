# dao.nodes.py

# cspell:ignore snmpinterfaces, ipinterfaces


import ipaddress
from pyonms.dao.api import Endpoint
import pyonms.models.node


class NodeAPI(Endpoint):
    def __init__(self, args):
        super().__init__(**args)
        self.url = self.base_v2 + "nodes"

    def get_node(self, id: int) -> pyonms.models.node.Node:
        record = self._get(uri=f"{self.url}/{id}")
        if record is not None:
            return self.process_node(record)
        else:
            return None

    def get_nodes(self, limit=10, batchSize=10) -> list:
        devices = []
        records = self.get_data(
            url=self.url,
            endpoint="node",
            limit=limit,
            batchSize=batchSize,
        )
        if records == [None]:
            return None
        for record in records:
            devices.append(self.process_node(record))
        return devices

    def get_node_snmpinterfaces(self, node_id: int) -> list:
        interfaces = []
        snmpRecords = self._get(uri=f"{self.url}/{node_id}/snmpinterfaces")
        if snmpRecords:
            for s in snmpRecords["snmpInterface"]:
                interfaces.append(pyonms.models.node.SnmpInterface(**s))
        return interfaces

    def get_node_ip_addresses(self, node_id: int) -> list:
        ip_addresses = []
        ipRecords = self._get(uri=f"{self.url}/{node_id}/ipinterfaces")
        if ipRecords:
            for i in ipRecords["ipInterface"]:
                ip = pyonms.models.node.IPInterface(**i)
                ip.services = self.get_node_ip_services(node_id, ip.ipAddress)
                ip_addresses.append(ip)
        return ip_addresses

    def get_node_ip_services(self, node_id: int, ip_address: str) -> list:
        services = []
        sRecords = self._get(
            uri=f"{self.url}/{node_id}/ipinterfaces/{ip_address}/services"
        )
        if sRecords:
            for sr in sRecords["service"]:
                services.append(pyonms.models.node.Service(**sr))
        return services

    def get_node_metadata(self, node_id: int) -> list:
        metadata = []
        mRecords = self._get(uri=f"{self.url}/{node_id}/metadata")
        for record in mRecords["metaData"]:
            metadata.append(pyonms.models.node.Metadata(**record))
        return metadata

    def process_node(self, data):
        node = pyonms.models.node.Node(**data)
        node.snmpInterfaces = self.get_node_snmpinterfaces(node.id)
        node.ipInterfaces = self.get_node_ip_addresses(node.id)
        node.metadata = self.get_node_metadata(node.id)

        return node
