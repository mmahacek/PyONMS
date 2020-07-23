# pyonms.py

from dao import api, alarms, events, nodes
from aiohttp import BasicAuth

class pyonms():
    def __init__(self, hostname, username, password):
        self.base_url = f'https://{hostname}:8443/opennms/rest/'
        self.api = api.API(hostname=hostname, username=username, password=password)
        self.nodes = nodes.Nodes(self.api)
        self.events = events.Events(self.api)
        self.alarms = alarms.Alarms(self.api)

    def __repr__(self):
        return self.base_url
