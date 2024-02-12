Examples
============

In Python, run:

::


  from Mshpy import msh_param


Then you can run msh_param as explained in the 'Usage'.

::


  msh_param('test','2012-03-01T02:00','2012-03-01T04:00','cluster4',mpoff=0,bsoff=0.08)

* path: File directory for output file.
   In case of using custom s/c trace file, see 'Usage' for the detail for the formats of each variable, .

Note that model magnetopause and bow shock positions may not accurately represent the actual magnetopause and bow shock positions manual offset parameter may be needed after reviewing the satellite crossing data.

You can plot the result by following:

::

  from Mshpy import Msh_sc_data
  Msh_sc_data.main(['test','2012-03-01T02:00','2012-03-01T04:00','cluster4'])


