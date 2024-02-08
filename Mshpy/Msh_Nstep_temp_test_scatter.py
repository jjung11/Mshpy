import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle as pl
import io
from sys import argv
from read_mhd                import *
from pkg_mhdplot             import mhd_vpkg
from openggcm_info           import runinfo,mhdtime,mhdt2tstr
from matplotlib.colors       import LogNorm
from matplotlib.ticker       import MultipleLocator, FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

if argv[1]=='cs':
    run='Msh_Nstep_cs'
    external='Elements'
else:
    run='Msh_Nstep'
    external='easystore'

x=np.linspace(0,20)

for i in range(1,7):
    a=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_data_0.1.'+str(1200+1200*i).zfill(6),header=None,sep='\s+',names=['the','phi','m','rad','x','y','z','bx1','by1','bz1','vx1','vy1','vz1','rr1','pp1','ex1','ey1','ez1','xjx1','xjy1','xjz1','resis1']).drop_duplicates()
    a2=a[a.the==0]

    b=pd.read_csv('/Volumes/Elements/openggcm_run/'+run+'_003/modeling/Msh_data_0.1.'+str(1200+1200*i).zfill(6),header=None,sep='\s+',names=['the','phi','m','rad','x','y','z','bx1','by1','bz1','vx1','vy1','vz1','rr1','pp1','ex1','ey1','ez1','xjx1','xjy1','xjz1','resis1']).drop_duplicates()
    b2=b[b.the==0]

    for phi in np.arange(-90+7.5,90,7.5):
        y=x*np.tan(phi*np.pi/180)


        a_list,b_list=[],[]
        for j in range(1,10):
            a_t=a2[(a2.phi<phi+7.5) & (a2.phi>phi-7.5)]
            a_t2=a_t[(a_t.m>j-.1) & (a_t.m<j+.1)]
            a_t3=a_t2.mean().to_frame().T
            a_t3.phi=phi
            a_t3['f']=j/10
            a_list.append(a_t3)
            b_t=b2[(b2.phi<phi+7.5) & (b2.phi>phi-7.5)]
            b_t2=b_t[(b_t.m>j-.1) & (b_t.m<j+.1)]
            b_t3=b_t2.mean().to_frame().T
            b_t3.phi=phi
            b_t3['f']=j/10
            b_list.append(b_t3)

        a3=pd.concat(a_list,axis=0).set_index('f')
        a3['B']=np.sqrt(a3.bx1**2+a3.by1**2+a3.bz1**2)
        a3['Ti']=72429.0*a3.pp1/a3.rr1/11600.
        a3['V']=np.sqrt(a3.vx1**2+a3.vy1**2+a3.vz1**2)
        a3['ni']=a3.rr1
        a6=a3[['B','ni','Ti','V']]

        b3=pd.concat(b_list,axis=0).set_index('f')
        b3['B4']=np.sqrt(b3.bx1**2+b3.by1**2+b3.bz1**2)
        b3['Ti4']=72429.0*b3.pp1/b3.rr1/11600.
        b3['V4']=np.sqrt(b3.vx1**2+b3.vy1**2+b3.vz1**2)
        b3['ni4']=b3.rr1
        b6=b3[['B4','ni4','Ti4','V4']]


        comp=pd.concat([a6,b6],axis=1)
        comp2=comp[['B4','B','ni4','ni','Ti4','Ti','V4','V']]
        comp2.to_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/comp_phi_0.1_temp_%.1f_' % phi+str(1200+1200*i).zfill(6),float_format='%.3f')
