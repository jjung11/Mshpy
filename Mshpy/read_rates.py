#!/usr/bin/python
#
# plot xray rate

import os
import sys
HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/lib/")

import math
import locale
import numpy              	as np
import matplotlib.pyplot  	as plt
from   openggcm_info            import *
from   read_mhd                 import *
from   mpl_toolkits.axes_grid1  import make_axes_locatable
from   pkg_rates                import rate_vpkg
#from   scipy                    import interpolate


def create_xray(fout,fgrd,f3df,dipt,scinfo,xrinfo):
  "create xray file seen from a virtual spacecraft			\
   scinfo : s/c location (xsc,ysc,zsc) and look direction (xlk,ylk,zlk)	\
   xrinfo : s/c field of view (the1,the2,dthe,phi1,phi2,dphi)		"
#### check if fout exists. If so, choose replacing or useing the old fout
  if os.path.isfile(fout):
    print('============================================================================')
    test=input('Files exist! Press (o/O) to Overwrite and (u/U) to use old ones :')
    if   test=='o' or test=='O' :
       run=True
       print('rm '+fout)
       os.system('rm '+fout)
    elif test=='u' or test=='U' :
       run=False
    else :
       print("Error! Press O for Overwrite, U for Using old file. Please Run again")
       sys.exit(1)
  else :
    run=True
#### calculate Xray
  if run:
    xsc,ysc,zsc,xlk,ylk,zlk       = scinfo
    the1,the2,dthe,phi1,phi2,dphi = xrinfo
#   xsc,ysc,zsc,xlk,ylk,zlk       = [ locale.atof(i) for i in scinfo.split(':') ]
#   the1,the2,dthe,phi1,phi2,dphi = [ locale.atof(i) for i in xrinfo.split(':') ]
    EXE = "$HOME/svn/hkc-project/trunk/src/xray_ena/xraysc_sight"
#   EXE = "$HOME/svn/hkc-project/trunk/src/xray_ena/xraysc_clipMP"
    OP1 = " -xsc %7.2f -ysc %7.2f -zsc %7.2f"%(xsc,ysc,zsc)
    OP2 = " -xlk %7.2f -ylk %7.2f -zlk %7.2f"%(xlk,ylk,zlk)
    OP3 = " -the1 %7.2f -the2 %7.2f -dthe %7.2f -phi1 %7.2f -phi2 %7.2f -dphi %7.2f"\
          %(the1,the2,dthe,phi1,phi2,dphi)
    OP4 = " -grid "+fgrd+" -fin "+f3df+" -diptime "+dipt+" -fo "+fout
    cmd = EXE+OP1+OP2+OP3+OP4
    os.system(cmd)
  return



