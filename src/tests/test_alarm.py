# _test_pyonms.py

import asyncio
import unittest

import config
from models.alarms import Alarm
from pyonms import pyonms

myServer = pyonms(
    hostname=config.hostname,
    username=config.username,
    password=config.password
)

sampleAlarm = {
            "id": 123456789,
            "uei": "uei.opennms.org/translator/traps/SNMP_Link_Up",
            "location": "Default",
            "nodeId": 4321,
            "nodeLabel": "0.0.0.0",
            "ipAddress": "0.0.0.0",
            "reductionKey": "uei.opennms.org/translator/traps/SNMP_Link_Up:00000000-0000-0000-0000-000000000000:4957:5",
            "type": 2,
            "count": 6074,
            "severity": "NORMAL",
            "firstEventTime": 1591294515888,
            "description": "<p>A linkUp trap signifies that the sending protocol entity recognizes that one of the communication\n            links represented in the agent's configuration has come up. </p>\n            <p>Instance: 5 </p>\n            <p>IfDescr: Unknown </p>\n            <p>IfName: Unknown </p>\n            <p>IfAlias: Unknown </p>",
            "logMessage": "Agent Interface Up (linkUp Trap)\n        ",
            "suppressedUntil": 1591294515888,
            "suppressedTime": 1591294515888,
            "ackUser": "admin",
            "ackTime": 1591294759437,
            "clearKey": "uei.opennms.org/translator/traps/SNMP_Link_Down:00000000-0000-0000-0000-000000000000:4957:5",
            "lastEvent": {
                "id": 15406356,
                "uei": "uei.opennms.org/translator/traps/SNMP_Link_Up",
                "label": "Translator Enriched LinkUp Event",
                "time": 1596048611919,
                "host": "2607:f380:08e4:1252:0000:0000:0000:0053",
                "source": "event-translator",
                "ipAddress": "0.0.0.0",
                "snmpHost": "0.0.0.0",
                "parameters": [
                    {
                        "name": ".1.3.6.1.2.1.2.2.1.1.5",
                        "value": "5",
                        "type": "Int32"
                    },
                    {
                        "name": "ifDescr",
                        "value": "Unknown",
                        "type": "string"
                    },
                    {
                        "name": "ifName",
                        "value": "Unknown",
                        "type": "string"
                    },
                    {
                        "name": "ifAlias",
                        "value": "Unknown",
                        "type": "string"
                    }
                ],
                "createTime": 1596048612751,
                "description": "<p>A linkUp trap signifies that the sending protocol entity recognizes that one of the communication\n            links represented in the agent's configuration has come up. </p>\n            <p>Instance: 5 </p>\n            <p>IfDescr: Unknown </p>\n            <p>IfName: Unknown </p>\n            <p>IfAlias: Unknown </p>",
                "logMessage": "Agent Interface Up (linkUp Trap)\n        ",
                "severity": "NORMAL",
                "log": "Y",
                "display": "Y",
                "nodeId": 4321,
                "nodeLabel": "0.0.0.0",
                "ifIndex": 5,
                "location": "Default"
            },
            "parameters": [
                {
                    "name": ".1.3.6.1.2.1.2.2.1.1.5",
                    "value": "5",
                    "type": "Int32"
                },
                {
                    "name": "ifDescr",
                    "value": "Unknown",
                    "type": "string"
                },
                {
                    "name": "ifName",
                    "value": "Unknown",
                    "type": "string"
                },
                {
                    "name": "ifAlias",
                    "value": "Unknown",
                    "type": "string"
                }
            ],
            "lastEventTime": 1596048611919,
            "x733ProbableCause": 0,
            "ifIndex": 5,
            "affectedNodeCount": 1
        }


class test_event_counts(unittest.TestCase):
    def test_specific_alarm(self):
        event = asyncio.run(myServer.alarms.get_alarms(id=597060))
        self.assertEqual(len(event), 1)

    def test_missing_alarm(self):
        event = asyncio.run(myServer.alarms.get_alarms(id=1))
        self.assertEqual(len(event), 0)

    def test_one_batch(self):
        event = asyncio.run(myServer.alarms.get_alarms())
        self.assertEqual(len(event), 10)

    def test_custom_limit(self):
        event = asyncio.run(myServer.alarms.get_alarms(limit=50))
        self.assertEqual(len(event), 50)

    def test_custom_batches(self):
        event = asyncio.run(myServer.alarms.get_alarms(limit=100, batchSize=15))
        self.assertGreaterEqual(len(event), 90)


class test_event_data(unittest.TestCase):
    def test_specific_alarm(self):
        alarm = Alarm(sampleAlarm)
        self.assertEqual(alarm.id, 123456789)

    def test_specific_alarm_uei(self):
        alarm = Alarm(sampleAlarm)
        self.assertIn('uei.opennms.org', alarm.uei)


if __name__ == "__main__":
    unittest.main()
