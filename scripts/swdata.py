#!/usr/bin/python
# make swdata from WIND MFI and SWE data

import os
import sys
sys.path.append("/home/hconnor/svn/hkc-project/trunk/lib/")

import locale
import matplotlib.pyplot as plt
import numpy as np
from read_sc		import *
from jrmod01  		import *
from numpy		import arange,average
from openggcm_info 	import mhdtime,mhdt2hrmi


def WI_swdata(fi1,fi2,t1,t2,t3,t4,av,setbx):
  "create swdata, the OpenGGCM input from WIND MFI and SWE data"

## interpolate WIND data every av seconds between t1 and t2
  name = ['bxgse','bygse','bzgse','vth','rr','xgse','ygse','zgse', \
          'vxgse','vygse','vzgse','pp']
  fo   = [ 'wi.'+i for i in name ]

  lda1=ldaf(fi1)
  lda2=ldaf(fi2)

  date1,time1,bx,by,bz                   = read_WIMFI(fi1,lda1,setbx)
  date2,time2,th,np2,xl,yl,zl,vx,vy,vz,pp = read_WISWE(fi2,lda2)

  date = [date1,date1,date1,date2,date2,date2,date2,date2,date2,date2,date2,date2]
  time = [time1,time1,time1,time2,time2,time2,time2,time2,time2,time2,time2,time2]
  vv   = [bx,by,bz,th,np2,xl,yl,zl,vx,vy,vz,pp]

  for i in range(len(date)) :
    interpolate_data(fo[i],t1,t2,av,date[i],time[i],vv[i])

## create swdata, the OpenGGCU input starting from t3
  name = ['bxgse','bygse','bzgse','vxgse','vygse','vzgse','rr','pp']
  fo   = [ 'wi.'+i for i in name ]
  create_swdata(fo,'swdata.wi',t1,t2,t3,t4)
  #print(np.shape(xl))
  print(np.average(np.array(xl).astype(float)))

  return


def AC_swdata(fi1,fi2,t1,t2,t3,t4,av,setbx):
  "create swdata, the OpenGGCM input from ACE MFI and SWE data"

## interpolate ACE data every av seconds between t1 and t2
  name = ['bxgse','bygse','bzgse','xgse','ygse','zgse', \
          'rr','pp','tk','vxgse','vygse','vzgse'        ]
  fo   = [ 'ac.'+i for i in name ]

  lda1=ldaf(fi1)
  lda2=ldaf(fi2)

  date1,time1,bx,by,bz,xl,yl,zl          = read_ACMFI(fi1,lda1,setbx)
  date2,time2,np,pp,tk,vx,vy,vz          = read_ACSWE(fi2,lda2)

  date = [date1,date1,date1,date1,date1,date1,date2,date2,date2,date2,date2,date2]
  time = [time1,time1,time1,time1,time1,time1,time2,time2,time2,time2,time2,time2]
  vv   = [bx,by,bz,xl,yl,zl,np,pp,tk,vx,vy,vz]

  for i in range(len(date)) :
    interpolate_data(fo[i],t1,t2,av,date[i],time[i],vv[i])

## create swdata, the OpenGGCU input starting from t3
  name = ['bxgse','bygse','bzgse','vxgse','vygse','vzgse','rr','pp']
  fo   = [ 'ac.'+i for i in name ]
  create_swdata(fo,'swdata.ac',t1,t2,t3,t4)

  return


def omni_swdata(fi1,fi2,t1,t2,t3,t4,av,setbx):
  "create swdata, the OpenGGCM input from OMNI data"

## interpolate OMNI data every av seconds between t1 and t2

  name = ['bxgse','bygse','bzgse','tk','rr','xgse','ygse','zgse', \
          'vxgse','vygse','vzgse','pp']
  fo   = [ 'omni.'+i for i in name ]



