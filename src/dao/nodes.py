# dao.nodes.py
# cspell:ignore snmpinterfaces, ipinterfaces

"""Data Access Object for dealing with Node objects
"""
from dao.core import Endpoint
import models.node
import utils.http


class Nodes(Endpoint):
    def __init__(self, api):
        self.api = api
        self.url = self.api.base_v2 + 'nodes'

    async def get_nodes(self, id=None, limit=10, batchSize=10) -> dict:
        """Get nodes from OpenNMS API

        Args:
            id (int, optional): If provided, request one specific node.
                Defaults to None, which gets all nodes.
            limit (int, optional): Max number of requests to return.
                Defaults to 10.
            batchSize (int, optional): Number of nodes to get per HTTP request.
                Defaults to 10.

        Returns:
            dict: Dictionary of Node objects
        """
        devices = {}
        if id is None:
            records = await self.get_data(api=self.api, url=self.url, endpoint='node', limit=limit, batchSize=batchSize)
            if records == [None]:
                return None
            for record in records:
                newNode = await self.process_node(record)
                devices[int(newNode.id)] = newNode
        else:
            record = await utils.http.get_http(uri=f'{self.url}/{id}', API=self.api)
            if record is not None:
                newNode = await self.process_node(record)
                devices[newNode.id] = newNode
        return devices

    async def process_node(self, node):
        newNode = models.node.Node(node)

        sUrl = f"{self.url}/{newNode.id}/snmpinterfaces"
        snmpRecords = await utils.http.get_http(uri=sUrl, API=self.api)
        snmp = {}
        if snmpRecords:
            for s in snmpRecords['snmpInterface']:
                snmp[s['ifName']] = models.node.snmpInterface(s)
            newNode.snmpInterface = snmp

        iUrl = f"{self.url}/{newNode.id}/ipinterfaces"
        ipRecords = await utils.http.get_http(uri=iUrl, API=self.api)
        ip = {}
        if ipRecords:
            for i in ipRecords['ipInterface']:
                ip[i['ipAddress']] = models.node.ipInterface(i)
                srUrl = self.url + f"/{i['ipAddress']}/services"
                sRecords = await utils.http.get_http(uri=srUrl, API=self.api)
                if sRecords:
                    service = {}
                    for sr in sRecords['service']:
                        service[sr['id']] = models.node.service(sr)
                    ip[i['ipAddress']].service = service
            newNode.ipInterface = ip
        return newNode
