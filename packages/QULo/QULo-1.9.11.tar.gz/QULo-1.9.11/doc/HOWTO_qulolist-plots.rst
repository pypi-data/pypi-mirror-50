=======================================
How to create plots from qulolist-plots
=======================================

--------------------
Job status bar plots
--------------------

^^^^^^^^^^^^^^^^
Getting the data
^^^^^^^^^^^^^^^^

There are two possibilities:
1. Data about jobs and job steps.
   In this case JobID, JobID.batch, JobID.0, JobID.1, ..., are all considered. This is
   important to keep in mind because if the slurm job associated with JobID has a "State"
   of "TIMEOUT", other active sub-tasks will have a "State" of "CANCELLED". In other words,
   when the steps are considered, "CANCELLED" might by related to a "TIMEOUT"... or maybe not.
   ``qulolist-hkhlr month`` returns this type of data by default.
   ::
      qulolist-hkhlr month -t
2. Data only about jobs.
   In this case, only genuine slurm jobs are considered, i.e. tasks which JobID's are numbers.
   This is what you want to get if the 

1. Get the data. If 
