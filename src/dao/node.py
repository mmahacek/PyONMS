# dao.node.py
# cspell:ignore snmpinterfaces, ipinterfaces

import models.node
import utils.http

async def getNodes(api, id=None, limit=100) -> dict:
    url = api.base_url + 'nodes'
    if id == None:
        records = await utils.http.getHttp(uri=f'{url}?limit={limit}', API=api)
    else:
        records = {'node': [await utils.http.getHttp(uri=f'{url}/{id}?limit={limit}', API=api)]}
    if records['node'] == [None]:
        return None
    devices = {}
    for d in records['node']:
        devices[d['id']] = models.node.Node(d)

        sUrl= f"{url}/{d['id']}/snmpinterfaces"
        records = await utils.http.getHttp(uri=sUrl, API=api)
        snmp = {}
        for s in records['snmpInterface']:
            snmp[s['ifName']] = models.node.snmpInterface(s)
        devices[d['id']].snmpInterface = snmp

        iUrl = f"{url}/{d['id']}/ipinterfaces"
        records = await utils.http.getHttp(uri=iUrl, API=api)
        ip = {}
        for i in records['ipInterface']:
            ip[i['ipAddress']] = models.node.ipInterface(i)
            srUrl = url + f"/{i['ipAddress']}/services"
            sRecords = await utils.http.getHttp(uri=srUrl, API=api)
            if sRecords:
                service = {}
                for sr in sRecords['service']:
                    service[sr['id']] = models.node.service(sr)
                ip[i['ipAddress']].service = service


    #        if i.get('snmpInterface'):
    #            ip[i['ipAddress']].snmpInterface = models.node.snmpInterface(i['snmpInterface'])
                
        devices[d['id']].ipInterface = ip
    return devices