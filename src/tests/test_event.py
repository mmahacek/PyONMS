# _test_pyonms.py

import asyncio
import unittest

import config
from models.events import Event
from pyonms import pyonms

myServer = pyonms(
    hostname=config.hostname,
    username=config.username,
    password=config.password
)

sampleEvent = {
            "id": 12345,
            "uei": "uei.opennms.org/nodes/nodeRegainedService",
            "label": "OpenNMS-defined node event: nodeRegainedService",
            "time": 1596046834402,
            "host": "test.pyonms.py",
            "source": "OpenNMS.Poller.DefaultPollContext",
            "ipAddress": "1.2.3.4",
            "serviceType": {
                "id": 6,
                "name": "HTTPS"
            },
            "parameters": [],
            "createTime": 1596046834405,
            "description": "<p>The HTTPS service on interface 1.2.3.4 was\n            previously down and has been restored.</p>\n            <p>This event is generated when a service which had\n            previously failed polling attempts is again responding to\n            polls by OpenNMS. </p> <p>This event will cause\n            any active outages associated with this service/interface\n            combination to be cleared.</p>",
            "logMessage": "\n            The HTTPS outage on interface 1.2.3.4 has been\n            cleared. Service is restored.\n        ",
            "severity": "NORMAL",
            "log": "Y",
            "display": "Y",
            "nodeId": 4321,
            "nodeLabel": "testnode",
            "location": "Default"
        }


class test_event_counts(unittest.TestCase):
    def test_specific_event(self):
        event = asyncio.run(myServer.events.get_events(id=17032591))
        self.assertEqual(len(event), 1)

    def test_missing_event(self):
        event = asyncio.run(myServer.events.get_events(id=1))
        self.assertEqual(len(event), 0)

    def test_one_batch(self):
        event = asyncio.run(myServer.events.get_events())
        self.assertEqual(len(event), 10)

    def test_custom_limit(self):
        event = asyncio.run(myServer.events.get_events(limit=50))
        self.assertGreaterEqual(len(event), 40)

    def test_custom_batches(self):
        event = asyncio.run(myServer.events.get_events(limit=100, batchSize=15))
        self.assertGreaterEqual(len(event), 90)


class test_event_data(unittest.TestCase):
    def test_specific_event(self):
        event = Event(sampleEvent)
        self.assertEqual(event.id, 12345)

    def test_specific_event_uei(self):
        event = Event(sampleEvent)
        self.assertIn('uei.opennms.org', event.uei)


if __name__ == "__main__":
    unittest.main()
