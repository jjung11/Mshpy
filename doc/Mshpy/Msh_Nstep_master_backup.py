import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv
from Msh_Nstep_test_n import main as mhd
from Msh_Nstep_Soucek import main as Soucek
from Msh_Nstep_Romashets import main as Romashets
from Msh_Nstep_Spreiter_test import main as Spreiter

def main(run, sc,mpdo=0,bsdo=0):
    """PURPOSE: Generate models result for given SW/IMF conditions & virtual spacecraft trace

    CALL: python Msh_Nstep_master.py run_name sc_name mpoff bsoff

    ARGUMENTS:
    1. SW/IMF conditions file
    text format: (without header)
    Year DOY HR MN Bx By Bz Vx Vy Vz n Pd Ma Mm, as in OMNIweb
    time is for the matching with sc trace.
    One line data can be used for constant SW cond.

    2. sc trace file
    text format: (without header)
    yy/mm/dd yy/mm/dd x y z, as in SSCWeb (x,y,z in GSE)

    3. (Optional) magnetopause offset
    Manual magnetopause offset along x axis
    Magnetopause model for the MHD-based MSH model is Shue et al. 1998.

    4. (Optional) bow shock offset
    Manual bow shock offset along x axis
    Bow shock model for the MHD-based MSH model is Jerab et al. 2005.


    """

    f_sw='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/'+run+'/omni.lst'
    #SW/IMF conditions file
    xyz='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/'+run+'/'+sc+'_orbit.txt'
    #sc trace file
    fout='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/'+run+'/Msh_test_out.txt'
    #MHD-based model output file
    fout_v='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/'+run+'/Msh_Soucek_out.txt'
    #Soucek model velocity output file
    fout_b='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/'+run+'/Msh_Romashets_out.txt'
    #Romashets model magnetic field output file
    fout_n='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/'+run+'/Msh_Spreiter_out.txt'
    #Spreiter plasma density & temperature output file
    foff='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/'+run+'/Msh_offset.txt'

    mhd(xyz,f_sw,fout,mpdo,bsdo,foff)
    print('MHD-based model result calculated\n')
    #Spreiter(xyz,f_sw,fout_n,mpdo,bsdo)
    print('Spreiter model n,T result calculated\n')
    #Soucek(xyz,f_sw,fout_v,mpdo,bsdo)
    print('Soucek & Escoubet 2012 velocity model result calculated\n')
    #Romashets(xyz,f_sw,fout_b,mpdo,bsdo)
    print('Romashets & Vandas 2019 magnetic field result calculated\n')
    return

if __name__=='__main__':
    main(*argv[1:])
