# models.alarms.py

from models.events import Event, Parameter
from models.node import serviceType
import dao.nodes as nodes


class Alarm():
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])
        if data['lastEvent']:
            setattr(self, 'lastEvent', Event(data['lastEvent']))
        if data['parameters']:
            setattr(self, 'parameters', [Parameter(parameter) for parameter in data['parameters']])
        if data.get('serviceType'):
            setattr(self, 'serviceType', serviceType(data['serviceType']))
        if data.get('ackTime'):
            self.isAcknowledged = True
        else:
            self.isAcknowledged = False

    def __repr__(self):
        return self.reductionKey

    def get_node(self, API):
        return nodes.get_nodes(API, self.nodeId)
