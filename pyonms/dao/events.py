# dao.events.py

"Events data access"

from typing import List, Optional

import pyonms.models.event
import pyonms.models.node
from pyonms.dao.base import Endpoint


class EventAPI(Endpoint):
    "Events API endpoint"

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "events"

    def get_event(self, id: int) -> Optional[pyonms.models.event.Event]:
        """Get event by ID number."""
        record = self._get(url=f"{self.url}/{id}")
        if record is not None:
            return self._process_event(record)
        else:
            return None

    def get_events(
        self, fiql: Optional[str] = None, limit: int = 100, batch_size: int = 100
    ) -> List[pyonms.models.event.Event]:
        """Get all matching event objects."""
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
        events = []
        for record in records:
            if record:
                events.append(self._process_event(record))
        return events

    def _process_event(self, data: dict) -> pyonms.models.event.Event:
        return pyonms.models.event.Event(**data)

    def send_event(self, event: pyonms.models.event.Event) -> bool:
        """Send Event object."""
        result = self._post(url=self.url, json=event.to_dict())
        if result.status_code == 204:
            return True
        else:
            return False
