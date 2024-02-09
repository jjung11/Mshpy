# Written by Jaewoon Jung, on 07/13/2022.
# Some of the code used are based on the code written by Hyunju K. Connor.
# I got help from Jan S. Soucek for implementing his velocity code.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv
from os.path import exists
from Msh_Nstep_test_n import main as mhd
from Msh_Nstep_Soucek import main as Soucek
from Msh_Nstep_Romashets import main as Romashets
from Msh_Nstep_Spreiter_test import main as Spreiter

def main(path):
    """Generate models result for given SW/IMF conditions & virtual spacecraft trace

    MHD-based model data files (*.npy) should be in /modeling/cn and /modeling/cs directory.

    Args:
        path: File directory. The directory should includes
            1. SW/IMF conditions file
            text format: (without header)
            Year DOY HR MN Bx By Bz Vx Vy Vz n Pd Ma Mm, as in OMNIweb
            Bx,By,Bz in GSE
            time is for the matching with sc trace.
            One line data can be used for constant SW cond.
            SW file should be named omni.lst

            2. sc trace file
            text format: (without header)
            yy/mm/dd yy/mm/dd x y z, as in SSCWeb (x,y,z in GSE)
            sc trace file should be named orbit.txt

            3. MP/BS offset file (Optional)
            File containing following information
            text format:
            mpoff bsoff
            mpoff: Manual magnetopause offset along x axis.
                Magnetopause model for the MHD-based MSH model is Shue et al. 1998,
                except for the Romashets et al. [2019] model which uses Jellinek et al. 2012 model.
            bsoff: Manual bow shock offset along x axis
                Bow shock model for the MHD-based MSH model is Jelinek et al. 2012.


    Returns:
        Following files are saved in the path.
            1. Msh_MHD_out.txt: MHD-based model result
            2. Msh_Soucek_out.txt: Soucek & Escoubet [2012] model plasma velocity results.
            3. Msh_Romashtes_out.txt: Romashets et al. [2019] model magnetic field results.
            4. Msh_Spreiter_out.txt: Spreiter et al. [1966] model plasma speed, density, and temperature results.
    """

    f_sw=path+'/omni.lst'
    #SW/IMF conditions file
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
    if exists(path+'/Msh_offset.txt'):
        foff=path+'/Msh_offset.txt'
    else:
        foff=0

    mhd(f_xyz,f_sw,fout,foff,'jel')
    print('MHD-based model result calculated\n')
    Spreiter(f_xyz,f_sw,fout_n,foff,'jel')
    print('Spreiter model n,T result calculated\n')
    Soucek(f_xyz,f_sw,fout_v,foff,'jel')
    print('Soucek & Escoubet 2012 velocity model result calculated\n')
    Romashets(f_xyz,f_sw,fout_b,foff,'jel')
    print('Romashets & Vandas 2019 magnetic field result calculated\n')
    return

if __name__=='__main__':
    main(*argv[1:])
