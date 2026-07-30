#!/opt/local/bin/python
#
# draw MHD plots

import os
import sys
HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/lib/")


import locale
import numpy              as np
import matplotlib.pyplot  as plt
from read_mhd                import *
from pkg_mhdplot             import mhd_vpkg
from openggcm_info           import runinfo,mhdtime,mhdt2tstr
from matplotlib.colors       import LogNorm
from matplotlib.ticker       import MultipleLocator, FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable



def mhd_2Dplot(nrow,ncol,fps,pn,lp,xran,yran,xx,yy,val,vstr,title):
  "plot mhd"

####### tick info for pn=xr
  def xr_zgse(x, pos):
    value=x*cos(radians(lp))
    return '%2d' % (round(value))
  def xr_ygse(x, pos):
    value=-x*sin(radians(lp))
    return '%2d' % (round(value))

####### draw graphs
  fig = plt.figure(figsize=(8,11))

  for i in range(len(val)):

    ax1      = fig.add_subplot(nrow,ncol,i+1,aspect='equal')
    ax1.tick_params(axis='both',which='major',labelsize=7)
    x,y      = np.meshgrid(xx,yy)
    pkg_plot = mhd_vpkg(vstr[i])

    if pkg_plot[5]==1:
      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], \
              cmap=pkg_plot[1],norm=LogNorm())
    else :
#      print(np.shape(x),np.shape(y),np.shape(val[i]),np.shape(pkg_plot[2]))
      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], cmap=pkg_plot[1],extend='both')

    cax1  = make_axes_locatable(ax1)
    cax2  = cax1.append_axes("right",size="3%",pad="5%")
    cb    = fig.colorbar(cs,cax=cax2,ticks=pkg_plot[4])
    cl    = plt.getp(cb.ax, 'ymajorticklabels')
    plt.setp(cl, fontsize=7)


#   circle1=plt.Circle((2.,0),3,facecolor='None',edgecolor='magenta')
#   circle2=plt.Circle((-2.,0),3,facecolor='None',edgecolor='magenta')
#   ax1.add_artist(circle1)
#   ax1.add_artist(circle2)


####### tick infomation

    if pn!='xr':
      ax1.yaxis.set_major_locator(MultipleLocator(yran[2]))
      ax1.yaxis.set_minor_locator(MultipleLocator(yran[3]))
      if pn=='xy' : xl='Xgse [Re]';yl='Ygse [Re]'
      if pn=='xz' : xl='Xgse [Re]';yl='Zgse [Re]'
      if pn=='yz' : xl='Ygse [Re]';yl='Zgse [Re]'
      if pn=='sc' : xl='Spin angle [deg]';yl='Polar angle [deg]'

    if pn=='xr': # xaxis rotation
      xl      = 'Xgse [Re]'
      yl      = 'Zgse [Re]'

    if pn=='zr': # zaxis rotation
      xl      = 'Xgse [Re]'
      yl      = 'Zgse [Re]'
## calculate zgse
      ax1.yaxis.set_major_locator(MultipleLocator(abs(yran[2]/np.cos(np.radians(lp)))))
      ax1.yaxis.set_minor_locator(MultipleLocator(abs(yran[3]/np.cos(np.radians(lp)))))
      ax1.yaxis.set_major_formatter(FuncFormatter(xr_zgse))
## calculate ygse
#     aa1=ax1.twinx()
#     aa1.set_ylim(-yran[0]*np.sin(np.radians(lp)),-yran[1]*np.sin(np.radians(lp)))
#     aa1.yaxis.set_major_locator(MultipleLocator(abs(yran[2]/np.sin(np.radians(lp)))))
#     aa1.yaxis.set_minor_locator(MultipleLocator(abs(yran[3]/np.sin(np.radians(lp)))))
#     aa1.grid(True)
#     aa1.yaxis.set_major_formatter(FuncFormatter(xr_ygse))

    ax1.xaxis.set_major_locator(MultipleLocator(xran[2]))
    ax1.xaxis.set_minor_locator(MultipleLocator(xran[3]))
    ax1.set_xlim(xran[0],xran[1])
    ax1.set_ylim(yran[0],yran[1])

    if i%ncol==0         : ax1.set_ylabel(yl,fontsize=10)
    if i>ncol*(nrow-1)-1 : ax1.set_xlabel(xl,fontsize=10)
    ax1.grid(True)


