# __init__.py

import pyonms.dao.alarms
import pyonms.dao.events
import pyonms.dao.nodes


class PyONMS:
    def __init__(self, hostname: str, username: str, password: str):
        self.hostname = hostname
        args = {
            "hostname": hostname,
            "username": username,
            "password": password,
        }
        if hasattr(self, "resolver"):
            args["resolver"] = self.resolver
        self.nodes = pyonms.dao.nodes.NodeAPI(args)
        self.events = pyonms.dao.events.EventAPI(args)
        self.alarms = pyonms.dao.alarms.AlarmAPI(args)

    def __repr__(self):
        return self.hostname
