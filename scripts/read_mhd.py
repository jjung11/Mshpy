#!/usr/bin/python
#
# draw MHD plots

import os
import sys
HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/lib/")

import locale
from numpy 		import ndarray,nan,cos,sin,radians
from pkg_rates        import rate_vpkg


def create_mhdPN(fmhd,fgrd,fpn,dipt,pn,xi,xf,yi,yf,ds):
  "create mhd from px,py,pz files"
  EXE = HOME+"/svn/hkc-project/trunk/src/mhd-openggcm/read_pxyz"
  OP  = "-xi %6.1f -xf %6.1f -yi %6.1f -yf %6.1f -ds %6.1f -pn "%(xi,xf,yi,yf,ds)+pn
  cmd = EXE+" -fout "+fmhd+" -fin "+fpn+" -grid "+fgrd+" -diptime "+dipt+" "+OP
  print  (cmd)
  os.system(cmd)
  return


def create_mhd(fmhd,fgrd,f3df,dipt,pn,lp,xi,xf,yi,yf,ds):
  "create mhd from 3df files"
  EXE = HOME+"/svn/hkc-project/trunk/src/mhd-openggcm/read_2DMHD"
  OP  = "-xi %6.1f -xf %6.1f -yi %6.1f -yf %6.1f -ds %6.1f -lp %6.1f -pn "%(xi,xf,yi,yf,ds,lp)+pn
  cmd = EXE+" -fout "+fmhd+" -fin "+f3df+" -grid "+fgrd+" -diptime "+dipt+" "+OP
  print  (cmd)
  os.system(cmd)
  return


def read_mhdPN(fi,re=3.5) :
  "read the output of create_mhd, i.e., read_2DMHD.f    \
   re : the radius to be masked                         "

  f=open(fi,'r');l=f.read().split('\n');f.close()

  s=l[0].split(None)
  nx=locale.atoi(s[0])
  ny=locale.atoi(s[1])


# define arrays  -------------------------------------------------------

  xx=[];yy=[]
  bx=ndarray((ny,nx));by=ndarray((ny,nx));bz=ndarray((ny,nx));bt=ndarray((ny,nx))
  jx=ndarray((ny,nx));jy=ndarray((ny,nx));jz=ndarray((ny,nx));jt=ndarray((ny,nx))
  vx=ndarray((ny,nx));vy=ndarray((ny,nx));vz=ndarray((ny,nx));vt=ndarray((ny,nx))
  rr=ndarray((ny,nx));pp=ndarray((ny,nx));pdy=ndarray((ny,nx));kev=ndarray((ny,nx))

  bx.fill(nan);by.fill(nan);bz.fill(nan);bt.fill(nan)
  jx.fill(nan);jy.fill(nan);jz.fill(nan);jt.fill(nan)
  vx.fill(nan);vy.fill(nan);vz.fill(nan);vt.fill(nan)
  rr.fill(nan);pp.fill(nan);pdy.fill(nan);kev.fill(nan)


# fill the arrays ------------------------------------------------------

  k=0
  for j in range(nx):
    for i in range(ny):

      k=k+1
      w=l[k].split(None)

      x1=locale.atof(w[2])
      y1=locale.atof(w[3])
      r1=(x1**2+y1**2)**0.5

      if i==0 : xx.append(x1)
      if j==0 : yy.append(y1)

      if r1>=re:

        bx1=locale.atof(w[4])
        by1=locale.atof(w[5])
        bz1=locale.atof(w[6])
        bt1=(bx1**2+by1**2+bz1**2)**0.5
        bx[i][j]=bx1
        by[i][j]=by1
        bz[i][j]=bz1
        bt[i][j]=bt1

        vx1=locale.atof(w[7])
        vy1=locale.atof(w[8])
        vz1=locale.atof(w[9])
        vt1=(vx1**2+vy1**2+vz1**2)**0.5
        vx[i][j]=vx1
        vy[i][j]=vy1
        vz[i][j]=vz1
        vt[i][j]=vt1

        jx1=locale.atof(w[12])
        jy1=locale.atof(w[13])
        jz1=locale.atof(w[14])
        jt1=(jx1**2+jy1**2+jz1**2)**0.5
        jx[i][j]=jx1
        jy[i][j]=jy1
        jz[i][j]=jz1
        jt[i][j]=jt1

        rr1  = locale.atof(w[10])
        pp1  = locale.atof(w[11])
        rr[i][j]  = rr1
        pp[i][j]  = pp1
        pdy[i][j] = rr1*vt1**2*1.672614e-6
        kev[i][j] = 72429.0*pp1/rr1/11600.e3

