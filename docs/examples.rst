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


Custom Trace Example
--------------------

To sample the model along a synthetic trace -- e.g. a line of sight,
rather than a real spacecraft orbit -- under a fixed solar wind condition:

::

  import numpy as np
  from Mshpy import msh_param_custom

  # points marched outward from some starting position, in GSE Re
  xyz = np.array([[8, 2, 1], [9, 2, 1], [10, 2, 1], [11, 2, 1], [12, 2, 1]])

  sw = {
      'Bx': -1.57, 'By': 1.14, 'Bz': 1.57,
      'Vx': -585.4, 'Vy': 22.0, 'Vz': 67.8,
      'n': 3.26, 'Pd': 2.28, 'Ma': 9.81, 'Mm': 6.26,
  }

  df = msh_param_custom(xyz, sw)

`df` is a pandas DataFrame with the same columns as `Msh_MHD_out.txt` (see
'Usage'), returned in memory -- no files are written unless you pass
`out_dir='test'`, in which case it also writes `Msh_MHD_out.txt` there,
same as `msh_param`.

Both `xyz` and `sw` also accept a file path instead (the virtual sc trace
format and OMNIweb format respectively, both described in 'Usage'), so you
can mix a real trace file with a fixed SW condition, or vice versa.


3D Output Example
-----------------

To generate 3D output:

::

  from Mshpy import Msh_Nstep_3D
  Msh_Nstep_3D.main(x, y, z, f_sw, fout)

- `x`, `y`, `z`: 1D arrays (e.g., from `numpy.linspace`) defining the 3D spatial grid in GSE coordinates (Re).
- `f_sw`: Input solar wind data file in the following format :

::

  Bx By Bz Vx Vy Vz n Pd Ma Mm


Each column represents:

- **Bx**, **By**, **Bz**: Interplanetary magnetic field components (nT, in GSE)  
- **Vx**, **Vy**, **Vz**: Solar wind velocity components (km/s, in GSE)  
- **n**: Proton number density (cm⁻³)  
- **Pd**: Dynamic pressure (nPa)  
- **Ma**: Alfvén Mach number  
- **Mm**: Magnetosonic Mach number


This format follows OMNIweb, for example:

::

  2 -2 -5 -400 0 0 10 2 10 6

- `fout`: Output netCDF file name to store the computed plasma and magnetic field quantities on the 3D grid.

This will create a netCDF file containing variables like `Bx`, `By`, `Bz`, `n`, `T`, `Vx`, `Vy`, `Vz`, along with coordinate axes `x`, `y`, `z`.

