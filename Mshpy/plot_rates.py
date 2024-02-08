#!/opt/local/bin/python
#
# plot xray rate

import os
import sys
HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/lib/")
sys.path.append(HOME+"/svn/hkc-project/trunk/src/mhd-openggcm")

import math
import locale
import numpy              as np
import matplotlib.pyplot  as plt
from read_rates               import read_mpbs,read_xray,read_ena, read_xraycut
from read_mhd                import *
from pkg_rates               import rate_vpkg
from openggcm_info           import runinfo,mhdtime,mhdt2tstr
from matplotlib.colors       import LogNorm
from matplotlib.ticker       import MultipleLocator, FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable



def rate_plot(nrow,ncol,fps,xran,yran,xx,yy,val,vstr,title,bl=[],mp=[]):

  fig = plt.figure(figsize=(8,11))
  for i in range(len(val)):
    #print(i)

    ax1      = fig.add_subplot(nrow,ncol,i+1,aspect='equal')
    ax1.tick_params(axis='both',which='major',labelsize=7)
    x,y      = np.meshgrid(xx,yy)
    pkg_plot = rate_vpkg(vstr[i])

    if pkg_plot[5]==1:
      #print(x,y)
#      print(val[i]*pkg_plot[2])
      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], cmap=pkg_plot[1],norm=LogNorm())
#     cs    = ax1.pcolor(x,y,val[i]*pkg_plot[2],cmap=pkg_plot[1],	\
#             norm=LogNorm(vmin=pkg_plot[3][0],vmax=pkg_plot[3][-1]))
    else :
#      print(x,y,val[i]*pkg_plot[2])
      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], cmap=pkg_plot[1],extend='both')
#      print(x,y)
#     cs    = ax1.pcolor(x,y,val[i]*pkg_plot[2],vmin=pkg_plot[3][0],vmax=pkg_plot[3][-1], \
#             cmap=pkg_plot[1]) #,extend='both')

    if len(bl)!=0 :
#     for j in range(len(bl[0])/15): pl = ax1.plot(bl[0][j*15],bl[1][j*15],'w-',lw=0.1)
      for j in range(len(bl[0])/1): pl = ax1.plot(bl[0][j*1],bl[1][j*1],'k-',lw=0.1)
    if len(mp)!=0 :
      pl1 = ax1.plot(mp[0],mp[1],'k-')
      pl2 = ax1.plot(mp[2],mp[3],'k-')

    cax1  = make_axes_locatable(ax1)
    cax2  = cax1.append_axes("right",size="3%",pad="5%")
    cb    = fig.colorbar(cs,cax=cax2,ticks=pkg_plot[4])
    cl    = plt.getp(cb.ax, 'ymajorticklabels')
    plt.setp(cl, fontsize=7)


    ax1.xaxis.set_major_locator(MultipleLocator(xran[2]))
    ax1.xaxis.set_minor_locator(MultipleLocator(xran[3]))
    ax1.yaxis.set_major_locator(MultipleLocator(yran[2]))
    ax1.yaxis.set_minor_locator(MultipleLocator(yran[3]))
    ax1.set_xlim(xran[0],xran[1])
    ax1.set_ylim(yran[0],yran[1])
#    print(xran,yran)
    if vstr[i]!='xraycut':
        ax1.set_ylabel('Polar angle [deg]',fontsize=10)
        ax1.set_xlabel('Azimuth angle [deg]', fontsize=10)
    else:
        ax1.set_ylabel('Ygse [Re]',fontsize=10)
        ax1.set_xlabel('Xgse [Re]', fontsize=10)
    ax1.grid(True)

##### titles for the figures
    vmax,vmin = maxmin_ran([xran[0],xran[1]],[yran[0],yran[1]],xx,yy,val[i])
    lmax = "Max: %.3f "%(vmax*pkg_plot[2])
    lmin = "Min: %.3f "%(vmin*pkg_plot[2])
    print(vstr[i],lmax,lmin)

#   if i==0: plt.figtext(0.5,0.95,title,fontsize=13,ha='center',va='bottom')
#ax1.set_title(title,fontsize=10)
    ax1.text(0.0,1.0,title,      fontsize=10,ha='left', va='bottom',transform=ax1.transAxes)
    ax1.text(1.0,1.0,pkg_plot[0],fontsize=10,ha='right',va='bottom',transform=ax1.transAxes)
    ax1.text(0.0,0.0,lmin       ,fontsize=10,ha='left' ,va='bottom',transform=ax1.transAxes,color='white')
    ax1.text(1.0,0.0,lmax       ,fontsize=10,ha='right',va='bottom',transform=ax1.transAxes,color='white')

  print("Save ",fps)
  plt.savefig(fps)
  plt.close()

  return

def rate_info(fps,fin,fbl,fmp,vstr,xran,yran,tash):
  "set information for mhd plots                                                "

  nrow  = 1
  ncol  = 1
#  print(fin[0])
  info  = runinfo(fin[0])
  time  = mhdt2tstr(locale.atoi(info.mhdt)+tash,info.ti)
  mhdt  = mhdtime(time)

