# dao.alarms.py

from dao.core import Endpoint
import models.alarms
import utils.http


class Alarms(Endpoint):
    def __init__(self, api):
        self.api = api
        self.url = self.api.base_v2 + 'alarms'

    async def get_alarms(self, id=None, limit=10, batchSize=10) -> dict:
        alarms = {}
        if id is None:
            records = await self.get_data(api=self.api, url=self.url, endpoint='alarm', limit=limit, batchSize=batchSize)
            if records == [None]:
                return None
            for record in records:
                newAlarm = await self.process_alarm(record)
                alarms[int(newAlarm.id)] = newAlarm
        else:
            record = await utils.http.get_http(uri=f'{self.url}/{id}', API=self.api)
            if record is not None:
                newEvent = await self.process_event(record)
                alarms[newEvent.id] = newEvent
        return alarms

    async def process_alarm(self, alarm):
        return models.alarms.Alarm(alarm)