#  print(lda1)
  lda1=0
  date1,time1,bx,by,bz,date2,time2,vx,vy,vz,nn,pp,tk,date3,time3,xl,yl,zl \
  = read_omni(fi1,lda1,setbx)



  date = [date1,date1,date1,date2,date2,date3,date3,date3,date2,date2,date2,date2]
  time = [time1,time1,time1,time2,time2,time3,time3,time3,time2,time2,time2,time2]
  vv   = [bx,by,bz,tk,nn,xl,yl,zl,vx,vy,vz,pp]

  for i in range(len(date)) :
    interpolate_data(fo[i],t1,t2,av,date[i],time[i],vv[i])



## create swdata, the OpenGGCM input starting from t3
  name = ['bxgse','bygse','bzgse','vxgse','vygse','vzgse','rr','pp']
  fo   = [ 'omni.'+i for i in name ]
  create_swdata(fo,'swdata.omni',t1,t2,t3,t4)

  return


def GE_swdata(fi1,fi2,lda1,lda2,t1,t2,t3,t4,av,setbx):
  "create swdata, the OpenGGCM input from Geotail data"

## interpolate OMNI data every av seconds between t1 and t2

  name = ['bxgse','bygse','bzgse','tk','rr','xgse','ygse','zgse', \
          'vxgse','vygse','vzgse','pp']
  fo   = [ 'ge.'+i for i in name ]

  date,time,bx,by,bz,vx,vy,vz,nn,pp,tk,xl,yl,zl = read_GE(fi1,lda1,setbx)

  date = [date,date,date,date,date,date,date,date,date,date,date,date]
  time = [time,time,time,time,time,time,time,time,time,time,time,time]
  vv   = [bx,by,bz,tk,nn,xl,yl,zl,vx,vy,vz,pp]

  for i in range(len(date)) :
    interpolate_data(fo[i],t1,t2,av,date[i],time[i],vv[i])

## create swdata, the OpenGGCM input starting from t3
  name = ['bxgse','bygse','bzgse','vxgse','vygse','vzgse','rr','pp']
  fo   = [ 'ge.'+i for i in name ]
  create_swdata(fo,'swdata.ge',t1,t2,t3,t4)

  return

def TH_swdata(fi1,fi2,lda1,lda2,t1,t2,t3,t4,av,setbx,sc):
  "create swdata, the OpenGGCM input from ACE MFI and SWE data"

## interpolate THEMIS data every av seconds between t1 and t2
  name = ['bxgse','bygse','bzgse','rr','pp','tk',	\
          'vxgse','vygse','vzgse'        ]
  fo   = [ sc+'.'+i for i in name ]

  date1,time1,bx,by,bz           = read_THFGM(fi1,lda1,setbx)
  date2,time2,np,pp,tk,vx,vy,vz          = read_THESA(fi2,lda2)

  date = [date1,date1,date1,date2,date2,date2,date2,date2,date2]
  time = [time1,time1,time1,time2,time2,time2,time2,time2,time2]
  vv   = [bx,by,bz,np,pp,tk,vx,vy,vz]

  for i in range(len(date)) :
    interpolate_data(fo[i],t1,t2,av,date[i],time[i],vv[i])

## create swdata, the OpenGGCU input starting from t3
  name = ['bxgse','bygse','bzgse','vxgse','vygse','vzgse','rr','pp']
  fo   = [ sc+'.'+i for i in name ]
  create_swdata(fo,'swdata.'+sc,t1,t2,t3,t4)
  return



def interpolate_data(fo,t1,t2,av,date,time,vv):
  "interpolate data every 'av' seconds between t1 and t2                        \
   fo   : output filename                                                       \
   t1   : start time of data                                                    \
   t2   : end time of data                                                      \
   av   : time interval for the interpolation                                   \
   date : date information                                                      \
   time : time information                                                      \
   vv   : data to be interpolated                                               "

  print("output filename: ",fo)
  ftmp="tmp."+fo
  f=open(ftmp,'w')
  for j in range(len(vv)):
    dd=date[j].split('-')
    tt=time[j].split(':')

    l1 = dd[2]+' '+dd[1]+' '+dd[0]+' '
    l2 = tt[0]+' '+tt[1]+' '+tt[2]+' '
    ll = l1+l2+' '+vv[j]+'\n'
    f.write(ll)
  f.close()

