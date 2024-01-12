# tests.test_pyonms.py

# pylint: disable=C0114,C0116,W0621,W0212,C2801

import pytest

import pyonms


@pytest.mark.vcr()
def test_instance_creation(test_instance: pyonms.PyONMS):
    assert test_instance.hostname == "http://localhost:8980/opennms"
    assert test_instance.name == "localhost"
    assert test_instance.__repr__() == "http://localhost:8980/opennms"
    assert test_instance.nodes.verify_ssl is True
    assert test_instance.nodes.timeout == 30

    server2 = pyonms.PyONMS(
        hostname="http://localhost:8980/opennms",
        username="admin",
        password="admin",
        name="Test Server",
        verify_ssl=False,
        timeout=60,
    )
    assert server2.name == "Test Server"
    assert server2.nodes.username == "admin"
    assert server2.nodes.password == "admin"
    assert server2.nodes.verify_ssl is False
    assert server2.nodes.timeout == 60


@pytest.mark.vcr()
def test_reload_daemon(test_instance: pyonms.PyONMS):
    assert test_instance.reload_daemon(name="pollerd")
    # with pytest.raises(pyonms.models.exceptions.InvalidValueError):
    #    assert test_instance.reload_daemon(name="nothing")
