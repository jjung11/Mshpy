import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv

B=argv[1]

df_list=[]
for i in range(1,7):
    b=pd.read_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/sheath_data_ascii/'+B+'%d.txt' % i,sep='\s+',header=None,names=['theta_1','theta_2','f_1','f_2','B','ni','Ti','V'],skiprows=1)
    b['phi1']=np.where(b.theta_1<=180,b.theta_1,b.theta_1-360)
    b['phi2']=np.where(b.theta_2<=180,b.theta_2,b.theta_2-360)
    b['phi']=(b.phi1+b.phi2)/2
    b['f']=(b.f_1+b.f_2)/2

    temp=b.drop(['theta_1','theta_2','f_1','f_2','phi1','phi2'],axis=1)
    temp.columns=['B_T','ni_T','Ti_T','V_T','phi','f']
    temp.to_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/sheath_data_ascii/'+B+'_Sp_%d.txt'% i,float_format='%.4f',index=False)
    df_list.append(temp)
d=pd.read_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/ssa.txt')
d_2=d[d.phi!=0].copy()
d_2.phi=-d_2.phi
d=pd.concat([d,d_2])

df_list2=[]
for i in range(1,7):
    temp=d.copy()
    temp.ni=temp.ni*5*i
    temp.V=temp.V*400
    temp.Ti=temp.Ti*2.586
    temp2=pd.merge(df_list[i-1],temp,on=['phi','f'])
    temp2.to_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/comp_'+B+'_'+str(1200+1200*i).zfill(6),float_format='%.3f')
    df_list2.append(temp2)
