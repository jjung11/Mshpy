Examples
========

Basic 1D Usage
--------------

In Python, run:

::

  from Mshpy import msh_param

Then you can run `msh_param` as follows:

::

  msh_param('test', '2012-03-01T02:00', '2012-03-01T04:00', 'cluster4', mpoff=0, bsoff=0.08)

- `path`: Output directory for the result file.  
  If you are using a custom spacecraft trace file, refer to the 'Usage' section for detailed format requirements.

Note: The model magnetopause and bow shock positions may not perfectly match actual boundaries. Manual offset (`mpoff`, `bsoff`) may be needed based on satellite boundary crossing data.

To plot the result:

::

  from Mshpy import Msh_sc_data
  Msh_sc_data.main(['test', '2012-03-01T02:00', '2012-03-01T04:00', 'cluster4'])


3D Output Example
-----------------

To generate 3D output:

::

  from Mshpy import Msh_Nstep_3D
  Msh_Nstep_3D.main(x, y, z, f_sw, fout)

- `x`, `y`, `z`: 1D arrays (e.g., from `numpy.linspace`) defining the 3D spatial grid in GSE coordinates (Re).
- `f_sw`: Input solar wind data file in the following format (one line per time step):

::

  Year DOY HR MN Bx By Bz Vx Vy Vz n Pd Ma Mm

This format follows OMNIweb, for example:

::

  1967 1 0 00 2 -2 -5 -400 0 0 10 2 10 6

- `fout`: Output netCDF file name to store the computed plasma and magnetic field quantities on the 3D grid.

This will create a netCDF file containing variables like `Bx`, `By`, `Bz`, `n`, `T`, `Vx`, `Vy`, `Vz`, along with coordinate axes `x`, `y`, `z`.

