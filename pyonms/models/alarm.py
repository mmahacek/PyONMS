# models.alarm.py

from pyonms.models.event import Event, Event_Parameter
from pyonms.models.node import serviceType
import pyonms.dao.nodes


class Alarm:
    def __init__(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
        if data["lastEvent"]:
            self.lastEvent = Event(data["lastEvent"])
        if data["parameters"]:
            self.parameters = [
                Event_Parameter(parameter) for parameter in data["parameters"]
            ]
        if data.get("serviceType"):
            self.serviceType = serviceType(data["serviceType"])
        if data.get("ackTime"):
            self.isAcknowledged = True
        else:
            self.isAcknowledged = False

    def __repr__(self):
        return self.reductionKey

    def get_node(self):
        return pyonms.dao.nodes.get_node(self.nodeId)
