# utils.api.py
import json
import aiohttp

# baseURL = 'https://mcoenms04.mcoe.org:8443/opennms/rest/'


class API:
   def __init__(self, hostname, username, password):
      self.base_url = f'https://{hostname}:8443/opennms/rest/'
      self.username = username
      self.password = password
      self.headers = {'Accept': 'application/json'}
      self.auth = aiohttp.BasicAuth(login=self.username,password=self.password)


async def getHttp(uri, API):
   async with aiohttp.ClientSession(auth=API.auth) as session:
      async with session.get(uri, headers=API.headers) as resp:
         response = await resp.text()
   if response:
      return json.loads(response)

async def postHttp(uri, headers, data=None, token=None, json=None):
   async with aiohttp.ClientSession() as session:
      if json:
         async with session.post(uri, headers=headers, json=json) as resp:
            return await resp.text()
      elif data:
         async with session.post(uri, headers=headers, data=data) as resp:
            return await resp.text()



# url = api.baseURL + 'nodes?limit=10'

# records = json.loads(asyncio.run(api.getHttp(url, user=auth)))