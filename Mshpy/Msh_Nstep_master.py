"""A simplified magnetosheath model"""

__version__='1.0.0'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv
from .Msh_Nstep_test_n import main as mhd
from .Msh_Nstep_Soucek import main as Soucek
from .Msh_Nstep_Romashets import main as Romashets
from .Msh_Nstep_Spreiter_test import main as Spreiter
from .omni import main as omni
from .sscweb import main as sscweb
from .sc_data import main as sc_data

def msh_param(path,ts,te,sc,mpoff=0,bsoff=0):
    """Generate models result for given SW/IMF conditions & virtual spacecraft trace

    MHD-based model data files (*.npy) should be in /modeling/cn and /modeling/cs directory.

    Args:
        path: File directory. 
        ts: start time, in the format: '%Y-%m-%dT%H:%M'
        te: end time
        sc: spacecraft name for downloading orbit and observed data. See sc_data.py.
        mpoff: Optional; Manual magnetopause offset along x axis.
            Magnetopause model for the MHD-based MSH model is Shue et al. 1998.
        bsoff: Optional; Manual bow shock offset along x axis
            Bow shock model for the MHD-based MSH model is Jelinek et al. 2012.

    Returns:
        Following files are saved in the path.
            1. Msh_MHD_out.txt: MHD-based model result.
            2. Msh_Soucek_out.txt: Soucek & Escoubet [2012] model plasma velocity results.
            3. Msh_Romashtes_out.txt: Romashets et al. [2019] model magnetic field results.
            4. Msh_Spreiter_out.txt: Spreiter et al. [1966] model plasma speed, density, and temperature results.
    """

    omni(path,ts,te)
    f_sw=path+'/omni.lst'
    #SW/IMF conditions file
    sscweb(path,ts,te,sc)
    f_xyz=path+'/orbit.txt'
    #sc trace file
    fout=path+'/Msh_MHD_out.txt'
    #MHD-based model output file
    fout_v=path+'/Msh_Soucek_out.txt'
    #Soucek model velocity output file
    fout_b=path+'/Msh_Romashets_out.txt'
    #Romashets model magnetic field output file
    fout_n=path+'/Msh_Spreiter_out.txt'
    #Spreiter plasma density & temperature output file
    foff=path+'/Msh_offset.txt'

    mhd(f_xyz,f_sw,fout,mpoff,bsoff,foff,'jel')
    print('MHD-based model result calculated\n')
    Spreiter(f_xyz,f_sw,fout_n,mpoff,bsoff,'jel')
    print('Spreiter model n,T result calculated\n')
    Soucek(f_xyz,f_sw,fout_v,mpoff,bsoff,'jel')
    print('Soucek & Escoubet 2012 velocity model result calculated\n')
    Romashets(f_xyz,f_sw,fout_b,mpoff,bsoff,'jel')
    print('Romashets & Vandas 2019 magnetic field result calculated\n')
    return

if __name__=='__main__':
    msh_param(*argv[1:])
