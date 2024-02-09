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
from matplotlib.colors       import LogNorm
from matplotlib.ticker       import MultipleLocator, FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

from read_rates               import read_mpbs,read_xray,read_ena, read_xraycut, rate_vpkg
from openggcm_info           import runinfo,mhdtime,mhdt2tstr

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


def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'$10^{{{}}}$'.format(b)


def rate_plot(nrow,ncol,fps,xran,yran,xx,yy,val,vstr,title,bl=[],mp=[]):

  fig = plt.figure(figsize=(8,8))
  for i in range(len(val)):
    #print(i)
    if vstr[i]=='xray':
        if i==1:
            xx0=xx[i]
            xx[i]=180-np.array(yy[i])
            yy[i]=np.array(xx0)-180
            val[i]=np.transpose(val[i])
#    print(np.shape(xx[i]),np.shape(yy[i]),np.shape(val[i]))
    #print(xx[i])

    ax1      = fig.add_subplot(nrow,ncol,i+1,aspect='equal')
    ax1.tick_params(axis='both',which='major',labelsize=7)
    x,y      = np.meshgrid(xx[i],yy[i])
    pkg_plot = rate_vpkg(vstr[i])
    valc=val[i][:-1,:-1]

    if pkg_plot[5]==1:
      #print(x,y)
#      print(val[i]*pkg_plot[2])
      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], cmap=pkg_plot[1],norm=LogNorm())
#     cs    = ax1.pcolor(x,y,val[i]*pkg_plot[2],cmap=pkg_plot[1],	\
#             norm=LogNorm(vmin=pkg_plot[3][0],vmax=pkg_plot[3][-1]))
    else :
#      print(x,y,val[i]*pkg_plot[2])
#      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], cmap=pkg_plot[1],extend='both')
#      cs    = ax1.pcolormesh(x,y,val[i]*pkg_plot[2], cmap=pkg_plot[1])
      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], cmap=pkg_plot[1])
#      print(np.min(x),np.max(x),np.min(y),np.max(y))
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
    if pkg_plot[5]==1:
        cb    = fig.colorbar(cs,cax=cax2,ticks=pkg_plot[4],format=FuncFormatter(fmt))
    else:
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
        if i==1:
            ax1.set_xlabel('Polar angle [deg]',fontsize=10)
            ax1.set_ylabel('Azimuth angle [deg]', fontsize=10)
        else:
            ax1.set_ylabel('Polar angle [deg]',fontsize=10)
            ax1.set_xlabel('Azimuth angle [deg]', fontsize=10)
    else:
        ax1.set_ylabel('Ygse [Re]',fontsize=10)
        ax1.set_xlabel('Xgse [Re]', fontsize=10)
    ax1.grid(True)

##### titles for the figures
    vmax,vmin = maxmin_ran([xran[0],xran[1]],[yran[0],yran[1]],xx[i],yy[i],val[i])

    if vstr[i]!='xraycut':
        lmax = "Max: %.3f "%(vmax*pkg_plot[2])
        lmin = "Min: %.3f "%(vmin*pkg_plot[2])
    else:
        lmax = "Max: %.3e "%(vmax*pkg_plot[2])
        lmin = "Min: %.3e "%(vmin*pkg_plot[2])

    print(vstr[i],lmax,lmin)

#   if i==0: plt.figtext(0.5,0.95,title,fontsize=13,ha='center',va='bottom')
#ax1.set_title(title,fontsize=10)
    ax1.text(0.0,1.0,title[i],      fontsize=10,ha='left', va='bottom',transform=ax1.transAxes)
    ax1.text(1.0,1.0,pkg_plot[0],fontsize=10,ha='right',va='bottom',transform=ax1.transAxes)
    if vstr[i]!='xraycut':
        ax1.text(0.0,0.0,lmin       ,fontsize=10,ha='left' ,va='bottom',transform=ax1.transAxes,color='white')
        ax1.text(1.0,0.0,lmax       ,fontsize=10,ha='right',va='bottom',transform=ax1.transAxes,color='white')
    else:
        ax1.text(0.0,0.0,lmin       ,fontsize=10,ha='left' ,va='bottom',transform=ax1.transAxes,color='black')
        ax1.text(1.0,0.05,lmax       ,fontsize=10,ha='right',va='bottom',transform=ax1.transAxes,color='black')


    ax1.invert_xaxis()
 # ax1.ticklabel_format(useOffset=False)
  plt.tight_layout()
  print("Save ",fps)
  plt.savefig(fps)
  plt.close()

  return

