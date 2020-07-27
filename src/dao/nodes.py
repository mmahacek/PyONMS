# dao.nodes.py
# cspell:ignore snmpinterfaces, ipinterfaces

import models.node
import utils.http

class Nodes():
    def __init__(self, api):
        self.api = api
    
    async def getNodes(self, id=None, limit=10) -> dict:
        url = self.api.base_url + 'nodes'
        if id == None:
            records = await utils.http.getHttp(uri=f'{url}?limit={limit}', API=self.api)
        else:
            records = {'node': [await utils.http.getHttp(uri=f'{url}/{id}?limit={limit}', API=self.api)]}
        if records['node'] == [None]:
            return None
        devices = {}
        for d in records['node']:
            devices[d['id']] = models.node.Node(d)

            sUrl= f"{url}/{d['id']}/snmpinterfaces"
            snmpRecords = await utils.http.getHttp(uri=sUrl, API=self.api)
            snmp = {}
            if snmpRecords:
                for s in snmpRecords['snmpInterface']:
                    snmp[s['ifName']] = models.node.snmpInterface(s)
                devices[d['id']].snmpInterface = snmp

            iUrl = f"{url}/{d['id']}/ipinterfaces"
            ipRecords = await utils.http.getHttp(uri=iUrl, API=self.api)
            ip = {}
            if ipRecords:
                for i in ipRecords['ipInterface']:
                    ip[i['ipAddress']] = models.node.ipInterface(i)
                    srUrl = url + f"/{i['ipAddress']}/services"
                    sRecords = await utils.http.getHttp(uri=srUrl, API=self.api)
                    if sRecords:
                        service = {}
                        for sr in sRecords['service']:
                            service[sr['id']] = models.node.service(sr)
                        ip[i['ipAddress']].service = service                
                devices[d['id']].ipInterface = ip
        return devices