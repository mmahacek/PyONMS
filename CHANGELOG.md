# Changelog


## [0.1.3] 2024-02-26

### What's Changed

* Revert nodes get functions to default components to `NodeComponents.NONE` instead of `ALL`.
* Added `Enlkind` endpoint and models.
* Update local testing/linting configuration.
* Add testing for `utils` methods.
* Add `mypy` for type checking during development.
* Add `pyonms.utils.check_ip_address()` to validate IP addresses.
* Fix type hint for `models.Info`'s `version` and `datetimeformatConfig` attributes.
* Rename all `_to_dict()` methods to `to_dict()`.  Added stub method reference to keep backward compatibility.

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.1.2...v0.1.3

## [0.1.2] 2023-12-21

### Breaking Change

* Updated `ApiPayloadError` exception to trigger when API returns HTTP 400+.

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.1.1...v0.1.2

## [0.1.1] 2023-12-21

### Breaking Change

* Add `ApiPayloadError` exception when API returns HTTP 500-599. Previously many error responses were steamrolled over.

### What's Changed

* Renamed internal `uri` parameters to be `url`.
* Deprecate `MethodNotImplemented` exception.  Replaced with base `NotImplementedError`.
* Docstring updates to satisfy pylint.
* Prevent `Event.id` from being sent as part of the event payload when posting to the `events` endpoint.
* Update `get_foreign_sources()` and `get_requisitions()` to no longer use custom `_get()` method.
* `Endpoint._put()` method now returns the `Requests.Response` object instead of null.
* Tweaks to testing framework settings.
* Added `NodeComponents.NONE` option.
* Fix type hint on `Endpoint_post.data` attribute.
* Add Node/IP/Service metadata modification to the `Nodes` endpoint.

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.0.13...v0.1.1


## [0.0.13] 2023-12-1

### What's Changed

* Fixed `foreign_source` model for processing `parameter`s.
* Updated `dao` and `model` module bases to allow importing within from the `pyonms` module
* Remove deprecated cloud portal module
* Remove deprecated Antora documentation

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.0.12...v0.0.13

## [0.0.12] 2023-11-30

### What's Changed

* Added IP Interface endpoint

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.0.11...v0.0.12

## [0.0.11] 2023-11-29

### What's Changed

* Add lastAutomationTime and firstAutomationTime parameters to the Alarm model
* Apply pylint suggestions
* Add option to set a timeout for REST calls
* Slightly improve error handling on some REST calls

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.0.10...v0.0.11

## [0.0.10] 2023-09-11

### Potentially Breaking Change
* If a GET call returns an error 500, previously we suppressed the error and returned a `None` value. Now we will raise an `InvalidValueError` exception and print out the error message.

### What's Changed
* Added User Defined Link endpoint
* Requisition endpoint updates
  * Added category add/remove methods
  * Ability to merge existing and new node if adding interfaces
  * Added method to send just one node to a requisition via REST
* Event model rework - converted parameters from list to dict
* Update `reload_daemon` method to use new event model
* Add FIQL support to alarms, events, and nodes
  * For `get_alarms`, `get_events`, and `get_nodes` methods, you can add a `fiql` parameter to specify a valid search.
* Option to ignore SSL certs

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.0.9...v0.0.10

## [0.0.9] 2023-08-02

### What's Changed

* Fix event object to_dict() method
* Add OnmsMonitoredService status enum values
* Add list of running daemons to Info object
* Update alarm object to handle situation fields
* Check for valid daemon name in reload_daemon()
* Add support for creating/updating/deleting User Defined Links
* Fix handling for non-JSON responses
* Import/type hint/doc updates

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.0.8...v0.0.9

## [0.0.8] 2023-04-11

* Requisition endpoint - add `set_asset` method
* Change from a Process Pool to Thread Pool
* Update docstrings, type hinting, and packaging settings

**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.0.6...v0.0.8

## [0.0.7]

Version skipped due to packaging issues.

## [0.0.6] 2023-02-23

### What's Changed

Added:
* Health and Info endpoints.  When creating a new `PyONMS` instance, these endpoints will be called to gather info and populate the `info` and `health_status` attributes.
* Improvements to the Requisitions and Foreign Source endpoints.
  * Methods to add/remove Foreign Source detectors and policies
  * Method to add metadata to Requisition objects
* Cleanup of import references


**Full Changelog**: https://github.com/mmahacek/PyONMS/compare/v0.0.5...v0.0.6

## [0.0.5] 2022-12-19

First GitHub release
