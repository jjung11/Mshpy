import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import sys

n=6
lf=int(sys.argv[1])
B=sys.argv[2]

run='Msh_Nstep'
external='easystore'

df_list2=[]
for i in range(1,n+1):
    df_list=[]
    for phi in np.arange(-90+7.5,90,7.5):
        a=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/Spreiter/comp_'+B+'_'+str(1200+1200*i).zfill(6))
        if lf==1:a=a[(a.f>=.3) & (a.f<=.7)]
        df_list.append(a)
    a2=pd.concat(df_list)
    a2['n']=i*5
    df_list2.append(a2)
a3=pd.concat(df_list2)

stat=pd.DataFrame([[round(a3.ni.mean(),3),round(a3.V.mean(),3),round(a3.Ti.mean(),3)],
[round(a3.ni_T.mean(),3),round(a3.V_T.mean(),3),round(a3.Ti_T.mean(),3)],
[a3.ni.median(),a3.V.median(),a3.Ti.median()],
[a3.ni_T.median(),a3.V_T.median(),a3.Ti_T.median()]])
if lf!=1:stat.to_csv('/Volumes/'+external+'/openggcm_run/'+run+'/Spreiter/stat_%s.txt' % B)
else:stat.to_csv('/Volumes/'+external+'/openggcm_run/'+run+'/Spreiter/stat_lf_%s.txt' % B)


list=['ni','Ti','V']
unit=['[cm$^{-3}$]','[eV]','[km/s]']
reg=[]
for j in range(3):
    mask=~np.isnan(a3[list[j]+'_T'])&~np.isnan(a3[list[j]])
    reg.append(stats.linregress(a3[list[j]+'_T'][mask],a3[list[j]][mask]))

label_l=np.arange(5,35,5)
fig,ax=plt.subplots(2,2,figsize=(10,10))
for j in range(3):
    ax_t=ax.flatten()[j+1]
    for i in range(n):
        ax_t.scatter(df_list2[i][list[j]+'_T'],df_list2[i][list[j]],label=str(label_l[i])+'cm$^{-3}$')
    ax_t.plot(a3[list[j]+'_T'],reg[j].slope*a3[list[j]+'_T']+reg[j].intercept)
    ax_t.annotate('y={:.2f}x+{:.2f}'.format(reg[j].slope,reg[j].intercept),xy=(.05,.95),xycoords='axes fraction')
    ax_t.plot(a3[list[j]+'_T'],a3[list[j]+'_T'],label='y=x')
    ax_t.grid()
#    ax_t.legend()
    ax_t.set_xlabel(list[j]+'_THEMIS '+unit[j])
    ax_t.set_ylabel(list[j]+'_Spreiter '+unit[j])
handles, labels = ax_t.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right',bbox_to_anchor=(0.9,0.99))
#plt.suptitle('B_z=-4nT, 0.3$\leq$f$\leq$0.7')
txt='Spreiter'
if B=='cn':txt+='\n B>0 THEMIS data'
else:txt+='\n B<0 THEMIS data'
if lf==1:txt+='\n 0.3$\leq$f$\leq$0.7'
plt.suptitle(txt)

path='/Volumes/'+external+'/openggcm_run/'+run+'/Spreiter/Scatter'
if lf==1: path+='_lf'
if B=='cn':path+='_cn'
else:path+='_cs'
path+='.png'
plt.savefig(path)
