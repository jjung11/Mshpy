#!/usr/bin/python
# read WIND MFI and SWE data
# read ACe MFI and SWE data

import os
import sys
HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/lib/")


import locale
import matplotlib.pyplot as plt
from jrmod01  		import *
from numpy		import arange
from openggcm_info 	import mhdtime,mhdt2hrmi

def ldaf(filename):
    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if line.startswith('dd'):
                lda=num
#                print ('found at line:', num)
    return lda

def read_GE(fi,lda,setbx=9999.99):
  "read Geotail data 								"

  BXerr=9999.99
  BErr='9999.99'                        # err of B field
  VErr='99999.9'                        # err of Velocity
  NErr='999.99'                         # err of Number density
  TErr='9999999.'                       # err of Temparature
  LErr='9999.99'                        # err of Satellite Location
  re  = 6.37814e3

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

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
  vx=[];vy=[];vz=[]
  xx=[];yy=[];zz=[]
  nn=[];pp=[];tk=[]

  for s in l:
    w=s.split(None)

    if w[2]!=BErr  and w[3]!=BErr  and w[4]!=BErr  and \
       w[5]!=VErr  and w[6]!=VErr  and w[7]!=VErr  and \
       w[8]!=NErr  and w[9]!=TErr  and			\
       w[10]!=LErr and w[11]!=LErr and w[12]!=LErr :

       date.append(w[0])
       time.append(w[1])

       print(setbx)
       if setbx==BXerr  : bx.append(w[2])
       else             : bx.append(str(setbx))
       by.append(w[3])
       bz.append(w[4])

       vx.append(w[5])
       vy.append(w[6])
       vz.append(w[7])

       nn.append(w[8])
       tk.append(w[9])

       print(w[8])
       nn1=locale.atof(w[8])
       tk1=locale.atof(w[9])
       pp1=nn1*1e6*tk1*1.380654e-23*1e12
       pp.append(locale.format('%f',pp1))

       xx.append(w[10])
       yy.append(w[11])
       zz.append(w[12])

  return  date,time,bx,by,bz,vx,vy,vz,nn,pp,tk,xx,yy,zz


def read_ACMFI(fi,lda,setbx=9999.99) :
  "read ACE MFI data                                                            \
   fi     : ACE/MFI data in the following order                                 \
            [ date,time,bx,by,bz,xx,yy,zz ]                                     \
   lda    : line number where data started                                      \
   setbx  : input setbx into IMF bx if setbx!=99999                             "


  BXerr=9999.99
  Err = '-1.00000E+31'
  re  = 6.37814e3

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

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
      if setbx==BXerr:  bx.append(w[2])
      else           :  bx.append(str(setbx))
      by.append(w[3])
      bz.append(w[4])

      x1=locale.format('%f',locale.atof(w[5])/re)
      y1=locale.format('%f',locale.atof(w[6])/re)
      z1=locale.format('%f',locale.atof(w[7])/re)
      xl.append(w[5])
      yl.append(w[6])
      zl.append(w[7])

  return date,time,bx,by,bz,xl,yl,zl


def read_ACSWE(fi,lda) :
  " read ACE SWE data only if all plasma data are not Err values             	\
    fi  : ACE/SWE data in the following order                                  	\
          [ date,time,np,Tk,vxgse,vygse,vzgse ]                 		\
    lda : the line number where data starts                                     "

  Err = '-1.00000E+31'

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

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
  np=[];pp=[];tk=[]
  vx=[];vy=[];vz=[];

  for s in l:
    w=s.split(None)
    if len(w)>2  and w[2]!=Err and w[3]!=Err and  \
       w[4]!=Err and w[5]!=Err and w[6]!=Err      :

      date.append(w[0])
      time.append(w[1])
      np.append(w[2])
      vx.append(w[4])
      vy.append(w[5])
      vz.append(w[6])

      np1=locale.atof(w[2])
      tk1=locale.atof(w[3])
      tk2=tk1*1.380654e-23/1.602176e-19
      pp1=np1*1e6*tk1*1.380654e-23*1e12
      pp.append(locale.format('%f',pp1))
      tk.append(locale.format('%f',tk2))

  return date,time,np,pp,tk,vx,vy,vz


