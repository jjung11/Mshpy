#!/usr/bin/python
#
# get sc orbit file to obtain MHD values along spacecraft orbit


import os
import sys
HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/lib/")
sys.path.append(HOME+"/svn/hkc-project/trunk/src/swdata/")

import locale
#from jrmod01            import *
from numpy              import arange
from openggcm_info      import mhdtime,mhdt2hrmi
from swdata		import interpolate_data
import numpy as np

def ldaf(filename):
    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if line.startswith('dd'):
                lda=num
#                print ('found at line:', num)
    return lda


def read_GEMGF(fi,vtype='string'):
  "read Geotail MGF data downloaded from SPDweb"

  Err = '-1.00000E+31'
  re  = 6.37814e3

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

  lda=ldaf(fi)

  print("===============  CLEAN ALL UNNECESSARY INFORMATION  ===============")
  print("REMOVE ALL HEADERS BEFORE")
  print(l[lda])
  del   l[:lda]
  print("REMOVE ALL THE FOLLOWING TAILS ")
  print(l[-4:])
  del   l[-4:]
  print("-------------------------------------------------------------------")
  print("THE FIRST & LAST DATA LINES ARE")
  print(l[0])
  print(l[-1])
  print("===================================================================")


  date=[]
  time=[]
  bx=[];by=[];bz=[]
  xl=[];yl=[];zl=[]

  for s in l:
    w=s.split(None)
    if len(w)>2  and w[2]!=Err and w[3]!=Err and w[4]!=Err and \
       w[5]!=Err and w[6]!=Err and w[7]!=Err                   :

      date.append(w[0])
      time.append(w[1])
      bx1=locale.format('%f',locale.atof(w[2])*0.1)
      by1=locale.format('%f',locale.atof(w[3])*0.1)
      bz1=locale.format('%f',locale.atof(w[4])*0.1)
      bx.append(bx1)
      by.append(by1)
      bz.append(bz1)
      x1=locale.format('%f',locale.atof(w[5])/re)
      y1=locale.format('%f',locale.atof(w[6])/re)
      z1=locale.format('%f',locale.atof(w[7])/re)
      xl.append(x1)
      yl.append(y1)
      zl.append(z1)

  if vtype=='real':
    bx = [locale.atof(i) for i in bx ]
    by = [locale.atof(i) for i in by ]
    bz = [locale.atof(i) for i in bz ]
    xl = [locale.atof(i) for i in xl  ]
    yl = [locale.atof(i) for i in yl  ]
    zl = [locale.atof(i) for i in zl  ]

  return date,time,bx,by,bz,xl,yl,zl

def read_GEH0CPI(fi,vtype='string'):
  "read Geotail CPI data"

  Err = '-1.00000E+31'

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

  lda=ldaf(fi)

  print("===============  CLEAN ALL UNNECESSARY INFORMATION  ===============")
  print("REMOVE ALL HEADERS BEFORE")
  print(l[lda])
  del   l[:lda]
  print("REMOVE ALL THE FOLLOWING TAILS ")
  print(l[-4:])
  del   l[-4:]
  print("-------------------------------------------------------------------")
  print("THE FIRST & LAST DATA LINES ARE")
  print(l[0])
  print(l[-1])
  print("===================================================================")

  date=[];time=[];nsw=[];tk=[];teV=[];nhp=[];thp=[];php=[];
  vswx=[];vswy=[];vswz=[];vhpx=[];vhpy=[]

  for s in l:
    w=s.split(None)
    if len(w)>2  and w[2]!=Err and w[3]!=Err  and w[4]!=Err  and  \
       w[5]!=Err and w[6]!=Err :

      date.append(w[0])
      time.append(w[1])
#     tsw.append(w[2])
      teV.append(locale.format('%f',locale.atof(w[2])/11600.))  # convert K to eV
      tk.append(w[2])
      nsw.append(w[3])
      vswx.append(w[4])
      vswy.append(w[5])
      vswz.append(w[6])

  if vtype=='real':
    nsw  = [locale.atof(i) for i in nsw ]
    tk   = [locale.atof(i) for i in tk  ]
    teV  = [locale.atof(i) for i in teV ]
    vswx = [locale.atof(i) for i in vswx ]
    vswy = [locale.atof(i) for i in vswy ]
    vswz = [locale.atof(i) for i in vswz ]

  return date,time,nsw,tk,teV,vswx,vswy,vswz

