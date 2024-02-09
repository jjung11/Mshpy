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