def find_MPBScontour(fmhd,pn,lp,rr,sc):
  " find MP/BS location from density contour lines.            	\
    fmhd  : need 2DMHD data on either xz or xy plane		\
    rr    : number density to select bs & mp                 	"

  xx,yy,vv,vstr = read_2DMHD(fmhd,pn)
  x,y           = np.meshgrid(xx,yy)
  cden          = plt.contourf(x,y,vv[16],levels=np.arange(0,51.,1.),extend='both')
  csbs          = plt.contour(xx,yy,vv[16],levels=[rr[0]],colors=['m'])
  vbs1          = csbs.collections[0].get_paths()[0]
  vbs2          = vbs1.vertices

  csmp          = plt.contour(xx,yy,vv[16],levels=[rr[1]],colors=['r'])
  if len(csmp.collections[0].get_paths())==1:
    vmp1        = csmp.collections[0].get_paths()[0]
  else:
    vmp1        = csmp.collections[0].get_paths()[1]
  vmp2          = vmp1.vertices

  if   pn=='xz':
    xbs  = vbs2[:,0]
    ybs  = [ lp for i in xbs]
    zbs  = vbs2[:,1]
    xmp  = vmp2[:,0]
    ymp  = [ lp for i in xmp]
    zmp  = vmp2[:,1]
    mp   = plt.plot(xmp,zmp,'w')
    bs   = plt.plot(xbs,zbs,'m')
  elif pn=='xy':
    xbs  = vbs2[:,0]
    ybs  = vbs2[:,1]
    zbs  = [ lp for i in xbs]
    xmp  = vmp2[:,0]
    ymp  = vmp2[:,1]
    zmp  = [ lp for i in xmp]
    mp   = plt.plot(xmp,ymp,'w')
    bs   = plt.plot(xbs,ybs,'m')

  info = runinfo(fmhd)
  fps  = 'test.'+info.run+'.contour.'+info.mhdt+'.pdf'
  print("SAVE ",fps)
  plt.savefig(fps)
  plt.close()

  tmp=[];pmp=[]
  tbs=[];pbs=[]
  for i in range(len(xmp)):
    x    = xmp[i]-sc[0]
    y    = ymp[i]-sc[1]
    z    = zmp[i]-sc[2]
    rr1  = (x**2+y**2+z**2)**0.5
    the1 = 90.-math.degrees(math.acos(z/rr1))
    phi1 = math.degrees(math.atan2(y,x)) #-90.
    if phi1<0: phi1=360.+phi1
    tmp.append(the1)
    pmp.append(phi1)

  for i in range(len(xbs)):
    x    = xbs[i]-sc[0]
    y    = ybs[i]-sc[1]
    z    = zbs[i]-sc[2]
    rr1  = (x**2+y**2+z**2)**0.5
    the1 = 90.-math.degrees(math.acos(z/rr1))
    phi1 = math.degrees(math.atan2(y,x)) #-90.
    if phi1<0: phi1=360.+phi1
    tbs.append(the1)
    pbs.append(phi1)

  bdxsc = [pmp,tmp,pbs,tbs]
  if pn=='xz': bdgse = [xmp,zmp,xbs,zbs]
  if pn=='xy': bdgse = [xmp,ymp,xbs,ybs]
  mpbs = [bdxsc,bdgse]

  return mpbs


def read_mpbs(fi,pn,sc):
  "read and calculate the locations of BS and Mpause in the s/c point of view"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  tmp=[];pmp=[]
  tbs=[];pbs=[]
  for s in l[1:-1]:
    w=s.split(None)
    xbs=locale.atof(w[2])-sc[0]
    ybs=locale.atof(w[3])-sc[1]
    zbs=locale.atof(w[4])-sc[2]
    xmp=locale.atof(w[6])-sc[0]
    ymp=locale.atof(w[7])-sc[1]
    zmp=locale.atof(w[8])-sc[2]
### calculate the locations in the satellite's view
    rr1  = (xmp**2+ymp**2+zmp**2)**0.5
    the1 = 90.-math.degrees(math.acos(zmp/rr1))
    phi1 = math.degrees(math.atan2(ymp,xmp))
    if phi1<0: phi1=360.+phi1
    rr2  = (xbs**2+ybs**2+zbs**2)**0.5
    the2 = 90.-math.degrees(math.acos(zbs/rr2))
    phi2 = math.degrees(math.atan2(ybs,xbs))
    if phi2<0: phi2=360.+phi2
    tmp.append(the1)
    pmp.append(phi1)
    tbs.append(the2)
    pbs.append(phi2)

  bdxsc = [pmp,tmp,pbs,tbs]
  if pn=='xz': bdgse = [xmp,zmp,xbs,zbs]
  if pn=='xy': bdgse = [xmp,ymp,xbs,ybs]
  mpbs = [bdxsc,bdgse]
  return mpbs


def read_bline(fi,sc):
  "read and calculate bline in the s/c point of view"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  nl  = locale.atoi(l[-2].split(None)[0])
  blt = [ [] for i in range(nl) ]
  blp = [ [] for i in range(nl) ]
  oc  = []
  for s in l[:-1]:
    w    = s.split(None)
    il   = locale.atoi(w[0])-1
    blx1 = locale.atof(w[4])
    bly1 = locale.atof(w[5])
    blz1 = locale.atof(w[6])
    blx  = blx1-sc[0]
    bly  = bly1-sc[1]
    blz  = blz1-sc[2]
    rr   = (blx**2+bly**2+blz**2)**0.5
    the  = 90.-math.degrees(math.acos(blz/rr))
    phi  = math.degrees(math.atan2(bly,blx))
    if phi<0: phi=360.+phi
#   if il==1105 :print nl,il,blx,bly,blz,rr,the,phi
    blt[il].append(the)
    blp[il].append(phi)
    oc.append(locale.atoi(w[4]))
  f.close()
  bl = [blp,blt,oc]
  return bl


