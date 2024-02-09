# dao.health.py

"Health endpoint data access"

from typing import Optional

import pyonms.models.health
from pyonms.dao.base import Endpoint


class HealthAPI(Endpoint):
    """Health API endpoint"""

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v1 + "health"

    def get_health(self) -> Optional[pyonms.models.health.Health]:
        """Get health status from current server instance"""
        record = self._get(url=f"{self.url}", endpoint="raw")
        if record is not None:
            health = self._process_health(record)
            if health.healthy is True:
                print(f"Connected to {self.name}")
            elif health.healthy is False:
                print(f"{self.name} is not healthy")
            else:
                print(f"{self.name} health status unknown")
            return health
        else:
            return None

    def probe(self) -> str:
        """Get probe status from current server instance"""
        return self._get(url=f"{self.url}/probe", endpoint="raw")

    def _process_health(self, data: dict) -> pyonms.models.health.Health:
        return pyonms.models.health.Health(**data)
