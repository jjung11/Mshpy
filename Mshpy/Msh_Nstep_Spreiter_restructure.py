import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp2d
from astropy.io import fits

cd=1/156
fits_image_filename_n='/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/ssa_density.fits'
hdu_n=fits.open(fits_image_filename_n)
data_n=hdu_n[0].data
fits_image_filename_v='/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/ssa_velocity.fits'
hdu_v=fits.open(fits_image_filename_v)
data_v=hdu_v[0].data
data_T=(data_v!=0)*(1+64/3*(1-data_v**2))
x=np.array([1-(i-133)*cd for i in range(512)])
y=np.array([(i-10)*cd for i in range(491)])
n=interp2d(x,y,data_n)
v=interp2d(x,y,data_v)
print(np.min(x),np.max(x))
print(np.min(y),np.max(y))

path='/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/BS2.txt'

def BS2(path_):
    a=open(path_,"w")
    n_r=0
    for phi in np.arange(0,181):
#        print(phi)
        r=0
        r_mp=0
        while (n_r==0) & (r<=3.6):
            n_r=n(r*np.cos(phi*np.pi/180),r*np.sin(phi*np.pi/180))
            r+=.01
        r_mp=r
        if n_r>0:
            while n_r>0:
                n_r=n(r*np.cos(phi*np.pi/180),r*np.sin(phi*np.pi/180))
                r+=.01
            a.write('%f %f %f\n'%(phi,r_mp,r))
    a.close()
    return

BS2(path)

b=pd.read_csv(path,header=None,sep='\s+')
#b=b[b[0]%1==0]
b.columns=['phi','rmp','rbs']


phi,f=np.mgrid[0:181:1,0:1:.1]
phif=np.array([phi.flatten(),f.flatten()]).T
c=pd.DataFrame(phif)
c.columns=['phi','f']
d=pd.merge(c,b,on='phi')
d['r']=d.rmp+d.f*(d.rbs-d.rmp)
d['x']=d.r*np.cos(d.phi*np.pi/180)
d['y']=d.r*np.sin(d.phi*np.pi/180)
d['ni']=d.apply(lambda x:n(x.x,x.y)[0],axis=1)
d['V']=d.apply(lambda x:v(x.x,x.y)[0],axis=1)
d['Ti']=1+64/3*(1-d.V**2)
path2='/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/ssa2.txt'
d.to_csv(path2,float_format='%.4f',index=False)

a=pd.read_csv(path2)
#a=a.sort_values(by=['phi'])
phi=np.arange(0,181,1)
m=np.arange(0,10,1)
print(np.shape(a))

print(np.shape(a)[0]//10)
n,T,V=np.zeros([3,np.shape(a)[0]//10-1,10])
for k in range(np.shape(a)[0]//10-1):
    for l in range(len(m)):
        cur=a.iloc[10*k+l]
#        print(cur)
        n[k,l]=cur.ni
        T[k,l]=cur.Ti
        V[k,l]=cur.V
np.savetxt('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/Msh_n' ,n,fmt='%.3f')
np.savetxt('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/Msh_T' ,T,fmt='%.3f')
np.savetxt('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/Msh_V' ,V,fmt='%.3f')
