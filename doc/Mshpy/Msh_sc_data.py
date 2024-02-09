#!/usr/bin
#
# compare Cluster data with MHD data


import os
import sys

import locale
import numpy            as np
import pandas           as pd
from   datetime         import datetime,timedelta
from   openggcm_info	import runinfo
from   easyplot		import easy1Dplot,easy1Dplot_l
from   get_scorbit      import read_CLFGM,read_CLCIS
from   get_THdata       import read_THFGM,read_THESA,read_THESAr
from   get_GEdata       import read_GEMGF,read_GEH0CPI,read_GEK0CPI,read_GESWCPI


def datetime_mhdt(date,time,mhdt0):
  "convert date & time in the following format to mhdt time.                  	\
   date  in format of dd-mm-yyyy                        			\
   time  in format of hr:mi:se.***                      			\
   mhdt0 in format of yyyy:mm:dd:hr:mi:se.**            			\
   mhdt  in format of %06d                              			"
  dd,mm,yy = [ locale.atoi(i) for i in date.split('-')]
  hr,mi    = [ locale.atoi(i) for i in time.split(':')[:-1]]
  se       = locale.atof(time.split(':')[-1])
  tdata    = datetime(yy,mm,dd,hr,mi,0)
  tstr     = [ int(locale.atof(i)) for i in mhdt0.split(':') ]
  tmhd0    = datetime(tstr[0],tstr[1],tstr[2],tstr[3],tstr[4],tstr[5] )
  dmhdt    = tdata - tmhd0
  mhdt     = dmhdt.days*86400 + dmhdt.seconds + se
# mhdt     = dmhdt.seconds + se
  return mhdt

def datetime_mhdt2(dt,mhdt0):
  tstr     = [ int(locale.atof(i)) for i in mhdt0.split(':') ]
  tmhd0    = datetime(tstr[0],tstr[1],tstr[2],tstr[3],tstr[4],tstr[5] )
  dt2=pd.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
  dmhdt    = dt2 - tmhd0
  mhdt     = dmhdt.days*86400 + dmhdt.seconds
# mhdt     = dmhdt.seconds + se
  return mhdt



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
    if not np.isnan(vv[i]):
     for j in range(len(tave)):
      if tt[i]>=tave[j]-dt/2 and tt[i] < tave[j]+dt/2 :
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


def compare_CLMHD(fps,fc1,fc2,fmsh,fvel,fmag,fsp,title,vln0t=-1,vln1t=-1,avt=60,foff=0):

  info = runinfo(fps)
#  tm,xm,ym,zm,vm                         = read_mhdCL(fmhd)
  Msh=pd.read_csv(fmsh)
  Msh['mhdt']=[datetime_mhdt2(i,info.ti) for i in Msh.time]

  vel=pd.read_csv(fvel)
  vel['mhdt']=[datetime_mhdt2(i,info.ti) for i in vel.time]

  mag=pd.read_csv(fmag)
  mag['mhdt']=[datetime_mhdt2(i,info.ti) for i in mag.time]

  spr=pd.read_csv(fsp)
  spr['mhdt']=[datetime_mhdt2(i,info.ti) for i in spr.time]


#  date1,time1,box,boy,boz                = read_THFGM(fc1,vtype='real')
#  date2,time2,nsw,tsw,vswx,vswy,vswz     = read_THESA(fc2,vtype='real')
  date1,time1,box,boy,boz,xo,yo,zo       = read_CLFGM(fc1,vtype='real')
  date2,time2,nsw,tpar,tper,vswx,vswy,vswz      = read_CLCIS(fc2,vtype='real')
#  bmx,bmy,bmz,vmx,vmy,vmz,rrm,ppm,emx,emy,emz,jmx,jmy,jmz = vm

  to1 = [ datetime_mhdt(date1[i],time1[i],info.ti) for i in range(len(date1)) ]
  to2 = [ datetime_mhdt(date2[i],time2[i],info.ti) for i in range(len(date2)) ]
