# dao.events.py

from pyonms.dao.api import Endpoint
import pyonms.models.event
import pyonms.models.node


class EventAPI(Endpoint):
    def __init__(self, args):
        super().__init__(**args)
        self.url = self.base_v2 + "events"

    def get_event(self, id: int) -> pyonms.models.event.Event:
        record = self._get(uri=f"{self.url}/{id}")
        if record is not None:
            return self.process_event(record)
        else:
            return None

    def get_events(self, limit=10, batchSize=10) -> list:
        events = []
        records = self.get_data(
            url=self.url,
            endpoint="event",
            limit=limit,
            batchSize=batchSize,
        )
        if records == [None]:
            return None
        for record in records:
            events.append(self.process_event(record))
        return events

    def process_event(self, event):
        return pyonms.models.event.Event(**event)
