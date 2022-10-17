# test.py

import os

from pyonms import PyONMS
from dotenv import load_dotenv

load_dotenv()

my_server = PyONMS(
    hostname=os.getenv("hostname"),
    username=os.getenv("username"),
    password=os.getenv("password"),
)


if __name__ == "__main__":
    nodes = my_server.nodes.get_nodes()
    print(f"\nDevices found: {len(nodes)}")
    print(nodes)

    events = my_server.events.get_events(limit=50, batch_size=25)
    print(f"\nEvents found: {len(events)}")
    print(events)

    alarms = my_server.alarms.get_alarms(limit=50, batch_size=25)
    print(f"\nAlarms found: {len(alarms)}")
    for alarm in alarms:
        print([alarm, my_server.nodes.get_node(alarm.nodeId)])

pass
