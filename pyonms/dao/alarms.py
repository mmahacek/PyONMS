# dao.alarms.py

from pyonms.dao.api import Endpoint
import pyonms.models.alarm


class AlarmAPI(Endpoint):
    def __init__(self, args):
        super().__init__(**args)
        self.url = self.base_v2 + "alarms"

    def get_alarm(self, id: int) -> pyonms.models.alarm.Alarm:
        record = self._get(uri=f"{self.url}/{id}")
        if record is not None:
            return self.process_alarm(record)
        else:
            return None

    def get_alarms(self, limit=10, batchSize=10) -> list:
        alarms = []
        records = self.get_data(
            url=self.url,
            endpoint="alarm",
            limit=limit,
            batchSize=batchSize,
        )
        if records == [None]:
            return None
        for record in records:
            alarms.append(self.process_alarm(record))
        return alarms

    def process_alarm(self, alarm):
        return pyonms.models.alarm.Alarm(alarm)
