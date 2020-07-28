# test.py

"""This is a sample file for testing the library.
    Copy `config.py.example` to `config.py` and enter your OpenNMS server info.
    Copy this file to `test.py` and run for testing purposes. Modify as needed.
"""

from pyonms import pyonms
import asyncio
import config

myServer = pyonms(
    hostname=config.hostname,
    username=config.username,
    password=config.password
)


if __name__ == "__main__":
    devices = asyncio.run(myServer.nodes.get_nodes(limit=50, batchSize=25))
    print(f'\nDevices found: {len(devices)}')
    print(devices)

    events = asyncio.run(myServer.events.get_events())
    print(f'\nEvents found: {len(events)}')
    print(events)

    alarms = asyncio.run(myServer.alarms.get_alarms())
    print(f'\nAlarms found: {len(alarms)}')
    print(alarms)
