import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fig, axes = plt.subplots(2,4,subplot_kw={'projection': 'polar'},figsize=(10,6))
axes[1,3].axis("off")

for i in range(1,8):
    a=pd.read_csv('modeling/xz_cusp_cn_n.'+str(1200*i).zfill(6),header=None,sep='\s+',skiprows=1)
    b=pd.read_csv('modeling/xz_cusp_cn_s.'+str(1200*i).zfill(6),header=None,sep='\s+',skiprows=1)
    ax=axes.flat[i-1]
    ax.plot(a[2]*np.pi/180,a[0])
    ax.plot(a[3]*np.pi/180,a[0])
    ax.plot(b[2]*np.pi/180,b[0])
    ax.plot(b[3]*np.pi/180,b[0])
    ax.set_thetamin(-90)
    ax.set_thetamax(90)
    mask=plt.Circle((0,0),3.5,transform=ax.transData._b)
    ax.add_artist(mask)
    ax.set_ylim(0,12)
    if i==1:
        ax.title.set_text('n_sw=1cm$^{-3}$')
    else:
        ax.title.set_text('n_sw=%d'%(5*(i-1))+'cm$^{-3}$')


plt.savefig('Cusp_plot.png')
