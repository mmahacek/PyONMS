# Changelog

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