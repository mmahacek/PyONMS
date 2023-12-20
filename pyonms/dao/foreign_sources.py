# dao.foreign_sources.py

from typing import List, Optional

from requests import Response

import pyonms.models.foreign_source
from pyonms.dao.base import Endpoint


class ForeignSourceAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "foreignSources"

    def get_foreign_source(
        self, name: str
    ) -> Optional[pyonms.models.foreign_source.ForeignSource]:
        record = self._get(url=f"{self.url}/{name}", endpoint="foreignSources")
        if record is not None:
            return self._process_foreign_source(record)
        else:
            return None

    def get_foreign_sources(
        self,
    ) -> List[Optional[pyonms.models.foreign_source.ForeignSource]]:
        foreign_sources = []
        records = self._get(
            url=self.url,
            endpoint="foreignSources",
        )
        if records == [None]:
            return [None]
        for record in records["foreignSources"]:
            foreign_sources.append(self._process_foreign_source(record))
        return foreign_sources

    def _process_foreign_source(
        self, data: dict
    ) -> pyonms.models.foreign_source.ForeignSource:
        if data.get("date-stamp"):
            data["date_stamp"] = data["date-stamp"]
            del data["date-stamp"]
        if data.get("scan-interval"):
            data["scan_interval"] = data["scan-interval"]
            del data["scan-interval"]
        for entry in data.get("detectors", []):
            if entry.get("class"):
                entry["class_type"] = entry["class"]
                del entry["class"]
        for entry in data.get("policies", []):
            if entry.get("class"):
                entry["class_type"] = entry["class"]
                del entry["class"]
        return pyonms.models.foreign_source.ForeignSource(**data)

    def update_foreign_source(
        self, foreign_source: pyonms.models.foreign_source.ForeignSource
    ) -> Response:
        response = self._post(
            url=self.url, headers=self.headers, json=foreign_source._to_dict()
        )
        return response
