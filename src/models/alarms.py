# models.alarms.py

import models.events as events
import dao.node as node

class Alarm:
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data[key])
        if data['parameters']:
            setattr(self, 'parameters', [events.Parameter(parameter) for parameter in data['parameters']])
        if data['lastEvent']:
            setattr(self, 'lastEvent', events.Event(data['lastEvent']))
        
    def __repr__(self):
        return self.uei
    
    async def getNode(self, API):
        return await node.getNodes(API, self.nodeId)