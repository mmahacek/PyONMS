# dao.events.py

from typing import List, Union

from pyonms.dao import Endpoint
import pyonms.models.event
import pyonms.models.node


class EventAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "events"

    def get_event(self, id: int) -> Union[pyonms.models.event.Event, None]:
        record = self._get(uri=f"{self.url}/{id}")
        if record is not None:
            return self._process_event(record)
        else:
            return None

    def get_events(
        self, limit=100, batch_size=100
    ) -> List[Union[pyonms.models.event.Event, None]]:
        events = []
        records = self._get_batch(
            url=self.url,
            endpoint="event",
            limit=limit,
            batch_size=batch_size,
        )
        if records == [None]:
            return [None]
        for record in records:
            events.append(self._process_event(record))
        return events

    def _process_event(self, data: dict) -> pyonms.models.event.Event:
        return pyonms.models.event.Event(**data)