#  exe="$HOME/svn/hkc-project/trunk/src/swdata/tser_ave"
  exe="/Volumes/easystore/code/tser_ave"
  print(t1,t2,av,ftmp,fo)
  cmd=exe+" -t1 " + t1 + " -t2 " + t2 + " -tav " + av \
      +" -fillgaps < "+ftmp+" > " + fo

  print(cmd)

  os.system(cmd)
  os.remove(ftmp)

  return



def create_swdata(fi,fo,t1,t2,t3,t4):
  " create swdata, the OpenGGCM input, in the following format                  \
    T(min) bx(nT) by(nT) bz(nT) vx(km/s) vy(km/s) vz(km/s) N(cc) P(pP)          \
    ----------------------------------------------------------------------------\
    fi   : input data lists in the folloing order                               \
           [ bx,by,bz,vx,vy,vz,nn,pp ]                                          \
    fo   : output data                                                          \
    t1   : start time of solar wind data                                        \
    t2   : end   time of solar wind data                                        \
    t3   : start time of OpenGGCM run                                           \
    t4   : end   time of OpenGGCM run                                           \
    ----------------------------------------------------------------------------"

  vv  = []
  tt1 = epo1c(t1)
  tt2 = epo1c(t2)
  tt3 = epo1c(t3)
  tt4 = epo1c(t4)
  fmt = "%7.2f %8.4f %8.4f %8.4f %8.2f %8.2f %8.2f %7.2f %7.2f -1  0  0\n"



  for i in range(len(fi)):
    #print(fi,tt1,tt2)
    x=read_tseries(fi[i],tt1,tt2)
    #print(x)
    if i==0: vv.append(x[6])
    vv.append(x[7])



  f=open(fo,'w')

  for j in range(len(vv[0])):

   if vv[0][j] >=tt3 and vv[0][j]<=tt4:

     t=(vv[0][j]-tt3)/60.
     if t==0:
       ll = fmt%(-999.00,vv[1][j],vv[2][j],vv[3][j],vv[4][j],\
               vv[5][j],vv[6][j],vv[7][j],vv[8][j])
       f.write(ll)

     ll = fmt%(t,vv[1][j],vv[2][j],vv[3][j],vv[4][j], \
               vv[5][j],vv[6][j],vv[7][j],vv[8][j])
     f.write(ll)

  f.close()

  return


def read_swdata(fi):
  "read swdata"

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

  tt=[];rr=[];pp=[]
  bx=[];by=[];bz=[]
  vx=[];vy=[];vz=[]

  for s in l:
    w=s.split(None)
    if len(w)>2:

      tt.append(locale.atof(w[0])*60.)

      bx.append(locale.atof(w[1]))
      by.append(locale.atof(w[2]))
      bz.append(locale.atof(w[3]))
      vx.append(locale.atof(w[4]))
      vy.append(locale.atof(w[5]))
      vz.append(locale.atof(w[6]))
      rr.append(locale.atof(w[7]))
      pp.append(locale.atof(w[8]))

  return tt,bx,by,bz,vx,vy,vz,rr,pp


def compare_swdata(time,sc1,sc2,tsc1,tsc2):
  "compare swdata from ACE and WIND 				\
   time    : start time of OpenGGCM RUN				\
   tac     : time shift of sc1 data to propagate SW propagation	\
   twi     : time shift of sc2 data to propagate SW propagation	"


  pm=1.672614e-27                 # proton mass

  fi='swdata.'+sc1
  tt,bx1,by1,bz1,vx1,vy1,vz1,rr1,pp1=read_swdata(fi)
  tt1=[ i + tsc1 for i in tt ]
# pp1=[ i*1e-3  for i in pp ]
  pdy1 = [ rr1[i]*pm*(vx1[i]**2+vy1[i]**2+vz1[i]**2)*1e21 for i in range(len(vx1)) ]
  bt1  = [ (bx1[i]**2+by1[i]**2+bz1[i]**2)**0.5 for i in range(len(bx1)) ]

  fi='swdata.'+sc2
  tt,bx2,by2,bz2,vx2,vy2,vz2,rr2,pp2=read_swdata(fi)
  tt2=[ i + tsc2 for i in tt ]
