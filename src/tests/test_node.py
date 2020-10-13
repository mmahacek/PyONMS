# _test_pyonms.py

import asyncio
import unittest

import config
from pyonms import pyonms


myServer = pyonms(
    hostname=config.hostname,
    username=config.username,
    password=config.password
)


class test_node_counts(unittest.TestCase):
    def test_one_batch(self):
        devices = asyncio.run(myServer.nodes.get_nodes())
        self.assertEqual(len(devices), 10)

    def test_specific_node(self):
        batch = asyncio.run(myServer.nodes.get_nodes(limit=1, batchSize=1))
        for device in batch:
            devices = asyncio.run(myServer.nodes.get_nodes(id=batch[device].id))
        self.assertEqual(len(devices), 1)

    def test_missing_node(self):
        devices = asyncio.run(myServer.nodes.get_nodes(id=1))
        self.assertEqual(len(devices), 0)

    def test_custom_limit(self):
        devices = asyncio.run(myServer.nodes.get_nodes(limit=50))
        self.assertEqual(len(devices), 50)

    def test_custom_batches(self):
        devices = asyncio.run(myServer.nodes.get_nodes(limit=100, batchSize=15))
        self.assertEqual(len(devices), 100)


class test_node_data(unittest.TestCase):
    def test_specific_node(self):
        device = asyncio.run(myServer.nodes.get_nodes(id=3591))
        self.assertEqual(device['3591'].id, '3591')

    def test_specific_node_ip(self):
        device = asyncio.run(myServer.nodes.get_nodes(id=3591))
        self.assertEqual(str(device['3591'].ipInterface['10.50.252.93']), '10.50.252.93')


if __name__ == "__main__":
    unittest.main()