# organize the arrays  ---------------------------------------------------

  vv   = [ bx,by,bz,bt,  \
           vx,vy,vz,vt,  \
           jx,jy,jz,jt,  \
           rr,pp,pdy,kev ]

  vstr = [ 'bx','by','bz','bt',  \
           'vx','vy','vz','vt',  \
           'jx','jy','jz','jt',  \
           'rr','pp','pdy','kev' ]

# unit change ------------------------------------------------------------
  for i in range(len(vv)):
    pkg_plot = mhd_vpkg(vstr[i])
    if pkg_plot[2]!=1 : vv[i]= vv[i]*pkg_plot[2]

  return xx,yy,vv,vstr

def read_2DMHD(fi,pn,re=3.5) :
  "read the output of create_mhd, i.e., read_2DMHD.f	\
   re : the radius to be masked				"

  pm=1.672614e-27   # proton mass
  bc=1.380649e-23   # boltzmann constant
  crs=1.1e-15       # broadband cross section from Collier [eV/cm2]

  print ("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()

  s=l[0].split(None)
  nx=locale.atoi(s[0])
  ny=locale.atoi(s[1])


# define arrays  -----------

  xx=[];yy=[]
  if pn=='cp': zz=ndarray((ny,nx));zz.fill(nan)

  bx=ndarray((ny,nx));by=ndarray((ny,nx));bz=ndarray((ny,nx));bt=ndarray((ny,nx))
  ex=ndarray((ny,nx));ey=ndarray((ny,nx));ez=ndarray((ny,nx));et=ndarray((ny,nx))
  jx=ndarray((ny,nx));jy=ndarray((ny,nx));jz=ndarray((ny,nx));jt=ndarray((ny,nx))
  vx=ndarray((ny,nx));vy=ndarray((ny,nx));vz=ndarray((ny,nx));vt=ndarray((ny,nx))
  rr=ndarray((ny,nx));pp=ndarray((ny,nx));pdy=ndarray((ny,nx));kev=ndarray((ny,nx))
  rn=ndarray((ny,nx));xr=ndarray((ny,nx));vth=ndarray((ny,nx));vrl=ndarray((ny,nx))	#xray
  res=ndarray((ny,nx))

  bx.fill(nan);by.fill(nan);bz.fill(nan);bt.fill(nan)
  ex.fill(nan);ey.fill(nan);ez.fill(nan);et.fill(nan)
  jx.fill(nan);jy.fill(nan);jz.fill(nan);jt.fill(nan)
  vx.fill(nan);vy.fill(nan);vz.fill(nan);vt.fill(nan)
  rr.fill(nan);pp.fill(nan);pdy.fill(nan);kev.fill(nan);res.fill(nan)
  vth.fill(nan);vrl.fill(nan);rn.fill(nan);xr.fill(nan)


# fill the arrays ----------

  k=0
  for i in range(ny):
    for j in range(nx):

      k=k+1
      w=l[k].split(None)

      x1=locale.atof(w[2])
      y1=locale.atof(w[3])
      z1=locale.atof(w[4])
      r1=(x1**2+y1**2+z1**2)**0.5

      if pn=='xz':
         if i==0 : xx.append(x1)
         if j==0 : yy.append(z1)
      if pn=='xy':
         if i==0 : xx.append(x1)
         if j==0 : yy.append(y1)
      if pn=='yz':
         if i==0 : xx.append(y1)
         if j==0 : yy.append(z1)
      if pn=='xr':  # rotated plane
#        if i==0 : xx.append(locale.atof(w[-4]))
#        if j==0 : yy.append(locale.atof(w[-2]))
         if i==0 : xx.append(x1)
         if j==0 : yy.append(z1)
      if pn=='zr':  # rotated plane
         if i==0 : xx.append(locale.atof(w[-4]))
         if j==0 : yy.append(locale.atof(w[-2]))
#        if i==0 : xx.append(x1)
#        if j==0 : yy.append(z1)
      if pn=='cp': # central plasma sheet
         if i==0 : xx.append(x1)
         if j==0 : yy.append(y1)
         zz[i][j]=z1

      if r1>=re:

        bx1=locale.atof(w[5])
        by1=locale.atof(w[6])
        bz1=locale.atof(w[7])
        bt1=(bx1**2+by1**2+bz1**2)**0.5
        bx[i][j]=bx1
        by[i][j]=by1
        bz[i][j]=bz1
        bt[i][j]=bt1

        vx1=locale.atof(w[8])
        vy1=locale.atof(w[9])
        vz1=locale.atof(w[10])
        vt1=(vx1**2+vy1**2+vz1**2)**0.5
        vx[i][j]=vx1
        vy[i][j]=vy1
        vz[i][j]=vz1
        vt[i][j]=vt1

        ex1=locale.atof(w[13])
        ey1=locale.atof(w[14])
        ez1=locale.atof(w[15])
        et1=(ex1**2+ey1**2+ez1**2)**0.5
        ex[i][j]=ex1
        ey[i][j]=ey1
        ez[i][j]=ez1
        et[i][j]=et1

        jx1=locale.atof(w[16])
        jy1=locale.atof(w[17])
        jz1=locale.atof(w[18])
        jt1=(jx1**2+jy1**2+jz1**2)**0.5
        jx[i][j]=jx1
        jy[i][j]=jy1
        jz[i][j]=jz1
        jt[i][j]=jt1

#       res1 = locale.atof(w[19])
        res1 = 0.
        rr1  = locale.atof(w[11])
        pp1  = locale.atof(w[12])
        tk1  = 72429.0*pp1/rr1
        vth1 = (3*bc*tk1/pm)**0.5/1e3   # Thermal velocity [km/s]
        vrl1 = (vth1**2+vt1**2)**0.5    # Relative velocity [km/s]
        rn1  = 25*(10./r1)**3	     	# Hodge's neutral density [cm-3]
        xr1  = rn1*rr1*vrl1*1e5         # Xray emission at a given plane (no line-of-sight integration)

        res[i][j] = res1
        rr[i][j]  = rr1
        pp[i][j]  = pp1
        rn[i][j]  = rn1
        xr[i][j]  = xr1
        pdy[i][j] = rr1*vt1**2*1.672614e-6
        kev[i][j] = tk1/11600.e3
        vth[i][j] = vth1
        vrl[i][j] = vrl1

  epar = (bx*ex+by*ey+bz*ez)/bt
  eper = (et**2-epar**2)**0.5

# organize the arrays  -----

  vv   = [ bx,by,bz,bt,  \
           vx,vy,vz,vt,  \
           ex,ey,ez,et,  \
           jx,jy,jz,jt,  \
           rr,pp,pdy,kev,\
           epar,res,	 \
           rn,vth,vrl,xr ]

# print len(epar),len(bx),len(epar[0]),len(bx[0])
  vstr = [ 'bx','by','bz','bt',  \
           'vx','vy','vz','vt',  \
           'ex','ey','ez','et',  \
           'jx','jy','jz','jt',  \
           'rr','pp','pdy','kev',\
           'epar','resis',	 \
           'nn','vth','vav','Qcut' ]

  if pn=='cp': vv.append(zz); vstr.append('zgse')

# the following is included for mhdplot
# unit change --------------
# for i in range(len(vv)):
#   pkg_plot = mhd_vpkg(vstr[i])
#   if pkg_plot[2]!=1 : vv[i]= vv[i]*pkg_plot[2]


  return xx,yy,vv,vstr

def read_2DMHD_BATSRUS(fi,pn,re=3.5):
   "read the output of create_mhd, i.e., read_2DMHD.f	\
    re : the radius to be masked				"

   pm=1.672614e-27   # proton mass
   bc=1.380649e-23   # boltzmann constant
   crs=1.1e-15       # broadband cross section from Collier [eV/cm2]

   print ("READ",fi)
   f=open(fi,'r');l=f.read().split('\n');f.close()

   s=l[0].split(None)
   nx=locale.atoi(s[0])
   ny=locale.atoi(s[1])


 # define arrays  -----------

   xx=[];yy=[]
   if pn=='cp': zz=ndarray((ny,nx));zz.fill(nan)

   bx=ndarray((ny,nx));by=ndarray((ny,nx));bz=ndarray((ny,nx));bt=ndarray((ny,nx))
   ex=ndarray((ny,nx));ey=ndarray((ny,nx));ez=ndarray((ny,nx));et=ndarray((ny,nx))
   jx=ndarray((ny,nx));jy=ndarray((ny,nx));jz=ndarray((ny,nx));jt=ndarray((ny,nx))
   vx=ndarray((ny,nx));vy=ndarray((ny,nx));vz=ndarray((ny,nx));vt=ndarray((ny,nx))
   rr=ndarray((ny,nx));pp=ndarray((ny,nx));pdy=ndarray((ny,nx));kev=ndarray((ny,nx))
   rn=ndarray((ny,nx));xr=ndarray((ny,nx));vth=ndarray((ny,nx));vrl=ndarray((ny,nx))	#xray
   res=ndarray((ny,nx))

   bx.fill(nan);by.fill(nan);bz.fill(nan);bt.fill(nan)
   ex.fill(nan);ey.fill(nan);ez.fill(nan);et.fill(nan)
   jx.fill(nan);jy.fill(nan);jz.fill(nan);jt.fill(nan)
   vx.fill(nan);vy.fill(nan);vz.fill(nan);vt.fill(nan)
   rr.fill(nan);pp.fill(nan);pdy.fill(nan);kev.fill(nan);res.fill(nan)
   vth.fill(nan);vrl.fill(nan);rn.fill(nan);xr.fill(nan)


 # fill the arrays ----------

   k=0
   for i in range(ny):
     for j in range(nx):

       k=k+1
       w=l[k].split(None)

       x1=locale.atof(w[2])
       y1=locale.atof(w[3])
       z1=locale.atof(w[4])
       r1=(x1**2+y1**2+z1**2)**0.5

       if pn=='xz':
          if i==0 : xx.append(x1)
          if j==0 : yy.append(z1)
       if pn=='xy':
          if i==0 : xx.append(x1)
          if j==0 : yy.append(y1)
       if pn=='yz':
          if i==0 : xx.append(y1)
          if j==0 : yy.append(z1)
       if pn=='xr':  # rotated plane
 #        if i==0 : xx.append(locale.atof(w[-4]))
 #        if j==0 : yy.append(locale.atof(w[-2]))
          if i==0 : xx.append(x1)
          if j==0 : yy.append(z1)
       if pn=='zr':  # rotated plane
          if i==0 : xx.append(locale.atof(w[-4]))
          if j==0 : yy.append(locale.atof(w[-2]))
 #        if i==0 : xx.append(x1)
 #        if j==0 : yy.append(z1)
       if pn=='cp': # central plasma sheet
          if i==0 : xx.append(x1)
          if j==0 : yy.append(y1)
          zz[i][j]=z1

       if r1>=re:

         bx1=locale.atof(w[5])
         by1=locale.atof(w[6])
         bz1=locale.atof(w[7])
         bt1=(bx1**2+by1**2+bz1**2)**0.5
         bx[i][j]=bx1
         by[i][j]=by1
         bz[i][j]=bz1
         bt[i][j]=bt1

         vx1=locale.atof(w[8])
         vy1=locale.atof(w[9])
         vz1=locale.atof(w[10])
         vt1=(vx1**2+vy1**2+vz1**2)**0.5
         vx[i][j]=vx1
         vy[i][j]=vy1
         vz[i][j]=vz1
         vt[i][j]=vt1

         jx1=locale.atof(w[13])*1e3
         jy1=locale.atof(w[14])*1e3
         jz1=locale.atof(w[15])*1e3
         jt1=(jx1**2+jy1**2+jz1**2)**0.5
         jx[i][j]=jx1
         jy[i][j]=jy1
         jz[i][j]=jz1
         jt[i][j]=jt1

 #       res1 = locale.atof(w[19])
         res1 = 0.
         rr1  = locale.atof(w[11])
         pp1  = locale.atof(w[12])*1e3
         tk1  = 72429.0*pp1/rr1
         vth1 = (3*bc*tk1/pm)**0.5/1e3   # Thermal velocity [km/s]
         vrl1 = (vth1**2+vt1**2)**0.5    # Relative velocity [km/s]
         rn1  = 80*(3.8/r1)**2	     	# Hodge's neutral density [cm-3]
         xr1  = rn1*rr1*vrl1*1e5         # Xray emission at a given plane (no line-of-sight integration)

         res[i][j] = res1
         rr[i][j]  = rr1
         pp[i][j]  = pp1
         rn[i][j]  = rn1
         xr[i][j]  = xr1
         pdy[i][j] = rr1*vt1**2*1.672614e-6
         kev[i][j] = tk1/11600.e3
         vth[i][j] = vth1
         vrl[i][j] = vrl1

#   epar = (bx*ex+by*ey+bz*ez)/bt
 #  eper = (et**2-epar**2)**0.5

 # organize the arrays  -----

   vv   = [ bx,by,bz,bt,  \
            vx,vy,vz,vt,  \
#            ex,ey,ez,et,  \
            jx,jy,jz,jt,  \
            rr,pp,pdy,kev,\
            res,	 \
            rn,vth,vrl,xr ]

 # print len(epar),len(bx),len(epar[0]),len(bx[0])
   vstr = [ 'bx','by','bz','bt',  \
            'vx','vy','vz','vt',  \
#            'ex','ey','ez','et',  \
            'jx','jy','jz','jt',  \
            'rr','pp','pdy','kev',\
            'resis',	 \
            'nn','vth','vav','Qcut' ]

   if pn=='cp': vv.append(zz); vstr.append('zgse')

 # the following is included for mhdplot
 # unit change --------------
 # for i in range(len(vv)):
 #   pkg_plot = mhd_vpkg(vstr[i])
 #   if pkg_plot[2]!=1 : vv[i]= vv[i]*pkg_plot[2]


   return xx,yy,vv,vstr




def maxmin_ran(xran,yran,xx,yy,val):
  " calculate max and min values between xran and yran \
    xx,yy should be increasing order, ext. [1,2,3] "

  nx   = len(xx)
  ny   = len(yy)
  vmax =-1.e9
  vmin = 1.e9
  if yran[1]>yran[0]: yran1=yran[0];yran2=yran[1]
  if yran[1]<yran[0]: yran1=yran[1];yran2=yran[0]
  if xran[1]>xran[0]: xran1=xran[0];xran2=xran[1]
  if xran[1]<xran[0]: xran1=xran[1];xran2=xran[0]

  for i in range(ny):
   if yy[i] >= yran1 and yy[i] <= yran2 :
     for j in range(nx):
      if xx[j] >= xran1 and xx[j] <=xran2 :
        if vmax <= val[i][j] : vmax = val[i][j]
        if vmin >= val[i][j] : vmin = val[i][j]
  return vmax,vmin
