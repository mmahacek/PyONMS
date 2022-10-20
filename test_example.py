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

    events = my_server.events.get_events(limit=50, batch_size=25)
    print(f"\nEvents found: {len(events)}")
    print(events)

    alarms = my_server.alarms.get_alarms(limit=50, batch_size=25)
    print(f"\nAlarms found: {len(alarms)}")
    # for alarm in alarms:
    #    print([alarm, my_server.nodes.get_node(alarm.nodeId)])

    main = my_server.fs.get_foreign_sources()
    print(main)
    pass
