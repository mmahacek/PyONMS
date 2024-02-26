# dao.info.py

"Info endpoint data access"

from typing import Optional

import pyonms.models.info
from pyonms.dao.base import Endpoint


class InfoAPI(Endpoint):
    "Info API endpoint"

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "info"

    def get_info(self) -> Optional[pyonms.models.info.Info]:
        """Get information about the current server instance"""
        record = self._get(url=f"{self.url}", endpoint="raw")
        if record is not None:
            return self._process_info(record)
        else:
            return None

    def _process_info(self, data: dict) -> pyonms.models.info.Info:
        return pyonms.models.info.Info(**data)
