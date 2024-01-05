# tests.test_nodes.py

# pylint: disable=C0114,C0116,W0621,W0212

from datetime import datetime

import pytest

from pyonms import PyONMS
from pyonms.dao.nodes import NodeComponents
from pyonms.models.node import (
    IPInterface,
    LabelSource,
    Metadata,
    Node,
    NodeType,
    Service,
    SnmpInterface,
)


@pytest.mark.vcr()
def test_node_one(test_instance: PyONMS):
    test_node = test_instance.nodes.get_node(
        id=2, components=[NodeComponents.IP, NodeComponents.SNMP, NodeComponents.SNMP]
    )
    assert isinstance(test_node, Node)
    assert test_node.id == 2
    assert test_node.label == "remwmmaha2"
    assert test_node.assetRecord.maintContractExpiration == "2030-12-31"
    assert test_node.labelSource == LabelSource.USER
    assert test_node.type == NodeType.ACTIVE
    assert isinstance(test_node.lastCapsdPoll, datetime)
    assert test_node.ipInterfaces[0].ifIndex == 30
    assert test_node.snmpInterfaces[1].ifType == 6


@pytest.mark.vcr()
def test_node_all(test_instance: PyONMS):
    nodes = test_instance.nodes.get_nodes(limit=0, components=[NodeComponents.NONE])
    assert len(nodes) == 23
    assert nodes[0].id == 7


@pytest.mark.vcr()
def test_node_batch(test_instance: PyONMS):
    nodes = test_instance.nodes.get_nodes(
        limit=10, batch_size=3, components=[NodeComponents.NONE]
    )
    assert len(nodes) == 10
    assert nodes[0].id == 7


@pytest.mark.vcr()
def test_node_snmp(test_instance: PyONMS):
    test_interfaces = test_instance.nodes._get_node_snmpinterfaces(2)
    assert len(test_interfaces) == 68
    assert isinstance(test_interfaces[0], SnmpInterface)
    assert test_interfaces[0].id == 195


@pytest.mark.vcr()
def test_node_ip(test_instance: PyONMS):
    test_interfaces = test_instance.nodes._get_node_ip_addresses(2, services=True)
    assert len(test_interfaces) == 4
    assert isinstance(test_interfaces[0], IPInterface)
    assert test_interfaces[0].ipAddress == "192.168.86.160"
    assert len(test_interfaces[0].services) == 5


@pytest.mark.vcr()
def test_node_ip_services(test_instance: PyONMS):
    test_services = test_instance.nodes._get_node_ip_services(2, "192.168.86.160")
    assert isinstance(test_services[0], Service)
    assert len(test_services) == 5
    assert test_services[0].id == 9
    assert test_services[0].lastGood == datetime(2024, 1, 4, 17, 45, 5, 647000)
    assert test_services[0].serviceType.id == 6


@pytest.mark.vcr()
def test_node_metadata(test_instance: PyONMS):
    test_metadata = test_instance.nodes._get_node_metadata(2)
    assert isinstance(test_metadata[0], Metadata)
    assert test_metadata[0].context == "requisition"
    assert len(test_metadata) == 5
