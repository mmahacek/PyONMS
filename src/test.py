import utils.api
import asyncio
import aiohttp
import json
import pprint as p
import models.node
import config

api = utils.api.API(hostname=config.hostname, username=config.username, password=config.password)

async def getNodes():
    url= api.base_url + 'nodes'
    records= await utils.api.getHttp(uri=f'{url}?limit=10', API=api)
    devices = {}
    for d in records['node']:
        devices[d['id']] = models.node.Node(d)

        sUrl= f"{url}/{d['id']}/snmpinterfaces"
        records= await utils.api.getHttp(uri=sUrl, API=api)
        snmp = {}
        for s in records['snmpInterface']:
            snmp[s['ifName']] = models.node.snmpInterface(s)
        devices[d['id']].snmpInterface = snmp

        iUrl = f"{url}/{d['id']}/ipinterfaces"
        records= await utils.api.getHttp(uri=iUrl, API=api)
        ip = {}
        for i in records['ipInterface']:
            ip[i['ipAddress']] = models.node.ipInterface(i)
            srUrl= url + f"/{i['ipAddress']}/services"
            sRecords=await utils.api.getHttp(uri=srUrl, API=api)
            if sRecords:
                service = {}
                for sr in sRecords['service']:
                    service[sr['id']] = models.node.service(sr)
                ip[i['ipAddress']].service = service


    #        if i.get('snmpInterface'):
    #            ip[i['ipAddress']].snmpInterface = models.node.snmpInterface(i['snmpInterface'])
                
        devices[d['id']].ipInterface = ip
    return devices


if __name__ == "__main__":
    devices = asyncio.run(getNodes())
    p.pprint(devices)