def rate_info(fps,fin,fbl,fmp,vstr,xran,yran,tash):
  "set information for mhd plots                                                "

  nrow  = 1
  ncol  = len(vstr)
#  print(fin[0])
  info  = runinfo(fin[0])
  time  = mhdt2tstr(locale.atoi(info.mhdt)+tash,info.ti)
  mhdt  = mhdtime(time)

# fps = Dps+'/'+fin.split('/')[-1]+'.ps'
# print "plot ",fps
  phi={}
  lat={}
  rate1={}
  sc={}
  rate={}
  stitle={}
  rate2={}
  title={}
  fname={}
  for i in range(len(vstr)):
    if   vstr[i]=='ena' :
        phi[i],lat[i],rate1[i],sc[i] = read_ena(fin[i])
        rate[i]             = rate1[i][0]
        stitle[i]           = vstr[i]+'%5.2fkeV_x%02dy%02dz%02d'%(sc[i][-1]/1e3,sc[i][0],sc[i][1],sc[i][2])
    elif vstr[i]=='xray':
        phi[i],lat[i],rate[i],sc[i] = read_xray(fin[i])
        if i==0:
            stitle[i]          = vstr[i]+'_side%02d%02d%02d'%(sc[i][0],sc[i][1],sc[i][2])
        else:
            stitle[i]          = vstr[i]+'_polar%02d%02d%02d'%(sc[i][0],sc[i][1],sc[i][2])
    elif vstr[i]=='xraycut':
        phi[i],lat[i],rate[i]    = read_xraycut(fin[i])
        stitle[i]          = vstr[i]+'_cut'
  if vstr[0]=='xraycut':
    prop=np.empty_like(rate[0])
    prop2=np.empty_like(rate[0])
    count_0,count,count_nan=0,0,0
    for index,value in np.ndenumerate(rate[0]):
        prop[index]=abs(value-rate[1][index])/rate[1][index]
        count_0+=1
        if value>0:
            prop2[index]=abs(value-rate[1][index])/rate[1][index]
            count+=1
        elif np.isnan(value):
            count_nan+=1
        #else:print(prop[index])
    print('prop',np.nanmean(prop),np.nanmean(prop2))
#    print(prop,prop2)
    print('count',count_0,count,count_nan)
  print("test max,min", np.nanmax(rate[i]),np.nanmin(rate[i]))



  for i in range(len(vstr)):
      title[i] = info.run+'.'+stitle[i]
      if vstr[i]=='xraycut':
        if i==0: title[i]='Mshpy\n'
        elif i==1: title[i]='Jorgensen2019\n'
  #    fname = fps+'/'+info.run+'.'+stitle+'.'+info.mhdt+'.ps'
  fname = fps+'/'+fin[0].split('/')[-1]+'_2.png'
  print(fname)

  bl=[];mp=[]
  if fbl!='none': bl  = read_bline(fbl,sc)
  if fmp!='none': mp  = read_mpbs(fmp,sc)


# print len(phi),len(lat),len(rate),len(rate[0])
  rate_plot(nrow,ncol,fname,xran,yran,phi,lat,rate,vstr,title,bl=bl,mp=mp)

  return


def main(argv):

  fps   = argv[0]                       # plot directory
  fin   = argv[1].split(':')		# input file
  print(fin)
  fbl   = argv[2]			# input file for bl
  fmp   = argv[3]			# input file for BS,MP
  pran  = argv[4].split(':')            # plot range: type:x1:x2:dx1:dx2:y1:y2:dy1:dy2
  tash  = locale.atoi(argv[5])

  vstr  = pran[0].split(',') 			# xray or ena
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
