"""A simplified magnetosheath model"""

__version__='1.0.0'
import os
import tempfile
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

_SW_FIELDS = ('Bx', 'By', 'Bz', 'Vx', 'Vy', 'Vz', 'n', 'Pd', 'Ma', 'Mm')


def _sw_dict_to_omni_file(sw, path):
    """Write a single-line, constant-SW file in the whitespace format
    Msh_Nstep_test_n.OMNIread2 parses: YR DOY HR MN Bx By Bz Vx Vy Vz n Pd Ma Mm.
    The YR/DOY/HR/MN columns are placeholders -- the MHD model broadcasts a
    single-row file to every trace point, so they don't affect the physics."""
    missing = [k for k in _SW_FIELDS if k not in sw]
    if missing:
        raise ValueError(f"sw dict missing required fields: {missing}")
    with open(path, 'w') as f:
        f.write('2000 1 0 0 ' + ' '.join(str(sw[k]) for k in _SW_FIELDS) + '\n')
    return path

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

def msh_param_custom(xyz, sw, mpoff=0, bsoff=0, model='jel', out_dir=None):
    """Run the MHD-based magnetosheath model on an arbitrary trace, rather
    than a real spacecraft orbit + live OMNI fetch (see msh_param for that).

    Useful for e.g. sampling along a synthetic ray (a line of sight, a grid
    cut) under a fixed or externally-supplied solar wind condition.

    Args:
        xyz: (N,3) ndarray of GSE positions [R_E] -- e.g. points marched
            along a line of sight. A file path in the orbit.txt format
            (see sscweb.py) also works, exactly as in msh_param.
        sw: dict of scalar solar wind/IMF conditions -- keys
            'Bx','By','Bz','Vx','Vy','Vz','n','Pd','Ma','Mm' (nT, nT, nT,
            km/s, km/s, km/s, cm^-3, nPa, unitless, unitless), applied as a
            constant condition across the whole trace. A file path in the
            OMNIweb whitespace format (see omni.py) also works.
        mpoff: Optional; manual magnetopause offset along x axis.
        bsoff: Optional; manual bow shock offset along x axis.
        model: Bow shock model, 'jel' (Jelinek et al. 2012) by default.
        out_dir: If given, also writes Msh_MHD_out.txt there, like
            msh_param does. Default None -- in-memory only.

    Returns:
        DataFrame with columns time, Bx, By, Bz, n, Tev, Vx, Vy, Vz, f,
        x, y, z, mpd, bsd (f is the fractional distance between the
        magnetopause and bow shock along that point's direction: 0 at the
        MP, 1 at the BS; NaN within 10% of either boundary, per the
        model's own reliability cut).
    """
    sw_path = sw if isinstance(sw, str) else None
    fout = os.path.join(out_dir, 'Msh_MHD_out.txt') if out_dir else None

    with tempfile.TemporaryDirectory() as tmp:
        if sw_path is None:
            sw_path = _sw_dict_to_omni_file(sw, os.path.join(tmp, 'sw.lst'))
        if fout is None:
            fout = os.path.join(tmp, 'Msh_MHD_out.txt')
        mhd(xyz, sw_path, fout, mpoff, bsoff, model=model)
        return pd.read_csv(fout)


if __name__=='__main__':
    msh_param(*argv[1:])
