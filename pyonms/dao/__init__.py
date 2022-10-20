# dao.__init__.py

from typing import List

import requests

from requests.auth import HTTPBasicAuth
from tqdm import tqdm

import pyonms.utils


class Endpoint:
    def __init__(self, hostname: str, username: str, password: str, **kwargs):
        if hostname[-1:] == "/":
            hostname = hostname[:-1]
        self.base_v1 = f"{hostname}/rest/"
        self.base_v2 = f"{hostname}/api/v2/"
        self.hostname = hostname
        self.username = username
        self.password = password
        self.headers = {"Accept": "application/json"}
        self.auth = HTTPBasicAuth(self.username, self.password)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_batch(
        self,
        url: str,
        endpoint: str,
        limit: int = 0,
        batch_size: int = 100,
        params: dict = {},
    ) -> List[dict]:
        with tqdm(total=limit, unit="record", desc=f"Pulling {endpoint} data") as pbar:
            result = []
            params["offset"] = 0
            if limit > batch_size:
                params["limit"] = batch_size
            else:
                params["limit"] = limit
            records = self._get(uri=url, params=params, endpoint=endpoint)
            if records.get(endpoint, [None]) == [None]:
                return [None]
            if limit == 0 or records["totalCount"] < limit:
                target_count = records["totalCount"]
                pbar.total = target_count
            else:
                target_count = limit
            while params["offset"] < target_count:
                for record in records[endpoint]:
                    result.append(record)
                    params["offset"] += 1
                    pbar.update(1)
                    if params["offset"] >= target_count:
                        return result
                records = self._get(uri=url, params=params, endpoint=endpoint)
            return result

    def _get(
        self, uri: str, headers: dict = {}, params: dict = {}, endpoint: str = None
    ) -> dict:
        if self.base_v1 in uri:
            return self._get_v1(
                uri=uri, headers=headers, params=params, endpoint=endpoint
            )
        headers["Accept"] = "application/json"
        response = requests.get(uri, auth=self.auth, headers=headers, params=params)
        if response.status_code == 200:
            if "was not found" not in response.text:
                return response.json()
        return {}

    def _get_v1(
        self, uri: str, endpoint: str, headers: dict = {}, params: dict = {}
    ) -> dict:
        response = requests.get(uri, auth=self.auth, headers=headers, params=params)
        if response.status_code == 200:
            if "was not found" not in response.text:
                if endpoint == "raw":
                    return response.text
                else:
                    xml_data = pyonms.utils.convert_xml(response.text)
                    return self._convert_v1_to_v2(endpoint, xml_data)
        return {}

    def _post(
        self,
        uri: str,
        headers: dict = {},
        data: dict = None,
        json: dict = None,
        params: dict = {},
    ) -> dict:
        if json:
            response = requests.post(
                uri, auth=self.auth, headers=headers, json=json, params=params
            )
        elif data:
            response = requests.post(
                uri, auth=self.auth, headers=headers, data=data, params=params
            )
        else:
            response = requests.post(uri, auth=self.auth, headers=headers)
        return response.text

    def _put(
        self,
        uri: str,
        data: dict = None,
        json: dict = None,
        headers: dict = {},
        params: dict = {},
    ) -> dict:
        if json:
            response = requests.put(
                uri, auth=self.auth, headers=headers, json=json, params=params
            )
        elif data:
            response = requests.put(
                uri, auth=self.auth, headers=headers, data=data, params=params
            )
        else:
            return None
        return response.text

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
                if isinstance(value["model_import"], list):
                    v2_data[key] = value["model_import"]
                elif isinstance(value["model_import"], dict):
                    v2_data[key] = [value["model_import"]]
        return v2_data

    def _delete(
        self, uri: str, headers: dict = {}, params: dict = {}, endpoint: str = None
    ) -> dict:
        headers["Accept"] = "application/json"
        requests.delete(uri, auth=self.auth, headers=headers)
        return {}