def read_cosmic(fi,plot=False):
  "read cosmic background of X-ray observed by ROSAT satellite			\
   INPUT  : X-ray cosmic background in unit of 10^-6 ROSAT counts/s/arcmin^2  	\
            111 x 111 pixels, 12 arcmin per pixel (1 arcmin = 1/60 deg)		\
   OuTPUT : return X-ray background in unit of counts/s/deg^2,			\
            22 x 22 pixels, 1 deg per pixel   					"

  f=open(fi,'r');l=f.read().split('\n');f.close()
  nx=111
  ny=111
  xx= [ i*12/60. for i in range(nx) ]
  yy= [ i*12/60. for i in range(nx) ]
  vv= np.ndarray((nx,ny))
  i=0;j=0
  for s in l[:-1]:
    w=s.split(None)
    for k in range(len(w)):
       vv[i][j] = locale.atof(w[k])*3600*1e-6  # convert to counts/s/deg^2
       j        = j+1
       if j==111: i=i+1;j=0
# bf  = interpolate.interp2d(xx,yy,vv,kind='linear')
# phi = range(xlen)
# lat = range(ylen)

# rate= bf(phi,lat).T
  if plot :
    fig  = plt.figure(figsize=(8,8))
    ax1  = plt.subplot(111,aspect='equal')
    X,Y  = np.meshgrid(xx,yy)
    pc1  = plt.pcolor(X,Y,vv)
    ax1.set_xlim(xx[0],xx[-1])
    ax1.set_ylim(yy[0],yy[-1])
    ax1.set_title(fi)
    cax1 = make_axes_locatable(ax1)
    cax2 = cax1.append_axes("right",size="3%",pad="5%")
    cb   = fig.colorbar(pc1,cax=cax2)
    plt.savefig('test.cosmic_bg.ps')
  return xx,yy,vv


def read_ena(fi):
  "read ena rates"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  s    = l[0].split(None)
  nt   = locale.atoi(s[0])
  np   = locale.atoi(s[1])
  tt   = locale.atof(s[2])
  info = [ locale.atof(i) for i in s[3:] ] # xsc,ysc,zsc,xlk,ylk,zlk,ena
  lat  = []
  phi  = []
  rate1= ndarray((np,nt))
  rate2= ndarray((np,nt))
  rate3= ndarray((np,nt))
  rate1.fill(nan)
  rate2.fill(nan)
  rate3.fill(nan)
  for s in l[1:]:
    w =s.split(None)
    if len(w)>2:
      i1   = locale.atoi(w[0])-1
      j1   = locale.atoi(w[1])-1
      rad1 = locale.atof(w[2])
      phi1 = locale.atof(w[3])
      lat1 = locale.atof(w[4])
      val1 = locale.atof(w[5])
      val2 = locale.atof(w[6])
      val3 = locale.atof(w[7])
      if i1==0       : lat.append(lat1)
      if j1==0       : phi.append(phi1)
      if val1!=9999.0 : rate1[j1][i1]=val1
      if val2!=9999.0 : rate2[j1][i1]=val2
      if val3!=9999.0 : rate3[j1][i1]=val3
  rate = [rate1,rate2,rate3]
  print(len(lat),len(phi))
  return phi,lat,rate,info


def read_xray(fi):
  "read xray rates in unit of eV cm-2 s-1 sr-1"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  s    = l[0].split(None)
  nt   = locale.atoi(s[0])
  np_   = locale.atoi(s[1])
  sc   = [ locale.atof(i) for i in s[2:] ]
  lat  = []
  phi  = []
  ival = False
  rate1= ndarray((np_,nt))
  rate2= ndarray((np_,nt))
  rate3= ndarray((np_,nt))
  rate1.fill(0)
  rate2.fill(0)
  rate3.fill(0)
