# dao.events.py

from dao.core import Endpoint
import models.events
import utils.http


class Events(Endpoint):
    def __init__(self, api):
        self.api = api
        self.url = self.api.base_v2 + 'events'

    def get_events(self, id=None, limit=10, batchSize=10) -> dict:
        events = {}
        if id is None:
            records = self.get_data(api=self.api, url=self.url, endpoint='event', limit=limit, batchSize=batchSize)
            if records == [None]:
                return None
            for record in records:
                newEvent = self.process_event(record)
                events[int(newEvent.id)] = newEvent
        else:
            record = utils.http.get_http(uri=f'{self.url}/{id}', API=self.api)
            if record is not None:
                newEvent = self.process_event(record)
                events[newEvent.id] = newEvent
        return events

    def process_event(self, event):
        return models.events.Event(event)
