Usage
-----------------------------------------

Main function is Mshpy.msh_param, which provides magnetosheath parameters along certain spacecraft orbit.

Args:
    1. path: File directory to save outputs.
    2. Start time: in the format of '2012-03-01T02:00'
    3. End time: in the same format
    4. Spacecraft name. It should be same as one used in SscWs. See https://sscweb.gsfc.nasa.gov/WebServices/REST/jupyter/SscWsExample.html.
    5. mpoff: Optional; Manual magnetopause offset along x axis.
        Magnetopause model for the MHD-based MSH model is Shue et al. 1998.
    6. bsoff: Optional; Manual bow shock offset along x axis
        Bow shock model for the MHD-based MSH model is Jelinek et al. 2012

Returns:
    Following files are saved in the 'path'.
1. Msh_MHD_out.txt: MHD-based model result.
        
    Format:
::    

        time   Bx[nT]  By  Bz  n[cm^-3]    T[eV]   Vx[km/s]    Vy  Vz  f   x[Re]   y   z
         
2. Msh_Soucek_out.txt: Soucek & Escoubet [2012] model plasma velocity results.
        
        Format:
::

        time    x[Re]   y   z   f   Vx[km/s]    Vy  Vz
        
3. Msh_Romashets_out.txt: Romashets et al. [2019] model magnetic field results.
        
        Format:
::

        time    Bx[nT]  By  Bz  |B|
        
4. Msh_Spreiter_out.txt: Spreiter et al. [1966] model plasma speed, density, and temperature results.

        Format:
::

        time    f   n[cm^-3]    n[cm^-3]    T[eV]   |V|[km/s]

Custom trace usage
-----------------------------------------

``Mshpy.msh_param_custom`` runs the MHD-based model on an arbitrary trace
under a fixed or externally-supplied solar wind condition, rather than a
real spacecraft orbit with a live OMNI/SSCWeb fetch. Useful for sampling
along a synthetic ray -- e.g. a line of sight -- rather than an actual orbit.

Args:
    1. xyz: (N,3) array of GSE positions (Earth radii), e.g. points sampled
        along a line of sight. A file path in the virtual sc trace format
        (see 'Datasets') also works, exactly as with ``msh_param``.
    2. sw: dict of scalar solar wind/IMF conditions -- keys
        ``Bx, By, Bz, Vx, Vy, Vz, n, Pd, Ma, Mm`` (nT, nT, nT, km/s, km/s,
        km/s, cm\ :sup:`-3`, nPa, unitless, unitless), applied as a constant
        condition across the whole trace. A file path in the OMNIweb
        whitespace format (see above) also works.
    3. mpoff: Optional; manual magnetopause offset along x axis.
    4. bsoff: Optional; manual bow shock offset along x axis.
    5. model: Bow shock model, ``'jel'`` (Jelinek et al. 2012) by default.
    6. out_dir: Optional; if given, also writes Msh_MHD_out.txt there, like
        ``msh_param`` does. Default ``None`` -- in-memory only, no files
        written.

Returns:
    A pandas DataFrame (not written to disk unless ``out_dir`` is given).

    Format:
::

        time   Bx[nT]  By  Bz  n[cm^-3]  Tev[eV]  Vx[km/s]  Vy  Vz  f  x[Re]  y  z  mpd  bsd

``f`` is the fractional distance between the magnetopause and bow shock
along that point's direction (0 at the MP, 1 at the BS); it is ``NaN``
within 10% of either boundary, per the model's own reliability cut.
``mpd``/``bsd`` are the magnetopause/bow shock distances (Earth radii)
along that point's direction.
