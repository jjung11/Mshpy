import os, locale
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import cm
from math import log10


def mhd_vpkg(val):
  "set colormap, title, and range of variables for mhd plot"

  print (val,val[:3])

#######
  if   val[:2]=="bx":
    cmap=plt.cm.bwr				# name of colormap
    name='Bx [nT]'				# name for colobar title
    vran=[-30.0,30.0]				# default range of value
    nlev=51 					# number of coutour level
    tick=10.					# interval of major ticks for colorbar
    ufac=1.	  				# unit factor for a val in a desried unit
    norm=0					# 0 for linear-scale, 1 for log-scale

  elif val[:2]=="by":
    cmap=plt.cm.bwr
    name='By [nT]'
    vran=[-30.0,30.0]
    nlev=51
    tick=10.
    ufac=1.
    norm=0

  elif val[:2]=="bz":
    cmap=plt.cm.bwr
    name='Bz [nT]'
    vran=[-30.0,30.0]
    nlev=51
    tick=10.
    ufac=1.
    norm=0

  elif val[:2]=="bt":
    cmap=plt.cm.jet
    name='|B| [nT]'
    vran=[0.0,30.0]
    nlev=51
    tick=10.
    ufac=1.
    norm=0

#######
  elif val=="vx":
    cmap=plt.cm.bwr                           # name of colormap
    name='Vx [km/s]'                            # name for colobar title
    vran=[-300.0,300.0]                         # default range of value
    nlev=51                                     # number of coutour level
    tick=100.                                   # interval of major ticks for colorbar
    ufac=1.                                     # unit factor for a val in a desried unit
    norm=0                                      # 0 for linear-scale, 1 for log-scale

  elif val=="vy":
    cmap=plt.cm.bwr
    name='Vy [km/s]'
    vran=[-100.0,100.0]
    nlev=51
    tick=25.
    ufac=1.
    norm=0

  elif val=="vz":
    cmap=plt.cm.bwr
    name='Vz [km/s]'
    vran=[-100.0,100.0]
    nlev=51
    tick=25.
    ufac=1.
    norm=0

  elif val=="vt":
    cmap=plt.cm.jet
    name='|V| [km/s]'
    vran=[0.0,400.0]
    nlev=51
    tick=50.
    ufac=1.
    norm=0



#######
  elif val=="jx":
    cmap=plt.cm.bwr                           # name of colormap
    name='Jx [nA/m$^2$]'                        # name for colobar title
    vran=[-10.0,10.0]                             # default range of value
    nlev=51                                     # number of coutour level
    tick=2.                                     # interval of major ticks for colorbar
    ufac=1.e3                                   # unit factor for a val in a desried unit
    norm=0                                      # 0 for linear-scale, 1 for log-scale

  elif val=="jy":
    cmap=plt.cm.bwr
    name='Jy [nA/m$^2$]'
    vran=[-10.0,10.0]
    nlev=51
    tick=2.
    ufac=1.e3
    norm=0

  elif val=="jz":
    cmap=plt.cm.bwr
    name='Jz [nA/m$^2$]'
    vran=[-10.0,10.0]
    nlev=51
    tick=2.
    ufac=1.e3
    norm=0

  elif val=="jt":
    cmap=plt.cm.jet
    name='|J| [nA/m$^2$]'
    vran=[0.0,10.0]
    nlev=51
    tick=2.
    ufac=1.e3
    norm=0



#######
  elif val[:2]=="ex":
    cmap=plt.cm.bwr                         # name of colormap
    name='Ex [mV/m]'                            # name for colobar title
    vran=[-3.0,3.0]                           # default range of value
    nlev=51                                     # number of coutour level
    tick=1.                                    # interval of major ticks for colorbar
    ufac=1.                                     # unit factor for a val in a desried unit
    norm=0                                      # 0 for linear-scale, 1 for log-scale

  elif val[:2]=="ey":
    cmap=plt.cm.bwr
    name='Ey [mV/m]'
    vran=[-3.0,3.0]
    nlev=51
    tick=1.
    ufac=1.
    norm=0

  elif val[:2]=="ez":
    cmap=plt.cm.bwr
    name='Ez [mV/m]'
    vran=[-3.0,3.0]
    nlev=51
    tick=1.
    ufac=1.
    norm=0

  elif val[:2]=="et":
    cmap=plt.cm.jet
    name='|E| [mV/m]'
    vran=[0.0,5.0]
    nlev=51
    tick=1.
    ufac=1.
    norm=0

  elif val[:4]=="epar":
    cmap=plt.cm.bwr
    name='Epar [mV/m]'
    vran=[-1.0,1.0]
    nlev=51
    tick=0.5
    ufac=1.
    norm=0

  elif val[:4]=="eper":
    cmap=plt.cm.bwr
    name='Eper [mV/m]'
    vran=[-2.0,2.0]
    nlev=51
    tick=1.
    ufac=1.
    norm=0


#######
  elif val=="rr":
    cmap=plt.cm.jet                             # name of colormap
#   cmap=plt.cm.nipy_spectral
    name='N [cm$^{-3}$]'                        # name for colobar title
    vran=[0.0,40.0]                             # default range of value
