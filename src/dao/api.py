# dao.api.py

from aiohttp import BasicAuth


class API:
   def __init__(self, hostname, username, password):
      self.base_url = f'https://{hostname}:8443/opennms/rest/'
      self.username = username
      self.password = password
      self.headers = {'Accept': 'application/json'}
      self.auth = BasicAuth(login=self.username,password=self.password)

   def __repr__(self) -> str:
      return self.base_url
