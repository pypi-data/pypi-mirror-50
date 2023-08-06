****************
The QULo package
****************

Introduction
============

**QULo** is a simple cluster monitoring tool. It is developed in Python.

The package contains:

* ``qagent``: customizable service/daemon that collects performance data from the a node on the
  cluster. It runs locally and collects data from sensors that can be activated and configured via
  a configuration file.
* ``qmaster``: a service/daemon that controls the agents and collects data from them. It runs in a
  master node of the cluster; it is controled via a configuration file.


  
Installation
============
   
Just install the QULo package from PyPI:
::

  $ pip install QULo


  
Usage
=====

1. Start ``qmaster``
   ::

      # qmaster start

   By default the configuration file is ``/etc/qulo/qmaster.conf``, but can be changed from the
   command line. A typical configuration might be:
   ::

      [qmaster]
      host = localhost
      incoming data port = 7888
      
      [Graphite]
      host = localhost
      carbon receiver pickle port = 2004
      
      [logging]
      filename = /tmp/qmaster.log
      maxBytes = 1073741824
      backupCount = 10
      level = DEBUG

   No option is mandatory. In the file ``qulo/constants.py`` the defaults are defined.
2. Start ``qagent``
   ::

      # qagent start

   By default the configuration file is ``/etc/qulo/qagent.conf``, but can be changed from the
   command line. In this configuration file is where a *sensor* is activated. A typical
   configuration with all sensors active is:
   ::
      
      [qmaster]
      host = localhost
      incoming data port = 7888
      
      [logging]
      filename = /tmp/qagent.log
      maxBytes = 1073741824
      backupCount = 10
      level = DEBUG

      [sensor:CPUPercent]
      time_interval = 10
      
      [sensor:VirtualMemory]
      time_interval = 30
      
      [sensor:CPUTimes]
      time_interval = 30
      
      [sensor:CPUTimesPercent]
      time_interval = 10
      
      [sensor:CPUCount]
      time_interval = 300
      
      [sensor:CPUStats]
      time_interval = 30
      
      [sensor:CPUFreq]
      time_interval = 300
      
      [sensor:SwapMemory]
      time_interval = 60
      
      [sensor:DiskPartitions]
      time_interval = 60
      
      [sensor:DiskUsage]
      time_interval = 30
      #path = /
      
      [sensor:DiskIOCounters]
      time_interval = 20
      
      [sensor:NetIOCounters]
      time_interval = 10
      
      [sensor:NetConnections]
      time_interval = 20
      
      [sensor:NetIFAddrs]
      time_interval = 30
      
      [sensor:NetIFStats]
      time_interval = 30
      
      [sensor:SensorsTemperatures]
      time_interval = 30
      
      [sensor:SensorsFans]
      time_interval = 30
      
      [sensor:SensorsBattery]
      time_interval = 30
      
      [sensor:BootTime]
      time_interval = 300
      
      [sensor:Users]
      time_interval = 10

   Again, no option is mandatory. But if ``qagent`` must measure anything, some sensor must
   be explicitly given. In the file ``qulo/constants.py`` the defaults are defined.
   The *time* given in the ``time_interval`` option is understood to be in *seconds*.
      
3. Start Graphite and inspect the dashboard to see the data.

   

TODO
====

* ``qagent`` should have an option to display the available sensors and some help for each sensor.
* Sensors should accept options: the mechanism is almost there, but need to be completed.
* Add sensors to read data from GPUs.
* Connect to Slurm.  

