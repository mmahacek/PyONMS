# test.py

import os

from dotenv import load_dotenv

from pyonms import PyONMS
from pyonms.dao.nodes import NodeComponents

load_dotenv()

my_server = PyONMS(
    hostname=os.getenv("hostname"),
    username=os.getenv("username"),
    password=os.getenv("password"),
)


if __name__ == "__main__":
    nodes = my_server.nodes.get_nodes(
        limit=500, batch_size=100, components=[NodeComponents.ALL]
    )
    print(f"Devices found: {len(nodes)}")
    # print(nodes)

    events = my_server.events.get_events(limit=1000, batch_size=100)
    print(f"Events found: {len(events)}")
    # print(events)

    alarms = my_server.alarms.get_alarms(limit=500, batch_size=100)
    print(f"Alarms found: {len(alarms)}")
    # for alarm in alarms:
    #    if alarm.nodeId:
    #        print([alarm, my_server.nodes.get_node(alarm.nodeId)])
    #    else:
    #        print([alarm])

    reqs = my_server.requisitions.get_requisitions()

    areq_count = my_server.requisitions.get_requisition_active_count()
    rreq_count = my_server.requisitions.get_requisition_deployed_count()
    print(f"Requisitions found: {len(reqs)} ({areq_count}/{rreq_count})")
    # main = my_server.requisitions.import_requisition("selfmonitor", rescan=False)
pass
