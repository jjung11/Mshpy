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

run=argv[1]
if run=='Msh_Nstep':external='easystore'
else:external='Elements'

x=np.linspace(0,20)

for i in range(1,7):
    a=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_data_0.1.'+str(1200+1200*i).zfill(6),header=None,sep='\s+',names=['the','phi','m','rad','x','y','z','bx1','by1','bz1','vx1','vy1','vz1','rr1','pp1','ex1','ey1','ez1','xjx1','xjy1','xjz1','resis1']).drop_duplicates()
    a2=a[a.the==0]
    if argv[1]=='cs':
        b=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/sheath_data_ascii/cs%d.txt' % i,sep='\s+',header=None,names=['theta_1','theta_2','f_1','f_2','B','ni','Ti','V'],skiprows=1)
    else:
        b=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/sheath_data_ascii/cn%d.txt' % i,sep='\s+',header=None,names=['theta_1','theta_2','f_1','f_2','B','ni','Ti','V'],skiprows=1)
    b['phi1']=np.where(b.theta_1<=180,b.theta_1,b.theta_1-360)
    b['phi2']=np.where(b.theta_2<=180,b.theta_2,b.theta_2-360)
    b['phi']=(b.phi1+b.phi2)/2
    b['f']=(b.f_1+b.f_2)/2
#    b2=b[(-90<=b.phi) & (b.phi<=90)]
    b2=b

    df_list2=[]
    for phi in np.arange(-90+7.5,90,7.5):
        y=x*np.tan(phi*np.pi/180)

        b3=b2[(b2.phi<phi+.01) & (b2.phi>phi-.01)]
        df1 = pd.DataFrame([[np.nan] * len(b3.columns)], columns=b3.columns)
        b3 = df1.append(b3, ignore_index=True)
        b3.iloc[0].f=0
        b3.iloc[0].phi=phi
        b3=b3.append(pd.Series(),ignore_index=True)
        b3.iloc[-1].f=1
        b3.iloc[-1].phi=phi
        #print(b3.f)

        b4=b3[['f','B','ni','Ti','V']].set_index('f')
        b4.columns=['B_T','ni_T','Ti_T','V_T']

        df_list=[]
        for j in range(0,11):
            a_t=a2[(a2.phi<phi+7.5) & (a2.phi>phi-7.5)]
            a_t2=a_t[(a_t.m>j-.1) & (a_t.m<j+.1)]
            a_t3=a_t2.mean().to_frame().T
            a_t3.phi=phi
            a_t3['f']=j/10
            df_list.append(a_t3)
        a3=pd.concat(df_list,axis=0).set_index('f')

        a4=a3.reindex(a3.index.union(b3.f))
        #print(a3.index.union(b3.f))
        a5=a4.interpolate('index').reindex(index=b3.f)
        a5['B']=np.sqrt(a5.bx1**2+a5.by1**2+a5.bz1**2)
        a5['Ti']=72429.0*a5.pp1/a5.rr1/11600.
        a5['V']=np.sqrt(a5.vx1**2+a5.vy1**2+a5.vz1**2)
        a5['ni']=a5.rr1
        a6=a5[['rad','B','ni','Ti','V']]

        comp=pd.concat([a6,b4],axis=1)
        comp2=comp[['rad','B_T','B','ni_T','ni','Ti_T','Ti','V_T','V']]
        comp2['phi']=phi
        df_list2.append(comp2)

    comp3=pd.concat(df_list2,axis=0)
    comp3.to_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/SMILE_'+str(1200+1200*i).zfill(6),float_format='%.3f')