def read_allACSWE(fi,lda) :
  " read all available non-Err ACE SWE data                                     \
    fi  : ACE/SWE data in the following order                                   \
          [ date,time,np,Tk,vxgse,vygse,vzgse ]                                 \
    lda : the line number where data starts                                     "

  ERR = '-1.00000E+31'

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

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

  ddnp=[];ddpp=[];ddtk=[];ddvx=[];ddvy=[];ddvz=[]
  ttnp=[];ttpp=[];tttk=[];ttvx=[];ttvy=[];ttvz=[]
  np=[];pp=[];tk=[]
  vx=[];vy=[];vz=[];

  for s in l:
    w=s.split(None)
    if len(w)>2 :
      if w[2]!=ERR: ddnp.append(w[0]);ttnp.append(w[1]);np.append(w[2])
      if w[4]!=ERR: ddvx.append(w[0]);ttvx.append(w[1]);vx.append(w[4])
      if w[5]!=ERR: ddvy.append(w[0]);ttvy.append(w[1]);vy.append(w[5])
      if w[6]!=ERR: ddvz.append(w[0]);ttvz.append(w[1]);vz.append(w[6])
      if w[3]!=ERR:
        tk1=locale.atof(w[3])
        tk2=tk1*1.380654e-23/1.602176e-19
        ddtk.append(w[0]);tttk.append(w[1])
        tk.append(locale.format('%f',tk2))
        if w[2]!=ERR:
          np1=locale.atof(w[2])
          pp1=np1*1e6*tk1*1.380654e-23*1e12
          ddpp.append(w[0]);ttpp.append(w[1])
          pp.append(locale.format('%f',pp1))
  date=[ddnp,ddpp,ddtk,ddvx,ddvy,ddvz]
  time=[ttnp,ttpp,tttk,ttvx,ttvy,ttvz]
  return date,time,np,pp,tk,vx,vy,vz

def read_WIMFI(fi,lda,setbx=9999.99) :
  "read WIND MFI data								\
   fi     : WIND/MFI data in the following order 				\
            [ date,time,bx,by,bz ]						\
   lda    : line number where data started					\
   setbx  : input setbx into IMF bx if setbx!=99999				"

  BXerr=9999.99
  Err='-1.00000E+31'

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

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

  for s in l:
    w=s.split(None)
    if len(w)>=2 and w[2]!=Err and w[3]!=Err and w[4]!=Err:
      date.append(w[0])
      time.append(w[1])
      if setbx==BXerr:  bx.append(w[2])
      else           :  bx.append(str(setbx))
      by.append(w[3])
      bz.append(w[4])

  return date,time,bx,by,bz


def read_WISWE(fi,lda):
  " read WIND SWE data 								\
    fi  : WIND/SWE data in the following order					\
          [ date,time,vth,np,xgse,ygse,zgse,vxgse,vygse,vzgse ]			\
    lda : the line number where data starts					\
    ----------------------------------						\
    CHANGES: As of Jul 14 2016, SWE data format changes, including DEL_TIME.	\
             [date,time,vth,np,DEL_TIME,xgse,ygse,zgse,vxgse,vygse,vzgse]    	\
             For swdata calculation, DEL_TIME is ignored 			"


  Err='-1.00000E+31'
  re=6.37814e3

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

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
  th=[];np=[];pp=[]
  xl=[];yl=[];zl=[]
  vx=[];vy=[];vz=[]

  print(len(l))
  for s in l:
    w=s.split(None)
    if len(w)>2 and 						\
       w[2]!=Err and w[3]!=Err and w[4]!=Err and w[5]!=Err and 	\
       w[6]!=Err and w[7]!=Err and w[8]!=Err and w[9]!=Err      :

      date.append(w[0])
      time.append(w[1])

      th.append(w[2])	# thermal velocity
      np.append(w[3])

      x1=locale.atof(w[5])/re
      y1=locale.atof(w[6])/re
      z1=locale.atof(w[7])/re
      xl.append(locale.format('%f',x1))
      yl.append(locale.format('%f',y1))
      zl.append(locale.format('%f',z1))

      vx.append(w[8])
      vy.append(w[9])
      vz.append(w[10])

# calculate thermal pressure
# Note that OpenGGCM needs THERMAL pressure, not DYNAMIC pressure

      th1  = locale.atof(w[2])
      np1  = locale.atof(w[3])
      pp1  = np1*1e6*(th1*1e3)**2*1.672614e-27/2*1e12

      pp.append(locale.format('%f',pp1))

  return date,time,th,np,xl,yl,zl,vx,vy,vz,pp


def read_THFGM(fi, lda,setbx=9999.99):
  "read THEMIS FGM data                                                           \
   fi     : THEMIS FGM data in the following order                                \
            [ date,time,Btot_goodquality,Btot_allquality,UT_seconds,bxgse_good,bygse_good,bzgse_good ]     \
   lda    : line number where data started                                      \
   setbx  : input setbx into IMF bx if setbx!=99999                             "

  BXerr=9999.99
  Err='-1.00000E+31'

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

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

  for s in l:
    w=s.split(None)
    if len(w)>=2 and w[2]!=Err and w[3]!=Err and w[4]!=Err:
      date.append(w[0])
      time.append(w[1])
      if setbx==BXerr:  bx.append(w[5])
      else           :  bx.append(str(setbx))
      by.append(w[6])
      bz.append(w[7])

  return date,time,bx,by,bz


