# dao.udl.py

# cSpell: ignore userdefinedlinks UDLAPI

"User Defined Links data access"

from typing import List, Optional

import pyonms.models.udl
from pyonms.dao.base import Endpoint


class UDLAPI(Endpoint):
    "UDL API Endpoint"

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "userdefinedlinks"

    def get_link(self, id: int) -> Optional[pyonms.models.udl.UserDefinedLink]:
        """Get UserDefinedLink by ID number.

        Args:
            id (int): ID number of UserDefinedLink to retrieve.
        """
        record = self._get(url=f"{self.url}/{id}")
        if record not in [None, {}]:
            return self._process_udl(record)
        else:
            return None

    def get_links(
        self, limit: int = 100, batch_size: int = 100
    ) -> List[pyonms.models.udl.UserDefinedLink]:
        """Get all UserDefinedLink objects

        Args:
            limit (int, optional): Max number of UserDefinedLink objects to retrieve. Defaults to 100.
            batch_size (int, optional): Number of UserDefinedLink to retrieve per API call. Defaults to 100.
        """
        links = []
        records = self._get_batch(
            url=self.url,
            endpoint="user_defined_link",
            limit=limit,
            batch_size=batch_size,
        )
        for record in records:
            if record:
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

    def delete_link(self, id: int):
        """Delete UserDefinedLink object.

        Args:
            id (int): ID number of UserDefinedLink to delete
        """
        self._delete(url=f"{self.url}/{id}")

    def create_link(self, link: pyonms.models.udl.UserDefinedLink) -> bool:
        """Create new UserDefinedLink between two nodes.

        Args:
            link (pyonms.models.udl.UserDefinedLink): UserDefinedLink object to create

        Returns:
            bool: _description_
        """
        x = self._post(url=self.url, json=link.to_dict())
        if x.status_code == 201:
            return True
        else:
            return False
