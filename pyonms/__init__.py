# __init__.py

# flake8: noqa W503
# cSpell: ignore UDLAPI

"""
.. include:: ../README.md
"""

__version__ = "0.1.3"

from multiprocessing import current_process
from typing import Optional
from urllib.parse import urlsplit

from pyonms import dao, models


class PyONMS:
    """Server instance class"""

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        name: Optional[str] = None,
        verify_ssl: Optional[bool] = True,
        timeout: Optional[int] = 30,
    ):
        """Attributes:
            hostname (str): OpenNMS URL
            username (str): Username
            password (str): Password
            name (str): Instance name. Defaults to hostname.
            verify_ssl (bool): Verify SSL certificate. Defaults to True.
            timeout (int): Timeout for HTTP requests. Defaults to 30 seconds.
        Returns:
            `PyONMS` object
        """
        self.hostname = hostname
        args = {
            "hostname": hostname,
            "username": username,
            "password": password,
            "verify_ssl": verify_ssl,
            "timeout": timeout,
        }
        if name:
            self.name = name
            args["name"] = name
        else:
            self.name = urlsplit(hostname).netloc.split(":")[0]
            args["name"] = self.name

        self.health = dao.health.HealthAPI(args)
        """`pyonms.dao.health.HealthAPI` endpoint"""
        self.info = dao.info.InfoAPI(args)
        """`pyonms.dao.info.InfoAPI` endpoint"""

        if current_process().name == "MainProcess":
            self.health_status = self.health.get_health()

        self.server_status = self.info.get_info()
        args["version"] = self.server_status.version

        self.alarms = dao.alarms.AlarmAPI(args)
        """`pyonms.dao.alarms.AlarmAPI` endpoint"""
        self.bsm = dao.business_services.BSMAPI(args)
        """`pyonms.dao.business_services.BSMAPI` endpoint"""
        self.enlinkd = dao.enlinkd.EnlinkdAPI(args)
        """`pyonms.dao.enlinkd.EnlinkdAPI` endpoint"""
        self.events = dao.events.EventAPI(args)
        """`pyonms.dao.events.EventAPI` endpoint"""
        self.fs = dao.foreign_sources.ForeignSourceAPI(args)
        """`pyonms.dao.foreign_sources.ForeignSourceAPI` endpoint"""
        self.nodes = dao.nodes.NodeAPI(args)
        """`pyonms.dao.nodes.NodeAPI` endpoint"""
        self.ips = dao.ips.IPAPI(args)
        """`pyonms.dao.ips.IPAPI` endpoint"""
        self.requisitions = dao.requisitions.RequisitionsAPI(args)
        """`pyonms.dao.requisitions.RequisitionsAPI` endpoint"""
        self.udl = dao.udl.UDLAPI(args)
        """`pyonms.dao.udl.UDLAPI` endpoint"""

    def __repr__(self):
        return self.hostname

    def reload_daemon(self, name: str) -> bool:
        """Send event to reload a given daemon
        Attributes:
            name (str): Daemon name
        """
        if (
            self.server_status.enabled_services
            and name.lower() not in self.server_status.enabled_services
        ):
            raise models.exceptions.InvalidValueError(
                name="name", value=name, valid=self.server_status.enabled_services
            )
        reload_event = models.event.Event(
            uei="uei.opennms.org/internal/reloadDaemonConfig", source="pyonms"
        )
        reload_event.set_parameter(name="daemonName", value=name, type="string")
        success = self.events.send_event(reload_event)
        if success:
            print(f"Sending event to trigger reload of the {name} daemon.")
        else:
            print(f"Sending event to trigger reload of the {name} daemon failed.")
        return success
