#################
Development notes
#################

The notes in the current document do not necessarily apply to the code inside
``qulolist`` and related material.


**************
Some decisions
**************

Structure of code
=================

* ``qulod.py``, ``qagent.py`` and ``qmaster.py`` contain code to trivially create executables
  via their main functions.


Functional Tests
================

In general, it is expected that ``qmaster`` and ``qagent`` (and other executables in the package)
run with privileges. Therefore to isolate and limit the impact of the functional tests on the
host, it was decided to run the daemons for FTing inside containers.

This behaviour can be controlled with an environment varaible called ``QULO_FT_ENVIRONMENT``.

* Setting ``QULO_FT_ENVIRONMENT=docker`` (default) makes the FTs run the programs under
  test inside docker containers.
* With ``QULO_FT_ENVIRONMENT=host`` the FTs run directly in the host.
  

****************
Daemon processes
****************

* typically accept command line options for
  * configuration file
  * logging file/directory
  * pidfile (?)
* general logging messages to a specific log file (like ``/var/log/qulod.log``); errors
  go to syslog (``/var/log/syslog``) -- done anyway by the Linux logging system
* Catch SIGHUP to allow re-reading of configuration
  

**************************
File locking and PID files
**************************

Ref. [Rago2013]_, pag. 473 (see also p. 494 for a definition of the ``lockfile`` function)
explains how to create a locked PID file.

Probably better explained can be found in ref. [Kerrisk2010]_, page 1142. The code for
``lockRegion`` can be found on page 1134.

In Python, one can use ``os.lockf``. See the docs. The meaning of the possible values for
``cmd`` can be seen with ``man 3 lockf``. Also the other parameters are explained, of course.


**********************
AsyncIO and unit tests
**********************

A simple approach is described by Miguel Grinberg in his blog:
https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code
I implemented my own version of his _run and AsyncMock in ``test/unit/qulo/aio_tools.py``.


************
Bibliography
************

[Rago2013] R. Stevens, S. Rago "Advanced Programming in the UNIX Environment", 3rd ed.
  Addison Wesley, 2013

[Kerrisk2010] M. Kerrisk, "The Linux Programming Interface", No Starch Press Press, 2010
