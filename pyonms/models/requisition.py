# models.requisition.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from pyonms.models import exceptions
from pyonms.models.node import AssetRecord, Metadata, PrimaryType
from pyonms.utils import convert_time

NODE_ATTRIBUTES = [
    "node_label",
    "location",
    "building",
    "city",
    "parent_foreign_source",
    "parent_foreign_id",
    "parent_node_label",
]

ASSET_FIELDS = [item for item in dir(AssetRecord) if item[0] != "_"]


@dataclass
class Category:
    name: str

    def __hash__(self):
        return hash((self.name))

    def _to_dict(self) -> dict:
        return {"name": self.name}


@dataclass
class AssetField:
    name: str
    value: str = None

    def __post_init__(self):
        if self.name not in ASSET_FIELDS:
            raise exceptions.InvalidValueError(
                "Asset field", self.name, valid=ASSET_FIELDS
            )

    def __hash__(self):
        return hash((self.name, self.value))

    def _to_dict(self) -> dict:
        return {"name": self.name, "value": self.value}


@dataclass
class Service:
    service_name: str
    category: List[Category] = field(default_factory=list)
    meta_data: List[Metadata] = field(default_factory=list)

    def __post_init__(self):
        for index, category in enumerate(self.category):
            if isinstance(category, dict):
                self.category[index] = Category(**category)
        for index, metadata in enumerate(self.meta_data):
            if isinstance(metadata, dict):
                self.meta_data[index] = Metadata(**metadata)

    def __hash__(self):
        return hash((self.service_name))

    def _to_dict(self) -> dict:
        payload = {"service-name": self.service_name}
        payload["category"] = [category._to_dict() for category in self.category]
        payload["meta-data"] = [
            data._to_dict() for data in self.meta_data if data.value
        ]

        return payload

    def set_metadata(self, key: str, value: str):
        """Add or update metadata for the service.
        If a Metadata record for the given key exists, it will be replaced with the new value, otherwise a new record will be added.
        Set `value` to none to remove the key.
        Context will be "requisition".
        """
        for data in self.meta_data:
            if data.key == key:
                data.value = value
                return
        self.meta_data.append(Metadata(context="requisition", key=key, value=value))


@dataclass
class Interface:
    ip_addr: str
    status: int = 1
    snmp_primary: PrimaryType = None
    descr: str = None
    managed: str = None
    monitored_service: List[Service] = field(default_factory=list)
    category: List[Category] = field(default_factory=list)
    meta_data: List[Metadata] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.snmp_primary, str):
            self.snmp_primary = PrimaryType(self.snmp_primary)
        for index, category in enumerate(self.category):
            if isinstance(category, dict):
                self.category[index] = Category(**category)
        for index, metadata in enumerate(self.meta_data):
            if isinstance(metadata, dict):
                self.meta_data[index] = Metadata(**metadata)
        for index, service in enumerate(self.monitored_service):
            if isinstance(service, dict):
                self.monitored_service[index] = Service(**service)

    def __hash__(self):
        return hash((self.ip_addr))

    def _to_dict(self):
        payload = {
            "ip-addr": self.ip_addr,
            "status": self.status,
            "snmp-primary": self.snmp_primary.value,
        }
        if self.descr:
            payload["descr"] = self.descr
        payload["monitored-service"] = [
            service._to_dict() for service in self.monitored_service
        ]
        payload["category"] = [category._to_dict() for category in self.category]
        payload["meta-data"] = [data.to_dict() for data in self.meta_data if data.value]
        return payload

    def set_metadata(self, key: str, value: str):
        """Add or update metadata for the interface.
        If a Metadata record for the given key exists, it will be replaced with the new value, otherwise a new record will be added.
        Set `value` to none to remove the key.
        Context will be "requisition".
        """
        for data in self.meta_data:
            if data.key == key:
                data.value = value
                return
        self.meta_data.append(Metadata(context="requisition", key=key, value=value))


