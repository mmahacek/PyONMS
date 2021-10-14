# dao.api.py

#from aiohttp import BasicAuth
from requests.auth import HTTPBasicAuth

class API():
    def __init__(self, hostname, username, password):
        if hostname[-1:] != '/':
            hostname += '/'
        self.base_v1 = f'{hostname}opennms/rest/'
        self.base_v2 = f'{hostname}opennms/api/v2/'
        self.hostname = hostname
        self.username = username
        self.password = password
        self.headers = {'Accept': 'application/json'}
        self.auth = HTTPBasicAuth(self.username, self.password)

    def __repr__(self):
        return self.hostname