#  tkm = [ 72429.0*ppm[i]/rrm[i]*1e-6 for i in range(len(ppm)) ]
 # tev = [ 72429.0*ppm[i]/rrm[i]/11600 for i in range(len(ppm)) ]
  tsw = [ (tpar[i]+tper[i])*1e6/(2*11600) for i in range(len(tpar)) ]


#  print(to1[0:10], to1[-10:])
#  print(to2[0:10], to2[-10:])
  tave = np.arange(0.,info.dur,avt)
  bxav = np.array(rolling_ave(to1,box,tave,avt))
  byav = np.array(rolling_ave(to1,boy,tave,avt))
  bzav = np.array(rolling_ave(to1,boz,tave,avt))
  n1av = np.array(rolling_ave(to2,nsw,tave,avt))
  vxav = np.array(rolling_ave(to2,vswx,tave,avt))
  vyav = np.array(rolling_ave(to2,vswy,tave,avt))
  vzav = np.array(rolling_ave(to2,vswz,tave,avt))
  tsav = np.array(rolling_ave(to2,tsw,tave,avt))
  btav=np.sqrt(bxav**2+byav**2+bzav**2)
  vtav=np.sqrt(vxav**2+vyav**2+vzav**2)

  mag['Bt']=np.sqrt(mag.Bx**2+mag.By**2+mag.Bz**2)
  vel['vt']=np.sqrt(vel.vx**2+vel.vy**2+vel.vz**2)
  Msh['Bt']=np.sqrt(Msh.Bx**2+Msh.By**2+Msh.Bz**2)
  Msh['Vt']=np.sqrt(Msh.Vx**2+Msh.Vy**2+Msh.Vz**2)

  print(np.nanmax(bxav),np.nanmax(byav),np.nanmax(bzav))


  xx =  [[tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,mag.mhdt],
         [tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,vel.mhdt],    \
         [tave,Msh.mhdt,vel.mhdt],    \
         [tave,Msh.mhdt,vel.mhdt],
         [tave,Msh.mhdt,vel.mhdt,spr.mhdt],         \
         [tave,Msh.mhdt,spr.mhdt],    \
         [tave,Msh.mhdt,spr.mhdt]     ]

  yy =  [[bxav,Msh.Bx,mag.Bx],                \
         [byav,Msh.By,mag.By],                \
         [bzav,Msh.Bz,mag.Bz],
         [btav,Msh.Bt,mag.Bt],           \
         [vxav,Msh.Vx,vel.vx],     \
         [vyav,Msh.Vy,vel.vy],     \
         [vzav,Msh.Vz,vel.vz],
         [vtav,Msh.Vt,vel.vt,spr.V],               \
         [n1av,Msh.n,spr.n],       \
         [tsav,Msh.Tev,spr.Tev]        ]


  lst = [['k-','g-','b-'],      \
         ['k-','g-','b-'],      \
         ['k-','g-','b-'],      \
         ['k-','g-','b-'],
         ['k-','g-','r-'], \
         ['k-','g-','r-'], \
         ['k-','g-','r-'], \
         ['k-','g-','r-','m-'], \
         ['k-','g-','m-'], \
         ['k-','g-','m-'], ]

  if vln0t==-1 and vln1t==-1:  vln0=[]
  else:
      vln0 = [ [vln0t,vln1t,'grey'],'vp']
  vln     = [ vln0 for i in xx ]

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

  yran= [ 0,      \
          0,        \
          0,        \
          0,   \
          0,     \
          0,     \
          0,          \
          0,
          0,
          [0,500]]

  vstr= ['' for i in xx ]

  vstr[0]= [ ['Cluster','Our model','Romashets','Soucek','Spreiter'], ['k','g','b','r','m'], [0.40,0.50,0.65,0.8,0.9],[0.2,0.2,0.2,0.2,0.2] ]
  tev = [0]


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
      easy1Dplot_l(fps,xx,yy,lst,vln,ylab,yran,vstr,title,label,annotate,anloc=(.1,.03),bottom=0.1)
  else:
      easy1Dplot(fps,xx,yy,lst,vln,ylab,yran,vstr,title)
  return