def read_THESA(fi,lda):
  " read THEMIS ESA data                                                          \
    fi  : WIND/SWE data in the following order                                  \
          [ date,time,vth,np,xgse,ygse,zgse,vxgse,vygse,vzgse ]                 \
    lda : the line number where data starts                                     \
    ----------------------------------                                          \
    CHANGES: As of Jul 14 2016, SWE data format changes, including DEL_TIME.    \
             [date,time,vth,np,DEL_TIME,xgse,ygse,zgse,vxgse,vygse,vzgse]       \
             For swdata calculation, DEL_TIME is ignored                        "


  Err='-1.00000E+31'
  re=6.37814e3

  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

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
  np=[];pp=[];tk=[];teV=[]
  vx=[];vy=[];vz=[]

  print(len(l))
  for s in l:
    w=s.split(None)
    if len(w)>2 and                                             \
       w[2]!=Err and w[3]!=Err and w[4]!=Err and w[5]!=Err and  \
       w[6]!=Err and w[7]!=Err and w[8]!=Err and w[9]!=Err      :

      date.append(w[0])
      time.append(w[1])

      np.append(w[2])
      teV.append(w[3])
      vx.append(w[6])
      vy.append(w[7])
      vz.append(w[8])

# calculate thermal pressure
# Note that OpenGGCM needs THERMAL pressure, not DYNAMIC pressure

      np1  = locale.atof(w[2])
      tk1  = locale.atof(w[3])*11600.
      pp1  = tk1*np1/72429.
      tk.append(locale.format('%f',tk1))
      pp.append(locale.format('%f',pp1))

  return date,time,np,pp,tk,vx,vy,vz


  return

def read_omni(fi,lda,setbx=9999.99):

  BXerr=9999.99
  BErr='9999.99'			# err of B field
  VErr='99999.9'			# err of Velocity
  NErr='999.99'				# err of Number density
  TErr='9999999.'			# err of Temparature
  LErr='9999.99'			# err of Satellite Location

  print("READ ",fi)
  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

  print("===============  CLEAN ALL UNNECESSARY INFORMATION  ===============")
  print("REMOVE ALL HEADERS BEFORE")
  print(l[lda])
  del   l[:lda]
#  print("REMOVE ALL THE FOLLOWING TAILS ")
#  print(l[-4:])
#  del   l[-4:]
  print("-------------------------------------------------------------------")
  print("THE FIRST & LAST DATA LINES ARE")
  print(l[0])
  print(l[-1])
  print("===================================================================")


  dateb=[]
  timeb=[]
  datev=[]
  timev=[]
  datel=[]
  timel=[]
  bx=[];by=[];bz=[]
  vx=[];vy=[];vz=[]
  xx=[];yy=[];zz=[]
  nn=[];tk=[];pp=[]


  for s in l:

    w=s.split(None)
    if len(w)>2 :

     yr1=locale.atoi(w[0])
     dy1=locale.atoi(w[1])
     hh1=locale.atoi(w[2])
     mi1=locale.atoi(w[3])

     mm1,dd1=dayofyear2date(yr1,dy1)

     date1='%02d-%02d-%04d'%(dd1,mm1,yr1)
     time1='%02d:%02d:0.0'%(hh1,mi1)

     print(date1,time1)

     if w[4]!=BErr and w[5]!=BErr and w[6]!=BErr:
       dateb.append(date1)
       timeb.append(time1)
       if setbx==BXerr: bx.append(w[4])
       else           : bx.append(str(setbx))
       by.append(w[5])
       bz.append(w[6])


     if  w[7] !=VErr and w[8] !=VErr and w[9] !=VErr and  \
         w[10]!=NErr and w[11]!=TErr                      :

       datev.append(date1)
       timev.append(time1)

       vx.append(w[7])
       vy.append(w[8])
       vz.append(w[9])

       nn.append(w[10])
       tk.append(w[11])

       nn1=locale.atof(w[10])
       tk1=locale.atof(w[11])
       pp1=nn1*1e6*tk1*1.380654e-23*1e12
       pp.append(locale.format('%f',pp1))


     if  w[12]!=LErr and w[13]!=LErr and w[14]!=LErr :
       datel.append(date1)
       timel.append(time1)
       xx.append(w[12])
       yy.append(w[13])
       zz.append(w[14])

  return  dateb,timeb,bx,by,bz,datev,timev,vx,vy,vz,nn,pp,tk,datel,timel,xx,yy,zz



def dayofyear2date(yy,dy):
  "convert day of year to date: 2005:135 -> 2005:05:15"

  if yy%4==0 : day=[31,29,31,30,31,30,31,31,30,31,30,31]
  else       : day=[31,28,31,30,31,30,31,31,30,31,30,31]


  for i in range(len(day)):
    if dy < day[0] :
      mm=1
      break

    dy=dy-day[i]

    if dy < day[i+1] :
      mm=i+2
      break

  return mm,dy


def main():

  yy=2005
  dy=135

  mm,dd=dayofyear2date(2005,135)

  print("year, dayofyear :",yy,dy)
  print("year, month, day:",yy,mm,dd)

  return


if __name__=='__main__':

  main()
