# tests.test_requisitions.py

# pylint: disable=C0114,C0116,W0621,W0212

import pytest

from pyonms import PyONMS
from pyonms.models.requisition import Requisition


@pytest.mark.vcr()
def test_requisition_one(test_instance: PyONMS):
    test_requisition = test_instance.requisitions.get_requisition("selfmonitor")
    assert isinstance(test_requisition, Requisition)
    assert test_requisition.foreign_source == "selfmonitor"
    assert len(test_requisition.node) == 2


@pytest.mark.vcr()
def test_requisition_all(test_instance: PyONMS):
    requisitions = test_instance.requisitions.get_requisitions()
    assert len(requisitions) == 7
    assert requisitions[0].foreign_source == "Blank"


@pytest.mark.vcr()
def test_requisition_count_active(test_instance: PyONMS):
    count = test_instance.requisitions.get_requisition_active_count()
    assert count == 0


@pytest.mark.vcr()
def test_requisition_count_deployed(test_instance: PyONMS):
    count = test_instance.requisitions.get_requisition_deployed_count()
    assert count == 7


@pytest.mark.vcr()
def test_requisition_import(test_instance: PyONMS):
    main = test_instance.requisitions.import_requisition("selfmonitor", rescan=True)
    assert main


@pytest.mark.vcr()
def test_requisition_add_metadata(test_instance: PyONMS):
    test_requisition = test_instance.requisitions.get_requisition("selfmonitor")
    assert len(test_requisition.node["1"].meta_data) == 1
    test_requisition.node["1"].set_metadata(key="key", value="value")
    assert len(test_requisition.node["1"].meta_data) == 2


@pytest.mark.vcr()
def test_requisition_update_metadata(test_instance: PyONMS):
    test_requisition = test_instance.requisitions.get_requisition("selfmonitor")
    assert test_requisition.node["1"].meta_data[0].value == "test"
    test_requisition.node["1"].set_metadata(key="test", value="value")
    assert test_requisition.node["1"].meta_data[0].value == "value"


@pytest.mark.vcr()
def test_requisition_add_asset(test_instance: PyONMS):
    test_requisition = test_instance.requisitions.get_requisition("selfmonitor")
    assert len(test_requisition.node["1"].asset) == 1
    test_requisition.node["1"].set_asset(name="city", value="value")
    assert len(test_requisition.node["1"].asset) == 2


@pytest.mark.vcr()
def test_requisition_update_asset(test_instance: PyONMS):
    test_requisition = test_instance.requisitions.get_requisition("selfmonitor")
    assert test_requisition.node["1"].asset[0].value == "test"
    test_requisition.node["1"].set_asset(name="region", value="value")
    assert test_requisition.node["1"].asset[0].value == "value"
