# dao.base.py

"""Base classes for DAO objects"""

from typing import List

import requests
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning

import pyonms.utils
from pyonms.models.exceptions import (
    ApiPayloadError,
    AuthenticationError,
    InvalidValueError,
)

urllib3.disable_warnings(category=InsecureRequestWarning)


class Endpoint:
    """Base class for endpoint data access"""

    def __init__(
        self, hostname: str, username: str, password: str, name: str, **kwargs
    ):
        if hostname[-1:] == "/":
            hostname = hostname[:-1]
        self.base_v1 = f"{hostname}/rest/"
        self.base_v2 = f"{hostname}/api/v2/"
        self.hostname = hostname
        self.username = username
        self.password = password
        self.verify_ssl = True
        self.timeout = 30
        self.name = name
        self.headers = {"Accept": "application/json"}
        self.auth = HTTPBasicAuth(self.username, self.password)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_batch(
        self,
        url: str,
        endpoint: str,
        limit: int = 0,
        batch_size: int = 100,
        params: dict = None,
        hide_progress: bool = False,
    ) -> List[dict]:
        if not params:
            params = {}
        with tqdm(
            total=limit,
            unit="record",
            desc=f"Pulling {self.name} {endpoint} data",
            disable=hide_progress,
        ) as pbar:
            result = []
            params["offset"] = 0
            if limit > batch_size:
                params["limit"] = batch_size
            else:
                params["limit"] = limit
            records = self._get(
                url=url,
                params=params,
                endpoint=endpoint,
                headers=self.headers,
            )
            if records.get(endpoint, [None]) in [[None], []]:
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
                records = self._get(url=url, params=params, endpoint=endpoint)
            return result

    def _get(
        self, url: str, headers: dict = None, params: dict = None, endpoint: str = None
    ):
        # if self.base_v1 in url:
        #    return self._get_v1(
        #        url=url, headers=headers, params=params, endpoint=endpoint
        #    )
        if not headers:
            headers = {}
        if not params:
            params = {}
        if endpoint != "raw":
            for key, value in self.headers.items():
                headers[key] = value
        response = requests.get(
            url,
            auth=self.auth,
            headers=headers,
            params=params,
            verify=self.verify_ssl,
            timeout=self.timeout,
        )
        if response.status_code == 200:
            if response.encoding in ("ISO-8859-1") or url[-5:] in ["probe"]:
                return response.text
            elif "was not found" not in response.text:
                return response.json()
        elif response.status_code == 401:
            raise AuthenticationError
        elif response.status_code >= 400:
            raise ApiPayloadError(message=response.text)
        return {}

    def _get_v1(
        self, url: str, endpoint: str, headers: dict = None, params: dict = None
    ) -> dict:
        if not headers:
            headers = {}
        if not params:
            params = {}
        response = requests.get(
            url,
            auth=self.auth,
            headers=headers,
            params=params,
            verify=self.verify_ssl,
            timeout=self.timeout,
        )
        if response.status_code == 200:
            if "Sign in to your account" in response.text:
                raise AuthenticationError
            elif "was not found" not in response.text:
                if endpoint == "raw":
                    return response.text
                else:
                    xml_data = pyonms.utils.convert_xml(response.text)
                    return self._convert_v1_to_v2(endpoint, xml_data)
        elif response.status_code >= 400:
            raise ApiPayloadError(message=response.text)
        return {}

    def _post(
        self,
        url: str,
        headers: dict = None,
        data: str = None,
        json: dict = None,
        params: dict = None,
    ) -> requests.Response:
        if not headers:
            headers = {}
        if not params:
            params = {}
        if json:
            response = requests.post(
                url,
                auth=self.auth,
                headers=headers,
                json=json,
                params=params,
                verify=self.verify_ssl,
                timeout=self.timeout,
            )
        elif data:
            response = requests.post(
                url,
                auth=self.auth,
                headers=headers,
                data=data,
                params=params,
                verify=self.verify_ssl,
                timeout=self.timeout,
            )
        else:
            response = requests.post(
                url,
                auth=self.auth,
                headers=headers,
                verify=self.verify_ssl,
                timeout=self.timeout,
            )
        if response.status_code >= 400:
            raise ApiPayloadError(message=response.text)
        return response

    def _put(
        self,
        url: str,
        data: dict = None,
        json: dict = None,
        headers: dict = None,
        params: dict = None,
    ) -> requests.Response:
        if not headers:
            headers = {}
        if not params:
            params = {}
        if json:
            response = requests.put(
                url,
                auth=self.auth,
                headers=headers,
                json=json,
                params=params,
                verify=self.verify_ssl,
                timeout=self.timeout,
            )
        elif data:
            response = requests.put(
                url,
                auth=self.auth,
                headers=headers,
                data=data,
                params=params,
                verify=self.verify_ssl,
                timeout=self.timeout,
            )
        else:
            response = requests.put(
                url,
                auth=self.auth,
                headers=headers,
                params=params,
                verify=self.verify_ssl,
                timeout=self.timeout,
            )
        if response.status_code >= 400:
            raise ApiPayloadError(message=response.text)
        return response

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

    def _delete(self, url: str, headers: dict = None, params: dict = None) -> dict:
        if not headers:
            headers = {}
        if not params:
            params = {}
        headers["Accept"] = "application/json"
        response = requests.delete(
            url,
            auth=self.auth,
            headers=headers,
            verify=self.verify_ssl,
            timeout=self.timeout,
        )
        if response.status_code >= 400:
            raise ApiPayloadError(message=response.text)
        return {}
