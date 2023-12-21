# dao.alarms.py

from typing import List, Optional

import pyonms.models.alarm
from pyonms.dao.base import Endpoint
from pyonms.models import exceptions


class AlarmAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "alarms"

    def get_alarm(self, id: int) -> Optional[pyonms.models.alarm.Alarm]:
        record = self._get(url=f"{self.url}/{id}")
        if record is not None:
            return self._process_alarm(record)
        else:
            return None

    def get_alarms(
        self, fiql: str = None, limit: int = 100, batch_size: int = 100
    ) -> List[Optional[pyonms.models.alarm.Alarm]]:
        alarms = []
        params = {}
        if fiql:
            params["_s"] = fiql
        records = self._get_batch(
            url=self.url,
            endpoint="alarm",
            limit=limit,
            batch_size=batch_size,
            params=params,
        )
        if records == [None]:
            return [None]
        for record in records:
            alarms.append(self._process_alarm(record))
        return alarms

    def _process_alarm(self, data: dict) -> pyonms.models.alarm.Alarm:
        return pyonms.models.alarm.Alarm(**data)

    def ack_alarm(self, id: int, ack: bool):
        if not isinstance(ack, bool):
            raise exceptions.InvalidValueError(
                name="ack", value=ack, valid="[True, False]"
            )
        params = {"ack": ack}
        self._put(url=f"{self.url}/{id}", params=params, data=params)
        return

    def clear_alarm(self, id: int):
        params = {"clear": True}
        self._put(url=f"{self.url}/{id}", params=params, data=params)
        return

    def escalate_alarm(self, id: int):
        params = {"escalate": True}
        self._put(url=f"{self.url}/{id}", params=params, data=params)
        return