def read_GESWCPI(fi,vtype='string'):
  "read Geotail SW CPI data"

  Err = '-1.00000E+31'

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

  lda=ldaf(fi)

  print("===============  CLEAN ALL UNNECESSARY INFORMATION  ===============")
  print("REMOVE ALL HEADERS BEFORE")
  print(l[lda])
  del   l[:lda]
  print("REMOVE ALL THE FOLLOWING TAILS ")
  print(l[-4:])
  del   l[-4:]
  print("-------------------------------------------------------------------")
  print("THE FIRST & LAST DATA LINES ARE")
  print(l[0])
  print(l[-1])
  print("===================================================================")

  date=[];time=[];nsw=[];tk=[];teV=[];nhp=[];thp=[];php=[];
  vswx=[];vswy=[];vswz=[];vhpx=[];vhpy=[];vsw=[];theta=[];phi=[]

  for s in l:
    w=s.split(None)
    if len(w)>2  and w[2]!=Err and w[3]!=Err  and w[4]!=Err  and  \
       w[5]!=Err and w[6]!=Err :

      date.append(w[0])
      time.append(w[1])
#     tsw.append(w[2])
      teV.append(locale.format('%f',locale.atof(w[5])/11600.))  # convert K to eV
      tk.append(w[5])
      nsw.append(w[6])
      vsw.append(w[2])
      theta.append(w[3])
      phi.append(w[4])

  if vtype=='real':
    nsw  = [locale.atof(i) for i in nsw ]
    tk   = [locale.atof(i) for i in tk  ]
    teV  = [locale.atof(i) for i in teV ]
    vsw = [locale.atof(i) for i in vsw ]
    theta = [locale.atof(i) for i in theta ]
    phi = [locale.atof(i) for i in phi ]
    vswx = [v*np.sin(the*np.pi/180)*np.cos(phi*np.pi/180) for v,the,phi in zip(vsw,theta,phi)]
    vswy = [v*np.sin(the*np.pi/180)*np.sin(phi*np.pi/180) for v,the,phi in zip(vsw,theta,phi)]
    vswz = [v*np.cos(the*np.pi/180) for v,the,phi in zip(vsw,theta,phi)]
    print('vsw min',np.min(nsw))


  return date,time,nsw,tk,teV,vswx,vswy,vswz


def read_GEK0CPI(fi,vtype='string'):
  "read Geotail CPI data"

  Err = '-1.00000E+31'

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

  lda=ldaf(fi)
  
  print("===============  CLEAN ALL UNNECESSARY INFORMATION  ===============")
  print("REMOVE ALL HEADERS BEFORE")
  print(l[lda])
  del   l[:lda]
  print("REMOVE ALL THE FOLLOWING TAILS ")
  print(l[-4:])
  del   l[-4:]
  print("-------------------------------------------------------------------")
  print("THE FIRST & LAST DATA LINES ARE")
  print(l[0])
  print(l[-1])
  print("===================================================================")

  date=[];time=[];nsw=[];tsw=[];nhp=[];thp=[];php=[];
  vswx=[];vswy=[];vswz=[];vhpx=[];vhpy=[]

  for s in l:
    w=s.split(None)
    if len(w)>2  and w[2]!=Err and w[3]!=Err  and w[4]!=Err  and  \
       w[5]!=Err and w[9]!=Err and w[10]!=Err and w[11]!=Err      :

      date.append(w[0])
      time.append(w[1])
      nsw.append(w[2])
#     tsw.append(locale.format('%f',locale.atof(w[3])*11600.))	# convert eV to K
      tsw.append(w[3])
      nhp.append(w[4])
#     thp.append(locale.format('%f',locale.atof(w[5])*11600.))  # convert eV to K
      thp.append(w[5])
      php.append(locale.format('%f',locale.atof(w[6])*1e9))	# pressure in  nP
      vswx.append(w[7])
      vswy.append(w[8])
      vswz.append(w[9])
      vhpx.append(w[10])
      vhpy.append(w[11])

  if vtype=='real':
    nsw  = [locale.atof(i) for i in nsw ]
    tsw  = [locale.atof(i) for i in tsw ]	# convert eV to K
    nhp  = [locale.atof(i) for i in nhp ]
    thp  = [locale.atof(i) for i in thp ]	# convert eV to K
    php  = [locale.atof(i) for i in php ]
    vswx = [locale.atof(i) for i in vswx ]
    vswy = [locale.atof(i) for i in vswy ]
    vswz = [locale.atof(i) for i in vswz ]
    vhpx = [locale.atof(i) for i in vhpx ]
    vhpy = [locale.atof(i) for i in vhpy ]

  return date,time,nsw,tsw,nhp,thp,php,vswx,vswy,vswz,vhpx,vhpy


