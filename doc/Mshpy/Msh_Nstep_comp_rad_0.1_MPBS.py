import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle as pl
import io
from read_mhd                import *
from pkg_mhdplot             import mhd_vpkg
from openggcm_info           import runinfo,mhdtime,mhdt2tstr
from matplotlib.colors       import LogNorm
from matplotlib.ticker       import MultipleLocator, FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

def mhd_2Dplot(nrow,ncol,fps,pn,lp,xran,yran,xx,yy,val,vstr,title,mpbs):
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

    ax1      = fig.add_subplot(nrow,ncol+1,2*i+1,aspect='equal')
    ax1.tick_params(axis='both',which='major',labelsize=7)
    x,y      = np.meshgrid(xx,yy)
    pkg_plot = mhd_vpkg(vstr[i])

    if pkg_plot[5]==1:
      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], \
              cmap=pkg_plot[1],norm=LogNorm())
    else :
#      print(np.shape(x),np.shape(y),np.shape(val[i]),np.shape(pkg_plot[2]))
      cs    = ax1.contourf(x,y,val[i]*pkg_plot[2],levels=pkg_plot[3], cmap=pkg_plot[1],extend='both')
      if 'y' in mpbs:
          cs2   = ax1.plot(mpbs.xmp,mpbs.y)
          cs2   = ax1.plot(mpbs.xbs,mpbs.y)
      if 'z' in mpbs:
          cs2   = ax1.plot(mpbs.xmp,mpbs.z)
          cs2   = ax1.plot(mpbs.xbs,mpbs.z)

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
  buf=io.BytesIO()
  pl.dump(fig,buf)
#  buf.seek(0)

  return buf

def mhd_info(Dps,info,fmhd,pn,lp,xran,yran,tash,fMPBS):
  "set information for mhd plots            \
   read_2DMHD gives MHD values in the following orders        \
   vv   = [ bx,by,bz,bt,vx,vy,vz,vt,ex,ey,ez,et,jx,jy,jz,jt,rr,pp,pdy,kev ] "


  nrow=4
  ncol=1

  xx,yy,vv,vstr = read_2DMHD(fmhd,pn)
  mpbs=pd.read_csv(fMPBS)



  val1=[ [vv[3],vv[16],vv[19],vv[7]]]

  vstr1=[ [vstr[3],vstr[16],vstr[19],vstr[7]]]

  fname=[ 'btrtvt'   ]

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
  for i in range(len(val1)) :

    Dps1=Dps+'/'+fname[i]
    if not os.path.exists(Dps1): os.system('mkdir '+Dps1)

    fps = Dps1+'/'+info.run+'.'+fname[i]+'.'+info.mhdt+'.'+pn+'_'+str(lp)+'.png'
    print ("SAVE ",fps)

    buf=mhd_2Dplot(nrow,ncol,fps,pn,lp,xran,yran,xx,yy,val1[i],vstr1[i],title,mpbs)

  return buf

def mhd_plot_main(argv):

  fname = argv[0].split(':')          # list of filenames
  fgrd  = fname[0]
  f3df  = fname[1]
  Dmhd  = fname[2]      # directory of openggcm ascii file
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


  pran  = argv[2].split(':')          # plot range: x1:x2:dx1:dx2:y1:y2:dy1:dy2:re
  x1    = locale.atof(pran[0])    # xrange x1-x2
  x2    = locale.atof(pran[1])
  dx1   = locale.atof(pran[2])    # major x-tick interval
  dx2   = locale.atof(pran[3])    # minor x-tick interval
  y1    = locale.atof(pran[4])    # yrange y1-y2
  y2    = locale.atof(pran[5])
  dy1   = locale.atof(pran[6])    # major y-tick interval
  dy2   = locale.atof(pran[7])    # minor y-tick interval
  xran  = [x1,x2,dx1,dx2]
  yran  = [y1,y2,dy1,dy2]

  tash  = locale.atoi(argv[3])

  info  = runinfo(f3df)
  fmhd  = Dmhd+'/'+info.run+'.'+pn+'_'+vran[1]+'.'+info.mhdt
  fMPBS = Dmhd+'/modeling/'+info.run+'.MPBS'+pn+'_car.'+info.mhdt
  #print('fmhd',fmhd)
  Dps1  = Dps+'/'+pn+'_'+vran[1]
  if not os.path.exists(Dps1): os.system('mkdir '+Dps1)

  buf=mhd_info(Dps1,info,fmhd,pn,lp,xran,yran,tash,fMPBS)

  return buf

x=np.linspace(0,20)

