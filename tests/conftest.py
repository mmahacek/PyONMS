# tests.conftest.py

# pylint: disable=C0114,C0116,W0621,W0212

import os

import pytest
from dotenv import load_dotenv

from pyonms import PyONMS

load_dotenv()


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": ["authorization"],
        "record_mode": os.getenv("pytest_mode", "none"),
        "record_on_exception": False,
    }


@pytest.fixture
def test_instance() -> PyONMS:
    return PyONMS(
        hostname=os.getenv("test_host", "http://localhost:8980/opennms"),
        username=os.getenv("test_user", "admin"),
        password=os.getenv("test_pass", "admin"),
    )
