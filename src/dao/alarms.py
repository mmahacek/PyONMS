# dao.alarms.py

import models.alarms
import utils.http

async def getAlarms(api, id=None, limit=100) -> dict:
    url = api.base_url + 'alarms'
    if id == None:
        records = await utils.http.getHttp(uri=f'{url}?limit={limit}', API=api)
    else:
        records = {'node': [await utils.http.getHttp(uri=f'{url}/{id}?limit={limit}', API=api)]}
    if records['node'] == [None]:
        return None
    alarms = {}
    for alarm in records['node']:
        alarms[alarm['id']] = models.alarms.Alarm(alarm)
    return alarms