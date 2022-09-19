# dao.__init__.py

import requests

from requests.auth import HTTPBasicAuth


class Endpoint:
    def __init__(self, hostname: str, username: str, password: str, **args):
        if hostname[-1:] != "/":
            hostname += "/"
        self.base_v1 = f"{hostname}opennms/rest/"
        self.base_v2 = f"{hostname}opennms/api/v2/"
        self.hostname = hostname
        self.username = username
        self.password = password
        self.headers = {"Accept": "application/json"}
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.resolver = args.get("resolver")

    def get_data(self, url: str, endpoint: str, limit: int, batchSize: int) -> list:
        offset = 0
        result = []
        records = self._get(uri=f"{url}?limit={batchSize}&offset={offset}")
        if records[endpoint] == [None]:
            return None
        actualCount = records["totalCount"]
        if limit in [0, None, False]:
            limit = actualCount
        processed = 0
        print(processed)
        while (actualCount - processed) > 0:
            for record in records[endpoint]:
                if processed >= limit:
                    break
                result.append(record)
                processed += 1
            print(processed)
            if processed >= limit:
                break
            records = self._get(uri=f"{url}?limit={batchSize}&offset={processed}")
        #            if records[endpoint] == [None]:
        #                break
        print(processed)
        return result

    def _get(self, uri: str) -> dict:
        response = requests.get(uri, auth=self.auth)
        if response.status_code == 200:
            if "was not found" in response.text:
                return None
            else:
                return response.json()

    def _post(self, uri: str, headers: dict = {}, data=None, json: dict = None) -> dict:
        if json:
            response = requests.get(uri, auth=self.auth, headers=headers, json=json)
        elif data:
            response = requests.get(uri, auth=self.auth, headers=headers, data=data)
        return response.json()
