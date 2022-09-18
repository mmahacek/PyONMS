# test.py

import os

from pyonms import PyONMS
from dotenv import load_dotenv

load_dotenv()

myServer = PyONMS(
    hostname=os.getenv("hostname"),
    username=os.getenv("username"),
    password=os.getenv("password"),
)


if __name__ == "__main__":
    # devices = myServer.nodes.get_nodes(limit=False)
    devices = myServer.nodes.get_nodes()
    # devices = myServer.nodes.get_node(1)
    # print(f"\nDevices found: {len(devices)}")
    print(devices)

    # events = myServer.events.get_events(limit=50, batchSize=25)
    # print(f"\nEvents found: {len(events)}")
    # print(events)

    # alarms = myServer.alarms.get_alarms(limit=50, batchSize=25)
    # print(f"\nAlarms found: {len(alarms)}")
    # for alarm in alarms:
    #    print(alarm)
    # print("done")

pass
