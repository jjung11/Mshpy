import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import datetime,timedelta
from matplotlib.dates import DateFormatter,AutoDateLocator

def rolling_ave(tt,vv,tave,dt,avetype='c'):
  "calculate centered average and previous value average                        \
   tt   : time series in seconds						\
   vv   : data to be averaged							\
   tave : time series of moving average						\
   dt   : time duration of the moving average in seconds 			\
   avetype : c for centered average, p for averaging previous values 		"

  v1 = np.zeros(len(tave))
  n1 = np.zeros(len(tave))
  if   avetype=='c':		# centered average
   for i in range(len(vv)):
#    print(vv[i])
    if not np.isnan(vv[i]):
     for j in range(len(tave)):
#      print(type(tt[i]),type(tave[j]),type((dt)))
#      print(i,tt[i],tave[j])
      if tt[i]>=tave[j]-np.timedelta64(int(dt/2),'s') and tt[i] < tave[j]+np.timedelta64(int(dt/2),'s') :
        v1[j]=v1[j]+vv[i]
        n1[j]=n1[j]+1
  elif avetype=='p':		# average of previous values
   for i in range(len(vv)):
    if not np.isnan(vv[i]):
     for j in range(len(tave)):
      if j<len(tave)-1:
        if tt[i]>=tave[j] and tt[i] < tave[j+1] :
          v1[j+1]=v1[j+1]+vv[i]
          n1[j+1]=n1[j+1]+1
  vave = [ v1[i]/n1[i] for i in range(len(v1)) ]
  return vave

def main(argv):
    run=argv[0]
    sc=argv[1]

    fps1=f'{run}/{run}.Msh_model.png'
    fmsh=f'{run}/Msh_MHD_out.txt'
    fvel=f'{run}/Msh_Soucek_out.txt'
    fmag=f'{run}/Msh_Romashets_out.txt'
    fsp=f'{run}/Msh_Spreiter_out.txt'
    foff=f'{run}/Msh_offset.txt'
#    print(run,sc)

    if sc=='cluster4':
#        print('test')
        fc1=f'{run}/c4_fgm.lst'
        fc2=f'{run}/c4_cis.lst'
        title=f'{run} comparison of {sc} data with Mshpy results'
        compare_CLMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title,foff=foff)