# pp2=[ i*1e-3  for i in pp ]
  pdy2 = [ rr2[i]*pm*(vx2[i]**2+vy2[i]**2+vz2[i]**2)*1e21 for i in range(len(vx2)) ]
  bt2  = [ (bx2[i]**2+by2[i]**2+bz2[i]**2)**0.5 for i in range(len(bx2)) ]

# print pp1,pp2
# print pdy1,pdy2
  vv1=[bx1,by1,bz1,bt1,vx1,vy1,vz1,rr1,pp1,pdy1]
  vv2=[bx2,by2,bz2,bt2,vx2,vy2,vz2,rr2,pp2,pdy2]


  vstr=[ 'Bx [nT]','By [nT]','Bz [nT]','Bt [nT]',		\
         'Vx [km/s]','Vy [km/s]','Vz [km/s]', 			\
         'N [/m3]','P [pPa]','Psw [nPa]'			]

  t0      =  mhdtime(time)
  title   ='SW data from '+sc1+'(blue) & '+sc2+'(green) on'+t0.date

  dtmaj   =  3600
  dtmin   =  600
  dtlab   =  3600*2
  xtick1  =  arange(0,tt[-1]+dtmaj,dtmaj)       # major tick location
  xtick2  =  arange(0,tt[-1]+dtmin,dtmin)       # minor tick location
  xlabel  =  mhdt2hrmi(xtick1,t0,dtlab)         # create tick label


  fig=plt.figure(figsize=(8,11))

  for i in range(len(vv1)) :
    ax1=plt.subplot(len(vv1),1,i+1)
    pl1=ax1.plot(tt1,vv1[i])
    pl2=ax1.plot(tt2,vv2[i])

    ax1.set_ylabel(vstr[i],fontsize=10)

    ax1.set_xticks (xtick1)
    ax1.set_xticks (xtick2,minor=True)
    ax1.set_xticklabels(xlabel,fontsize=10)
    ax1.set_xlim   (0.,tt[-1])

    ax1.grid(axis='x')

    if i==0         : ax1.set_title (title,fontsize=12)
    if i==len(vv1)-1 : ax1.set_xlabel('UT',fontsize=10)

  fo='compare_swdata_'+t0.date+'.pdf'
  plt.savefig(fo)
  return


def plot_swdata(sc,time,dt=1) :
  "plot swdata									\
   sc    : satellite name, ac for ACE and wi for WIND				\
   time  : start time of OpenGGCM						\
   dt    : time interval for tick in hour, i.e., dt=4 makes ticks every 4 hours "

  pm=1.672614e-27                 # proton mass

  fi='swdata.'+sc
  tt,bx,by,bz,vx,vy,vz,rr,pp=read_swdata(fi)

  pdy = [ rr[i]*pm*(vx[i]**2+vy[i]**2+vz[i]**2)*1e21 for i in range(len(vx)) ]
  bt  = [ (bx[i]**2+by[i]**2+bz[i]**2)**0.5 for i in range(len(bx)) ]
  vt  = [ (vx[i]**2+vy[i]**2+vz[i]**2)**0.5 for i in range(len(vx)) ]
  rv  = [ rr[i]*vt[i]*1e5/1e8 for i in range(len(rr)) ]

