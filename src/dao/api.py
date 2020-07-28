# dao.api.py

from aiohttp import BasicAuth


class API():
    def __init__(self, hostname, username, password):
        self.base_v1 = f'https://{hostname}:8443/opennms/rest/'
        self.base_v2 = f'https://{hostname}:8443/opennms/api/v2/'
        self.hostname = hostname
        self.username = username
        self.password = password
        self.headers = {'Accept': 'application/json'}
        self.auth = BasicAuth(login=self.username, password=self.password)

    def __repr__(self):
        return self.hostname
