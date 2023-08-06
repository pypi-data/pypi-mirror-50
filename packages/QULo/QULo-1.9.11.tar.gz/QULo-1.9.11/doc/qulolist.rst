****************
The QULo package
****************

This is an old document describing older versions of QULo and particularly ``qulo-list``.


Introduction
============
 
**QULo** stands for **Quality Usage of Loewe-CSC**. It is the first attempt to create a cluster
monitoring solution within the HKHLR/CSC that is

* complete: intended as a framework where all types of metrics can be collected and visualized
* independent of privative thrid party tools: in the past, other solutions to collect data where
  developed, but they relied on expensive licenses (e.g. ``jobmon`` was coupled to the
  ``Bright Cluster Manager``).
  
The package contains:

* ``qagent``: customizable service/daemon that collects performance data from the a node on the
  cluster. It runs locally and collects data from sensors that can be activated and configured via
  a configuration file.
* ``qmaster``: a service/daemon that controls the agents and collects data from them. It runs in a
  master node of the cluster; it is controled via a configuration file.
* ``qulolist``: command line tool that prepares, an optionally delivers by email, brief summaries
  about the performance of the jobs run by users or accounts in a period of time. It simply uses
  Slurm to collect the data.
* ``qulolist-hkhlr``: command line tool that collects data for the HKHLR reports: monthly data and
  details about jobs, depending on the chosen mode. The data comes also from Slurm.
* ``qulolist-plots``: a little program that prepares useful plots from the data collected by
  the ``qulolist-hkhlr`` program.
* ``qulocl``: command line tool expanding the functionality provided by ``qulolist`` (**WIP**)


TODO
====

* Make sure that all sensors work as expected. Review FTs.
* Hosts and ports for communications should be configurable.
* Tests for the integration with Graphite.
* ``qagent`` should have an option to display the available sensors and some help for each sensor.
* Sensors should accept options: the mechanism is almost there, but need to be completed.

  

QULo-list
=========

Description
-----------
   
While we develop a real cluster monitoring solution, we need a quick and dirty
replacement for jobmon. That is **QULo-list**. This application is provided
by the **QULo** package.


Installation
------------
   
1. Create a virtual environment (tested with CPython-3.3 and -3.4)
2. Activate it.
3. Install the QULo package inside that virtual environment. For instance: ::

  $ pip install QULo-1.x.2.tar.gz

4. Run it with ``qulolist``.

On Loewe-CSC, it is installed on master1, under::

  /cm/shared/admintools/QULo

That directory also contains a virtual environment to make QULo working.


Execution
---------

To run ``qulolist``: ::

  $ /cm/shared/admintools/QULo/bin/qulolist

Alternatively, one could activate first the virtual environment and then execute the command without the prefix: ::

  $ source /cm/shared/admintools/QULo/bin/activate
  $ qulolist

The execution of qulolist without arguments, gives an output like: ::

  $ qulolist 

  Summary of 10 Users at Loewe-CSC with highest wasted_CPU in the latest 7 days with:
    [initial time: 2016-10-04T12:42:58]
    [final time:   2016-10-11T12:42:58]

  User            | Wasted CPU [c*h] | Avail CPU [c*h] | #jobs | median(NCPUs) | global eff. CPU | mean(Efficiency CPU)
  =====================================================================================================================
  gauss           |         285528.4 |        355413.8 |    49 |            40 |         0.19663 |              0.39700
  born            |         157696.1 |        157696.1 |     2 |           264 |         0.00000 |              0.00000
  fermi           |         119399.0 |        120017.6 |    19 |            24 |         0.00515 |              0.08809
  feynman         |         114005.4 |        114005.8 |     5 |            45 |         0.00000 |              0.08969
  eckert          |          89675.0 |        329953.2 |    30 |           120 |         0.72822 |              0.60663
  majorana        |          75667.8 |        111691.7 |   168 |            40 |         0.32253 |              0.46200
  planck          |          61579.3 |         61579.3 |     1 |          1584 |         0.00000 |              0.00000
  einstein        |          57718.0 |         59520.4 |    67 |           288 |         0.03028 |              0.30189
  euler           |          43754.8 |         56818.8 |    18 |            24 |         0.22992 |              0.23451
  euclides        |          39593.4 |         91093.8 |     3 |           768 |         0.56536 |              0.31167
  
  all jobs        |        1274130.6 |       2645786.1 |  1737 |            24 |         0.51843 |              0.53721


