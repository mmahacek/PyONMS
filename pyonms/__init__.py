# __init__.py

import pyonms.dao.alarms
import pyonms.dao.business_services
import pyonms.dao.events
import pyonms.dao.foreign_sources
import pyonms.dao.nodes
import pyonms.dao.requisitions


class PyONMS:
    def __init__(self, hostname: str, username: str, password: str, name: str = None):
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
            self.name = hostname
            args["name"] = ""
        self.alarms = pyonms.dao.alarms.AlarmAPI(args)
        self.bsm = pyonms.dao.business_services.BSMAPI(args)
        self.events = pyonms.dao.events.EventAPI(args)
        self.fs = pyonms.dao.foreign_sources.ForeignSourceAPI(args)
        self.nodes = pyonms.dao.nodes.NodeAPI(args)
        self.requisitions = pyonms.dao.requisitions.RequisitionsAPI(args)

    def __repr__(self):
        return self.hostname