def compare_THMHD(fps,fc1,fc2,fmsh,fvel,fmag,fsp,title,vln0t=-1,vln1t=-1,avt=60,foff=0):

  info = runinfo(fps)
  Msh=pd.read_csv(fmsh)
  Msh['mhdt']=[datetime_mhdt2(i,info.ti) for i in Msh.time]
  date1,time1,box,boy,boz                = read_THFGM(fc1,vtype='real')
  date2,time2,nsw,tsw,vswx,vswy,vswz     = read_THESA(fc2,vtype='real')

  vel=pd.read_csv(fvel)
  vel['mhdt']=[datetime_mhdt2(i,info.ti) for i in vel.time]

  mag=pd.read_csv(fmag)
  mag['mhdt']=[datetime_mhdt2(i,info.ti) for i in mag.time]

  spr=pd.read_csv(fsp)
  spr['mhdt']=[datetime_mhdt2(i,info.ti) for i in spr.time]

  to1 = [ datetime_mhdt(date1[i],time1[i],info.ti) for i in range(len(date1)) ]
  to2 = [ datetime_mhdt(date2[i],time2[i],info.ti) for i in range(len(date2)) ]

  tave = np.arange(0.,info.dur,avt)
  bxav = np.array(rolling_ave(to1,box,tave,avt))
  byav = np.array(rolling_ave(to1,boy,tave,avt))
  bzav = np.array(rolling_ave(to1,boz,tave,avt))
  n1av = np.array(rolling_ave(to2,nsw,tave,avt))
  vxav = np.array(rolling_ave(to2,vswx,tave,avt))
  vyav = np.array(rolling_ave(to2,vswy,tave,avt))
  vzav = np.array(rolling_ave(to2,vswz,tave,avt))
  tsav = np.array(rolling_ave(to2,tsw,tave,avt))
  btav=np.sqrt(bxav**2+byav**2+bzav**2)
  vtav=np.sqrt(vxav**2+vyav**2+vzav**2)
  mag['Bt']=np.sqrt(mag.Bx**2+mag.By**2+mag.Bz**2)
  vel['vt']=np.sqrt(vel.vx**2+vel.vy**2+vel.vz**2)
  Msh['Bt']=np.sqrt(Msh.Bx**2+Msh.By**2+Msh.Bz**2)
  Msh['Vt']=np.sqrt(Msh.Vx**2+Msh.Vy**2+Msh.Vz**2)


  print(np.nanmax(bxav),np.nanmax(byav),np.nanmax(bzav))


  xx =  [[tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,mag.mhdt],
         [tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,vel.mhdt],    \
         [tave,Msh.mhdt,vel.mhdt],    \
         [tave,Msh.mhdt,vel.mhdt],
         [tave,Msh.mhdt,vel.mhdt,spr.mhdt],         \
         [tave,Msh.mhdt,spr.mhdt],    \
         [tave,Msh.mhdt,spr.mhdt]     ]

  yy =  [[bxav,Msh.Bx,mag.Bx],                \
         [byav,Msh.By,mag.By],                \
         [bzav,Msh.Bz,mag.Bz],
         [btav,Msh.Bt,mag.Bt],           \
         [vxav,Msh.Vx,vel.vx],     \
         [vyav,Msh.Vy,vel.vy],     \
         [vzav,Msh.Vz,vel.vz],
         [vtav,Msh.Vt,vel.vt,spr.V],               \
         [n1av,Msh.n,spr.n],       \
         [tsav,Msh.Tev,spr.Tev]        ]


  lst = [['k-','g-','b-'],      \
         ['k-','g-','b-'],      \
         ['k-','g-','b-'],      \
         ['k-','g-','b-'],
         ['k-','g-','r-'], \
         ['k-','g-','r-'], \
         ['k-','g-','r-'], \
         ['k-','g-','r-','m-'], \
         ['k-','g-','m-'], \
         ['k-','g-','m-'], ]

  if vln0t==-1 and vln1t==-1:  vln0=[]
  else:
      vln0 = [ [vln0t,vln1t,'grey'],'vp']
  vln     = [ vln0 for i in xx ]

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

  yran= [ 0,      \
          0,        \
          0,        \
          0,   \
          0,     \
          0,     \
          0,          \
          0,
          0,
          [0,500]]

  vstr= ['' for i in xx ]

  vstr[0]= [ ['THEMIS','Our model','Romashets','Soucek','Spreiter'], ['k','g','b','r','m'], [0.40,0.50,0.65,0.8,0.9],[0.9,0.9,0.9,0.9,0.9] ]
  #tev = [0]

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
      easy1Dplot_l(fps,xx,yy,lst,vln,ylab,yran,vstr,title,label,annotate,anloc=(.1,.03),bottom=0.1)
  else:
      easy1Dplot(fps,xx,yy,lst,vln,ylab,yran,vstr,title)
  return

