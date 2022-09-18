# dao.nodes.py

# cspell:ignore snmpinterfaces, ipinterfaces

from pyonms.dao.api import Endpoint
import pyonms.models.node


class NodeAPI(Endpoint):
    def __init__(self, args):
        super().__init__(**args)
        self.url = self.base_v2 + "nodes"

    def get_node(self, id: int) -> pyonms.models.node.Node:
        record = self._get(uri=f"{self.url}/{id}")
        if record is not None:
            return self.process_node(record)
        else:
            return None

    def get_nodes(self, limit=10, batchSize=10) -> list:
        devices = []
        records = self.get_data(
            url=self.url,
            endpoint="node",
            limit=limit,
            batchSize=batchSize,
        )
        if records == [None]:
            return None
        for record in records:
            devices.append(self.process_node(record))
        return devices

    def process_node(self, node):
        newNode = pyonms.models.node.Node(node)

        sUrl = f"{self.url}/{newNode.id}/snmpinterfaces"
        snmpRecords = self._get(uri=sUrl)
        snmp = {}
        if snmpRecords:
            for s in snmpRecords["snmpInterface"]:
                snmp[s["ifName"]] = pyonms.models.node.snmpInterface(s)
            newNode.snmpInterface = snmp

        iUrl = f"{self.url}/{newNode.id}/ipinterfaces"
        ipRecords = self._get(uri=iUrl)
        ip = {}
        if ipRecords:
            for i in ipRecords["ipInterface"]:
                ip[i["ipAddress"]] = pyonms.models.node.ipInterface(i)
                srUrl = (
                    f"{self.url}/{newNode.id}/ipinterfaces/{i['ipAddress']}/services"
                )
                sRecords = self._get(uri=srUrl)
                if sRecords:
                    service = {}
                    for sr in sRecords["service"]:
                        service[sr["id"]] = pyonms.models.node.service(sr)
                    ip[i["ipAddress"]].service = service
            newNode.ipInterface = ip
        metadata = {}
        mUrl = f"{self.url}/{newNode.id}/metadata"
        mRecords = self._get(uri=mUrl)
        newNode.metadata = []
        for record in mRecords["metaData"]:
            newNode.metadata.append(pyonms.models.node.metadata(**record))
        return newNode
