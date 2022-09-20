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
        self, limit=100, batch_size=100
    ) -> List[Union[pyonms.models.requisition.Requisition, None]]:
        requisitions = []
        records = self.get_batch(
            url=self.url,
            endpoint="requisitions",
            limit=limit,
            batch_size=batch_size,
        )
        if records == [None]:
            return [None]
        for record in records:
            requisitions.append(self.process_requisition(record))
        return requisitions

    def process_requisition(self, requisition) -> pyonms.models.requisition.Requisition:
        return pyonms.models.requisition.Requisition(**requisition)
