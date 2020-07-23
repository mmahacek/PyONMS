# dao.alarms.py

import models.alarms
import utils.http

class Alarms():
    def __init__(self, api):
        self.api = api

    async def getAlarms(self, id=None, limit=100) -> dict:
        url = self.api.base_url + 'alarms'
        if id == None:
            records = await utils.http.getHttp(uri=f'{url}?limit={limit}', API=self.api)
        else:
            records = {'node': [await utils.http.getHttp(uri=f'{url}/{id}?limit={limit}', API=self.api)]}
        if records['node'] == [None]:
            return None
        alarms = {}
        for alarm in records['node']:
            alarms[alarm['id']] = models.alarms.Alarm(alarm)
        return alarms