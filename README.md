# PyONMS

A Python library for accessing the OpenNMS REST API.

This is being developed with Python 3.10 and OpenNMS 30.
It may work on older versions, but they haven't been tested yet.

- [OpenNMS API documentation](https://docs.opennms.com/horizon/30/development/rest/rest-api.html)

## Information

This is currently an early, pre-alpha version of this library.
More details will be added as I figure out what they are.


## Endpoints Supported

Currently there are three endpoints supported:

* Nodes
* Events
* Alarms

The actions supported on each are to get one object or get all objects.

## Getting Started

See `test_example.py` for an example of each endpoint.

Create a `.env` file and set values to connect to your server.

* `hostname` (Example: `http://localhost:8980`)
* `username`
* `password`