# rate1.fill(nan)
# rate2.fill(nan)
# rate3.fill(nan)
  for s in l[1:]:
    w =s.split(None)
    if len(w)>2:
      i1   = locale.atoi(w[0])-1
      j1   = locale.atoi(w[1])-1
      rad1 = locale.atof(w[2])
      phi1 = locale.atof(w[3])
      lat1 = locale.atof(w[4])
      val1 = locale.atof(w[5])
      if len(w)==8:
        ival = True
        val2 = locale.atof(w[6])
        val3 = locale.atof(w[7])
        if val2!=9999.0 : rate2[j1][i1]=val2
        if val3!=9999.0 : rate3[j1][i1]=val3
      if i1==0       : lat.append(lat1)
      if j1==0       : phi.append(phi1)
      if val1!=9999.0: rate1[j1][i1]=val1

  if ival: rate=[rate1,rate2,rate3]
  else   : rate=rate1
  lat=np.array(lat)
  return phi,lat,rate,sc

def read_xraycut(fi):
  "read xray rates in unit of eV cm-2 s-1 sr-1"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  s    = l[0].split(None)
  nt   = locale.atoi(s[0])
  np_   = locale.atoi(s[1])
  sc   = [ locale.atof(i) for i in s[2:] ]
  lat  = []
  phi  = []
  ival = False
  rate1= ndarray((np_,nt))
  rate2= ndarray((np_,nt))
  rate3= ndarray((np_,nt))
  rate1.fill(0)
  rate2.fill(0)
  rate3.fill(0)
# rate1.fill(nan)
# rate2.fill(nan)
# rate3.fill(nan)
  for s in l[1:]:
    w =s.split(None)
    if len(w)>2:
      i1   = locale.atoi(w[0])-1
      j1   = locale.atoi(w[1])-1
      phi1 = locale.atof(w[2])
      lat1 = locale.atof(w[3])
      val1 = locale.atof(w[4])
      if i1==0       : lat.append(lat1)
      if j1==0       : phi.append(phi1)
      if val1!=9999.0: rate1[j1][i1]=val1

  if ival: rate=[rate1,rate2,rate3]
  else   : rate=rate1
  lat=np.array(lat)
  return phi,lat,rate

def read_LOS(fi):
  "read 1D data of LOS xray rates"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  s    = l[0].split(None)
  phi  = locale.atof(s[2])
  the  = locale.atof(s[3])
  lat  = 90.-the
  sc   = [ locale.atof(i) for i in s[4:] ]

  rad=[];rate1=[];rate2=[];rate3=[]
  x=[];y=[];z=[];bx=[];by=[];bz=[];vx=[];vy=[];vz=[];rr=[];pp=[]
  ex=[];ey=[];ez=[];xjx=[];xjy=[];xjz=[];tk=[];vth=[];vsw=[];vel=[]
  rrn1=[];rrn2=[];rrn3=[];xray1=[];xray2=[];xray3=[]

  for s in l[1:]:
    w =s.split(None)
    if len(w)>2:
      rad1,phi1,lat1,rate11,rate12,rate13,x1,y1,z1,bx1,by1,bz1,			\
      vx1,vy1,vz1,rr1,pp1,ex1,ey1,ez1,xjx1,xjy1,xjz1,temp1,vth1,vsw1,vel1,	\
      rrn11,rrn12,rrn13,xray11,xray12,xray13 = [locale.atof(i) for i in w[3:] ]

      rad.append(rad1)
      x.append(x1)
      y.append(y1)
      z.append(z1)
      bx.append(bx1)
      by.append(by1)
      bz.append(bz1)
      vx.append(vx1)
      vy.append(vy1)
      vz.append(vz1)
      rr.append(rr1)
      pp.append(pp1)
      ex.append(ex1)
      ey.append(ey1)
      ez.append(ez1)
      xjx.append(xjx1)
      xjy.append(xjy1)
      xjz.append(xjz1)
      tk.append(temp1)
      vth.append(vth1)
      vsw.append(vsw1)
      vel.append(vel1)
      rrn1.append(rrn11)
      rrn2.append(rrn12)
      rrn3.append(rrn13)
      xray1.append(xray11)
      xray2.append(xray12)
      xray3.append(xray13)
      rate1.append(rate11)
      rate2.append(rate12)
      rate3.append(rate13)
  pos  =[sc,phi,lat,rad,x,y,z]
  vmhd =[bx,by,bz,vx,vy,vz,ex,ey,ez,xjx,xjy,xjz,rr,pp,tk]
  vxr1 =[rr,vsw,vth,vel,tk,rrn1,rrn2,rrn3]
  vxr2 =[xray1,xray2,xray3,rate1,rate2,rate3]
  return pos,vmhd,vxr1,vxr2


