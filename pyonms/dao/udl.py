# dao.udl.py

# cSpell: ignore userdefinedlinks UDLAPI

from typing import List, Optional

import pyonms.models.udl
from pyonms.dao import Endpoint


class UDLAPI(Endpoint):
    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "userdefinedlinks"

    def get_link(self, id: int) -> Optional[pyonms.models.udl.UserDefinedLink]:
        record = self._get(uri=f"{self.url}/{id}")
        if record not in [None, {}]:
            return self._process_udl(record)
        else:
            return None

    def get_links(
        self, limit: int = 100, batch_size: int = 100
    ) -> List[Optional[pyonms.models.udl.UserDefinedLink]]:
        links = []
        records = self._get_batch(
            url=self.url,
            endpoint="user_defined_link",
            limit=limit,
            batch_size=batch_size,
        )
        if records == [None]:
            return [None]
        for record in records:
            links.append(self._process_udl(record))
        return links

    def _process_udl(self, data: dict) -> pyonms.models.udl.UserDefinedLink:
        clean_data = {"owner": data["owner"]}
        clean_data["node_id_a"] = data["node-id-a"]
        clean_data["node_id_z"] = data["node-id-z"]
        clean_data["component_label_a"] = data["component-label-a"]
        clean_data["component_label_z"] = data["component-label-z"]
        clean_data["link_id"] = data["link-id"]
        clean_data["db_id"] = data["db-id"]
        return pyonms.models.udl.UserDefinedLink(**clean_data)

    def delete_link(self, id: int) -> bool:
        x = self._delete(uri=f"{self.url}/{id}")
        return x

    def create_link(self, link: pyonms.models.udl.UserDefinedLink) -> bool:
        x = self._post(uri=self.url, json=link._to_dict())
        if x.status_code == 201:
            return True
        else:
            return False
