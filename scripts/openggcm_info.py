#!/usr/bin/python
# openggcm modules

import os
import sys
HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/lib/")

import locale
import matplotlib.pyplot as     plt
from   run_info          import openggcm_run
from   datetime         import datetime,timedelta

class mhdtime(object):
  "create class of mhdtime for easy access"

  def __init__(self,t_str) :
      self.tstr=t_str
      w=self.tstr.split(':')

      self.yy=locale.atoi(w[0])
      self.mm=locale.atoi(w[1])
      self.dd=locale.atoi(w[2])
      self.hr=locale.atoi(w[3])
      self.mi=locale.atoi(w[4])
      self.se=locale.atof(w[5])


      Mon  = ['Jan','Feb','Mar','Apr','May','Jun', \
              'Jul','Aug','Sep','Oct','Nov','Dec']

      self.date  = '%02d-'%self.dd+Mon[self.mm-1]+'-%04d'%self.yy
      self.time  = '%02d:%02d UT'%(self.hr,self.mi)
      self.name  = self.date+' '+self.time
      self.mdate = '%04d'%self.yy+Mon[self.mm-1]+'%02d'%self.dd
      return


class runinfo(object):
  "read run name, data type (iof,ioc,3df,etc.), and mhdtime from filename   	\
   ex. name='iof.hjk2001/hjk2001.iof.003600'				    	\
       name.dir = 'iof.hjk2001' 					    	\
       name.run = 'hjk2001'						    	\
       name.type= 'iof'								\
       name.mhdt= '003600'							\
       self.ti  = '1967:01:01:00:00:0.0' :start time of mhdrun			"

  def __init__(self,fname):
   self.fname=fname

   s1        = fname.split('/')
   s2        = s1[-1].split('.')

   ll=' '
   for i in range(len(s1)-1) : ll=ll+s1[i]+'/'

   self.dir  = ll
   self.name = s1[-1]
   self.run  = s2[0]
   self.type = s2[1]
   self.mhdt = s2[2]

   times     = openggcm_run(self.run)
   #print(times)
   self.ti   = times[0]
   self.tf   = times[1]
   self.dipt = times[2]
   tstr      = [ int(locale.atof(i)) for i in self.ti.split(':') ]
   tmhd0     = datetime(tstr[0],tstr[1],tstr[2],tstr[3],tstr[4],tstr[5] )
   tstr1     = [ int(locale.atof(i)) for i in self.tf.split(':') ]
   tmhd1     = datetime(tstr1[0],tstr1[1],tstr1[2],tstr1[3],tstr1[4],tstr1[5] )
   self.dur  = (tmhd1-tmhd0).total_seconds()
#   print(self.dur)

   tstrs     = mhdtime(self.ti)
   self.date = tstrs.date
   self.time = tstrs.time
   self.ddtt = tstrs.name
   self.mdate= tstrs.mdate

   return



def mhdt2tstr(mhdt,starttime):
  "convert mhdt to time string.                                                 \
   ex: convert 010800 to 1967:01:01:03:00:0.0 if startime=1967:01:01:00:00:0.0  "

  time=mhdtime(starttime)

  ay = int(mhdt/364)

  a1 = int(mhdt/3600)
  a2 = int(mhdt%3600)/60

  yy = time.yy
  mm = time.mm
  dd = time.dd
  hr = time.hr+a1
  mi = time.mi+a2
  se = time.se+mhdt%60.


  if yy%4 == 0    : Mon = [31,29,31,30,31,30,31,31,30,31,30,31]
  else            : Mon = [31,28,31,30,31,30,31,31,30,31,30,31]

  if se>=60       : se=se-60 ; mi=mi+1
  if mi>=60       : mi=mi-60 ; hr=hr+1
  if hr>=24       : d1=int(hr/24);hr=hr-24*d1 ; dd=dd+d1
  if dd>Mon[mm-1] : dd=1     ; mm=mm+1
  if mm>12        : mm=1     ; yy=yy+1


  tstr="%4d:%02d:%02d:%02d:%02d:%05.2f"%(yy,mm,dd,hr,mi,se)

  return tstr


def mhdt2tstr(mhdt,starttime):
  "convert mhdt to time string.							\
   ex: convert 010800 to 1967:01:01:03:00:0.0 if startime=1967:01:01:00:00:0.0	"

  time=mhdtime(starttime)

  a1 = int(mhdt/3600)
  a2 = int(mhdt%3600)/60

  yy = time.yy
  mm = time.mm
  dd = time.dd
  hr = time.hr+a1
  mi = time.mi+a2
  se = time.se+mhdt%60.


  if yy%4 == 0    : Mon = [31,29,31,30,31,30,31,31,30,31,30,31]
  else            : Mon = [31,28,31,30,31,30,31,31,30,31,30,31]

  if se>=60       : se=se-60 ; mi=mi+1
  if mi>=60       : mi=mi-60 ; hr=hr+1
  if hr>=24       : d1=int(hr/24);hr=hr-24*d1 ; dd=dd+d1
  if dd>Mon[mm-1] : dd=1     ; mm=mm+1
  if mm>12	  : mm=1     ; yy=yy+1


  tstr="%4d:%02d:%02d:%02d:%02d:%05.2f"%(yy,mm,dd,hr,mi,se)

  return tstr


