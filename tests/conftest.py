# tests.conftest.py

import pytest

from pyonms import PyONMS


class MockAPI(PyONMS):
    def __init__(self, hostname: str, username: str, password: str):
        super().__init__(hostname, username, password)


@pytest.fixture
def test_instance() -> PyONMS:
    return MockAPI(
        hostname="http://localhost:8980/opennms",
        username="admin",
        password="admin",
    )
