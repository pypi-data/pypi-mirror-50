Mdclogpy
========

Structured logging library with Mapped Diagnostic Context

* Outputs the log entries to standard out in structured format, json currently.
* Severity based filtering.
* Supports Mapped Diagnostic Context (MDC).
  Set MDC pairs are automatically added to log entries by the library.


Log entry format
----------------

Each log entry written with mdclog_write() function contains

* Timestamp
* Logger identity
* Log entry severity
* All existing MDC pairs
* Log message text

Currently the library only supports JSON formatted output written to standard
out of the process.

*Example log output*

`{"ts": 1559285893047, "crit": "INFO", "id": "myprog", "mdc": {"second key":"other value","mykey":"keyval"}, "msg": "Hello world!"}`

Install
-------

Install from PyPi

```
python3 -m pip install mdclogpy
```

Install using the source

```
python3 setup.py install
```

Usage
-----

The library can be used in two ways shown below.

1) Use the root logger

```python
  import mdclogpy
  mdclogpy.error("This is an error log")
```

2) Create a logger instance

```python
  from mdclogpy import Logger
  my_logger = Logger()
  my_logger.error("This is an error log")
```

A program can create several logger instances.


Mapped Diagnostics Context
--------------------------

The MDCs are logger instance specific key-value pairs, which are included to
all log entries written via the logger instance.

By default, the library implements a root logger instance.
MDCs added to the root logger instance are added only to the log entries
written via the root logger instance.


License
-------

Copyright (c) 2019 AT&T Intellectual Property.
Copyright (c) 2018-2019 Nokia.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Unit testing
------------

To run the unit tests run the following command in the package directory::
`
python3 -m unittest discover
`
