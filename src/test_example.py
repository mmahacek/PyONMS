# test.py

"""This is a sample file for testing the library.
    Copy `config.py.example` to `config.py` and enter your OpenNMS server info.
    Copy this file to `test.py` and run for testing purposes. Modify as needed.
"""

from pyonms import pyonms
import config

myServer = pyonms(
    hostname=config.hostname,
    username=config.username,
    password=config.password
)


if __name__ == "__main__":
    devices = myServer.nodes.get_nodes(limit=10, batchSize=2)
    print(f'\nDevices found: {len(devices)}')
    print(devices)

    # events = myServer.events.get_events(limit=50, batchSize=25)
    # print(f'\nEvents found: {len(events)}')
    # print(events)

    #alarms = myServer.alarms.get_alarms(limit=50, batchSize=25)
    #print(f'\nAlarms found: {len(alarms)}')
    #for alarm in alarms:
    #    print(alarm)
    print('done')
