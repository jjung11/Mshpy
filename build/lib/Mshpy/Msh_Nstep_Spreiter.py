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
print(np.min(x),np.max(x))
print(np.min(y),np.max(y))
n=interp2d(x,y,data_n)
v=interp2d(x,y,data_v)

def BS():
    a=open('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/BS.txt',"w")
    n_r=0
    for phi in np.arange(0,90.5,0.5):
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

#BS()

fig, ax = plt.subplots(1,3,figsize=(12,4))
plot_n=ax[0].pcolormesh(x, y, data_n)
plot_v=ax[1].pcolormesh(x, y, data_v)
plot_T=ax[2].pcolormesh(x, y, data_T)
ax[0].grid()
ax[1].grid()
ax[2].grid()
ax[0].set_xlabel('x/R_MP')
ax[0].set_ylabel('y(z)/R_MP')
ax[1].set_xlabel('x/R_MP')
#ax[1].set_ylabel('y(z)/R_MP')
ax[2].set_xlabel('x/R_MP')
#ax[2].set_ylabel('y(z)/R_MP')
fig.suptitle('Spreiter ($\gamma=5/3$, $M_\infty=8$)')
c1=fig.colorbar(plot_n,ax=ax[0])
c1.ax.set_title('n/n_SW')
c2=fig.colorbar(plot_n,ax=ax[1])
c2.ax.set_title('v/v_SW')
c3=fig.colorbar(plot_T,ax=ax[2])
c3.ax.set_title('T/T_SW')
plt.savefig('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/ssa.png')


b=pd.read_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/BS.txt',header=None,sep='\s+')
b=b[b[0]%7.5==0]
b.columns=['phi','rmp','rbs']
#b_2=b.copy()
#b_2.phi=-b_2.phi
#b=pd.concat([b,b_2])

phi,f=np.mgrid[-82.5:90:7.5,0.1:1:.1]
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
d.to_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/Spreiter/ssa.txt',float_format='%.4f',index=False)