def compare_THMHDr(fps,fc1,fc2,fc3,fmsh,fvel,fmag,fsp,title,vln0t=-1,vln1t=-1,avt=60):

  info = runinfo(fps)
  Msh=pd.read_csv(fmsh)
  Msh['mhdt']=[datetime_mhdt2(i,info.ti) for i in Msh.time]
  date1,time1,box,boy,boz                = read_THFGM(fc1,vtype='real')
  date2,time2,nsw,tsw,vswx,vswy,vswz     = read_THESA(fc2,vtype='real')
  date3,time3,nsw,tsw                    = read_THESAr(fc3,vtype='real')

  vel=pd.read_csv(fvel)
  vel['mhdt']=[datetime_mhdt2(i,info.ti) for i in vel.time]

  mag=pd.read_csv(fmag)
  mag['mhdt']=[datetime_mhdt2(i,info.ti) for i in mag.time]

  spr=pd.read_csv(fsp)
  spr['mhdt']=[datetime_mhdt2(i,info.ti) for i in spr.time]

  to1 = [ datetime_mhdt(date1[i],time1[i],info.ti) for i in range(len(date1)) ]
  to2 = [ datetime_mhdt(date2[i],time2[i],info.ti) for i in range(len(date2)) ]
  to3 = [ datetime_mhdt(date3[i],time3[i],info.ti) for i in range(len(date3)) ]

  tave = np.arange(0.,info.dur,avt)
  bxav = np.array(rolling_ave(to1,box,tave,avt))
  byav = np.array(rolling_ave(to1,boy,tave,avt))
  bzav = np.array(rolling_ave(to1,boz,tave,avt))
  n1av = np.array(rolling_ave(to3,nsw,tave,avt))
  vxav = np.array(rolling_ave(to2,vswx,tave,avt))
  vyav = np.array(rolling_ave(to2,vswy,tave,avt))
  vzav = np.array(rolling_ave(to2,vswz,tave,avt))
  tsav = np.array(rolling_ave(to3,tsw,tave,avt))

  print(np.nanmax(bxav),np.nanmax(byav),np.nanmax(bzav))


  xx =  [[tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,vel.mhdt],    \
         [tave,Msh.mhdt,vel.mhdt],    \
         [tave,Msh.mhdt,vel.mhdt],         \
         [tave,Msh.mhdt,spr.mhdt],    \
         [tave,Msh.mhdt,spr.mhdt]     ]

  yy =  [[bxav,Msh.Bx,mag.Bx],                \
         [byav,Msh.By,mag.By],                \
         [bzav,Msh.Bz,mag.Bz],                \
         [vxav,Msh.Vx,vel.vx],     \
         [vyav,Msh.Vy,vel.vy],     \
         [vzav,Msh.Vz,vel.vz],               \
         [n1av,Msh.n,spr.n],       \
         [tsav,Msh.Tev,spr.Tev]        ]


  lst = [['k-','g-','b-'],      \
         ['k-','g-','b-'],      \
         ['k-','g-','b-'],      \
         ['k-','g-','r-'], \
         ['k-','g-','r-'], \
         ['k-','g-','r-'], \
         ['k-','g-','m-'], \
         ['k-','g-','m-'], ]

  if vln0t==-1 and vln1t==-1:  vln0=[]
  else:
      vln0 = [ [vln0t,vln1t,'grey'],'vp']
  vln     = [ vln0 for i in xx ]

  ylab= [ 'Bx [nT]',            \
          'By [nT]',            \
          'Bz [nT]',            \
          'Vx [km/s]',          \
          'Vy [km/s]',          \
          'Vz [km/s]',          \
          'N [cm$^{-3}$]',      \
          'T [eV]'              ]

  yran= [ 0,      \
          0,        \
          0,        \
          0,   \
          0,     \
          0,     \
          0,          \
          [0,500]]

  vstr= ['' for i in xx ]

  vstr[0]= [ ['THEMIS','Our model','Romashets','Soucek','Spreiter'], ['k','g','b','r','m'], [0.40,0.50,0.65,0.8,0.9],[0.9,0.9,0.9,0.9,0.9] ]
  tev = [0]


  easy1Dplot(fps,xx,yy,lst,vln,ylab,yran,vstr,title,tev)
  return

