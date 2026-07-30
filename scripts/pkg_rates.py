import os, locale
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import cm
from math import log10


def rate_vpkg(val):
  "set colormap, title, and range of variables for mhd plot"

####### xray values
  if val=='xray':
    cmap=plt.cm.jet
    name='Xray Intensity [$keV{}cm^{-2}s^{-1}sr^{-1}$]'
    name='[$keV{}cm^{-2}s^{-1}sr^{-1}$]'
    vran=[0,15]
    nlev=51
    tick=5
    ufac=1e-3
    norm=0

  elif val=='xraycut':
    cmap=plt.cm.jet
    name='Xray Rate [keVcm$^{-3}$s$^{-1}$]'
    vran=[0.,0.1]
    nlev=51
    tick=0.01
    ufac=1e-3
    norm=0

#   name='[LOG $eV{}cm^{-2}s^{-1}sr^{-1}$]'
#   vran=[100,100000]
#   tick=10.
#   ufac=1.
#   norm=1

  elif val=='Qxray' or val=='Qxray_nhmax' or val=='Qxray_nhmin':
    cmap=plt.cm.jet
#   cmap=plt.cm.gnuplot
    name='Q [10$^{20}$ cm$^{-4}$s$^{-1}$]'
    vran=[0.0,4.0]
    nlev=51
    tick=1.0
    ufac=1e-20
    norm=0

  elif val=='sQxray':	# strong Qxray
    cmap=plt.cm.jet
#   cmap=plt.cm.gnuplot
    name='Q [10$^{20}$ cm$^{-4}$s$^{-1}$]'
    vran=[0.,20.]
    nlev=51
    tick=4.
    ufac=1e-20
    norm=0

#   name='LOG Q [cm$^{-4}$s$^{-1}$]'
#   vran=[0.5e20,1e20]
#   tick=0.1e20
#   ufac=1.
#   norm=1

  elif val=='dxray':
    cmap=plt.cm.bwr
    name='$\Delta$ Q [10$^{20}$ cm$^{-4}$s$^{-1}$]'
    vran=[-0.5,0.5]
    nlev=51
    tick=0.1
    ufac=1e-20
    norm=0

  elif val=='ena' or val=='ena_nhmax' or val=='ena_nhmin':
    cmap=plt.cm.jet
    name='[$10^3 cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
#   name='ENA Flux [$10^3 cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
    vran=[0.,50.]
    nlev=51
    tick=10.
    ufac=1.e-3
    norm=0

#   name='[LOG $cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
#   vran=[100,100000]
#   ufac=1.
#   tick=10
#   norm=1

#   name='ENA Flux [$cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
#   vran=[0.,10]
#   tick=2.
#   ufac=1.

#   name='ENA Flux [$cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
#   vran=[1e3,1e5]
#   tick=10.
#   ufac=1.
#   norm=1

  elif val=='ena_5keV':
    cmap=plt.cm.jet
    name='[LOG $cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
    name='[$cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
#   name='ENA Flux [$10^3 cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
    vran=[0.1,100000]
    nlev=51
    tick=10
    ufac=1. #.e-3
    norm=1.

  elif val=='ena_10keV':
    cmap=plt.cm.jet
    name='[LOG $cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
    name='[$cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
#   name='ENA Flux [$10^3 cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
    vran=[0.1,10000]
    nlev=51
    tick=10
    ufac=1. #.e-3
    norm=1.

  elif val=='dena':
    cmap=plt.cm.bwr
    name='$\Delta$ ENA Flux [$10^3 cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
    name='[$10^3 cm^{-2}s^{-1}sr^{-1}keV^{-1}$]'
    vran=[-5.,5.]
    nlev=51
    tick=1.
    ufac=1e-3
    norm=0


  elif val=='Rcount':
    cmap=plt.cm.jet
#   cmap=plt.cm.hot
    name='Xray count [$counts min^{-1} deg^{-2}$]'
    name='[counts/pix]'
    vran=[0.,100.]
    nlev=51
    tick=20.
    ufac=1.
    norm=0

  elif val=='Bin_count':
    cmap=plt.cm.jet
    name='[counts/pix]'
    vran=[0.,200.]
    nlev=51
    tick=40.
    ufac=1.
    norm=0

#   vran=[1e1,1e3]
#   tick=1e1
#   norm=1


  elif val=='Kcount':
    cmap=plt.cm.hot
    cmap=plt.cm.jet
    name='ROSAT Xray count [$counts min^{-1} deg^{-2}$]'
    name='[counts/$0.25^{2{}\circ}$pix/$2$ min]'
    vran=[0.,150.]
    nlev=51
    tick=30.
    ufac=1.
    norm=0


  elif val=="prec_e_fe_1":
    cmap=plt.cm.jet                             # name of colormap
    name='Energy Flux [mW/m$^2$]'               # name of colorbar title
    name='[mW/m$^2$]'               # name of colorbar title
    vran=[0.1,300]                              # default range of value
    nlev=51                                     # number of contour level
    tick=10                                     # interval of major ticks for colorbar
    ufac=1.e3                                   # unit factor for a val in a desired unit
    norm=1                                      # 0 for linear-scale, 1 for log-scale



  elif val=='nsw':
    cmap=plt.cm.jet
    name='N [cm$^{-3}$]'
    name='[$cm^{-3}$]'
    vran=[0.,40.]
    nlev=51
    tick=10.
    ufac=1.
    norm=0

  elif val=='nn':
    cmap=plt.cm.jet
    cmap=plt.cm.gnuplot
    name='Nn [cm$^{-3}$]'
    vran=[0.,50.]
    nlev=51
    tick=10
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

  elif val=='vx':
    cmap=plt.cm.bwr
    name='[km/s]'
    vran=[-400.,400.]
    nlev=51
    tick=200
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
    cmap=plt.cm.gnuplot
    name='<G> [km/s]'
    vran=[100.,500.]
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

  elif val=='bt':
    cmap=plt.cm.jet
    cmap=plt.cm.gnuplot
    name='|B| [nT]'
    vran=[0.,100.]
    nlev=51
    tick=20
    ufac=1.
    norm=0

  elif val=='bx':
    cmap=plt.cm.bwr
    name='Bx [nT]'
    vran=[-100,100.]
    nlev=51
    tick=20
    ufac=1.
    norm=0

  elif val=='rr':
#   cmap=plt.cm.Greys
    cmap=plt.cm.jet
    name='Np [cm$^{-3}$]'
    vran=[0.,40.]
    nlev=51
    tick=10.
    ufac=1.
    norm=0

  elif val=="jt":
    cmap=plt.cm.jet
    cmap=plt.cm.gnuplot
    name='|J| [nA/m$^2$]'
    vran=[0.0,10.0]
    nlev=51
    tick=2.
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
     print("norm vran: v1,v2,dv=",t1,t2,dt)

     dlev=(t2-t1)/(nlev-1)
     clev=[ 10**i for i in np.arange(t1,t2+dlev,dlev)]
     tlev=[ 10**i for i in np.arange(t1,t2+dt,dt) ]


  pkg_plot=[name,cmap,ufac,clev,tlev,norm]

  return pkg_plot
