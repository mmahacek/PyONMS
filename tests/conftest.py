# tests.conftest.py

import pytest

from pyonms import PyONMS


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("authorization", "REDACTED")],
        "record_mode": "new_episodes",
        "record_on_exception": False,
    }


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
