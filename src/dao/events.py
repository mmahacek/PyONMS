# dao.events.py

import models.events
import utils.http

async def getEvents(api, id=None, limit=100) -> dict:
    url = api.base_url + 'events'
    if id == None:
        records = await utils.http.getHttp(uri=f'{url}?limit={limit}', API=api)
    else:
        records = {'node': [await utils.http.getHttp(uri=f'{url}/{id}?limit={limit}', API=api)]}
    if records['node'] == [None]:
        return None
    events = {}
    for event in records['node']:
        events[event['id']] = models.events.Event(event)
    return events