def tstr2mhdt(tstr,starttime):
  "convert tstr to mhdt time							\
   ex: convert 1999:01:01:01:00:0.0 to 3600 if starttime=1999:01:01:00:00:0.0	"

  tt1=epo1c(starttime)
  tt2=epo1c(tstr)
  mhdt=tt2-tt1
  return mhdt


def grep_swdata(fsw,tsh,info):
  "read solar wind data for your taste"
  ftest=fsw.split('/')
  if ftest[-1]=='in.'+info.run:
    tsw,sw     = read_swdata(fsw,tsh)
    swtype     = 'input'
    vstr_add   = ' : OpenGGCM Input'
  elif ftest[-1]=='swdata.omni':
    tsw,sw     = read_swomni(fsw,0.)
    swtype     = 'OMNI'
    vstr_add   = ' : OMNI data'
  else :
    tsw,sw     = read_timehist(fsw,'SW-01',120)
    vstr_add   = ' at (16,16,16) Re'
    swtype     = 'SW01'
  return tsw,sw,swtype,vstr_add


def read_swomni(fi,tsh):
  "read swdata"

  pm=1.672614e-27               # proton mass
  f=open(fi,'r')
  l=f.read().split('\n')
  f.close()

  tt=[];rr=[];pp=[]
  bx=[];by=[];bz=[]
  vx=[];vy=[];vz=[]
  pd=[];symh=[]

  for s in l:
    w=s.split(None)
    if len(w)>2:

      tt.append(locale.atof(w[0])*60.+tsh)
      bx.append(locale.atof(w[1]))
      by.append(locale.atof(w[2]))
      bz.append(locale.atof(w[3]))
      vx.append(locale.atof(w[4]))
      vy.append(locale.atof(w[5]))
      vz.append(locale.atof(w[6]))
      rr.append(locale.atof(w[7]))
      pp.append(locale.atof(w[8]))
      vx1=locale.atof(w[4])
      vy1=locale.atof(w[5])
      vz1=locale.atof(w[6])
      rr1=locale.atof(w[7])
      pd1=(vx1**2+vy1**2+vz1**2)*rr1*pm*1.e21    # dynamic pressure in nPa: rho v**2
      pd.append(pd1)
      symh.append(locale.atof(w[9]))

  vv=[bx,by,bz,vx,vy,vz,rr,pp,pd,symh]
  return tt,vv



def read_swdata(fi,tpush=0):
  "read swdata from in.$RUN 						\
   tpush : shifted time in seconds to account for solar wind propagation "

  test0=fi.split('/')
  test1=test0[-1].split('.')
  if test1[0]=='in' : wlen=13
  else              : wlen=12

  pm=1.672614e-27 		# proton mass
  f = open(fi,'r')
  l = f.read().split('\n')
  f.close()

  i=0
  tt=[];rr=[];pp=[];pd=[]
  bx=[];by=[];bz=[];bt=[]
  vx=[];vy=[];vz=[];vt=[];fl=[]

  for s in l :

   w=s.split(None)

   if len(w)==wlen:
      tt1=locale.atof(w[0])*60.+tpush
      bx1=locale.atof(w[1])
      by1=locale.atof(w[2])
      bz1=locale.atof(w[3])
      vx1=locale.atof(w[4])
      vy1=locale.atof(w[5])
      vz1=locale.atof(w[6])
      rr1=locale.atof(w[7])
      pp1=locale.atof(w[8])
      bt1=(bx1**2+by1**2+bz1**2)**0.5
      vt1=(vx1**2+vy1**2+vz1**2)**0.5
#     pd1=1./2.*pm*rr1*(vx1**2+vy1**2+vz1**2)*1.e21  	# dynamic pressure in nPa: rho v**2/2
#     pd1=pm*rr1*(vx1**2+vy1**2+vz1**2)*1.e21  		# dynamic pressure in nPa: rho v**2
      pd1=(vx1**2+vy1**2+vz1**2)*rr1*pm*1.e21		# dynamic pressure in nPa: rho v**2
      fl1=vt1*rr1*1e5
      tt.append(tt1)
      bx.append(bx1)
      by.append(by1)
      bz.append(bz1)
      bt.append(bt1)
      vx.append(vx1)
      vy.append(vy1)
      vz.append(vz1)
      vt.append(vt1)
      rr.append(rr1)
      pp.append(pp1)
      pd.append(pd1)
      fl.append(fl1)

  swdata=[bx,by,bz,vx,vy,vz,rr,pp,pd,bt,vt,fl]
  return tt,swdata