def compare_CLMHD(fps,fc1,fc2,fmsh,fvel,fmag,fsp,title,avt=60,foff=0):
    Msh=pd.read_csv(fmsh,parse_dates=['time'])
    vel=pd.read_csv(fvel,parse_dates=['time'])
    mag=pd.read_csv(fmag,parse_dates=['time'])
    spr=pd.read_csv(fsp,parse_dates=['time'])

    fgm=pd.read_csv(fc1,parse_dates=['time'])
    cis=pd.read_csv(fc2,parse_dates=['time'])

    tave=np.arange(Msh.time.iloc[0],Msh.time.iloc[-1],timedelta(seconds=avt))
    ave_df=pd.DataFrame({
        'bxav':rolling_ave(fgm.time,fgm.Bx,tave,avt),
        'byav':rolling_ave(fgm.time,fgm.By,tave,avt),
        'bzav':rolling_ave(fgm.time,fgm.Bz,tave,avt),
        'n1av':rolling_ave(cis.time,cis.n,tave,avt),
        'vxav':rolling_ave(cis.time,cis.Vx,tave,avt),
        'vyav':rolling_ave(cis.time,cis.Vy,tave,avt),
        'vzav':rolling_ave(cis.time,cis.Vz,tave,avt),
        'tsav':rolling_ave(cis.time,cis.Tev,tave,avt)
    })
    ave_df['btav']=np.sqrt(ave_df.bxav**2+ave_df.byav**2+ave_df.bzav**2)
    ave_df['vtav']=np.sqrt(ave_df.vxav**2+ave_df.vyav**2+ave_df.vzav**2)

    mag['Bt']=np.sqrt(mag.Bx**2+mag.By**2+mag.Bz**2)
    vel['vt']=np.sqrt(vel.vx**2+vel.vy**2+vel.vz**2)
    Msh['Bt']=np.sqrt(Msh.Bx**2+Msh.By**2+Msh.Bz**2)
    Msh['Vt']=np.sqrt(Msh.Vx**2+Msh.Vy**2+Msh.Vz**2)

    fig,ax=plt.subplots(10,1,sharex=True,figsize=(6.4,10))
    plt.subplots_adjust(hspace=0)
    
    ax[0].plot(tave,ave_df.bxav,'k-',label='Cluster')
    ax[0].plot(Msh.time,Msh.Bx,'g-',label='MHD-based')
    ax[0].plot(mag.time,mag.Bx,'b-',label='Romashets')
    ax[0].legend()

    ax[1].plot(tave,ave_df.byav,'k-',label='Cluster')
    ax[1].plot(Msh.time,Msh.By,'g-',label='MHD-based')
    ax[1].plot(mag.time,mag.By,'b-',label='Romashets')

    ax[2].plot(tave,ave_df.bzav,'k-',label='Cluster')
    ax[2].plot(Msh.time,Msh.Bz,'g-',label='MHD-based')
    ax[2].plot(mag.time,mag.Bz,'b-',label='Romashets')

    ax[3].plot(tave,ave_df.btav,'k-',label='Cluster')
    ax[3].plot(Msh.time,Msh.Bt,'g-',label='MHD-based')
    ax[3].plot(mag.time,mag.Bt,'b-',label='Romashets')

    ax[4].plot(tave,ave_df.vxav,'k-',label='Cluster')
    ax[4].plot(Msh.time,Msh.Vx,'g-',label='MHD-based')
    ax[4].plot(vel.time,vel.vx,'r-',label='Soucek')
    ax[4].legend()

    ax[5].plot(tave,ave_df.vyav,'k-',label='Cluster')
    ax[5].plot(Msh.time,Msh.Vy,'g-',label='MHD-based')
    ax[5].plot(vel.time,vel.vy,'r-',label='Soucek')

    ax[6].plot(tave,ave_df.vzav,'k-',label='Cluster')
    ax[6].plot(Msh.time,Msh.Vz,'g-',label='MHD-based')
    ax[6].plot(vel.time,vel.vz,'r-',label='Soucek')

    ax[7].plot(tave,ave_df.vtav,'k-',label='Cluster')
    ax[7].plot(Msh.time,Msh.Vt,'g-',label='MHD-based')
    ax[7].plot(vel.time,vel.vt,'r-',label='Soucek')
    ax[7].plot(spr.time,spr.V,'m-',label='Spreiter')

    ax[8].plot(tave,ave_df.n1av,'k-',label='Cluster')
    ax[8].plot(Msh.time,Msh.n,'g-',label='MHD-based')
    ax[8].plot(spr.time,spr.n,'m-',label='Spreiter')
    ax[8].legend()

    ax[9].plot(tave,ave_df.tsav,'k-',label='Cluster')
    ax[9].plot(Msh.time,Msh.Tev,'g-',label='MHD-based')
    ax[9].plot(spr.time,spr.Tev,'m-',label='Spreiter')
    ax[9].set_xlabel(f'Time starting from {(tave[0]).astype(datetime).strftime("%b %d %H:%MUT")}')

    ylab= [ 'Bx [nT]',            \
            'By [nT]',            \
            'Bz [nT]',            \
            '|B| [nT]',            \
            'Vx [km/s]',          \
            'Vy [km/s]',          \
            'Vz [km/s]',          \
            '|V| [km/s]',          \
            'N [cm$^{-3}$]',      \
            'T [eV]'              ]

    for i in range(10):
        ax[i].grid()
        ax[i].set_ylabel(ylab[i])
        ax[i].xaxis.set_major_formatter(DateFormatter("%H:%M"))   

    if foff!=0:
        with open(foff) as f:
            for line in f:
                mpdo,bsdo = line.split()
                mpdo=float(mpdo)
                bsdo=float(bsdo)
    #        print(mpdo,bsdo)
        label=[]
        annotate=f'MP adjustment = {mpdo}R$_E$\nBS adjustment = {bsdo}R$_E$'
        print(annotate)
    
    anloc=(.1,.03)
    plt.annotate(annotate,xy=anloc, xycoords='figure fraction')
    print("Save",fps)
    plt.savefig(fps)
    plt.close()
    
    return

if __name__=='__main__':
    main(sys.argv[1:])


    