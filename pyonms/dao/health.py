# dao.health.py

from pyonms.dao import Endpoint

import pyonms.models.health


class HealthAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "health"

    def get_health(self) -> pyonms.models.health.Health:
        record = self._get(uri=f"{self.url}", endpoint="raw")
        if record is not None:
            health = self._process_health(record)
            if health.healthy:
                print(f"Connected to {self.name}")
            else:
                print(f"{self.name} is not healthy")
            return health
        else:
            return None

    def probe(self) -> str:
        return self._get(uri=f"{self.url}/probe", endpoint="raw")

    def _process_health(self, data: dict) -> pyonms.models.health.Health:
        return pyonms.models.health.Health(**data)
