# dao.info.py

import json

from pyonms.dao import Endpoint

import pyonms.models.info


class InfoAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "info"

    def get_info(self) -> pyonms.models.info.Info:
        record = self._get(uri=f"{self.url}", endpoint="raw")
        if record is not None:
            record = json.loads(record)
            return self._process_info(record)
        else:
            return None

    def _process_info(self, data: dict) -> pyonms.models.info.Info:
        return pyonms.models.info.Info(**data)