def compare_GEMHD(fps,fc1,fc2,fmsh,title,vln0t=-1,vln1t=-1,avt=60):

  info = runinfo(fps)
  Msh=pd.read_csv(fmsh)
  Msh['mhdt']=[datetime_mhdt2(i,info.ti) for i in Msh.time]

  vel=pd.read_csv(fvel)
  vel['mhdt']=[datetime_mhdt2(i,info.ti) for i in vel.time]

  mag=pd.read_csv(fmag)
  mag['mhdt']=[datetime_mhdt2(i,info.ti) for i in mag.time]

  spr=pd.read_csv(fsp)
  spr['mhdt']=[datetime_mhdt2(i,info.ti) for i in spr.time]

  date1,time1,box,boy,boz,xo,yo,zo       = read_GEMGF(fc1,vtype='real')
  date2,time2,nsw,tk,tsw,vswx,vswy,vswz=read_GESWCPI(fc2,vtype='real')

  to1 = [ datetime_mhdt(date1[i],time1[i],info.ti) for i in range(len(date1)) ]
  to2 = [ datetime_mhdt(date2[i],time2[i],info.ti) for i in range(len(date2)) ]

  tave = np.arange(0.,info.dur,avt)
  bxav = rolling_ave(to1,box,tave,avt)
  byav = rolling_ave(to1,boy,tave,avt)
  bzav = rolling_ave(to1,boz,tave,avt)
  n1av = rolling_ave(to2,nsw,tave,avt)
  vxav = rolling_ave(to2,vswx,tave,avt)
  vyav = rolling_ave(to2,vswy,tave,avt)
  vzav = rolling_ave(to2,vswz,tave,avt)
  tsav = rolling_ave(to2,tsw,tave,avt)

  print(np.nanmax(bxav),np.nanmax(byav),np.nanmax(bzav))


  xx =  [[tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,mag.mhdt],         \
         [tave,Msh.mhdt,vel.mhdt],    \
         [tave,Msh.mhdt,vel.mhdt],    \
         [tave,Msh.mhdt,vel.mhdt],         \
         [tave,Msh.mhdt,spr.mhdt],    \
         [tave,Msh.mhdt,spr.mhdt]     ]

  yy =  [[bxav,Msh.Bx,mag.Bx],                \
         [byav,Msh.By,mag.By],                \
         [bzav,Msh.Bz,mag.Bz],                \
         [vxav,Msh.Vx,vel.vx],     \
         [vyav,Msh.Vy,vel.vy],     \
         [vzav,Msh.Vz,vel.vz],               \
         [n1av,Msh.n,spr.n],       \
         [tsav,Msh.Tev,spr.Tev]        ]

  lst = [['k-','g-','b-'],      \
         ['k-','g-','b-'],      \
         ['k-','g-','b-'],      \
         ['k-','g-','r-'], \
         ['k-','g-','r-'], \
         ['k-','g-','r-'], \
         ['k-','g-','m-'], \
         ['k-','g-','m-'], ]

  if vln0t==-1 and vln1t==-1:  vln0=[]
  else:
      vln0 = [ [vln0t,vln1t,'grey'],'vp']
  vln     = [ vln0 for i in xx ]

  ylab= [ 'Bx [nT]',            \
          'By [nT]',            \
          'Bz [nT]',            \
          'Vx [km/s]',          \
          'Vy [km/s]',          \
          'Vz [km/s]',          \
          'N [cm$^{-3}$]',      \
          'T [eV]'              ]

  yran= [ 0,      \
          0,        \
          0,        \
          0,   \
          0,     \
          0,     \
          0,          \
          0]

  vstr= ['' for i in xx ]

  vstr[0]= [ ['Geotail','Our model','Romashets','Soucek','Spreiter'], ['k','g','b','r','m'], [0.40,0.50,0.65,0.8,0.9],[0.2,0.2,0.2,0.2,0.2] ]
  tev = [0]


  easy1Dplot(fps,xx,yy,lst,vln,ylab,yran,vstr,title,tev)
  return fps,xx,yy,lst,vln,ylab,yran,vstr,title,tev