# fps = Dps+'/'+fin.split('/')[-1]+'.ps'
# print "plot ",fps

  if   vstr=='ena' :
    phi,lat,rate1,sc = read_ena(fin[0])
    rate             = rate1[0]
    stitle           = vstr+'%5.2fkeV_x%02dy%02dz%02d'%(sc[-1]/1e3,sc[0],sc[1],sc[2])
  elif vstr=='ena_nhmax':
    phi,lat,rate1,sc = read_ena(fin[0])
    rate             = rate1[1]
    stitle           = vstr+'%5.2fkeV_x%02dy%02dz%02d'%(sc[-1]/1e3,sc[0],sc[1],sc[2])
  elif vstr=='ena_nhmin':
    phi,lat,rate1,sc = read_ena(fin[0])
    rate             = rate1[2]
    stitle           = vstr+'%5.2fkeV_x%02dy%02dz%02d'%(sc[-1]/1e3,sc[0],sc[1],sc[2])
  elif vstr=='ena_10keV':
    phi,lat,rate1,sc = read_ena(fin[0])
    rate             = rate1[0]
    stitle           = 'ena_%5.2fkeV_x%02dy%02dz%02d'%(sc[-1]/1e3,sc[0],sc[1],sc[2])
  elif vstr=='ena_5keV':
    phi,lat,rate1,sc = read_ena(fin[0])
    rate             = rate1[0]
    stitle           = 'ena_%5.2fkeV_x%02dy%02dz%02d'%(sc[-1]/1e3,sc[0],sc[1],sc[2])
  elif vstr=='dena' :
    phi,lat,rate1,sc = read_ena(fin[0])
    phi,lat,rate2,sc = read_ena(fin[1])
    rate             = rate1[0]-rate2[0]
    stitle           = vstr+'%5.2fkeV_x%02dy%02dz%02d'%(sc[3]/1e3,sc[0],sc[1],sc[2])
  elif vstr=='xray':
    phi,lat,rate,sc = read_xray(fin[0])
    stitle          = vstr+'_sc%02d%02d%02d'%(sc[0],sc[1],sc[2])
  elif vstr=='xraycut':
    phi,lat,rate    = read_xraycut(fin[0])
    stitle          = vstr+'_cut'
  elif vstr=='Qxray':
    phi,lat,xrate,sc = read_xray(fin[0])
    if len(xrate)==3 : rate=xrate[0]
    stitle          = vstr+'_sc%02d%02d%02d_nh0'%(sc[0],sc[1],sc[2])
  elif vstr=='Qxray_nhmin':
    phi,lat,xrate,sc = read_xray(fin[0])
    if len(xrate)==3 : rate=xrate[1]
    stitle          = vstr+'_sc%02d%02d%02d_nhmin'%(sc[0],sc[1],sc[2])
  elif vstr=='Qxray_nhmax':
    phi,lat,xrate,sc = read_xray(fin[0])
    if len(xrate)==3 : rate=xrate[2]
    stitle          = vstr+'_sc%02d%02d%02d_nhmax'%(sc[0],sc[1],sc[2])
  elif vstr=='dxray':
    phi,lat,rate1,sc = read_xray(fin[0])
    phi,lat,rate2,sc = read_xray(fin[1])
    rate             = rate1-rate2
    stitle           = vstr+'_sc%02d%02d%02d'%(sc[0],sc[1],sc[2])
  print("test max,min", np.nanmax(rate),np.nanmin(rate))


  bl=[];mp=[]
  if fbl!='none': bl  = read_bline(fbl,sc)
  if fmp!='none': mp  = read_mpbs(fmp,sc)


  title = mhdt.name+'\n'+info.run+'.'+stitle+'.'+info.mhdt
  fname = fps+'/'+info.run+'.'+stitle+'.'+info.mhdt+'.ps'
  if vstr=='dena' or vstr=='dxray':
    title = title+'-'+runinfo(fin[1]).mhdt
    fname = fps+'/'+info.run+'.'+stitle+'.'+info.mhdt+'-'+runinfo(fin[1]).mhdt+'.ps'

  fname = fps+'/'+fin[0].split('/')[-1]+'.png'
  print(fname)

# print len(phi),len(lat),len(rate),len(rate[0])
  rate_plot(nrow,ncol,fname,xran,yran,phi,lat,[rate],[vstr],title,bl=bl,mp=mp)

  return


def main(argv):

  fps   = argv[0]                       # plot directory
  fin   = argv[1].split(':')		# input file
  fbl   = argv[2]			# input file for bl
  fmp   = argv[3]			# input file for BS,MP
  pran  = argv[4].split(':')            # plot range: type:x1:x2:dx1:dx2:y1:y2:dy1:dy2
  tash  = locale.atoi(argv[5])

  vstr  = pran[0] 			# xray or ena
  x1    = locale.atof(pran[1])          # xrange x1-x2
  x2    = locale.atof(pran[2])
  dx1   = locale.atof(pran[3])          # major x-tick interval
  dx2   = locale.atof(pran[4])          # minor x-tick interval
  y1    = locale.atof(pran[5])          # yrange y1-y2
  y2    = locale.atof(pran[6])
  dy1   = locale.atof(pran[7])          # major y-tick interval
  dy2   = locale.atof(pran[8])          # minor y-tick interval
  xran  = [x1,x2,dx1,dx2]
  yran  = [y1,y2,dy1,dy2]

  if vstr=='dena' or vstr=='dxray':
     fin.append(fin[0][:-6]+'%06d'%locale.atoi(pran[9]));print(fin)
  rate_info(fps,fin,fbl,fmp,vstr,xran,yran,tash)

  return


if __name__ == "__main__":
  main(sys.argv[1:])