@dataclass
class RequisitionNode:
    foreign_id: str
    node_label: str
    location: str = None
    building: str = None
    city: str = None
    parent_foreign_source: str = None
    parent_foreign_id: str = None
    parent_node_label: str = None
    asset: List[AssetField] = field(default_factory=list)
    category: List[Category] = field(default_factory=list)
    interface: Dict[str, Interface] = field(default_factory=dict)
    meta_data: List[Metadata] = field(default_factory=list)

    def __post_init__(self):  # noqa C901
        self.foreign_id = str(self.foreign_id)
        for index, asset in enumerate(self.asset):
            if isinstance(asset, dict):
                self.asset[index] = AssetField(**asset)
        for index, category in enumerate(self.category):
            if isinstance(category, dict):
                self.category[index] = Category(**category)
        for index, metadata in enumerate(self.meta_data):
            if isinstance(metadata, dict):
                self.meta_data[index] = Metadata(**metadata)
        if isinstance(self.interface, list):
            interfaces = {}
            for interface in self.interface:
                if isinstance(interface, dict):
                    new_interface = Interface(**interface)
                    interfaces[new_interface.ip_addr] = new_interface
                elif isinstance(interface, Interface):
                    interfaces[interface.ip_addr] = interface
            self.interface = interfaces
        elif self.interface and isinstance(self.interface, dict):
            new_interface = Interface(**self.interface)
            self.interface = {new_interface.ip_addr: new_interface}

    def _to_dict(self) -> dict:
        payload = {"foreign-id": self.foreign_id}
        for node_field in NODE_ATTRIBUTES:
            if getattr(self, node_field):
                payload[node_field.replace("_", "-")] = getattr(self, node_field)
        payload["asset"] = [asset._to_dict() for asset in self.asset if asset.value]
        payload["category"] = [category._to_dict() for category in self.category]
        payload["interface"] = [
            interface._to_dict() for interface in self.interface.values()
        ]
        payload["meta-data"] = [
            data._to_dict() for data in self.meta_data if data.value
        ]
        return payload

    def add_interface(self, interface: Interface, merge: bool = True):
        """Add an IP interface to the node

        Args:
            node (`Interface`): IP interface to add.
            merge (bool, optional): Merge non-null attributes with existing interface in requisition. Set to `False` to overwrite entire node record. Defaults to `True`.

        Raises:
            pyonms.models.exceptions.MethodNotImplemented: If `merge` not set to `False`
        """  # noqa
        if merge:
            if interface.ip_addr not in self.interface.keys():
                self.interface[interface.ip_addr] = interface
            else:
                raise exceptions.MethodNotImplemented
        else:
            self.interface[interface.ip_addr] = interface

    def change_ip(self, old_ip: str, new_ip: str):
        """Change the IP address of an existing IP interface

        Args:
            old_ip (str): Existing IP address
            new_ip (str): New IP address

        Raises:
            pyonms.models.exceptions.InvalidValueError: If the `old_ip` does not exist on the node.
            pyonms.models.exceptions.DuplicateEntityError: If the `new_ip` already exists on another IP Interface.
        """  # noqa
        if old_ip not in self.interface.keys():
            raise exceptions.InvalidValueError(
                name="old_ip", value=old_ip, valid=self.interface.keys()
            )
        if new_ip not in self.interface.keys():
            self.interface[new_ip] = self.interface[old_ip]
            self.interface[new_ip].ip_addr = new_ip
            del self.interface[old_ip]
        else:
            raise exceptions.DuplicateEntityError(name="IP Address", value=new_ip)

    def set_metadata(self, key: str, value: str):
        """Add or update metadata for the node.

        Args:
            key (str):   Metadata key.
            value (str): Metadata value. Set to `None` to remove the entry.
        """
        for data in self.meta_data:
            if data.key == key:
                data.value = value
                return
        self.meta_data.append(Metadata(context="requisition", key=key, value=value))

    def set_asset(self, name: str, value: str):
        """Add or update asset data for the node.

        Args:
            name (str):  Asset field name.
            value (str): Asset field value. Set to `None` to remove the entry.
        """
        for data in self.asset:
            if data.name == name:
                data.value = value
                return
        self.asset.append(AssetField(name=name, value=value))

    def add_category(self, category: str):
        """Add category to node, if not currently assigned

        Args:
            category (str): Category name
        """
        if category not in [cat.name for cat in self.category]:
            self.category.append(Category(name=category))

    def remove_category(self, category: str):
        """Remove category from node

        Args:
            category (str): Category name"""
        self.category = [cat for cat in self.category if cat.name != category]


@dataclass
class Requisition:
    foreign_source: str
    date_stamp: datetime = None
    last_import: datetime = None
    node: Dict[str, RequisitionNode] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.date_stamp, int):
            self.date_stamp = convert_time(self.date_stamp)
        if isinstance(self.last_import, int):
            self.last_import = convert_time(self.last_import)
        if isinstance(self.node, dict):
            self.node = [self.node]
        if self.node and isinstance(self.node, list):
            nodes = {}
            for node in self.node:
                if node and isinstance(node, dict):
                    new_node = RequisitionNode(**node)
                    nodes[new_node.foreign_id] = new_node
                elif node and isinstance(node, RequisitionNode):
                    nodes[node.foreign_id] = node
            self.node = nodes

    def _to_dict(self) -> dict:
        payload = {"foreign-source": self.foreign_source}
        payload["node"] = [node._to_dict() for node in self.node.values()]
        for time_field in ["date_stamp", "last_import"]:
            if getattr(self, time_field):
                payload[time_field.replace("_", "-")] = int(
                    datetime.timestamp(getattr(self, time_field)) * 1000
                )
        return payload

    def add_node(self, node: RequisitionNode, merge: bool = True):
        """Add a node to the requisition

        Args:
            node (`RequisitionNode`): Node to add.
            merge (bool, optional): Merge non-null attributes with existing node in requisition. Set to `False` to overwrite entire node record. Defaults to `True`.

        Raises:
            pyonms.models.exceptions.MethodNotImplemented: If `merge` not set to `False`
        """  # noqa
        if merge:
            if node.foreign_id not in self.node.keys():
                self.node[node.foreign_id] = node
            else:
                raise exceptions.MethodNotImplemented
        else:
            self.node[node.foreign_id] = node

    def remove_node(self, foreign_id: str):
        if foreign_id in self.node.keys():
            del self.node[foreign_id]
        else:
            raise exceptions.InvalidValueError(name="Foreign ID", value=foreign_id)
