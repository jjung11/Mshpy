import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


a=pd.read_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/modeling/SMILE_002400')
fig=plt.figure()
ax=fig.add_subplot(projection='polar')
ax.set_thetamin(-90)
ax.set_thetamax(90)
ax.set_ylim([0,25])
im=ax.scatter(a.phi*np.pi/180,a.rad,c=a.ni_T,cmap='jet')
cb=fig.colorbar(im,ax=ax)
cb.set_label('n [cm$^{-3}$]')
b=a[a.f==0]
ax.plot(b.phi*np.pi/180,b.rad,label='MP')
b=a[a.f==1]
ax.plot(b.phi*np.pi/180,b.rad,label='BS')
ax.set_title('B>0 $n_{sw}=5cm^{-3}$')

plt.savefig('SMILE_fig_5.png')
