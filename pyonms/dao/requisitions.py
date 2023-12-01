# dao.requisitions.py

from typing import List, Union

import requests

import pyonms.models.requisition
from pyonms.dao.base import Endpoint
from pyonms.utils import normalize_dict


class RequisitionsAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "requisitions"

    def get_requisition_names(self) -> List[str]:
        names = self._get(
            uri=f"{self.base_v1}/requisitionNames",
            endpoint="requisitionNames",
            headers=self.headers,
        )
        return names["foreign-source"]

    def get_requisition(
        self, name: str
    ) -> Union[pyonms.models.requisition.Requisition, None]:
        record = self._get(
            uri=f"{self.url}/{name}", endpoint="requisitions", headers=self.headers
        )
        if record is not None:
            return self._process_requisition(record)
        else:
            return None

    def get_requisitions(
        self,
        limit=100,
        batch_size=100,
    ) -> List[Union[pyonms.models.requisition.Requisition, None]]:
        requisitions = []
        params = {}
        records = self._get_batch(
            url=self.url,
            endpoint="model-import",
            limit=limit,
            batch_size=batch_size,
            params=params,
        )
        if records == [None]:
            return [None]
        for record in records:
            requisitions.append(self._process_requisition(record))
        return requisitions

    def _process_requisition(self, data: dict) -> pyonms.models.requisition.Requisition:
        # if data.get("foreign-source"):
        #     data["foreign_source"] = data["foreign-source"]
        #     del data["foreign-source"]
        # if data.get("date-stamp"):
        #     data["date_stamp"] = data["date-stamp"]
        #     del data["date-stamp"]
        # if data.get("last-import") or data["last-import"] is None:
        #     data["last_import"] = data["last-import"]
        #     del data["last-import"]
        data = normalize_dict(data)
        return pyonms.models.requisition.Requisition(**data)

    def get_requisition_active_count(self) -> int:
        count = self._get(uri=f"{self.url}/count", endpoint="raw")
        return int(count)

    def get_requisition_deployed_count(self) -> int:
        count = self._get(uri=f"{self.url}/deployed/count", endpoint="raw")
        return int(count)

    def import_requisition(self, name: str, rescan: bool = False) -> bool:
        response = self._put(
            uri=f"{self.url}/{name}/import",
            params={"rescanExisting": rescan},
        )
        if response.status_code in [202, 204]:
            return True
        else:
            return False

    def _put(
        self,
        uri: str,
        data: dict = {},
        params: dict = {},
    ) -> requests.Response:
        response = requests.put(
            uri,
            auth=self.auth,
            headers=self.headers,
            data=data,
            params=params,
            verify=self.verify_ssl,
        )
        return response

    def update_requisition(self, requisition: pyonms.models.requisition.Requisition):
        """Post an entire requisition to create or overwrite."""
        response = self._post(
            uri=self.url, headers=self.headers, json=requisition._to_dict()
        )
        return response

    def update_node(
        self,
        requisition: Union[str, pyonms.models.requisition.Requisition],
        node: pyonms.models.requisition.RequisitionNode,
    ):
        """Post a single node to create or overwrite."""
        if isinstance(requisition, pyonms.models.requisition.Requisition):
            requisition = requisition.foreign_source
        response = self._post(
            uri=f"{self.url}/{requisition}/nodes",
            headers=self.headers,
            json=node._to_dict(),
        )
        return response
