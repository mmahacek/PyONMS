# dao.alarms.py

import models.alarms
import utils.http


class Alarms():
    def __init__(self, api):
        self.api = api

    async def get_alarms(self, id=None, limit=10) -> dict:
        url = self.api.base_url + 'alarms'
        if id is None:
            records = await utils.http.get_http(uri=f'{url}?limit={limit}', API=self.api)
        else:
            records = {'alarm': [await utils.http.get_http(uri=f'{url}/{id}?limit={limit}', API=self.api)]}
        if records['alarm'] == [None]:
            return None
        alarms = {}
        for alarm in records['alarm']:
            alarms[alarm['id']] = models.alarms.Alarm(alarm)
        return alarms
