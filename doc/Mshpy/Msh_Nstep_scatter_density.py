import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from scipy import stats

n=6
run=sys.argv[1]
lf=int(sys.argv[2])
if run=='Msh_Nstep':external='easystore'
else:external='Elements'

df_list2=[]
for i in range(1,7):
    df_list=[]
    for phi in np.arange(-90+7.5,90,7.5):
        a=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/comp_phi_0.1_%.1f_' % phi+str(1200+1200*i).zfill(6))
        if lf==1: a=a[(a.f>=.3) & (a.f<=.7)]
        df_list.append(a)
    a2=pd.concat(df_list)
    df_list2.append(a2)
a3=pd.concat(df_list2)

list=['B','ni','Ti','V']
unit=['[nT]','[cm$^{-3}$]','[eV]','[km/s]']

label_l=np.arange(5,35,5)
for j in range(4):
    reg=[]
    fig,ax=plt.subplots(2,3,figsize=(10,10))
    ax_t=ax.flatten()
    for i in range(6):
        mask=~np.isnan(df_list2[i][list[j]+'_T'])&~np.isnan(df_list2[i][list[j]])
        reg.append(stats.linregress(df_list2[i][list[j]+'_T'][mask],df_list2[i][list[j]][mask]))

        ax_t[i].scatter(df_list2[i][list[j]+'_T'],df_list2[i][list[j]])
        ax_t[i].plot(df_list2[i][list[j]+'_T'][mask],reg[i].slope*df_list2[i][list[j]+'_T'][mask]+reg[i].intercept,label='y={:.2f}x+{:.2f}'.format(reg[i].slope,reg[i].intercept))
#        ax_t[i].annotate('y={:.2f}x+{:.2f}'.format(reg[i].slope,reg[i].intercept),xy=(.05,.95),xycoords='axes fraction')
        ax_t[i].plot(df_list2[i][list[j]+'_T'][mask],df_list2[i][list[j]+'_T'][mask],label='y=x')
        ax_t[i].grid()
        ax_t[i].legend()
        ax_t[i].set_xlabel(list[j]+'_THEMIS '+unit[j])
        ax_t[i].set_ylabel(list[j]+'_MHD '+unit[j])
        ax_t[i].set_title(str(label_l[i])+'cm$^{-3}$')
#    handles, labels = ax_t[i].get_legend_handles_labels()
#    fig.legend(handles, labels, loc='upper right',bbox_to_anchor=(0.9,0.99))
    #plt.suptitle('B_z=-4nT, 0.3$\leq$f$\leq$0.7, Maximum current')
    if run=='Msh_Nstep': plt.suptitle('B_z=4nT '+list[j]+' Comparison')
    else: plt.suptitle('B_z=-4nT '+list[j]+' Comparison')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/plots/comp/Scatter_0.1'+list[j]+'.png')
