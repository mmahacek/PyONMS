# dao.events.py

import models.events
import utils.http

class Events():
    def __init__(self, api):
        self.api = api

    async def getEvents(self, id=None, limit=10) -> dict:
        url = self.api.base_url + 'events'
        if id == None:
            records = await utils.http.getHttp(uri=f'{url}?limit={limit}', API=self.api)
        else:
            records = {'event': [await utils.http.getHttp(uri=f'{url}/{id}?limit={limit}', API=self.api)]}
        if records['event'] == [None]:
            return None
        events = {}
        for event in records['event']:
            events[event['id']] = models.events.Event(event)
        return events