def read_xcounts(fi):
  "read xray crount rates in unit of eV cm-2 s-1 sr-1"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  s    = l[0].split(None)
  nt   = locale.atoi(s[0])
  np   = locale.atoi(s[1])
  sc   = [ locale.atof(i) for i in s[2:] ]
  lat  = []
  phi  = []
  brate = ndarray((np,nt))
  xrate = ndarray((np,nt))
  xblur = ndarray((np,nt))
  xbfin = ndarray((np,nt))
  xbsig = ndarray((np,nt))
  for s in l[1:]:
    w =s.split(None)
    if len(w)>2:
      i1   = locale.atoi(w[0])-1
      j1   = locale.atoi(w[1])-1
      phi1 = locale.atof(w[2])
      lat1 = locale.atof(w[3])
      val1 = locale.atof(w[4])
      val2 = locale.atof(w[5])
      val3 = locale.atof(w[6])
      val4 = locale.atof(w[7])
      val5 = locale.atof(w[8])
      if i1==0       : lat.append(lat1)
      if j1==0       : phi.append(phi1)
      bprate[j1][i1] = val1
      xrate[j1][i1]  = val2
      xbblur[j1][i1] = val3
      xbfin[j1][i1]  = val4
      xbsig[j1][i1]  = val5
  rates = [brate,xrate,xblur,xbfin,xbsig]
  return phi,lat,rates,sc


def read_kipcounts(fi):
  "read Kip's xray crount rates in counts/pix for Texp"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  s    = l[0].split(None)
  nthe = locale.atoi(s[0])
  nphi = locale.atoi(s[1])
  sc   = [ locale.atof(i) for i in s[2:] ]	# xsc,ysc,zsc,xlk,ylk,zlk,Rpix,Texp
  lat  = []
  phi  = []
  xrexp  = ndarray((nthe,nphi))
  xcount = ndarray((nthe,nphi))
  xbrate = ndarray((nthe,nphi))
  xbblur = ndarray((nthe,nphi))
  xbinst = ndarray((nthe,nphi))
  xbfin  = ndarray((nthe,nphi))
  bgblur = ndarray((nthe,nphi))
  xbsig  = ndarray((nthe,nphi))

  for s in l[1:]:
    w =s.split(None)
    if len(w)>2:
      i1   = locale.atoi(w[0])
      j1   = locale.atoi(w[1])
      phi1 = locale.atof(w[2])
      lat1 = locale.atof(w[3])
      val1 = locale.atof(w[4])
      val2 = locale.atof(w[5])
      val3 = locale.atof(w[6])
      val4 = locale.atof(w[7])
      val5 = locale.atof(w[8])
      val6 = locale.atof(w[9])
      val7 = locale.atof(w[10])
      val8 = locale.atof(w[11])
      if i1==0       : phi.append(phi1)
      if j1==0       : lat.append(lat1)
      xrexp [i1][j1] = val1
      xcount[i1][j1] = val2
      xbrate[i1][j1] = val3
      xbblur[i1][j1] = val4
      xbinst[i1][j1] = val5
      xbfin [i1][j1] = val6
      bgblur[i1][j1] = val7
      xbsig [i1][j1] = val8

  print('max & min xrate  in Q:',np.nanmax(xrexp),np.nanmin(xrexp))
  print('max & min xcount in counts/pix/Texp:',np.nanmax(xcount),np.nanmin(xcount))
  print('max & min xbrate in counts/pix/Texp:',np.nanmax(xbrate),np.nanmin(xbrate))
  print('max & min xbblur in counts/pix/Texp:',np.nanmax(xbblur),np.nanmin(xbblur))
  print('max & min xbinst in counts/pix/Texp:',np.nanmax(xbinst),np.nanmin(xbinst))
  print('max & min xbfin  in counts/pix/Texp:',np.nanmax(xbfin),np.nanmin(xbfin))
  print('max & min xbsig  in counts/pix/Texp:',np.nanmax(xbsig),np.nanmin(xbsig))
  print('xcount mean,std:',np.mean(xcount),np.std(xcount))
  print('bgblur mean,std:',np.mean(bgblur),np.std(bgblur))
  print('xbrate mean,std:',np.mean(xbrate),np.std(xbrate))
  print('xbblur mean,std:',np.mean(xbblur),np.std(xbblur))
  print('xbinst mean,std:',np.mean(xbinst),np.std(xbinst))
  print('xbfin  mean,std:',np.mean(xbfin),np.std(xbfin))
  print('xbsig  mean,std:',np.mean(xbsig),np.std(xbsig))

  rates = [xrexp,xcount,xbrate,xbblur,xbinst,xbfin,bgblur,xbsig]
  return phi,lat,rates,sc

