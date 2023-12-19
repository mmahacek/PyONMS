# dao.nodes.py

# cspell:ignore snmpinterfaces, ipinterfaces

import concurrent.futures
from enum import Enum
from typing import List, Optional

from tqdm import tqdm

import pyonms.models.node
from pyonms.dao.base import Endpoint


class NodeComponents(Enum):
    ALL = "ALL"
    SNMP = "SnmpInterfaces"
    IP = "IpInterfaces"
    SERVICES = "IpServices"
    METADATA = "MetaData"
    HARDWARE = "HardwareInventory"


class NodeAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "nodes"

    def get_node(
        self, id: int, components: List[NodeComponents] = None
    ) -> Optional[pyonms.models.node.Node]:
        if not components:
            components = [NodeComponents.ALL]
        record = self._get(url=f"{self.url}/{id}")
        if record is not None:
            return self._process_node(record, components=components)
        else:
            return None

    def get_nodes(
        self,
        fiql: str = None,
        limit: int = 100,
        batch_size: int = 100,
        components: List[NodeComponents] = None,
        threads: int = 10,
    ) -> List[Optional[pyonms.models.node.Node]]:
        if not components:
            components = [NodeComponents.ALL]
        devices = []
        params = {}
        if fiql:
            params["_s"] = fiql
        records = self._get_batch(
            url=self.url,
            endpoint="node",
            limit=limit,
            batch_size=batch_size,
            params=params,
        )
        if records == [None]:
            return [None]
        if threads > len(records):
            threads = len(records)
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as pool:
            with tqdm(
                total=len(records),
                unit="node",
                desc=f"Hydrating {self.name} Node objects",
            ) as progress:
                futures = []
                for record in records:
                    future = pool.submit(
                        self._process_node, data=record, components=components
                    )
                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)
                for future in futures:
                    result = future.result()
                    devices.append(result)
        return devices

    def _get_node_snmpinterfaces(
        self, node_id: int
    ) -> List[Optional[pyonms.models.node.SnmpInterface]]:
        interfaces = []
        records = self._get_batch(
            url=f"{self.url}/{node_id}/snmpinterfaces",
            endpoint="snmpInterface",
            hide_progress=True,
        )
        if records:
            for snmp_interface in records:
                if snmp_interface:
                    interfaces.append(
                        pyonms.models.node.SnmpInterface(**snmp_interface)
                    )
        return interfaces

    def _get_node_ip_addresses(
        self, node_id: int, services: bool = False, metadata: bool = False
    ) -> List[Optional[pyonms.models.node.IPInterface]]:
        ip_addresses = []
        records = self._get_batch(
            url=f"{self.url}/{node_id}/ipinterfaces",
            endpoint="ipInterface",
            hide_progress=True,
        )
        if records:
            for ip_interface in records:
                if ip_interface:
                    ip = pyonms.models.node.IPInterface(**ip_interface)
                    if services:
                        ip.services = self._get_node_ip_services(
                            node_id=node_id, ip_address=ip.ipAddress, metadata=metadata
                        )
                    if metadata:
                        ip.metadata = self._get_ip_metadata(
                            node_id=node_id, ipaddress=ip.ipAddress
                        )
                    ip_addresses.append(ip)
                else:
                    pass
        return ip_addresses

    def _get_node_ip_services(
        self, node_id: int, ip_address: str, metadata: bool = False
    ) -> List[Optional[pyonms.models.node.Service]]:
        services = []
        records = self._get_batch(
            url=f"{self.url}/{node_id}/ipinterfaces/{ip_address}/services",
            endpoint="service",
            hide_progress=True,
        )
        if records:
            for service in records:
                if service:
                    new_service = pyonms.models.node.Service(**service)
                    if metadata:
                        new_service.metadata = self._get_service_metadata(
                            node_id=node_id,
                            ipaddress=ip_address,
                            service=new_service.serviceType.name,
                        )
                    if new_service not in services:
                        services.append(new_service)
        return services

    def _get_node_metadata(
        self, node_id: int
    ) -> List[Optional[pyonms.models.node.Metadata]]:
        metadata = []
        records = self._get_batch(
            url=f"{self.url}/{node_id}/metadata",
            endpoint="metaData",
            hide_progress=True,
        )
        for record in records:
            if record:
                metadata.append(pyonms.models.node.Metadata(**record))
        return metadata

    def _get_ip_metadata(
        self, node_id: int, ipaddress: str
    ) -> List[Optional[pyonms.models.node.Metadata]]:
        metadata = []
        records = self._get_batch(
            url=f"{self.url}/{node_id}/ipinterfaces/{ipaddress}/metadata",
            endpoint="metaData",
            hide_progress=True,
        )
        for record in records:
            if record:
                metadata.append(pyonms.models.node.Metadata(**record))
        return metadata

    def _get_service_metadata(
        self, node_id: int, ipaddress: str, service: str
    ) -> List[Optional[pyonms.models.node.Metadata]]:
        metadata = []
        records = self._get_batch(
            url=f"{self.url}/{node_id}/ipinterfaces/{ipaddress}/services/{service}/metadata",
            endpoint="metaData",
            hide_progress=True,
        )
        for record in records:
            if record:
                metadata.append(pyonms.models.node.Metadata(**record))
        return metadata

    def _get_node_hardware(
        self, node_id: int
    ) -> Optional[pyonms.models.node.HardwareInventory]:
        record = self._get(url=f"{self.url}/{node_id}/hardwareInventory")
        return pyonms.models.node.HardwareInventory(**record)

    def _process_node(self, data: dict, components: list) -> pyonms.models.node.Node:
        node = pyonms.models.node.Node(**data)
        if NodeComponents.ALL in components:
            node.ipInterfaces = self._get_node_ip_addresses(
                node.id, services=True, metadata=True
            )
            node.snmpInterfaces = self._get_node_snmpinterfaces(node.id)
            node.metadata = self._get_node_metadata(node.id)
            node.hardwareInventory = self._get_node_hardware(node.id)
            return node
        get_metadata = False
        if NodeComponents.METADATA in components:
            node.metadata = self._get_node_metadata(node.id)
            get_metadata = True
        if NodeComponents.SERVICES in components:
            node.ipInterfaces = self._get_node_ip_addresses(
                node.id, services=True, metadata=get_metadata
            )
        elif NodeComponents.IP in components:
            node.ipInterfaces = self._get_node_ip_addresses(
                node.id, services=False, metadata=get_metadata
            )
        if NodeComponents.SNMP in components:
            node.snmpInterfaces = self._get_node_snmpinterfaces(node.id)
        if NodeComponents.HARDWARE in components:
            node.hardwareInventory = self._get_node_hardware(node.id)

        return node
