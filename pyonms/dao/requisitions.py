# dao.requisitions.py

from typing import List, Union

from pyonms.dao import Endpoint
import pyonms.models.requisition


class RequisitionsAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "requisitions"

    def get_requisition(
        self, name: str
    ) -> Union[pyonms.models.requisition.Requisition, None]:
        record = self._get(uri=f"{self.url}/{name}", endpoint="requisitions")
        if record is not None:
            return self.process_requisition(record)
        else:
            return None

    def get_requisitions(
        self,
        limit=100,
        batch_size=100,
    ) -> List[Union[pyonms.models.requisition.Requisition, None]]:
        requisitions = []
        params = {}
        records = self.get_batch(
            url=self.url,
            endpoint="requisitions",
            limit=limit,
            batch_size=batch_size,
            params=params,
        )
        if records == [None]:
            return [None]
        for record in records:
            requisitions.append(self.process_requisition(record))
        return requisitions

    def process_requisition(self, data: dict) -> pyonms.models.requisition.Requisition:
        return pyonms.models.requisition.Requisition(**data)

    def get_requisition_active_count(self) -> int:
        count = self._get(uri=f"{self.url}/count", endpoint="raw")
        return int(count)

    def get_requisition_deployed_count(self) -> int:
        count = self._get(uri=f"{self.url}/deployed/count", endpoint="raw")
        return int(count)

    def import_requisition(self, name: str, rescan: bool = False):
        status = self._put(
            uri=f"{self.url}/{name}/import", data={}, params={"rescanExisting": rescan}
        )
        if status in [202, 204]:
            return True
        else:
            return False