def read_xrbin(fi):
  "read rebinned xray crount rates in counts/pix for Texp"
  print("READ",fi)
  f=open(fi,'r');l=f.read().split('\n');f.close()
  s    = l[0].split(None)
  nthe = locale.atoi(s[0])
  nphi = locale.atoi(s[1])
  sc   = [ locale.atof(i) for i in s[2:] ]      # xsc,ysc,zsc,xlk,ylk,zlk,Rpix,Texp
  lat  = []
  phi  = []
  xrbin  = np.ndarray((nthe,nphi))

  for s in l[1:]:
    w =s.split(None)
    if len(w)>2:
      i1   = locale.atoi(w[0])
      j1   = locale.atoi(w[1])
      phi1 = locale.atof(w[2])
      lat1 = locale.atof(w[3])
      val1 = locale.atof(w[4])
      if i1==0       : phi.append(phi1)
      if j1==0       : lat.append(lat1)
      xrbin [i1][j1] = val1

  print('max & min xrbin in couns/pix/Texp:',np.nanmax(xrbin),np.nanmin(xrbin))
  print('xrbin mean,std:',np.mean(xrbin),np.std(xrbin))
  return phi,lat,xrbin,sc


def read_psf(fi,plot=False):
  "read Kip's point spred function.				\
   The pixcel size is selected to be 0.375 degree		"

  f=open(fi,'r');l=f.read().split('\n');f.close()
  nx  = len(l[0].split(None))
  ny  = len(l)-1
  x   = [0.375*i for i in np.arange(-30,31,1) ]
  y   = [0.375*i for i in np.arange(-30,31,1) ]
# x   = [0.1*i for i in np.arange(-30,31,1) ]
# y   = [0.1*i for i in np.arange(-30,31,1) ]
  psf = ndarray((nx,ny))
  psf.fill(0.)

  print(nx,ny)
  for i in range(ny):
    w=l[i].split(None)
    if len(w)>2:
      for j in range(len(w)):
        psf[i][j]= locale.atof(w[j])
#       if w[j]!=0 : psf[i][j]= np.log10(locale.atof(w[j]))
#       else       : psf[i][j]= -9999.

  if plot==True:
    vmax  = 0.
    vmin  = -10.
    tint  = 2.
    dlev  = (vmax-vmin)/50.
    clev  = np.arange(vmin,vmax+dlev,dlev)
    tlev  = np.arange(vmin,vmax+tint,tint)

    fig   = plt.figure()
    ax1   = fig.add_subplot(111,aspect='equal')
    xx,yy = np.meshgrid(x,y)
#   cs    = ax1.contourf(xx,yy,psf,levels=clev)
    cs    = ax1.scatter(xx,yy,c=np.log10(psf),vmin=vmin,vmax=vmax,cmap=plt.cm.jet,\
            edgecolors='none',marker='s')
    cax1  = make_axes_locatable(ax1)
    cax2  = cax1.append_axes("right",size="3%",pad="5%")
    cb    = fig.colorbar(cs,cax=cax2,ticks=tlev)
    ax1.set_xlabel("0.375$^{\circ}$ pixels")
    ax1.set_ylabel("0.375$^{\circ}$ pixels")
    ax1.set_title('SMILE Point Spread Function')
    plt.savefig('test_psf.pdf')

  return x,y,psf


def main(argv):

  fi       = 'rass_3a.txt'
# fi       = 'rass_3b.txt'
# xx,yy,vv = read_cosmic(fi,plot=True)
  fi       = read_psf('temp_psf_t0.txt',plot=True)
  x,y,zz   = read_psf(fi)

  return




if __name__=='__main__':
  main(sys.argv[1:])
