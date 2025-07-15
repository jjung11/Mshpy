import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import sys

n=6
run=sys.argv[1]
lf=int(sys.argv[2])
#external='Elements'
if run=='Msh_Nstep':external='easystore'
else:external='Elements'

df_list2=[]
for i in range(1,n+1):
    df_list=[]
    for phi in np.arange(-90+7.5,90,7.5):
        a=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/comp_phi_0.1_temp_%.1f_' % phi+str(1200+1200*i).zfill(6))
        if lf==1:a=a[(a.f>=.3) & (a.f<=.7)]
        df_list.append(a)
    a2=pd.concat(df_list)
    a2['n']=i*5
    df_list2.append(a2)
a3=pd.concat(df_list2)
stat=pd.DataFrame([[round(a3.B.mean(),3),round(a3.ni.mean(),3),round(a3.Ti.mean(),3),round(a3.V.mean(),3)],
[round(a3.B4.mean(),3),round(a3.ni4.mean(),3),round(a3.Ti4.mean(),3),round(a3.V4.mean(),3)],
[a3.B.median(),a3.ni.median(),a3.Ti.median(),a3.V.median()],
[a3.B4.median(),a3.ni4.median(),a3.Ti4.median(),a3.V4.median()]])
if lf!=1:stat.to_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/stat_0.1_temp_test.txt')
else:stat.to_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/stat_lf_0.1_temp_test.txt')


list=['B','ni','Ti','V']
unit=['[nT]','[cm$^{-3}$]','[eV]','[km/s]']
reg=[]
for j in range(4):
    mask=~np.isnan(a3[list[j]+'4'])&~np.isnan(a3[list[j]])
    reg.append(stats.linregress(a3[list[j]+'4'][mask],a3[list[j]][mask]))

label_l=np.arange(5,35,5)
fig,ax=plt.subplots(2,2,figsize=(10,10))
for j in range(4):
    ax_t=ax.flatten()[j]
    for i in range(n):
        ax_t.scatter(df_list2[i][list[j]+'4'],df_list2[i][list[j]],label=str(label_l[i])+'cm$^{-3}$')
    ax_t.plot(a3[list[j]+'4'],reg[j].slope*a3[list[j]+'4']+reg[j].intercept)
    ax_t.annotate('y={:.2f}x+{:.2f}'.format(reg[j].slope,reg[j].intercept),xy=(.05,.95),xycoords='axes fraction')
    ax_t.plot(a3[list[j]+'4'],a3[list[j]+'4'],label='y=x')
    ax_t.grid()
#    ax_t.legend()
    ax_t.set_xlabel(list[j]+'_10^4K '+unit[j])
    ax_t.set_ylabel(list[j]+'_10^5K '+unit[j])
handles, labels = ax_t.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right',bbox_to_anchor=(0.9,0.99))
#plt.suptitle('B_z=-4nT, 0.3$\leq$f$\leq$0.7')
if run=='Msh_Nstep':txt='B_z=4nT'
else:txt='B_z=-4nT'
if lf==1:txt+='\n 0.3$\leq$f$\leq$0.7'
plt.suptitle(txt)

if lf!=1:plt.savefig('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/plots/comp/Scatter_0.1_temp_test.png')
else:plt.savefig('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/plots/comp/Scatter_lf_0.1_temp_test.png')