##### titles for the figures
    if pkg_plot[5]==1:
      vmax,vmin = maxmin_ran([xran[0],xran[1]],[yran[0],yran[1]],xx,yy,np.log10(val[i]*pkg_plot[2]))
    else :
      vmax,vmin = maxmin_ran([xran[0],xran[1]],[yran[0],yran[1]],xx,yy,val[i]*pkg_plot[2])

    lmax = "Max: %.2f "%vmax
    lmin = "Min: %.2f "%vmin
    print (vstr[i],lmax,lmin)

#   if i==0:  ax1.set_title(title,fontsize=10)
#plt.figtext(0.5,0.95,title,fontsize=13,ha='center',va='bottom')
    if i==0: ax1.text(0.0,1.1,title,fontsize=10,ha='left', va='bottom',transform=ax1.transAxes)
    ax1.text(1.0,1.0,pkg_plot[0],fontsize=10,ha='right',va='bottom',transform=ax1.transAxes)
    ax1.text(0.0,0.0,lmin       ,fontsize=10,ha='left' ,va='bottom',transform=ax1.transAxes)
    ax1.text(1.0,0.0,lmax       ,fontsize=10,ha='right',va='bottom',transform=ax1.transAxes)


  plt.savefig(fps)

  return





def mhd_info(Dps,info,fmhd,pn,lp,xran,yran,tash):
  "set information for mhd plots 						\
   read_2DMHD gives MHD values in the following orders				\
   vv   = [ bx,by,bz,bt,vx,vy,vz,vt,ex,ey,ez,et,jx,jy,jz,jt,rr,pp,pdy,kev ]	"


  nrow=4
  ncol=1

  xx,yy,vv,vstr = read_2DMHD(fmhd,pn)


  val1=[ [vv[0],vv[1],vv[2],vv[3]], 	\
         [vv[4],vv[5],vv[6],vv[7]], 	\
         [vv[8],vv[9],vv[10],vv[11]], 	\
         [vv[12],vv[13],vv[14],vv[15]],	\
         [vv[16],vv[17],vv[18],vv[19]], \
         [vv[22],vv[23],vv[24],vv[25]], \
         [vv[20],vv[21]]  		]


  vstr1=[ [vstr[0],vstr[1],vstr[2],vstr[3]], 		\
          [vstr[4],vstr[5],vstr[6],vstr[7]], 		\
          [vstr[8],vstr[9],vstr[10],vstr[11]], 		\
          [vstr[12],vstr[13],vstr[14],vstr[15]], 	\
          [vstr[16],vstr[17],vstr[18],vstr[19]],	\
          [vstr[22],vstr[23],vstr[24],vstr[25]],	\
          [vstr[20],vstr[21]] 				]


  fname=[ 'bxyzt', \
          'vxyzt', \
          'exyzt', \
          'jxyzt', \
          'rppt' , \
          'xray' , \
          'epareta'   ]

# nrow = 1
# ncol = 1
# val1 = [[vv[16]]]
# vstr1= [[vstr[16]]]
# fname= ['rr']

  time = mhdt2tstr(locale.atoi(info.mhdt)+tash,info.ti)
  mhdt = mhdtime(time)

  if tash==0: title= mhdt.name+'\n'+info.run+'.'+pn+'_'+str(lp)+'.'+info.mhdt
  else: title= mhdt.name+': %dmin shifted\n'%int(tash/60)+info.run+'.'+pn+'_'+str(lp)+'.'+info.mhdt

  print ('============================================================================')
  lps=''
  for i in [0,1,4,5] :

    Dps1=Dps+'/'+fname[i]
    if not os.path.exists(Dps1): os.system('mkdir '+Dps1)

    fps = Dps1+'/'+info.run+'.'+fname[i]+'.'+info.mhdt+'.'+pn+'_'+str(lp)+'.png'
    print ("SAVE ",fps)

    mhd_2Dplot(nrow,ncol,fps,pn,lp,xran,yran,xx,yy,val1[i],vstr1[i],title)

    lps=lps+' '+fps


  print ('============================================================================')
  print ("MAKE ONE SUMMARY PLOT")

  Dps1=Dps+'/summary/'
  if not os.path.exists(Dps1): os.system('mkdir '+Dps1)
  fname=Dps1+info.run+'.'+pn+'_'+str(lp)+'.'+info.mhdt+'.jpg'
  cmd='convert -trim '+lps+' +append '+fname
  print (cmd)
  os.system(cmd)

  return


