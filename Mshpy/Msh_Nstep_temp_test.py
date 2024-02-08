#Compare 10^5K run and 10^4K run temperature along radial directions

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

f1='/Volumes/easystore/openggcm_run/Msh_Nstep/Msh_Nstep.3D.002400'
f2='/Volumes/Elements/openggcm_run/Msh_Nstep_003/Msh_Nstep_003.3D.002400'

a=pd.read_csv(f1,names=['i','the','j','radi','x1','y1','z1','rr1','k','phi','rr1','pp1'],sep='\s+',skiprows=1)
b=pd.read_csv(f2,names=['i','the','j','radi','x1','y1','z1','rr1','k','phi','rr1','pp1'],sep='\s+',skiprows=1)
a=a[a.the==0]
b=b[b.the==0]
a['T1']=72429*a.pp1/a.rr1/11600
b['T1']=72429*b.pp1/b.rr1/11600



fig,axes=plt.subplots(1,5,figsize=(15,6))

phil=[-90,-45,0,45,90]
for i in range(5):
    tempa=a[a.phi==phil[i]].sort_values(by=['radi'])
    tempb=b[b.phi==phil[i]].sort_values(by=['radi'])
    axes[i].plot(tempa.radi,tempa.T1,label='$T_{sw}=10^5K$')
    axes[i].plot(tempb.radi,tempb.T1,label='$T_{sw}=10^4K$')
    axes[i].legend()
    axes[i].set_xlabel('r [Re]')
    axes[i].set_ylabel('T [eV]')
    axes[i].set_title('$\phi=$'+str(phil[i])+'$^\circ$')
    axes[i].grid()

plt.tight_layout()
plt.savefig('Msh_temp_test.png')
