# dao.__init__.py

from typing import List

import requests

from requests.auth import HTTPBasicAuth

import pyonms.utils


class Endpoint:
    def __init__(self, hostname: str, username: str, password: str, **kwargs):
        if hostname[-1:] != "/":
            hostname += "/"
        self.base_v1 = f"{hostname}opennms/rest/"
        self.base_v2 = f"{hostname}opennms/api/v2/"
        self.hostname = hostname
        self.username = username
        self.password = password
        self.headers = {"Accept": "application/json"}
        self.auth = HTTPBasicAuth(self.username, self.password)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_batch(
        self, url: str, endpoint: str, limit: int = 0, batch_size: int = 100
    ) -> List[dict]:
        result = []
        params = {"offset": 0}
        if limit > batch_size:
            params["limit"] = batch_size
        else:
            params["limit"] = limit
        records = self._get(uri=url, params=params, endpoint=endpoint)
        if records[endpoint] == [None]:
            return [None]
        if limit == 0 or records["totalCount"] < limit:
            target_count = records["totalCount"]
        else:
            target_count = limit
        while params["offset"] < target_count:
            for record in records[endpoint]:
                result.append(record)
                params["offset"] += 1
                if params["offset"] >= target_count:
                    break
            records = self._get(uri=url, params=params, endpoint=endpoint)
        return result

    def _get(self, uri: str, params: dict = {}, endpoint: str = None) -> dict:
        if self.base_v1 in uri:
            return self._get_v1(uri=uri, params=params, endpoint=endpoint)
        response = requests.get(uri, auth=self.auth, params=params)
        if response.status_code == 200:
            if "was not found" not in response.text:
                return response.json()
        return {}

    def _get_v1(self, uri: str, endpoint: str, params: dict = {}) -> dict:
        response = requests.get(uri, auth=self.auth, params=params)
        if response.status_code == 200:
            if "was not found" not in response.text:
                xml_data = pyonms.utils.convert_xml(response.text)
                return self._convert_v1_to_v2(endpoint, xml_data)
        return {}

    def _post(
        self, uri: str, headers: dict = {}, data: dict = None, json: dict = None
    ) -> dict:
        if json:
            response = requests.post(uri, auth=self.auth, headers=headers, json=json)
        elif data:
            response = requests.post(uri, auth=self.auth, headers=headers, data=data)
        else:
            response = requests.post(uri, auth=self.auth, headers=headers)
        return response.json()

    def _put(self, uri: str, data: dict, headers: dict = {}) -> dict:
        return requests.put(uri, auth=self.auth, headers=headers, data=data).json()

    def _convert_v1_to_v2(self, endpoint: str, data: dict) -> dict:
        v2_data = {}
        if "model_import" in data.keys():
            if data["model_import"].get("xmlns"):
                del data["model_import"]["xmlns"]
            v2_data = data["model_import"]
        elif endpoint in data.keys():
            for key, value in data.items():
                v2_data["count"] = int(value["count"])
                v2_data["offset"] = int(value["offset"])
                v2_data["totalCount"] = int(value["totalCount"])
                if type(value["model_import"] == list):
                    v2_data[key] = value["model_import"]
                elif type(value["model_import"] == dict):
                    v2_data[key] = [value["model_import"]]
        return v2_data
