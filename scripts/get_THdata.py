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

def ldaf(filename):
    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if line.startswith('dd'):
                lda=num
#                print ('found at line:', num)
    return lda


def read_THFGM(fi,vtype='string'):
  "read THEMIS FGM data downloaded from SPDweb"

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
#  xl=[];yl=[];zl=[]

  for s in l:
    w=s.split(None)
    if len(w)>2  and w[2]!=Err and w[3]!=Err and w[4]!=Err  :

      date.append(w[0])
      time.append(w[1])
      bx1=locale.format('%f',locale.atof(w[2]))
      by1=locale.format('%f',locale.atof(w[3]))
      bz1=locale.format('%f',locale.atof(w[4]))
      bx.append(bx1)
      by.append(by1)
      bz.append(bz1)
#      x1=locale.format('%f',locale.atof(w[5])/re)
#      y1=locale.format('%f',locale.atof(w[6])/re)
#      z1=locale.format('%f',locale.atof(w[7])/re)
#      xl.append(x1)
#      yl.append(y1)
#      zl.append(z1)

  if vtype=='real':
    bx = [locale.atof(i) for i in bx ]
    by = [locale.atof(i) for i in by ]
    bz = [locale.atof(i) for i in bz ]
#    xl = [locale.atof(i) for i in xl  ]
#    yl = [locale.atof(i) for i in yl  ]
#    zl = [locale.atof(i) for i in zl  ]

  return date,time,bx,by,bz

def read_THorbit(fi,lda,vtype='string'):
  "read THEMIS orbit data downloaded from SPDweb"

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
#  xl=[];yl=[];zl=[]

  for s in l:
    w=s.split(None)
    if len(w)>2  and w[2]!=Err and w[3]!=Err and w[4]!=Err  :

      date.append(w[0])
      time.append(w[1])
      bx1=locale.format('%f',locale.atof(w[2]))
      by1=locale.format('%f',locale.atof(w[3]))
      bz1=locale.format('%f',locale.atof(w[4]))
      bx.append(bx1)
      by.append(by1)
      bz.append(bz1)
#      x1=locale.format('%f',locale.atof(w[5])/re)
#      y1=locale.format('%f',locale.atof(w[6])/re)
#      z1=locale.format('%f',locale.atof(w[7])/re)
#      xl.append(x1)
#      yl.append(y1)
#      zl.append(z1)

  if vtype=='real':
    bx = [locale.atof(i) for i in bx ]
    by = [locale.atof(i) for i in by ]
    bz = [locale.atof(i) for i in bz ]
#    xl = [locale.atof(i) for i in xl  ]
#    yl = [locale.atof(i) for i in yl  ]
#    zl = [locale.atof(i) for i in zl  ]

  return date,time,bx,by,bz


def read_THESA(fi,vtype='string'):
  "read THEMIS ESA data"

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
      teV.append(w[3])
#      teV.append(locale.format('%f',locale.atof(w[2])/11600.))  # convert K to eV
      tk.append(w[3])
      nsw.append(w[2])
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

  return date,time,nsw,teV,vswx,vswy,vswz

def read_THESAr(fi,vtype='string'):
  "read THEMIS ESA data- number density and temperature from reduced data"

  lda=ldaf(fi)


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

  date=[];time=[];nsw=[];tk=[];teV=[];nhp=[];thp=[];php=[];
  vswx=[];vswy=[];vswz=[];vhpx=[];vhpy=[]

  for s in l:
    w=s.split(None)
    if len(w)>2  and w[2]!=Err and w[3]!=Err:

      date.append(w[0])
      time.append(w[1])
      tk.append(w[3])
      nsw.append(w[2])

  if vtype=='real':
    nsw  = [locale.atof(i) for i in nsw ]
    tk   = [locale.atof(i) for i in tk  ]

  return date,time,nsw,tk



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
