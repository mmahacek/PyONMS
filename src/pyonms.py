# pyonms.py

from dao import api, alarms, events, nodes


class pyonms():
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.api = api.API(hostname=hostname, username=username, password=password)
        self.nodes = nodes.Nodes(self.api)
        self.events = events.Events(self.api)
        self.alarms = alarms.Alarms(self.api)

    def __repr__(self):
        return self.hostname
