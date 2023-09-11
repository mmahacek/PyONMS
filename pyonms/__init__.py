# __init__.py

# flake8: noqa W503
# cSpell: ignore UDLAPI

"""
.. include:: ../README.md
"""

__version__ = "0.0.11"

from multiprocessing import current_process
from urllib.parse import urlsplit

import pyonms.dao.alarms
import pyonms.dao.business_services
import pyonms.dao.events
import pyonms.dao.foreign_sources
import pyonms.dao.health
import pyonms.dao.info
import pyonms.dao.nodes
import pyonms.dao.requisitions
import pyonms.dao.udl
from pyonms.models.event import Event
from pyonms.models.exceptions import InvalidValueError


class PyONMS:
    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        name: str = None,
        verify_ssl: bool = True,
    ):
        """Attributes:
            hostname (str): OpenNMS URL
            username (str): Username
            password (str): Password
            name (str): Instance name. Defaults to hostname.
            verify_ssl (bool): Verify SSL certificate. Defaults to True.
        Returns:
            `PyONMS` object
        """
        self.hostname = hostname
        args = {
            "hostname": hostname,
            "username": username,
            "password": password,
            "verify_ssl": verify_ssl,
        }
        if name:
            self.name = name
            args["name"] = name
        else:
            self.name = urlsplit(hostname).netloc.split(":")[0]
            args["name"] = self.name

        self.health = pyonms.dao.health.HealthAPI(args)
        """`pyonms.dao.health.HealthAPI` endpoint"""
        self.info = pyonms.dao.info.InfoAPI(args)
        """`pyonms.dao.info.InfoAPI` endpoint"""

        if current_process().name == "MainProcess":
            self.health_status = self.health.get_health()

        self.server_status = self.info.get_info()
        args["version"] = self.server_status.version

        self.alarms = pyonms.dao.alarms.AlarmAPI(args)
        """`pyonms.dao.alarms.AlarmAPI` endpoint"""
        self.bsm = pyonms.dao.business_services.BSMAPI(args)
        """`pyonms.dao.business_services.BSMAPI` endpoint"""
        self.events = pyonms.dao.events.EventAPI(args)
        """`pyonms.dao.events.EventAPI` endpoint"""
        self.fs = pyonms.dao.foreign_sources.ForeignSourceAPI(args)
        """`pyonms.dao.foreign_sources.ForeignSourceAPI` endpoint"""
        self.nodes = pyonms.dao.nodes.NodeAPI(args)
        """`pyonms.dao.nodes.NodeAPI` endpoint"""
        self.requisitions = pyonms.dao.requisitions.RequisitionsAPI(args)
        """`pyonms.dao.requisitions.RequisitionsAPI` endpoint"""
        self.udl = pyonms.dao.udl.UDLAPI(args)
        """`pyonms.dao.udl.UDLAPI` endpoint"""

    def __repr__(self):
        return self.hostname

    def reload_daemon(self, name: str):
        """Send event to reload a given daemon
        Attributes:
            name (str): Daemon name
        """
        if (
            self.server_status.enabled_services
            and name.lower() not in self.server_status.enabled_services
        ):
            raise InvalidValueError(
                name="name", value=name, valid=self.server_status.enabled_services
            )
        reload_event = Event(
            uei="uei.opennms.org/internal/reloadDaemonConfig", source="pyonms"
        )
        reload_event.set_parameter(name="daemonName", value=name, type="string")
        self.events.send_event(reload_event)
        print(f"Sending event to trigger reload of the {name} daemon.")