def mhdt2hrmi(ticks,time,tint):
  "create labels for mhdtimes in \"hr:mi\" format.                              \n \
   tcks : tick locations                                                       \n \
   time  : class mhdtime                                                        \n \
   tint  : interval between tick labels                                         \n "

  labels=[]

  for x in ticks :

    if (x-ticks[0])%tint==0 :
      a1 = int(x/3600)
      a2 = int(x%3600)/60

      hr = time.hr+a1
      mi = time.mi+a2

      while (mi >= 60): hr = hr + 1 ; mi = mi-60
      while (hr >= 24): hr = hr -24

      fmt ='%02d:%02d'%(hr,mi)

    else         :
      fmt = ' '

    labels.append(fmt)

  return labels


def epo1c(c):
  w=c.split(':')
  return(epo1(locale.atoi(w[0]),
              locale.atoi(w[1]),
              locale.atoi(w[2]),
              locale.atoi(w[3]),
              locale.atoi(w[4]),
              locale.atof(w[5])))

def epo1(iy,mo,id,ih,mi,se):
  if iy < 200 : iy = 1900 + iy
  i1=367*iy
  i2=int((mo+9)/12)
  i2=(i2+iy)*7
  i2=int(i2/4)
  i3=int((275*mo)/9)
  i4=100*iy+mo
  d1=(1.0)
  if (i4-190002.5) < 0.0 : d1=(-1.0)
  rr = ( i1 - i2 + i3 + id + 1721013.5 -0.5*d1 +0.5 )*86400.0
  rr = rr + 3600.0*ih + 60.0*mi +se
  return(rr)


def fdoy2time(yr,fr):
  "convert fraction of DOY (day of year) to yyyy:mm:dd:hr:mi:se    \
   (yr,fr) = (2005,134.00)  --->  2005:05:15:00:00:0.0) "

  dy    = int(fr)
  mm,dd = doy2date(yr,dy)
  fr    = (fr-dy)*86400.
  hr    = int(fr/3600.)
  mi    = int((fr-hr*3600.)/60.)
  se    = fr-hr*3600.-mi*60.
  ctime = "%04d:%02d:%02d:%02d:%02d:%05.2f"%(yr,mm,dd,hr,mi,se)
  return ctime


def time2fdoy(ctime):
  "convert yyyy:mm:dd:hr:mi:se to fraction of day"

  tt   = ctime.split(':')
  yy   = locale.atoi(tt[0])
  mm   = locale.atoi(tt[1])
  dd   = locale.atoi(tt[2])
  hr   = locale.atoi(tt[3])
  mi   = locale.atoi(tt[4])
  se   = locale.atof(tt[5])

  doy  = date2doy(yy,mm,dd)
  fr   = doy+hr/24.+mi/24./60.+se/24./60./60.
  return yy,fr


def doy2date(yy,dy):
  "convert day of year (DOY) to date"

  if yy%4==0 : day=[31,29,31,30,31,30,31,31,30,31,30,31]
  else       : day=[31,28,31,30,31,30,31,31,30,31,30,31]

  for i in range(len(day)):
    if dy <= day[i] : break
    else            : dy=dy-day[i]
  mm=i+1
  return mm,dy


def date2doy(yy,mm,dd):
  "convert date to day of year"

  if yy%4==0 : day=[31,29,31,30,31,30,31,31,30,31,30,31]
  else       : day=[31,28,31,30,31,30,31,31,30,31,30,31]

  doy=0
  for i in range(mm-1): doy=doy+day[i]
  doy=doy+dd

  return doy


def main():
  "test functions"

  tstr = "1998:01:10:23:48:33.0"
  time = mhdtime(tstr)

  print ("test class mhdtime")
  print (time.yy,time.mm,time.dd,time.hr,time.mi,time.se)
  print (time.date,time.time,time.name)


  name = "iof.djl00703a/djl00703a.iof.013200"
  info = runinfo(name)
  print (info.run,info.type,info.mhdt,info.dir,info.name)


  starttime = "1995:02:28:00:00:25.0"
  timestr   = mhdt2tstr(60*60*24+3663,starttime)
  print (timestr)

  starttime = "1996:02:28:00:00:0.0"
  timestr   = mhdt2tstr(60*60*24+3660,starttime)
  print (timestr)

  starttime = "1996:12:31:00:00:0.0"
  timestr   = mhdt2tstr(60*60*24+3660,starttime)
  print (timestr)

  starttime = "1996:12:31:00:00:0.0"
  mhdt      = tstr2mhdt('1996:12:31:03:00:0.0',starttime)
  print (mhdt)

  starttime = "1998:01:01:00:00:0.0"
  timestr      = mhdt2tstr(1.6844600e+08,starttime)
  print (timestr)


if __name__=="__main__":
  main()
