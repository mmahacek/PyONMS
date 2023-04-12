![package version](https://img.shields.io/pypi/v/pyonms)
![python version](https://img.shields.io/pypi/pyversions/pyonms)

# PyONMS

A Python library for accessing the OpenNMS REST API.

This is being developed with Python 3.10 and OpenNMS 31.
It may work on older versions, but they haven't been tested yet.

- [OpenNMS REST API documentation](https://docs.opennms.com/horizon/31/development/rest/rest-api.html)

## Information

This currently is an early, pre-release version of this library.
It is not maintained or published by The OpenNMS Group.


## Endpoints Supported

Currently supported endpoints include:

* Alarms (read-only)
* Business Services (read-write)
* Events (read, send)
* Foreign Sources (read-write)
* Heath (read-only)
* Info (read-only)
* Nodes (read-only)
* Requisitions (read-write)

## Getting Started

See the [project documentation](https://mmahacek.github.io/PyONMS/) for instructions on using this library.
