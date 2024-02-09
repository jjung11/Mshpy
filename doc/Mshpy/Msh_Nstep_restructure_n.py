import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv

external=argv[1]
run=argv[2]

for i in range(0,2):
    a=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_data_0.1.'+str(7200+7200*i).zfill(6),header=None,sep='\s+',
    names=['the','phi','m','rad','x','y','z','bx1','by1','bz1','vx1','vy1','vz1','rr1','pp1','ex1','ey1','ez1','xjx1','xjy1','xjz1','resis1']).drop_duplicates()

    a=a.sort_values(by=['the','phi'])
    the=np.arange(-90,91,1)
    phi=np.arange(-90,91,1)
    m=np.arange(0,11,1)
    print(np.shape(a))

    Bx,By,Bz,Vx,Vy,Vz,n,pp=np.zeros([8,181,181,11])
    for j in range(len(the)):
        for k in range(len(phi)):
            for l in range(len(m)):
                cur=a.iloc[(j*181+k)*11+l]
                Bx[j,k,l]=cur.bx1
                By[j,k,l]=cur.by1
                Bz[j,k,l]=cur.bz1
                Vx[j,k,l]=cur.vx1
                Vy[j,k,l]=cur.vy1
                Vz[j,k,l]=cur.vz1
                n[j,k,l]=cur.rr1
                pp[j,k,l]=cur.pp1
    np.save('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Bx_%d' % i,Bx)
    np.save('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_By_%d' % i,By)
    np.save('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Bz_%d' % i,Bz)
    np.save('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vx_%d' % i,Vx)
    np.save('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vy_%d' % i,Vy)
    np.save('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vz_%d' % i,Vz)
    np.save('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_n_%d' % i,n)
    np.save('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_pp_%d' % i,pp)
