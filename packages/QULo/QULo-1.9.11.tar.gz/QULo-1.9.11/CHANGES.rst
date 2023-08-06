v. 1.10
-------

* Some bugs fixed:

  * When no battery is available, the SensorsBattery does not crashes,
    but returns None

* Added optional section ``qmaster`` to ``qagent.conf`` and ``qmaster.conf``
  with two possible keys (both optional):

  * ``host``
  * ``incoming data port``

* Added optional section ``Graphite`` to ``qmaster.conf`` with two possible
  keys (both optional):

  * ``host``
  * ``carbon receiver pickle port``

* Included example docker compose yml file to start graphite/qmaster/qagent [TODO]
* Exit code of qulod, qmaster and qagent is != 0 in case of errors with the PID file
* Improved behaviour of "stop" command
* Added optional section ``logging`` in qmaster, qagent and qulod, to customize what
  I call "own logging", logging that goes to a dedicated file. The possible options
  have all defaults defined in ``qulo.constants``:

  * ``filename`` (default: DEFAULT_OWN_FILE_LOGGING_PATH)
  * ``maxBytes``: max size of the log file before rollover; set it to ``0`` to disable
    the rollover mechanism and allow the file to grow indefinitely
    (default: DEAFULT_OWN_FILE_MAXBYTES)
  * ``backupCount`` (default: DEFAULT_OWN_FILE_BACKUP_COUNT)
  * ``level`` (default: DEFAULT_OWN_FILE_LOGGER_LEVEL)


  
v. 1.9
------

* ``QMaster`` can send messages to ``Graphite``
* Several bugs fixed
  

v. 1.8
------

* Starting work to integrate ``QMaster`` with ``Graphite``.
* Several bugs fixed


v. 1.7
------

* ``QMaster`` operational
* ``QAgent`` can communicate with ``QMaster``: it can send data from the sensors


v. 1.6
------

* ``QAgent`` operational (without communications)
* a few sensors available for ``qagent`` (see ``qulo/sensors.py``)