def main(argv):

  fname = argv[0].split(':') 	        # list of filenames
  fgrd  = fname[0]
  f3df  = fname[1]
  Dmhd  = fname[2]			# directory of openggcm ascii file
#  print(Dmhd)
  Dps   = fname[3]                      # directory to save plots


  vran  = argv[1].split(':')            # value range: pn:lp:xi:xf:yi:yf:ds
  pn    = vran[0]                       # plane : xy,xz,yz,xr
  lp    = locale.atof(vran[1])          # plane location
  xi    = locale.atof(vran[2])
  xf    = locale.atof(vran[3])
  yi    = locale.atof(vran[4])
  yf    = locale.atof(vran[5])
  ds    = locale.atof(vran[6])


  pran  = argv[2].split(':')         	# plot range: x1:x2:dx1:dx2:y1:y2:dy1:dy2:re
  x1    = locale.atof(pran[0])		# xrange x1-x2
  x2    = locale.atof(pran[1])
  dx1   = locale.atof(pran[2])		# major x-tick interval
  dx2   = locale.atof(pran[3])		# minor x-tick interval
  y1    = locale.atof(pran[4])		# yrange y1-y2
  y2    = locale.atof(pran[5])
  dy1   = locale.atof(pran[6])		# major y-tick interval
  dy2   = locale.atof(pran[7])		# minor y-tick interval
  xran  = [x1,x2,dx1,dx2]
  yran  = [y1,y2,dy1,dy2]

  tash  = locale.atoi(argv[3])

  info  = runinfo(f3df)
  fmhd  = Dmhd+'/'+info.run+'.'+pn+'_'+vran[1]+'.'+info.mhdt
  #print('fmhd',fmhd)
  Dps1  = Dps+'/'+pn+'_'+vran[1]
  #print(Dps1)
  if not os.path.exists(Dps1): os.system('mkdir '+Dps1)

###### create and read an ascii file of openggcm
# if os.path.isfile(fmhd):
#   print '============================================================================'
#   print "create ",fmhd
#   print ' '
#   test=raw_input('Fmhd exists! Press (o/O) to Overwrite and (u/U) to use the old Fmhd :')
#   if   test=='o' or test=='O' :
#      os.system('rm '+fmhd)
#      create_mhd(fmhd,fgrd,f3df,info.dipt,pn,lp,xi,xf,yi,yf,ds)
#   elif test=='u' or test=='U' :
#      pass
#   else           :
#      print "Error! Press O for Overwrite, U for Using old file. Please Run again"
#      sys.exit(1)
# else :
#      create_mhd(fmhd,fgrd,f3df,info.dipt,pn,lp,xi,xf,yi,yf,ds)

#  print('mhdinfo('+str(Dps1)+','+str(info)+','+str(fmhd)+','+str(pn)+','+str(lp)+','+str(xran)+','+str(yran)+','+str(tash)+')')
  mhd_info(Dps1,info,fmhd,pn,lp,xran,yran,tash)

####### one plot per a figure
# xx,yy,vv,vstr = read_2DMHD(fmhd,pn)
# print '============================================================================'
# for i in range(len(vstr)):
#   fps = Dps+'/'+vstr[i]+'/'+info.run+'.'+vstr[i]+'.'+info.mhdt+'.'+pn+'_'+vran[1]+'.ps'
#   print "SAVE ",fps
#   mhd_2Dplots(1,1,fps,pn,lp,xran,yran,xx,yy,[vv[i]],[vstr[i]])
####### several plots per a figure

  return


# if this current python file is used as main, execute the function 'main'
if __name__ == "__main__":

  main(sys.argv[1:])
