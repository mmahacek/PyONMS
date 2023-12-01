# dao.events.py

from typing import List, Union

import pyonms.models.event
import pyonms.models.node
from pyonms.dao.base import Endpoint


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
        self, fiql: str = None, limit: int = 100, batch_size: int = 100
    ) -> List[Union[pyonms.models.event.Event, None]]:
        events = []
        params = {}
        if fiql:
            params["_s"] = fiql
        records = self._get_batch(
            url=self.url,
            endpoint="event",
            limit=limit,
            batch_size=batch_size,
            params=params,
        )
        if records == [None]:
            return [None]
        for record in records:
            events.append(self._process_event(record))
        return events

    def _process_event(self, data: dict) -> pyonms.models.event.Event:
        return pyonms.models.event.Event(**data)

    def send_event(self, event: pyonms.models.event.Event) -> bool:
        result = self._post(uri=self.url, json=event._to_dict())
        if result.status_code == 204:
            return True
        else:
            return False