def create_GEH0data(sc,fi1,fi2,lda1,lda2,t1,t2,t3,t4,av):
  "interpolate Geotail MGF and CPI data"

## interpolate Geotail data every av seconds between t1 and t2
  name = ['bxgse','bygse','bzgse','xgse','ygse','zgse', \
          'nsw','tsw','vswx','vswy','vswz' ]
  fo   = [ sc+'.'+i for i in name ]

  date1,time1,bx,by,bz,xl,yl,zl                            = read_GEMGF(fi1,lda1)
  date2,time2,nsw,tsw,vswx,vswy,vswz                       = read_GEH0CPI(fi2,lda2)

  date = [date1,date1,date1,date1,date1,date1,date2,date2,date2,date2,date2]
  time = [time1,time1,time1,time1,time1,time1,time2,time2,time2,time2,time2]
  vv   = [bx,by,bz,xl,yl,zl,nsw,tsw,vswx,vswy,vswz]

  for i in range(len(date)) :
    interpolate_data(fo[i],t1,t2,av,date[i],time[i],vv[i])

## create orbit, the OpenGGCU input starting from t3
  name = ['xgse','ygse','zgse' ]
  fo   = [ sc+'.'+i for i in name ]
  create_GEorbit(fo,sc+'.GSEorbit',t1,t2,t3,t4)
  return


def create_GEK0data(sc,fi1,fi2,lda1,lda2,t1,t2,t3,t4,av):
  "interpolate Geotail MGF and CPI data"

## interpolate Geotail data every av seconds between t1 and t2
  name = ['bxgse','bygse','bzgse','xgse','ygse','zgse', \
          'nsw','tsw','nhp','thp','php','vswx','vswy','vswz','vhpx','vhpy'  ]
  fo   = [ sc+'.'+i for i in name ]

  date1,time1,bx,by,bz,xl,yl,zl                            = read_GEMGF(fi1,lda1)
  date2,time2,nsw,tsw,nhp,thp,php,vswx,vswy,vswz,vhpx,vhpy = read_GECPI(fi2,lda2)

  date = [date1,date1,date1,date1,date1,date1,date2,date2,date2,date2,date2,date2]
  time = [time1,time1,time1,time1,time1,time1,time2,time2,time2,time2,time2,time2]
  vv   = [bx,by,bz,xl,yl,zl,nsw,tsw,nhp,thp,php,vswx,vswy,vswz,vhpx,vhpy]

  for i in range(len(date)) :
    interpolate_data(fo[i],t1,t2,av,date[i],time[i],vv[i])

## create orbit, the OpenGGCU input starting from t3
  name = ['xgse','ygse','zgse' ]
  fo   = [ sc+'.'+i for i in name ]
  create_GEorbit(fo,sc+'.GSEorbit',t1,t2,t3,t4)
  return


def create_GEorbit(fi,fo,t1,t2,t3,t4):
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
  fmt = "%10.2f %8.4f %8.4f %8.4f\n"

  for i in range(len(fi)):
    x=read_tseries(fi[i],tt1,tt2)
    if i==0: vv.append(x[6])
    vv.append(x[7])

  f=open(fo,'w')
  for j in range(len(vv[0])):
   if vv[0][j] >=tt3 and vv[0][j]<=tt4:
     t=(vv[0][j]-tt3)
     ll = fmt%(t,vv[1][j],vv[2][j],vv[3][j])
     f.write(ll)
  f.close()
  return


def main(argv):

  sc=argv[0]                    # satellite info
  f1=argv[1]                    #MFI data: date time bxgse bygse bzgse
  f2=argv[2]                    #SWE data: date time vth rr xgse ygse zgse vxgse vygse vzgse
  t1=argv[3]                    #starttime for interpolation
  t2=argv[4]                    #endtime   for interpolation
  t3=argv[5]                    #starttime for MHD simulation
  t4=argv[6]                    #endtime   for MHD simulation
  av=argv[7]                    #time interval of interpolation in sec

  lda=argv[8].split(':')        #the line where data starts
  lda1=locale.atoi(lda[0])-1
  lda2=locale.atoi(lda[1])-1

  print(lda,lda1,lda2)

  create_GEdata(sc,f1,f2,lda1,lda2,t1,t2,t3,t4,av)


  return


if __name__=='__main__':
   main(sys.argv[1:])
