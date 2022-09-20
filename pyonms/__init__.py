# __init__.py

import pyonms.dao.alarms
import pyonms.dao.events
import pyonms.dao.nodes
import pyonms.dao.requisitions


class PyONMS:
    def __init__(self, hostname: str, username: str, password: str):
        self.hostname = hostname
        args = {
            "hostname": hostname,
            "username": username,
            "password": password,
        }
        self.alarms = pyonms.dao.alarms.AlarmAPI(args)
        self.events = pyonms.dao.events.EventAPI(args)
        self.nodes = pyonms.dao.nodes.NodeAPI(args)
        self.requisitions = pyonms.dao.requisitions.RequisitionsAPI(args)

    def __repr__(self):
        return self.hostname