for i in range(1,7):
    a=pd.read_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/modeling/Msh_data_0.1.'+str(1200+1200*i).zfill(6),header=None,sep='\s+',names=['the','phi','m','rad','x','y','z','bx1','by1','bz1','vx1','vy1','vz1','rr1','pp1','ex1','ey1','ez1','xjx1','xjy1','xjz1','resis1']).drop_duplicates()
    a2=a[a.the==0]
    b=pd.read_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/sheath_data_ascii/cn%d.txt' % i,sep='\s+',header=None,names=['theta_1','theta_2','f_1','f_2','B','ni','Ti','V'],skiprows=1)
    b['phi1']=np.where(b.theta_1<=180,b.theta_1,b.theta_1-360)
    b['phi2']=np.where(b.theta_2<=180,b.theta_2,b.theta_2-360)
    b['phi']=(b.phi1+b.phi2)/2
    b['f']=(b.f_1+b.f_2)/2
#    b2=b[(-90<=b.phi) & (b.phi<=90)]
    b2=b

    buf=mhd_plot_main([':/Msh_Nstep.3df.'+str(1200+1200*i).zfill(6)+':/Volumes/easystore/openggcm_run/Msh_Nstep:.',
        'xy:0:-40:20:-30:30:.2','-40:20:10:1:-30:30:10:1','0'])

    for phi in np.arange(-90+7.5,90,7.5):
        y=x*np.tan(phi*np.pi/180)

        b3=b2[(b2.phi<phi+.01) & (b2.phi>phi-.01)]
        b4=b3[['f','B','ni','Ti','V']].set_index('f')
        b4.columns=['B_T','ni_T','Ti_T','V_T']

        df_list=[]
        for j in range(1,10):
            a_t=a2[(a2.phi<phi+7.5) & (a2.phi>phi-7.5)]
            a_t2=a_t[(a_t.m>j-.1) & (a_t.m<j+.1)]
            a_t3=a_t2.mean().to_frame().T
            a_t3.phi=phi
            a_t3['f']=j/10
            df_list.append(a_t3)
        a3=pd.concat(df_list,axis=0).set_index('f')

        a4=a3.reindex(a3.index.union(b3.f))
        a5=a4.interpolate('index').reindex(index=b3.f)
        a5['B']=np.sqrt(a5.bx1**2+a5.by1**2+a5.bz1**2)
        a5['Ti']=72429.0*a5.pp1/a5.rr1/11600.
        a5['V']=np.sqrt(a5.vx1**2+a5.vy1**2+a5.vz1**2)
        a5['ni']=a5.rr1
        a6=a5[['B','ni','Ti','V']]

        comp=pd.concat([a6,b4],axis=1)
        comp2=comp[['B_T','B','ni_T','ni','Ti_T','Ti','V_T','V']]
        comp2.to_csv('/Volumes/easystore/openggcm_run/Msh_Nstep/modeling/comp_phi_0.1_%.1f_' % phi+str(1200+1200*i).zfill(6),float_format='%.3f')

        buf.seek(0)
        fig=pl.load(buf)
        fig.axes[0].plot(x,y,color='green')
        fig.axes[2].plot(x,y,color='green')
        fig.axes[4].plot(x,y,color='green')
        fig.axes[6].plot(x,y,color='green')

        ax1=fig.add_subplot(4,2,2)
        ax2=fig.add_subplot(4,2,4)
        ax3=fig.add_subplot(4,2,6)
        ax4=fig.add_subplot(4,2,8)

        ax1.plot(comp2.index,comp2.B_T,'o-',label='THEMIS')
        ax1.plot(comp2.index,comp2.B,'o-',label='OpenGGCM')
        ax2.plot(comp2.index,comp2.ni_T,'o-',label='THEMIS')
        ax2.plot(comp2.index,comp2.ni,'o-',label='OpenGGCM')
        ax3.plot(comp2.index,comp2.Ti_T,'o-',label='THEMIS')
        ax3.plot(comp2.index,comp2.Ti,'o-',label='OpenGGCM')
        ax4.plot(comp2.index,comp2.V_T,'o-',label='THEMIS')
        ax4.plot(comp2.index,comp2.V,'o-',label='OpenGGCM')
        ax4.set_xlabel('f')
        ax1.set_ylabel('B (nT)')
        ax2.set_ylabel('n (cm$^{-3}$)')
        ax3.set_ylabel('T (eV)')
        ax4.set_ylabel('V (km/s)')
        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        fig.suptitle('$\phi$=%.1f' % phi)
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper right',bbox_to_anchor=(0.9,0.05))
        fig.savefig('/Volumes/easystore/openggcm_run/Msh_Nstep/modeling/plots/comp/comp_%d_phi_0.1_%.1f.png' % (20*i+20,phi))
        plt.close()
