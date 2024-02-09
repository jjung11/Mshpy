# get 2D data from f3df
# read bx,by,bz(nT),vx,vy,vz(km/s),rr(/cm3),pp(pPa) from Msh model

# fout : output
# fgrid: grid file
# f3df : 3df file
# l1   : values to read  ex. bx,by,bz
# pn   : plane xy,yz,xz
# l2   : set plane [re]  ex. y=10.0 means a plane at y=10re

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv
from Msh_Nstep_test_n import main as mhd
from scipy import constants

rrio1=5.
rrio2=7.
pie=3.141592654

xi=float(argv[2])
xf=float(argv[4])
yi=float(argv[6])
yf=float(argv[8])
ds=float(argv[10])
lp=float(argv[12])

pn=argv[14]
f_out=argv[16]
f_out2=f_out+'_temp'
print('xi,xf,yi,yf,ds,pn,lp',xi,xf,yi,yf,ds,pn,lp)

nnx=int((xf-xi)/ds+1)
nny=int((yf-yi)/ds+1)


f=open(f_out,'w')
f.write('%d %d\n' %(nnx,nny))

x=[]
y=[]
z=[]
for i in range(1,nny+1):
    for j in range(1,nnx+1):

        if pn=='xr':
            xr=xi+(j-1)*ds
            yr=0.
            zr=yi+(i-1)*ds
            xx=xr
            yy=yr*np.cos(lp*np.pi/180.)-zr*np.sin(lp*np.pi/180.)
            zz=yr*np.sin(lp*np.pi/180.)+zr*np.cos(lp*np.pi/180.)
        elif pn=='zr':
            xr=xi+(j-1)*ds
            yr=0.
            zr=yi+(i-1)*ds
            xx=xr*np.cos(lp*np.pi/180.)-yr*np.sin(lp*np.pi/180.)
            yy=xr*np.sin(lp*np.pi/180.)+yr*np.cos(lp*np.pi/180.)
            zz=zr
        elif pn=='xz':
            xx=xi+(j-1)*ds
            yy=lp
            zz=yi+(i-1)*ds
        elif pn=='xy':
            xx=xi+(j-1)*ds
            yy=yi+(i-1)*ds
            zz=lp
        elif pn=='yz':
            xx=lp
            yy=xi+(j-1)*ds
            zz=yi+(i-1)*ds
        x.append(xx)
        y.append(yy)
        z.append(zz)

xyz=np.array(list(zip(x,y,z))).astype('float64')
print(xyz)
f_sw='SW_cond_test.txt'
mhd(xyz,f_sw,f_out2)
print('Model value extracted')

Msh=pd.read_csv(f_out2)

for i in range(1,nny+1):
    for j in range(1,nnx+1):
        temp=Msh.iloc[j-1+(i-1)*nnx]
        bx1=temp.Bx
        by1=temp.By
        bz1=temp.Bz
        vx1=temp.Vx
        vy1=temp.Vy
        vz1=temp.Vz
        rr1=temp.n
        tk1=temp.Tev
        pp1=11600e18*constants.k*rr1*tk1
        xx=x[j-1+(i-1)*nnx]
        yy=y[j-1+(i-1)*nnx]
        zz=z[j-1+(i-1)*nnx]

        if pn=='xr' or pn=='zr':
            f.write('%d %d %f %f %f %f %f %f %f %f %f %f %f nan nan nan nan nan nan %f %f %f nan\n'%(j,i,xx,yy,zz,bx1,by1,bz1,vx1,vy1,vz1,rr1,pp1,xr,yr,zr))
        else:
            f.write('%d %d %f %f %f %f %f %f %f %f %f %f %f nan nan nan nan nan nan nan\n'%(j,i,xx,yy,zz,bx1,by1,bz1,vx1,vy1,vz1,rr1,pp1))
    if i%10==0: print(i)
f.close()
