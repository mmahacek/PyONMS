![package version](https://img.shields.io/pypi/v/pyonms)
![python version](https://img.shields.io/pypi/pyversions/pyonms)
![license](https://img.shields.io/github/license/mmahacek/pyonms)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# PyONMS

A Python library for accessing the OpenNMS REST API.

This is being developed with Python 3.11 and OpenNMS 32.
It may work on older versions, but they haven't been tested yet.

- [OpenNMS REST API documentation](https://docs.opennms.com/horizon/32/development/rest/rest-api.html)
- [PyONMS documentation](https://mmahacek.github.io/PyONMS/)
- [PyPi Library](https://pypi.org/project/pyonms/)

## Information

This currently is an early, pre-release version of this library.
It is not maintained or supported by The OpenNMS Group.


## Endpoints Supported

Currently supported endpoints include:

* Alarms (read-write)
* Business Services (read-write)
* Enlinkd (read-only)
* Events (read, send)
* Foreign Sources (read-write)
* Health (read-only)
* Info (read-only)
* IP Interfaces (read-only)
* Nodes (read, metadata modify requires Horizon 32.0.6+ or Meridian 2023.1.11+)
* RequisitionNodes (read-only)
* Requisitions (read-write)
* User Defined Links (read-write)

## Getting Started

You can install this library by running:

```
pip3 install pyonms
```

See the [project documentation](https://mmahacek.github.io/PyONMS/) for instructions on using this library.


## Changelog

[Changelog](https://github.com/mmahacek/PyONMS/blob/main/CHANGELOG.md)