def main(argv):
  run=argv[0]

  if run=="2003May04_001":
    fps1 ='2003May04_001.CL4_Msh_model_aberrated.png'
    fc1  ='/Volumes/easystore/openggcm_run/2003May04_001/data.2003May04_001/Cluster/C4_CP_FGM_SPIN_83121.txt'
    fc2  ='/Volumes/easystore/openggcm_run/2003May04_001/data.2003May04_001/Cluster/C4_PP_CIS_83121.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Msh_Spreiter_out.txt'
    foff='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Msh_offset.txt'
    title='2003May04_001 Comparison of CL4 data with MHD results'
    compare_CLMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title,(6*60+50)*60,(8*60+5)*60,foff=foff)

  if run=="2003May04_001_Jel":
    fps1 ='2003May04_001_Jel.CL4_Msh_model_aberrated.png'
    fc1  ='/Volumes/easystore/openggcm_run/2003May04_001/data.2003May04_001/Cluster/C4_CP_FGM_SPIN_83121.txt'
    fc2  ='/Volumes/easystore/openggcm_run/2003May04_001/data.2003May04_001/Cluster/C4_PP_CIS_83121.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001_Jel/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001_Jel/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001_Jel/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001_Jel/Msh_Spreiter_out.txt'
    foff='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001_Jel/Msh_offset.txt'
    title='2003May04_001_Jel Comparison of CL4 data with MHD results'
    compare_CLMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title,(6*60+50)*60,(8*60+5)*60,foff=foff)

  if run=="2006Jan10_003":
    fps1 ='2006Jan10_003.CL4_Msh_model_aberrated.png'
    fc1  ='/Volumes/Elements/openggcm_run/2006Jan10_003/data.2006Jan10_003/Cluster/C4_CP_FGM_SPIN_51586.txt'
    fc2  ='/Volumes/Elements/openggcm_run/2006Jan10_003/data.2006Jan10_003/Cluster/C4_PP_CIS_51586.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan10_003/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan10_003/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan10_003/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan10_003/Msh_Spreiter_out.txt'
    title='2006Jan10_003 Comparison of CL4 data with MHD results'
    compare_CLMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title)

  if run=="2006Jan13_002":
    fps1 ='2006Jan13_002.CL4_Msh_model_aberrated.png'
    fc1  ='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan13_002/C4_CP_FGM_SPIN_228860.txt'
    fc2  ='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan13_002/C4_PP_CIS_228860.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan13_002/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan13_002/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan13_002/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2006Jan13_002/Msh_Spreiter_out.txt'
    title='2006Jan13_002 Comparison of CL4 data with MHD results'
    compare_CLMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title)

  if run=="2008Jun28_005":
    fps1 ='2008Jun28_005.THC_Msh_model_aberrated.png'
    fc1  ='/Volumes/easystore2/openggcm_run/2008Jun28_005/data.2008Jun28_005/THEMIS/THC_L2_FGM_233697.txt'
    fc2  ='/Volumes/easystore2/openggcm_run/2008Jun28_005/data.2008Jun28_005/THEMIS/THC_L2_ESA_177255.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005/Msh_Spreiter_out.txt'
    foff='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005/Msh_offset.txt'
    title='2008Jun28_005 Comparison of THC data with MHD results'
    compare_THMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title,(5*60+10)*60,10*3600,300,foff=foff)

  if run=="2008Jun28_005_Jel":
    fps1 ='2008Jun28_005_Jel.THC_Msh_model_aberrated.png'
    fc1  ='/Volumes/easystore2/openggcm_run/2008Jun28_005/data.2008Jun28_005/THEMIS/THC_L2_FGM_233697.txt'
    fc2  ='/Volumes/easystore2/openggcm_run/2008Jun28_005/data.2008Jun28_005/THEMIS/THC_L2_ESA_177255.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005_Jel/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005_Jel/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005_Jel/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005_Jel/Msh_Spreiter_out.txt'
    foff='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Jun28_005_Jel/Msh_offset.txt'
    title='2008Jun28_005_Jel Comparison of THC data with MHD results'
    compare_THMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title,(5*60+10)*60,10*3600,300,foff=foff)

  if run=="2001Apr26_001":
    fps1 ='2001Apr26_001.CL4_Msh_model_aberrated.png'
    fc1  ='/Volumes/Elements/openggcm_run/2001Apr26_001/data.2001Apr26_001/Cluster/C4_CP_FGM_SPIN_144151.txt'
    fc2  ='/Volumes/Elements/openggcm_run/2001Apr26_001/data.2001Apr26_001/Cluster/C4_PP_CIS_144151.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2001Apr26_001/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2001Apr26_001/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2001Apr26_001/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2001Apr26_001/Msh_Spreiter_out.txt'
    title='2001Apr26_001 Comparison of CL4 data with MHD results'
    compare_CLMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title)

  if run=="2009Oct14_002":
    fps1 ='2009Oct14_002.THA_Msh_model_aberrated.png'
    fc1  ='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2009Oct14_002/THA_L2_FGM_66064.txt'
    fc2  ='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2009Oct14_002/THA_L2_ESA_68412.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2009Oct14_002/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2009Oct14_002/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2009Oct14_002/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2009Oct14_002/Msh_Spreiter_out.txt'
    title='2009Oct14_002 Comparison of THA data with MHD results'
    compare_THMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title,3600,(13*60+15)*60,avt=600)

  if run=="2010Aug20_002":
    fps1 ='2010Aug20_002.CL4_Msh_model_aberrated.png'
    fc1  ='/Volumes/Elements/openggcm_run/2010Aug20_002/data.2010Aug20_002/Cluster/C4_CP_FGM_SPIN_144151.txt'
    fc2  ='/Volumes/Elements/openggcm_run/2010Aug20_002/data.2010Aug20_002/Cluster/C4_PP_CIS_144151.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2010Aug20_002/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2010Aug20_002/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2010Aug20_002/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2010Aug20_002/Msh_Spreiter_out.txt'
    title='2010Aug20_002 Comparison of CL4 data with MHD results'
    compare_CLMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title)

  if run=="2008Oct09_001":
    fps1 ='2008Oct09_001.THC_Msh_model_aberrated.png'
    fc1  ='/Volumes/SEAGATE/openggcm_run/2008Oct09_001/data.2008Oct09_001/THEMIS/THC_L2_FGM_54802.txt'
    fc2  ='/Volumes/SEAGATE/openggcm_run/2008Oct09_001/data.2008Oct09_001/THEMIS/THC_L2_ESA_54802.txt'
    fc3  ='/Volumes/SEAGATE/openggcm_run/2008Oct09_001/data.2008Oct09_001/THEMIS/THC_L2_ESA_146171.txt'
    fmsh='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Oct09_001/Msh_MHD_out.txt'
    fvel='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Oct09_001/Msh_Soucek_out.txt'
    fmag='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Oct09_001/Msh_Romashets_out.txt'
    fsp='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2008Oct09_001/Msh_Spreiter_out.txt'
    title='2008Oct09_001 Comparison of THC data with MHD results'
    compare_THMHD(fps1,fc1,fc2,fmsh,fvel,fmag,fsp,title,(2*60+10)*60,(6*60+40)*60,avt=400)


  return

if __name__=='__main__':
    main(sys.argv[1:])
