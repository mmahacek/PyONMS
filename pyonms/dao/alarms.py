# dao.alarms.py

from typing import List, Union

import pyonms.models.alarm
from pyonms.dao import Endpoint
from pyonms.models import exceptions


class AlarmAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "alarms"

    def get_alarm(self, id: int) -> Union[pyonms.models.alarm.Alarm, None]:
        record = self._get(uri=f"{self.url}/{id}")
        if record is not None:
            return self._process_alarm(record)
        else:
            return None

    def get_alarms(
        self, limit: int = 100, batch_size: int = 100
    ) -> List[Union[pyonms.models.alarm.Alarm, None]]:
        alarms = []
        records = self._get_batch(
            url=self.url,
            endpoint="alarm",
            limit=limit,
            batch_size=batch_size,
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
        self._put(uri=f"{self.url}/{id}", params=params, data=params)
        return

    def clear_alarm(self, id: int):
        params = {"clear": True}
        self._put(uri=f"{self.url}/{id}", params=params, data=params)
        return

    def escalate_alarm(self, id: int):
        params = {"escalate": True}
        self._put(uri=f"{self.url}/{id}", params=params, data=params)
        return
