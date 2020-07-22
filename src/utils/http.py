# utils.http

import json
import aiohttp

async def getHttp(uri, API):
   async with aiohttp.ClientSession(auth=API.auth) as session:
      async with session.get(uri, headers=API.headers) as resp:
         response = await resp.text()
   if response:
      if 'was not found' in response:
         return None
      else:
         return json.loads(response)

async def postHttp(uri, API, headers, data=None, token=None, json=None):
   async with aiohttp.ClientSession(auth=API.auth) as session:
      if json:
         async with session.post(uri, headers=headers, json=json) as resp:
            return await resp.text()
      elif data:
         async with session.post(uri, headers=headers, data=data) as resp:
            return await resp.text()