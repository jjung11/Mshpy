import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

for i in range(1,7):
    a=pd.read_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/modeling/Msh_data.'+str(1200+1200*i).zfill(6),header=None,sep='\s+',names=['the','phi','m','rad','x','y','z','bx1','by1','bz1','vx1','vy1','vz1','rr1','pp1','ex1','ey1','ez1','xjx1','xjy1','xjz1','resis1']).drop_duplicates()
    a2=a[a.the==0]
    b=pd.read_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/sheath_data_ascii/cn%d.txt' % i,sep='\s+',header=None,names=['theta_1','theta_2','f_1','f_2','B','ni','Ti','V'],skiprows=1)
    b['theta']=(b.theta_1+b.theta_2)/2
    b['f']=(b.f_1+b.f_2)/2
    b['phi']=np.where(b.theta<=180,b.theta,b.theta-360)
    b2=b[(-90<=b.phi) & (b.phi<=90)]

    for j in range(1,10):
        f=j/10
        b3=b2[(b2.f<f+.01) & (b2.f>f-.01)]
        b4=b3[['phi','B','ni','Ti','V']].set_index('phi')
        b4.columns=['B_T','ni_T','Ti_T','V_T']

        a3=a2[a2.m==10*j].set_index('phi')
        a4=a3.reindex(a3.index.union(b3.phi))
        a5=a4.interpolate('index').reindex(index=b3.phi)
        a5['B']=np.sqrt(a5.bx1**2+a5.by1**2+a5.bz1**2)
        a5['Ti']=72429.0*a5.pp1/a5.rr1/11600.
        a5['V']=np.sqrt(a5.vx1**2+a5.vy1**2+a5.vz1**2)
        a5['ni']=a5.rr1
        a6=a5[['B','ni','Ti','V']]

        comp=pd.concat([a6,b4],axis=1)
        comp2=comp[['B_T','B','ni_T','ni','Ti_T','Ti','V_T','V']]
        comp2.to_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/modeling/comp_%.1f.' % j+str(1200+1200*i).zfill(6),float_format='%.3f')

        fig, axs=plt.subplots(4,figsize=(6.4,8))
        axs[0].plot(comp2.index,comp2.B_T,'o-')
        axs[0].plot(comp2.index,comp2.B,'o-')
        axs[1].plot(comp2.index,comp2.ni_T,'o-')
        axs[1].plot(comp2.index,comp2.ni,'o-')
        axs[2].plot(comp2.index,comp2.Ti_T,'o-')
        axs[2].plot(comp2.index,comp2.Ti,'o-')
        axs[3].plot(comp2.index,comp2.V_T,'o-')
        axs[3].plot(comp2.index,comp2.V,'o-')
        axs[3].set_xlabel('$\phi(^\circ)$ ')
        axs[0].set_ylabel('B (nT)')
        axs[1].set_ylabel('n (cm$^{-3}$)')
        axs[2].set_ylabel('T (eV)')
        axs[3].set_ylabel('V (km/s)')
        axs[0].grid()
        axs[1].grid()
        axs[2].grid()
        axs[3].grid()
        fig.suptitle('f=%.1f' % f)
        fig.savefig('/Volumes/easystore/openggcm_run/Msh_Nstep/modeling/plots/comp/comp_%d_m_f%.1f.png' % (20*i+20,f))
        plt.close()
