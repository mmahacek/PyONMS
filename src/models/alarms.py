# models.alarms.py

import models.events as events
import dao.nodes as nodes


class Alarm:
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])
        if data['parameters']:
            setattr(self, 'parameters', [events.Parameter(parameter) for parameter in data['parameters']])
        if data['lastEvent']:
            setattr(self, 'lastEvent', events.Event(data['lastEvent']))
        try:
            if self.ackTime is not None:
                self.isAcknowledged = True
            else:
                self.isAcknowledged = False
        except AttributeError:
            self.isAcknowledged = False

    def __repr__(self):
        return self.uei

    async def get_node(self, API):
        return await nodes.get_nodes(API, self.nodeId)
