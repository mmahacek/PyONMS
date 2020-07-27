# dao.nodes.py
# cspell:ignore snmpinterfaces, ipinterfaces

import models.node
import utils.http

class Nodes():
    def __init__(self, api):
        self.api = api
        self.url = self.api.base_url + 'nodes'

    async def getNodes(self, id=None, limit=10, batchSize=10, offset=0) -> dict:
        devices = {}
        if id == None:
            records = await utils.http.getHttp(uri=f'{self.url}?limit={batchSize}&offset={offset}', API=self.api)
            if records['node'] == [None]:
                return None
            actualCount = records['totalCount']
            if limit == 0 or limit == None:
                limit = actualCount
            processed = 0
            while (actualCount - processed) > 0:
                print(processed)
                for node in records['node']:
                    if processed >= limit:
                        break
                    newNode = await self.processNode(node)
                    devices[int(newNode.id)] = newNode
                    processed += 1
                if processed >= limit:
                    break
                records = await utils.http.getHttp(uri=f'{self.url}?limit={batchSize}&offset={processed}', API=self.api)
                if records['node'] == [None]:
                    break
        else:
            records = await utils.http.getHttp(uri=f'{self.url}/{id}', API=self.api)
            actualCount = 1
            if records != None:
                newNode = await self.processNode(records)
                devices[newNode.id] = newNode
        return devices

    async def processNode(self, node):
        newNode = models.node.Node(node)

        sUrl= f"{self.url}/{newNode.id}/snmpinterfaces"
        snmpRecords = await utils.http.getHttp(uri=sUrl, API=self.api)
        snmp = {}
        if snmpRecords:
            for s in snmpRecords['snmpInterface']:
                snmp[s['ifName']] = models.node.snmpInterface(s)
            newNode.snmpInterface = snmp

        iUrl = f"{self.url}/{newNode.id}/ipinterfaces"
        ipRecords = await utils.http.getHttp(uri=iUrl, API=self.api)
        ip = {}
        if ipRecords:
            for i in ipRecords['ipInterface']:
                ip[i['ipAddress']] = models.node.ipInterface(i)
                srUrl = self.url + f"/{i['ipAddress']}/services"
                sRecords = await utils.http.getHttp(uri=srUrl, API=self.api)
                if sRecords:
                    service = {}
                    for sr in sRecords['service']:
                        service[sr['id']] = models.node.service(sr)
                    ip[i['ipAddress']].service = service                
            newNode.ipInterface = ip
        return newNode