#   vran=[0.0,80.0]                             # default range of value
    nlev=51                                     # number of coutour level
    tick=10.                                    # interval of major ticks for colorbar
    ufac=1.                                     # unit factor for a val in a desried unit
    norm=0                                      # 0 for linear-scale, 1 for log-scale

  elif val=="pp":
    cmap=plt.cm.jet
    name='Pp [pPa]'
    vran=[0.0,3000.0]
    nlev=51
    tick=500.
    ufac=1.
    norm=0

  elif val=="pdy":
    cmap=plt.cm.jet
    name='Pdy [nPa]'
    vran=[0.0,20.0]
    nlev=51
    tick=5.
    ufac=1.
    norm=0

  elif val=="kev":
    cmap=plt.cm.jet
    name='T [keV]'
    vran=[0,1.0]
    nlev=51
    tick=0.2
    ufac=1.
    norm=0


#######
  elif val=="resis":
    cmap=plt.cm.jet
    name='Resis [Ohm m]'
    vran=[0,0.5]
    nlev=51
    tick=0.1
    ufac=1.
    norm=0


  elif val=="absepar":
    cmap=plt.cm.jet
    name='absepar [V/m]'
    vran=[1e-7,1e-1]
    nlev=51
    tick=0.1
    ufac=1.
    norm=1

  elif val=="eint":
    cmap=plt.cm.bwr
    name=r'$\int E_{||} ds$ [kV]'
    vran=[-30.0,30.0]
    nlev=51
    tick=10.
    ufac=1.
    norm=0

  elif val=="abseint":
    cmap=plt.cm.jet
    name=r'$| \int E_{||} ds |$ [kV]'
    vran=[0.0,30.0]
    nlev=51
    tick=5.
    ufac=1.
    norm=0

  elif val=="fbalx":
    cmap=plt.cm.bwr				# name of colormap
    name='fbalx [fN/m$^3$]'                     # name for colobar title
    vran=[-50.0,50.0]                           # default range of value
    nlev=51                                     # number of coutour level
    tick=10.                                    # interval of major ticks for colorbar
    ufac=1.                                     # unit factor for a val in a desried unit
    norm=0                                      # 0 for linear-scale, 1 for log-scale

  elif val=="fbaly":
    cmap=plt.cm.bwr
    name='fbaly [fN/m$^3$]'
    vran=[-50.0,50.0]
    nlev=51
    tick=10.
    ufac=1.
    norm=0

  elif val=="zgse":
    cmap=plt.cm.bwr
    name='Zgse [Re]'
    vran=[-20.,20.]
    nlev=51
    tick=5.
    ufac=1.
    norm=0


####### xray values
  elif val=='xray':
    cmap=plt.cm.jet
    name='Xray Rate [keVcm$^{-2}$s$^{-1}$sr$^{-1}$]'
    vran=[0.,20.]
    nlev=51
    tick=5.
    ufac=1e-3
    norm=0

  elif val=='xraycut':
    cmap=plt.cm.jet
    name='Xray Rate [keVcm$^{-3}$s$^{-1}$]'
    vran=[0.,3.]
    nlev=51
    tick=0.5
    ufac=1e-3
    norm=0

  elif val=='Qcut':
    cmap=plt.cm.jet
    name='Qcut [LOG cm$^{-5}$s$^{-1}$]'
    vran=[1e8,1e12]
#   vran=[1e7,1e12]
    nlev=51
    tick=10.
    ufac=1.
    norm=1


  elif val=='nsw':
    cmap=plt.cm.jet
    name='Nsw [cm$^{-3}$]'
    vran=[0.,50.]
    nlev=51
    tick=10
    ufac=1.
    norm=0

  elif val=='nn':
    cmap=plt.cm.jet
    name='Nn [cm$^{-3}$]'
    vran=[0.,20.]
    nlev=51
    tick=5
    ufac=1.
    norm=0

  elif val=='vsw':
    cmap=plt.cm.jet
    name='Vsw [km/s]'
    vran=[0.,400.]
    nlev=51
    tick=50
    ufac=1.
    norm=0

  elif val=='vth':
    cmap=plt.cm.jet
    name='Vth [km/s]'
    vran=[0.,800.]
    nlev=51
    tick=100
    ufac=1.
    norm=0

  elif val=='vav':
    cmap=plt.cm.jet
    name='<V> [km/s]'
    vran=[0.,800.]
    nlev=51
    tick=100
    ufac=1.
    norm=0

  elif val=='tev':
    cmap=plt.cm.jet
    name='T [eV]'
    vran=[0.,400.]
    nlev=51
    tick=50
    ufac=1.
    norm=0


  else  :		# defalut values
    cmap=plt.cm.jet
    name=val+' [?]'
    vran=[0,100.0]
    nlev=51
    tick=20.
    ufac=1.
    norm=0


  if norm==0:   # for linear-scale contour
     dlev = (vran[1]-vran[0])/(nlev-1)		 	# interval of contour level
     clev = np.arange(vran[0],vran[1]+dlev,dlev)	# contour levels
     tlev = np.arange(vran[0],vran[1]+tick,tick) 	# tick levels for the colorbar

  if norm==1: 	# for log-scale contour
     t1=log10(vran[0])
     t2=log10(vran[1])
     dt=log10(tick)

     dlev=(t2-t1)/(nlev-1)
     clev=[ 10**i for i in np.arange(t1,t2+dlev,dlev)]
     tlev=[ 10**i for i in np.arange(t1,t2+dt,dt) ]


  pkg_plot=[name,cmap,ufac,clev,tlev,norm]

  return pkg_plot
