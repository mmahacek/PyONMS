# dao.requisitions.py

"Requisitions data access"

from typing import List, Optional, Union

from requests import Response

import pyonms.models.requisition
from pyonms.dao.base import Endpoint
from pyonms.utils import normalize_dict


class RequisitionsAPI(Endpoint):
    "Requisitions API endpoint"

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "requisitions"

    def get_requisition_names(self) -> List[str]:
        """Get a list of Requisition names"""
        names = self._get(
            url=f"{self.base_v1}/requisitionNames",
            endpoint="requisitionNames",
            headers=self.headers,
        )
        return names["foreign-source"]

    def get_requisition(
        self, name: str
    ) -> Optional[pyonms.models.requisition.Requisition]:
        """Get the contents of a requisition"""
        record = self._get(
            url=f"{self.url}/{name}", endpoint="requisitions", headers=self.headers
        )
        if record is not None:
            return self._process_requisition(record)
        else:
            return None

    def get_requisitions(
        self,
    ) -> List[pyonms.models.requisition.Requisition]:
        """Get the contents of all requisitions"""
        records = self._get(
            url=self.url,
            endpoint="model-import",
        )
        requisitions = []
        for record in records["model-import"]:
            if record:
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
        parsed_data = dict(normalize_dict(data))
        return pyonms.models.requisition.Requisition(**parsed_data)

    def get_requisition_active_count(self) -> int:
        """Get number of active requisitions"""
        count = self._get(url=f"{self.url}/count", endpoint="raw")
        return int(count)

    def get_requisition_deployed_count(self) -> int:
        """Get number of deployed requisitions"""
        count = self._get(url=f"{self.url}/deployed/count", endpoint="raw")
        return int(count)

    def import_requisition(self, name: str, rescan: bool = False) -> bool:
        """Trigger rescan of an existing requisition"""
        response = self._put(
            url=f"{self.url}/{name}/import",
            params={"rescanExisting": rescan},
        )
        if response.status_code in [202, 204]:
            return True
        else:
            return False

    def update_requisition(
        self, requisition: pyonms.models.requisition.Requisition
    ) -> Response:
        """Post an entire requisition to create or overwrite."""
        response = self._post(
            url=self.url, headers=self.headers, json=requisition.to_dict()
        )
        return response

    def update_node(
        self,
        requisition: Union[str, pyonms.models.requisition.Requisition],
        node: pyonms.models.requisition.RequisitionNode,
    ) -> Response:
        """Post a single node to create or overwrite."""
        if isinstance(requisition, pyonms.models.requisition.Requisition):
            requisition = requisition.foreign_source
        response = self._post(
            url=f"{self.url}/{requisition}/nodes",
            headers=self.headers,
            json=node.to_dict(),
        )
        return response
