# dao.alarms.py

from typing import List, Union

from pyonms.dao import Endpoint
import pyonms.models.alarm


class AlarmAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "alarms"

    def get_alarm(self, id: int) -> Union[pyonms.models.alarm.Alarm, None]:
        record = self._get(uri=f"{self.url}/{id}")
        if record is not None:
            return self.process_alarm(record)
        else:
            return None

    def get_alarms(
        self, limit=100, batch_size=100
    ) -> List[Union[pyonms.models.alarm.Alarm, None]]:
        alarms = []
        records = self.get_batch(
            url=self.url,
            endpoint="alarm",
            limit=limit,
            batch_size=batch_size,
        )
        if records == [None]:
            return [None]
        for record in records:
            alarms.append(self.process_alarm(record))
        return alarms

    def process_alarm(self, alarm) -> pyonms.models.alarm.Alarm:
        return pyonms.models.alarm.Alarm(**alarm)