Of course, some interesting parameters can be given: ::

  $ qulolist -h
  usage: qulolist [-h] [-u USER] [-H HOST] [-P PARTITIONS] [-E] [-n NITEMS]
		  [-c OUTPUT_CATEGORY] [-r RESOURCE_TYPE] [-o OUTPUT_ORDER]
		  [--order-after-second-cut SECOND_SORT_ORDER] [-s SORTED_BY]
		  [--sort-after-cut-by AFTER_CUT_SORT_BY] [-e EMAIL_TO]
		  [-f FILTER] [-t DAYS] [-T SECONDS_SINCE_EPOCH] [-X]
		  [--attach-csv-file-to-email ATTACHED_CSV]
		  [--ram-upper-bound GB] [--ram-lower-bound GB] [-d] [-j]

  A command line tool to show a list with worst/best usage cases in the latest
  given days.

  optional arguments:
    -h, --help            show this help message and exit
    -u USER, --remote-user USER
			  ssh remote user (DEFAULT: root)
    -H HOST, --remote-host HOST
			  ssh remote host (DEFAULT: master1.loewe-csc.hhlr-
			  gu.de)
    -P PARTITIONS, --partitions PARTITIONS
			  comma sep. list of partition names; a special value
			  'all' is allowed, meaning all partitions together
			  (DEFAULT: all)
    -E, --each-partition  Want an individual report for each given partition?
    -n NITEMS, --num-items NITEMS
			  number of items in output (DEFAULT: 10)
    -c OUTPUT_CATEGORY, --category OUTPUT_CATEGORY
			  comma sep. list; possible values: User, Account
			  (DEFAULT: User)
    -r RESOURCE_TYPE, --resource-type RESOURCE_TYPE
			  Type of resource to report about. Possible values are:
			  CPU (DEFAULT: CPU)
    -o OUTPUT_ORDER, --output-order OUTPUT_ORDER
			  possible orders: lowest, highest (DEFAULT: highest)
    --order-after-second-cut SECOND_SORT_ORDER
			  order for optional second sort after cut. Possible
			  orders: lowest, highest (DEFAULT: highest)
    -s SORTED_BY, --sorted-by SORTED_BY
			  possible values: NCPUs, wasted_CPU, available_CPU,
			  global_efficiency_CPU, efficiency_CPU (DEFAULT:
			  wasted_CPU)
    --sort-after-cut-by AFTER_CUT_SORT_BY
			  optional second sort after cut. Possible values:
			  NCPUs, wasted_CPU, available_CPU,
			  global_efficiency_CPU, efficiency_CPU
    -e EMAIL_TO, --send-email-to EMAIL_TO
			  comma sep. list of addresses to send the output to
    -f FILTER, --filter FILTER
			  [Account|User]:comma sep. list. For example: '-f
			  Account:staff,frankfurt' to display only info about
			  accounts 'frankfurt' and 'staff'. This option can be
			  given many times. Values within each filter are or-ed;
			  but different filters are and-ed. For example: with
			  '-f Account:staff -f User:user1,user2' one gets info
			  from jobs run with account 'staff' by either 'user1'
			  or 'user2'.
    -t DAYS, --initial-time DAYS
			  the initial time of the list in days is t_end-DAYS
			  (DEFAULT: 7)
    -T SECONDS_SINCE_EPOCH, --end-time SECONDS_SINCE_EPOCH
			  the end time of the list in seconds since the Epoch
			  (DEFAULT: NOW [=1518605534.81])
    -X, --supress-stdout  supress standard output
    --attach-csv-file-to-email ATTACHED_CSV
			  file name's prefix of output csv file to be attached
			  by email
    --ram-upper-bound GB  only jobs with ram/core <= GB are considered
			  (DISABLED)
    --ram-lower-bound GB  only jobs with ram/core >= GB are considered
			  (DISABLED)
    -d, --dump-performance-data
			  Simply dump the performance data, before any anlysis,
			  and exit
    -j, --discard-subtasks-data
			  Want to produce data related only to slurm jobs, and
			  not to any sub-task?




Cron
----
   
On Loewe-CSC there is a cron task running on master1: ::

  /etc/cron.d/qulolist
  
it runs the tool at the beginning of every week and sends reports to the CSC staff.


TODO
----
   
* Cross-check (by Anja?): Warning! Contrary to my principles, qulolist has not been systematically tested... take it as a spike (in a very broad sense).
* Keep working to develop a more complete and flexible solution.

  * particularly to collect data about GPU activity

* Add other resources (like RAM or network traffic).
  
