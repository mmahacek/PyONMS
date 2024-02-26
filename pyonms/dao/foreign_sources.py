# dao.foreign_sources.py

"Foreign Sources data access"

from typing import List, Optional

from requests import Response

import pyonms.models.foreign_source
from pyonms.dao.base import Endpoint


class ForeignSourceAPI(Endpoint):
    "Foreign Sources API endpoint"

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "foreignSources"

    def get_foreign_source(
        self, name: str
    ) -> Optional[pyonms.models.foreign_source.ForeignSource]:
        """Get foreign source definition."""
        record = self._get(url=f"{self.url}/{name}", endpoint="foreignSources")
        if record is not None:
            return self._process_foreign_source(record)
        else:
            return None

    def get_foreign_sources(
        self,
    ) -> List[pyonms.models.foreign_source.ForeignSource]:
        """Get all foreign source definitions"""
        records = self._get(
            url=self.url,
            endpoint="foreignSources",
        )
        foreign_sources = []
        for record in records["foreignSources"]:
            if record:
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
        """Update foreign source definition on server."""
        response = self._post(
            url=self.url, headers=self.headers, json=foreign_source.to_dict()
        )
        return response
