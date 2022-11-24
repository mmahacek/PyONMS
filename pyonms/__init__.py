# __init__.py

"""
.. include:: ../README.md
"""

from urllib.parse import urlsplit

import pyonms.dao.alarms
import pyonms.dao.business_services
import pyonms.dao.events
import pyonms.dao.foreign_sources
import pyonms.dao.health
import pyonms.dao.info
import pyonms.dao.nodes
import pyonms.dao.requisitions

from pyonms.models.event import Event, EventParameter


class PyONMS:
    def __init__(self, hostname: str, username: str, password: str, name: str = None):
        """Attributes:
            hostname (str): OpenNMS URL
            username (str): Username
            password (str): Password
            name (str): Instance name
        Returns:
            `PyONMS` object
        """
        self.hostname = hostname
        args = {
            "hostname": hostname,
            "username": username,
            "password": password,
        }
        if name:
            self.name = name
            args["name"] = name
        else:
            self.name = urlsplit(hostname).netloc.split(":")[0]
            args["name"] = self.name
        self.alarms = pyonms.dao.alarms.AlarmAPI(args)
        """`pyonms.dao.alarms.AlarmAPI` endpoint"""
        self.bsm = pyonms.dao.business_services.BSMAPI(args)
        """`pyonms.dao.business_services.BSMAPI` endpoint"""
        self.events = pyonms.dao.events.EventAPI(args)
        """`pyonms.dao.events.EventAPI` endpoint"""
        self.fs = pyonms.dao.foreign_sources.ForeignSourceAPI(args)
        """`pyonms.dao.foreign_sources.ForeignSourceAPI` endpoint"""
        self.health = pyonms.dao.health.HealthAPI(args)
        """`pyonms.dao.health.HealthAPI` endpoint"""
        self.info = pyonms.dao.info.InfoAPI(args)
        """`pyonms.dao.info.InfoAPI` endpoint"""
        self.nodes = pyonms.dao.nodes.NodeAPI(args)
        """`pyonms.dao.nodes.NodeAPI` endpoint"""
        self.requisitions = pyonms.dao.requisitions.RequisitionsAPI(args)
        """`pyonms.dao.requisitions.RequisitionsAPI` endpoint"""

        self.status = self.info.get_info()

    def __repr__(self):
        return self.hostname

    def reload_daemon(self, name: str):
        reload_event = Event(
            uei="uei.opennms.org/internal/reloadDaemonConfig", source="pyonms"
        )
        reload_event.parameters.append(
            EventParameter(name="daemonName", value=name, type="string")
        )
        self.events.send_event(reload_event)