# for  i in range(len(bx)):
#  if tt[i]> 7200 and tt[i] < 10800: print tt[i],bt[i],vx[i],pdy[i]

  vv=[bx,by,bz,bt,vx,vy,vz,rr,pp,pdy,rv]
  vstr=[ 'Bx [nT]','By [nT]','Bz [nT]','|B| [nT]',			\
         'Vx [km/s]','Vy [km/s]','Vz [km/s]', 				\
         'N [cm$^{-3}$]','Pth=nkT [pPa]','Pdy='+r'$\rho v^2$'+' [nPa]', \
         r'Flux=$\rho v$ [10$^8$ cm$^{-2}$s$^{-1}$]']

  t0      =  mhdtime(time)
  if   sc=='ac'  : title='SW data from ACE  on'+t0.date
  elif sc=='wi'  : title='SW data from WIND on '+t0.date
  elif sc=='ge'  : title='SW data from Geotail on '+t0.date
  elif sc=='omni': title='SW data from OMNI on '+t0.date
  else           : title='SW data from '+sc+' on '+t0.date


  dtmaj   =  3600*dt
  dtmin   =  600
  dtlab   =  3600*dt
  xtick1  =  arange(0,tt[-1]+dtmaj,dtmaj)   	# major tick location
  xtick2  =  arange(0,tt[-1]+dtmin,dtmin)   	# minor tick location
  xlabel  =  mhdt2hrmi(xtick1,t0,dtlab)         # create tick label

  fig=plt.figure(figsize=(8,11))


  for i in range(len(vv)) :
    ax1=plt.subplot(len(vv),1,i+1)
    plt.subplots_adjust(hspace = .001)
    ax1.tick_params(axis='both',which='major',labelsize=10)


    pl1=ax1.plot(tt,vv[i])

#   ax1.set_ylabel(vstr[i],fontsize=10)

    ax1.set_xticks (xtick1)
    ax1.set_xticks (xtick2,minor=True)
    ax1.set_xlim   (0.,tt[-1])
    ax1.grid       (axis='x')
    if i==len(vv)-1: ax1.set_xticklabels(xlabel)
    else           : ax1.set_xticklabels ([ '' for j in xlabel])

    plt.setp(ax1.get_yticklabels()[-1],visible=False)

    if i==0         : ax1.set_title (title,fontsize=12)
    if i==len(vv)-1 : ax1.set_xlabel('UT',fontsize=10)
    if i<=2         : ax1.axhline(y=0,ls=':',c='k')

    ax1.text(0.01,0.9,vstr[i],ha='left',va='top', \
             fontsize=10,transform=ax1.transAxes)

    if i==0         :
      ax1.text(0.99,0.1,'Ave_bx: %f'%average(bx),ha='right',va='bottom', \
               fontsize=10,transform=ax1.transAxes)
# plt.tight_layout()
  if bx[0]==bx[-1]: fo=fi+'_'+t0.date+'_constBz.pdf'
  else            : fo=fi+'_'+t0.date+'.pdf'
  plt.savefig(fo)
  return


def main(argv):

  sc=argv[0]			# satellite info
  f1=argv[1]           		#MFI data: date time bxgse bygse bzgse
  f2=argv[2]           		#SWE data: date time vth rr xgse ygse zgse vxgse vygse vzgse
  t1=argv[3]          		#starttime for interpolation
  t2=argv[4]            	#endtime   for interpolation
  t3=argv[5]           		#starttime for MHD simulation
  t4=argv[6]           		#endtime   for MHD simulation
  av=argv[7]      		#time interval of interpolation in sec
  dt=locale.atof(argv[8])	#time for major tick  in hr for plot

#  lda=argv[9].split(':')	#the line where data starts
 # lda1=locale.atoi(lda[0])-1
  #lda2=locale.atoi(lda[1])-1

  setbx=locale.atof(argv[9])  	#set up Bx value : 9999.99 for no change in Bx



#  print(lda,lda1,lda2)

### create swdata from WIND
  if sc=='wi'     : WI_swdata  (f1,f2,t1,t2,t3,t4,av,setbx)
  if sc=='ac'     : AC_swdata  (f1,f2,t1,t2,t3,t4,av,setbx)
  if sc=='ge'     : GE_swdata  (f1,f2,t1,t2,t3,t4,av,setbx)
  if sc=='omni'   : omni_swdata(f1,f2,t1,t2,t3,t4,av,setbx)
  if sc[:2]=='TH' : TH_swdata  (f1,f2,t1,t2,t3,t4,av,setbx,sc)

### plot swdata

  plot_swdata(sc,t3,dt)

# compare_swdata(t3,'wi','omni',-1700,0)
# plot_swdata('wi',t3)
# plot_swdata('ac',t3)
# compare_swdata(t3,0,0)

  return


if __name__=='__main__':
   main(sys.argv[1:])
