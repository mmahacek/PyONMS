# dao.ips.py

# cspell:ignore ipinterfaces

"IP Interface data access"

from typing import List, Optional, Union

import pyonms.models.node
from pyonms.dao.base import Endpoint
from pyonms.models import exceptions


class IPAPI(Endpoint):
    "IP Interface API endpoint"

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "ipinterfaces"

    def get_ips(
        self,
        limit: int = 10,
        batch_size: int = 100,
        ip: Optional[str] = None,
        nodeId: Optional[int] = None,
        nodeLabel: Optional[str] = None,
        primary: Optional[Union[pyonms.models.node.PrimaryType, str]] = None,
    ) -> List[pyonms.models.node.IPInterface]:
        """Search for IP Interface objects.
            If more than one of `ip`, `nodeId`, `nodeLabel`, and `primary` are specified, the search acts as an `AND`.

        Args:
            limit (int, optional): Number of IPs to return. Defaults to 10.
            batch_size (int, optional): Number of IPs to return per page. Defaults to 100.
            ip (str, optional): IP address to search.
            nodeId (int, optional): Node ID to search.
            nodeLabel (str, optional): Node label to search.
            primary (Union[pyonms.models.node.PrimaryType, str], optional):
                Search for `Primary`, `Secondary`, or `Not_Eligible` IP Interfaces.

        Raises:
            exceptions.InvalidValueError: If `primary` is not a valid value.

        Returns:
            List[pyonms.models.node.IPInterface]: List of `IPInterface` objects.
        """
        params = {}
        search = []
        if ip:
            search.append(f"ipAddress=={ip}")
        if nodeId:
            search.append(f"node.id=={nodeId}")
        if nodeLabel:
            search.append(f"node.label=={nodeLabel}")
        if isinstance(primary, pyonms.models.node.PrimaryType):
            search.append(f"snmpPrimary=={primary.value}")
        elif isinstance(primary, str):
            if primary in pyonms.models.node.PrimaryType.list():
                search.append(f"snmpPrimary=={primary}")
            else:
                raise exceptions.InvalidValueError(
                    name="primary",
                    value=primary,
                    valid=pyonms.models.node.PrimaryType.list(),
                )
        params["_s"] = ";".join(search)
        record = self._get_batch(
            url=self.url,
            limit=limit,
            params=params,
            batch_size=batch_size,
            endpoint="ipInterface",
        )
        ip_list = []
        for address in record:
            if address:
                ip_list.append(self._process_ip(address))
        return ip_list

    def _process_ip(self, data: dict) -> pyonms.models.node.IPInterface:
        ip = pyonms.models.node.IPInterface(**data)
        return ip
