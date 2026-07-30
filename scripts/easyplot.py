#/opt/local/bin/python
# make plot easily

import os
import sys
HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/lib/")

import locale
import numpy             	as np
import matplotlib.pyplot 	as plt
from   numpy             	import arange
from   read_mhd                	import maxmin_ran
from   run_info          	import tick_info,mrplt_info
from   matplotlib        	import rc
from   pkg_mhdplot             	import mhd_vpkg
from   openggcm_info     	import mhdtime,read_swdata,mhdt2hrmi,runinfo
from   matplotlib.colors       	import LogNorm
from   matplotlib.ticker       	import MultipleLocator, FuncFormatter
#from   mpl_toolkits.axes_grid1 	import make_axes_locatable


def colorful_text(vstr,col):
  rc('text',usetex=True)
  rc('text.latex', preamble='\\usepackage{color}')
  cstr=' '
  for i in range(len(vstr)) :
    cstr=cstr+r'\textcolor{'+col[i]+'}{'+vstr[i]+'} '
# print cstr
  return cstr



def easyplot(FPS,tt,val,vran,vstr,title,tevent='none'):
  "plot values easily                                                    \n \
   FPS : example) $DIR/$RUN.**.**   					\
         $RUN (the OpenGGCM runname) should be located after $DIR/.	\
   tstr	\
   tstr = val=[ pcpot,parea,marea,drate,nrate,mrdif,dmfds,dm1,dm2                ]        "


#### set tick information depending on the events

  info=runinfo(FPS)
  tstr=mhdtime(info.ti)
  dtmaj,dtmin,dtlab,xran= tick_info(info.run)

  if xran[0]==-9999 and xran[-1]==9999 :
    xran    =  [ tt[-1][0], tt[-1][-1] ]


  i       =  0
  xtick1  =  arange(xran[0],xran[1]+dtmaj,dtmaj)   # major tick location
  xtick2  =  arange(xran[0],xran[1]+dtmin,dtmin)   # minor tick location
  xlabel  =  mhdt2hrmi(xtick1,tstr,dtlab)         # create tick label
  ytick1  =  arange(0,30,6)
  ytick2  =  arange(0,25,1)



#### mr_rate graph

  fig=plt.figure(figsize=(8,11))


  for i in range(len(val)):

    ax1 = plt.subplot(len(val),1,i+1)
    plt.subplots_adjust(hspace = .001)


    print(len(val[i]),type(val[i][-1]))
    if type(val[i][-1]) is list  :      # draw several values in the same plot

      if val[i][0]==0 :                 # share the plot
        for jj in val[i][1:] : pl1 = ax1.plot(tt[i],jj)
        ax1.set_ylim (vran[i])

      if val[i][0]==1 :                 # share only xaxis
                                        # ONLY TWO VALUES should be used!!
        pl1 = ax1.plot(tt[i],val[i][1])
        for tl in ax1.get_yticklabels(): tl.set_color('b')
        ax1.set_ylim (vran[i][0])

        ax2 = ax1.twinx()
        pl2 = ax2.plot(tt[i],val[i][2],'g')
        for tl in ax2.get_yticklabels(): tl.set_color('g')
        ax2.set_ylim (vran[i][1])

#       for j in range(len(tt[i])):
#          if tt[i][j]>=12000 and tt[i][j]<=13500:
#              print tt[i][j],val[i][1][j],val[i][2][j]

    else :                              # draw one value plot

      print(vran[i])
      pl1=ax1.plot(tt[i],val[i])
      ax1.set_ylim (vran[i])

    plt.setp(ax1.get_yticklabels()[-1],visible=False)
    ax1.text(0.01,0.9,vstr[i],ha='left',va='top', \
             fontsize=10,transform=ax1.transAxes)


    ax1.set_xlim   (xran)
    ax1.set_xticks (xtick1)
    ax1.set_xticks (xtick2,minor=True)


    if i==len(tt)-1:
      ax1.set_xticklabels (xlabel)
    else :
      ax1.set_xticklabels ([ '' for j in xlabel])

    ax1.grid(axis='x')
    ax1.axhline(y=0,ls=':',c='k')

    if tevent!='none':
      ax1.axvline(x=tevent,ls='-',lw=2,c='k')

    if i==0 :
      ax1.set_title(title,fontsize=12)

# plt.tight_layout(h_pad=0.2)
# plt.show()
  plt.savefig(FPS)
  plt.close()


  return



def easy1Dplot(fps,tt,vv,ty,vline,ylab,vran,vstr,title,tevent='none',tkinfo=[],figsize=(8,11)):
  " time  info  : tt   = [ [t1,t2], [t2], [t3,t1,t4]                            \
    value info  : vv   = [ [v1,v2], [v2], [v3,v1,v4]                            \
    line style  : ty   = [ ['ro','b-'], ['r-'], ['r-','b-','g-]                 \
    string of vv: vstr = [ 'IMF By & Bz [nT]', 'Vsw [km/s]','CPCP [kV]' ]       \
    yrange of vv: vran = [ [-10,10], [300,500],[0,300] ]                        \
    title of fps: title= 'Jan 10 1997 summary plot'                             \
    eventtime for vertical bar :     tevent = 20000                             \
    tevent[0]   : must be the event time, makes thick black vertical lines      \
    tevent[1:]  : other timelines, makes thin red vertical lines                "

  print('easy1Dplot starts!')

  if len(tkinfo)!=0 :
    tstr = mhdtime(tkinfo[0])
    dtmaj,dtmin,dtlab,xran = tkinfo[1:]
  else :
    info = runinfo(fps)
    tstr = mhdtime(info.ti)
    dtmaj,dtmin,dtlab,xran = tick_info(info.run)

  if xran[0]==-9999 and xran[-1]==9999 :
    xran = [ tt[-1][0][0], tt[-1][0][-1] ]

  print(dtmaj,dtmin,dtlab,xran)

  i       =  0
  xtick1  =  arange(xran[0],xran[1]+dtmaj,dtmaj)   # major tick location
  xtick2  =  arange(xran[0],xran[1]+dtmin,dtmin)   # minor tick location
  xlabel  =  mhdt2hrmi(xtick1,tstr,dtlab)          # create tick label

# fig=plt.figure(figsize=(8,11))
  if figsize==() :fig=plt.figure()
  else           :fig=plt.figure(figsize=figsize)

  for i in range(len(tt)):

    ax1=plt.subplot(len(tt),1,i+1)
    plt.subplots_adjust(hspace = .001)

    for j in range(len(tt[i])):
#      print(i,j)

      lst = ty[i][j].split(':')
#      breakpoint()
      if len(lst)==1: ax1.plot(tt[i][j],vv[i][j],ty[i][j])
      else:
#         print(lst[1],tt[i][j],vv[i][j])
         if lst[1]=='plot': ax1.plot(tt[i][j],vv[i][j],lst[0])
         if lst[1]=='step': ax1.step(tt[i][j],vv[i][j],lst[0],where='mid')
         if lst[1]=='yerr': ax1.errorbar(tt[i][j],vv[i][j][0],yerr=vv[i][j][1],fmt=lst[0])


#   ax1.text(0.01,0.9,vstr[i],ha='left',va='top', \
#            fontsize=10,transform=ax1.transAxes)

    if isinstance(vstr[i],list):
      vstr1,colr1,x1,y1 = vstr[i]
      for j in range(len(vstr1)):
         ax1.text(x1[j],y1[j],vstr1[j],ha='left',va='top',color=colr1[j],	\
             fontsize=10,transform=ax1.transAxes)
    else :
      ax1.text(0.99,0.9,vstr[i],ha='right',va='top', \
               fontsize=10,transform=ax1.transAxes)

#...xticks
    ax1.set_xticks (xtick1)
    ax1.set_xticks (xtick2,minor=True)
    if i==len(tt)-1: ax1.set_xticklabels (xlabel,fontsize=10);ax1.set_xlabel('TIME [UT]')
    else           : ax1.set_xticklabels ([ '' for j in xlabel])
    ax1.set_xlim   (xran)
    ax1.tick_params(axis='x',which='major',direction='inout',length=6) #,width=2)
    ax1.tick_params(axis='x',which='minor',direction='inout',length=6)


#...yticks
    ax1.set_ylabel(ylab[i],fontsize=10)
    if isinstance(vran[i],list):
        ax1.set_ylim(vran[i][0],vran[i][1])
        if len(vran[i])>=3:
          ytick1 = arange(vran[i][0],vran[i][1]+vran[i][2],vran[i][2])
          ax1.set_yticks (ytick1)
          if len(vran[i])==4:
            ytick2 = arange(vran[i][0],vran[i][1],vran[i][3])
            ax1.set_yticks (ytick2,minor=True)
    plt.setp(ax1.get_yticklabels(),fontsize=10)
    plt.setp(ax1.get_yticklabels()[-1],visible=False)
    plt.setp(ax1.get_yticklabels()[0],visible=False)

    ax1.grid(axis='both')
    if isinstance(vran[i],list):
        if vran[i][0]==0: pass
        else: ax1.axhline(y=0,ls=':',c='k')
    else:   ax1.axhline(y=0,ls=':',c='k')

    if tevent!='none'     : ax1.axvline(x=tevent,ls='--',lw=2,c='k')
    if len(vline[i])!=0   :
       if   vline[i][-1] == 'v' :
         for j in vline[i][:-1]  : ax1.axvline(x=j[0],ls=j[1],lw=j[2],c=j[3])
       elif vline[i][-1] == 'h' :
         for j in vline[i][:-1]  : ax1.axhline(y=j[0],ls=j[1],lw=j[2],c=j[3]);print(j)
       elif vline[i][-1] == 'vp':
         for j in vline[i][:-1]  : ax1.axvspan(j[0],j[1],facecolor=j[2],alpha=0.4,linewidth=2.,linestyle='--')
         for j in vline[i][:-1]  : ax1.axvline(x=j[0],lw=2.,ls='--',c=j[2]);ax1.axvline(x=j[1],lw=2.,ls='--',c=j[2])
       elif vline[i][-1] == 'hp':
         for j in vline[i][:-1]  : ax1.axhspan(j[0],j[1],facecolor=j[2],alpha=0.4)
         for j in vline[i][:-1]  : ax1.axhline(y=j[0],lw=2.,ls='--',c=j[2]);ax1.axhline(y=j[1],lw=2.,ls='--',c=j[2])
       elif vline[i][-1] == 'vph':
         for j in vline[i][:-1]  :
            ax1.axvspan(j[0],j[1],facecolor=j[2],alpha=0.4)
            ax1.axhline(y=j[3],ls=j[4],lw=j[5],c=j[6])
            ax1.axvline(x=j[0],lw=2.,ls='--',c=j[2])
            ax1.axvline(x=j[1],lw=2.,ls='--',c=j[2])



    if i==0 :
      ax1.set_title(title,fontsize=12)

# plt.show()
# plt.tight_layout(h_pad=0.2)
  print("Save ",fps)
  plt.savefig(fps)
  plt.savefig(fps[:-4]+'.png')
  plt.close()

  return

def easy1Dplot_dot(fps,tt,vv,ty,vline,ylab,vran,vstr,title,tevent='none',tkinfo=[],figsize=(8,11)):
  " time  info  : tt   = [ [t1,t2], [t2], [t3,t1,t4]                            \
    value info  : vv   = [ [v1,v2], [v2], [v3,v1,v4]                            \
    line style  : ty   = [ ['ro','b-'], ['r-'], ['r-','b-','g-]                 \
    string of vv: vstr = [ 'IMF By & Bz [nT]', 'Vsw [km/s]','CPCP [kV]' ]       \
    yrange of vv: vran = [ [-10,10], [300,500],[0,300] ]                        \
    title of fps: title= 'Jan 10 1997 summary plot'                             \
    eventtime for vertical bar :     tevent = 20000                             \
    tevent[0]   : must be the event time, makes thick black vertical lines      \
    tevent[1:]  : other timelines, makes thin red vertical lines                "

  print('easy1Dplot_dot starts!')

  if len(tkinfo)!=0 :
    tstr = mhdtime(tkinfo[0])
    dtmaj,dtmin,dtlab,xran = tkinfo[1:]
  else :
    info = runinfo(fps)
    tstr = mhdtime(info.ti)
    dtmaj,dtmin,dtlab,xran = tick_info(info.run)

  if xran[0]==-9999 and xran[-1]==9999 :
    xran = [ tt[-1][0][0], tt[-1][0][-1] ]

  print(dtmaj,dtmin,dtlab,xran)

  i       =  0
  xtick1  =  arange(xran[0],xran[1]+dtmaj,dtmaj)   # major tick location
  xtick2  =  arange(xran[0],xran[1]+dtmin,dtmin)   # minor tick location
  xlabel  =  mhdt2hrmi(xtick1,tstr,dtlab)          # create tick label

# fig=plt.figure(figsize=(8,11))
  if figsize==() :fig=plt.figure()
  else           :fig=plt.figure(figsize=figsize)

  for i in range(len(tt)):

    ax1=plt.subplot(len(tt),1,i+1)
    plt.subplots_adjust(hspace = .001)

    for j in range(len(tt[i])):
#      print(i,j)

      lst = ty[i][j].split(':')
#      breakpoint()
      if len(lst)==1: ax1.plot(tt[i][j],vv[i][j],ty[i][j],ls='',marker='.',ms=4)
      else:
#         print(lst[1],tt[i][j],vv[i][j])
         if lst[1]=='plot': ax1.plot(tt[i][j],vv[i][j],lst[0])
         if lst[1]=='step': ax1.step(tt[i][j],vv[i][j],lst[0],where='mid')
         if lst[1]=='yerr': ax1.errorbar(tt[i][j],vv[i][j][0],yerr=vv[i][j][1],fmt=lst[0])


#   ax1.text(0.01,0.9,vstr[i],ha='left',va='top', \
#            fontsize=10,transform=ax1.transAxes)

    if isinstance(vstr[i],list):
      vstr1,colr1,x1,y1 = vstr[i]
      for j in range(len(vstr1)):
         ax1.text(x1[j],y1[j],vstr1[j],ha='left',va='top',color=colr1[j],	\
             fontsize=10,transform=ax1.transAxes)
    else :
      ax1.text(0.99,0.9,vstr[i],ha='right',va='top', \
               fontsize=10,transform=ax1.transAxes)

#...xticks
    ax1.set_xticks (xtick1)
    ax1.set_xticks (xtick2,minor=True)
    if i==len(tt)-1: ax1.set_xticklabels (xlabel,fontsize=10);ax1.set_xlabel('TIME [UT]')
    else           : ax1.set_xticklabels ([ '' for j in xlabel])
    ax1.set_xlim   (xran)
    ax1.tick_params(axis='x',which='major',direction='inout',length=6) #,width=2)
    ax1.tick_params(axis='x',which='minor',direction='inout',length=6)


#...yticks
    ax1.set_ylabel(ylab[i],fontsize=10)
    if isinstance(vran[i],list):
        ax1.set_ylim(vran[i][0],vran[i][1])
        if len(vran[i])>=3:
          ytick1 = arange(vran[i][0],vran[i][1]+vran[i][2],vran[i][2])
          ax1.set_yticks (ytick1)
          if len(vran[i])==4:
            ytick2 = arange(vran[i][0],vran[i][1],vran[i][3])
            ax1.set_yticks (ytick2,minor=True)
    plt.setp(ax1.get_yticklabels(),fontsize=10)
    plt.setp(ax1.get_yticklabels()[-1],visible=False)
    plt.setp(ax1.get_yticklabels()[0],visible=False)

    ax1.grid(axis='both')
    if isinstance(vran[i],list):
        if vran[i][0]==0: pass
        else: ax1.axhline(y=0,ls=':',c='k')
    else:   ax1.axhline(y=0,ls=':',c='k')

    if tevent!='none'     : ax1.axvline(x=tevent,ls='--',lw=2,c='k')
    if len(vline[i])!=0   :
       if   vline[i][-1] == 'v' :
         for j in vline[i][:-1]  : ax1.axvline(x=j[0],ls=j[1],lw=j[2],c=j[3])
       elif vline[i][-1] == 'h' :
         for j in vline[i][:-1]  : ax1.axhline(y=j[0],ls=j[1],lw=j[2],c=j[3]);print(j)
       elif vline[i][-1] == 'vp':
         for j in vline[i][:-1]  : ax1.axvspan(j[0],j[1],facecolor=j[2],alpha=0.4,linewidth=2.,linestyle='--')
         for j in vline[i][:-1]  : ax1.axvline(x=j[0],lw=2.,ls='--',c=j[2]);ax1.axvline(x=j[1],lw=2.,ls='--',c=j[2])
       elif vline[i][-1] == 'hp':
         for j in vline[i][:-1]  : ax1.axhspan(j[0],j[1],facecolor=j[2],alpha=0.4)
         for j in vline[i][:-1]  : ax1.axhline(y=j[0],lw=2.,ls='--',c=j[2]);ax1.axhline(y=j[1],lw=2.,ls='--',c=j[2])
       elif vline[i][-1] == 'vph':
         for j in vline[i][:-1]  :
            ax1.axvspan(j[0],j[1],facecolor=j[2],alpha=0.4)
            ax1.axhline(y=j[3],ls=j[4],lw=j[5],c=j[6])
            ax1.axvline(x=j[0],lw=2.,ls='--',c=j[2])
            ax1.axvline(x=j[1],lw=2.,ls='--',c=j[2])



    if i==0 :
      ax1.set_title(title,fontsize=12)

# plt.show()
# plt.tight_layout(h_pad=0.2)
  print("Save ",fps)
  plt.savefig(fps)
  plt.savefig(fps[:-4]+'.png')
  plt.close()

  return


def easy1Dplot_l(fps,tt,vv,ty,vline,ylab,vran,vstr,title,label,annotate,tevent='none',tkinfo=[],figsize=(8,11),anloc=(.1,.005),bottom=0.25,legloc=(0.9,0.2)):
  " time  info  : tt   = [ [t1,t2], [t2], [t3,t1,t4]                            \
    value info  : vv   = [ [v1,v2], [v2], [v3,v1,v4]                            \
    line style  : ty   = [ ['ro','b-'], ['r-'], ['r-','b-','g-]                 \
    string of vv: vstr = [ 'IMF By & Bz [nT]', 'Vsw [km/s]','CPCP [kV]' ]       \
    yrange of vv: vran = [ [-10,10], [300,500],[0,300] ]                        \
    title of fps: title= 'Jan 10 1997 summary plot'                             \
    eventtime for vertical bar :     tevent = 20000                             \
    tevent[0]   : must be the event time, makes thick black vertical lines      \
    tevent[1:]  : other timelines, makes thin red vertical lines                "

  print('easy1Dplot_l starts!')
  #print(annotate)

  if len(tkinfo)!=0 :
    tstr = mhdtime(tkinfo[0])
    dtmaj,dtmin,dtlab,xran = tkinfo[1:]
  else :
    info = runinfo(fps)
    tstr = mhdtime(info.ti)
    dtmaj,dtmin,dtlab,xran = tick_info(info.run)

  if xran[0]==-9999 and xran[-1]==9999 :
    xran = [ tt[-1][0][0], tt[-1][0][-1] ]

  print(dtmaj,dtmin,dtlab,xran)

  i       =  0
  xtick1  =  arange(xran[0],xran[1]+dtmaj,dtmaj)   # major tick location
  xtick2  =  arange(xran[0],xran[1]+dtmin,dtmin)   # minor tick location
  xlabel  =  mhdt2hrmi(xtick1,tstr,dtlab)          # create tick label

# fig=plt.figure(figsize=(8,11))
  if figsize==() :fig=plt.figure()
  else           :fig=plt.figure(figsize=figsize)

  for i in range(len(tt)):

    ax1=plt.subplot(len(tt),1,i+1)
    plt.subplots_adjust(hspace = .001)

    for j in range(len(tt[i])):
#      print(i,j)

      lst = ty[i][j].split(':')
#      breakpoint()
      if len(lst)==1: ax1.plot(tt[i][j],vv[i][j],ty[i][j])
      else:
#         print(lst[1],tt[i][j],vv[i][j])
         if lst[1]=='plot': ax1.plot(tt[i][j],vv[i][j],lst[0],label=label[j])
         if lst[1]=='step': ax1.step(tt[i][j],vv[i][j],lst[0],where='mid')
         if lst[1]=='yerr':
             ax1.errorbar(tt[i][j],vv[i][j][0],yerr=vv[i][j][1],fmt=lst[0],label=label[j])


#   ax1.text(0.01,0.9,vstr[i],ha='left',va='top', \
#            fontsize=10,transform=ax1.transAxes)

    if isinstance(vstr[i],list):
      vstr1,colr1,x1,y1 = vstr[i]
      for j in range(len(vstr1)):
         ax1.text(x1[j],y1[j],vstr1[j],ha='left',va='top',color=colr1[j],	\
             fontsize=10,transform=ax1.transAxes)
    else :
      ax1.text(0.99,0.9,vstr[i],ha='right',va='top', \
               fontsize=10,transform=ax1.transAxes)

#...xticks
    ax1.set_xticks (xtick1)
    ax1.set_xticks (xtick2,minor=True)
    if i==len(tt)-1: ax1.set_xticklabels (xlabel,fontsize=10);ax1.set_xlabel('TIME [UT]')
    else           : ax1.set_xticklabels ([ '' for j in xlabel])
    ax1.set_xlim   (xran)
    ax1.tick_params(axis='x',which='major',direction='inout',length=6) #,width=2)
    ax1.tick_params(axis='x',which='minor',direction='inout',length=6)


#...yticks
    ax1.set_ylabel(ylab[i],fontsize=10)
    if isinstance(vran[i],list):
        ax1.set_ylim(vran[i][0],vran[i][1])
        if len(vran[i])>=3:
          ytick1 = arange(vran[i][0],vran[i][1]+vran[i][2],vran[i][2])
          ax1.set_yticks (ytick1)
          if len(vran[i])==4:
            ytick2 = arange(vran[i][0],vran[i][1],vran[i][3])
            ax1.set_yticks (ytick2,minor=True)
    plt.setp(ax1.get_yticklabels(),fontsize=10)
    plt.setp(ax1.get_yticklabels()[-1],visible=False)
    plt.setp(ax1.get_yticklabels()[0],visible=False)

    ax1.grid(axis='both')
    if isinstance(vran[i],list):
        if vran[i][0]==0: pass
        else: ax1.axhline(y=0,ls=':',c='k')
#    else:   ax1.axhline(y=0,ls=':',c='k')

    if tevent!='none'     : ax1.axvline(x=tevent,ls='--',lw=2,c='k')
    if len(vline[i])!=0   :
       if   vline[i][-1] == 'v' :
         for j in vline[i][:-1]  : ax1.axvline(x=j[0],ls=j[1],lw=j[2],c=j[3])
       elif vline[i][-1] == 'h' :
         for j in vline[i][:-1]  : ax1.axhline(y=j[0],ls=j[1],lw=j[2],c=j[3]);print(j)
       elif vline[i][-1] == 'vp':
         for j in vline[i][:-1]  : ax1.axvspan(j[0],j[1],facecolor=j[2],alpha=0.4,linewidth=2.,linestyle='--')
         for j in vline[i][:-1]  : ax1.axvline(x=j[0],lw=2.,ls='--',c=j[2]);ax1.axvline(x=j[1],lw=2.,ls='--',c=j[2])
       elif vline[i][-1] == 'hp':
         for j in vline[i][:-1]  : ax1.axhspan(j[0],j[1],facecolor=j[2],alpha=0.4)
         for j in vline[i][:-1]  : ax1.axhline(y=j[0],lw=2.,ls='--',c=j[2]);ax1.axhline(y=j[1],lw=2.,ls='--',c=j[2])
       elif vline[i][-1] == 'vph':
         for j in vline[i][:-1]  :
            ax1.axvspan(j[0],j[1],facecolor=j[2],alpha=0.4)
            ax1.axhline(y=j[3],ls=j[4],lw=j[5],c=j[6])
            ax1.axvline(x=j[0],lw=2.,ls='--',c=j[2])
            ax1.axvline(x=j[1],lw=2.,ls='--',c=j[2])


#    if len(tt[i])>=3: ax1.legend()

    if i==0 :
      ax1.set_title(title,fontsize=12)
    ax1.minorticks_on()
#    ax1.tick_params(axis='x', which='minor', bottom=False)
    #ax1.grid(axis='both')
  #plt.grid()
  handles, labels = ax1.get_legend_handles_labels()
  fig.legend(handles, labels, loc='upper right',bbox_to_anchor=legloc)

  plt.annotate(annotate,xy=anloc, xycoords='figure fraction')
  plt.subplots_adjust(bottom=bottom)
# plt.show()
# plt.tight_layout(h_pad=0.2)
  print("Save ",fps)
  plt.savefig(fps)
  plt.savefig(fps[:-4]+'.png')
  plt.close()

  return

def easylineplot(fps,xx,yy,lst,pst,xran,yran,xlab,ylab,tlab,vstr,twin=[],vline=[],hline=[],figsize=(8,11)):
  " draw line plots that shares the same x axis 				\
    xaxis info  : tt   = [ [t1,t2], [t2], [t3,t1,t4]                            \
    yaxis info  : vv   = [ [v1,v2], [v2], [v3,v1,v4]                            \
    line style  : lst  = [ ['ro','b-'], ['r-'], ['r-','b-','g-]                 \
    xrange      : xran = [ [minx,maxx,major tick space ,minor tick space], ..] 	\
    yrange      : yran = [ [minx,maxx,major tick space ,minor tick space], ..] 	\
    xy labels   : xlab,ylab = ['xgse','xgse',...]				\
    plot text   : vstr = [ 'IMF By & Bz [nT]', 'Vsw [km/s]','CPCP [kV]' ]       \
    plot title  : tlab - [ 'velocity','temerature',...]				\
    ===================								\
    twin        : set values to share x axis and plot yvalues 			\
                  twin = [yy,lst,pst,yran,ylab]					\
    vline/hline : set vertical/horizontal lines					\
                  vline =[ [loc,col],[loc,col], ]				"

  print('easylineplot starts!')

  if len(twin)!=0  : xtw,ytw,lstw,pstw,yrtw,yltw = twin

  fig=plt.figure(figsize=figsize)

  for i in range(len(xx)):
    ax1=plt.subplot(len(xx),1,i+1)
    plt.subplots_adjust(hspace = .003)

    for j in range(len(xx[i])):
      if   pst[i][j]=='step'    : ax1.step(xx[i][j],yy[i][j],lst[i][j])
      elif pst[i][j]=='semilogy': ax1.semilogy(xx[i][j],yy[i][j],lst[i][j])
      else                      : ax1.plot(xx[i][j],yy[i][j],lst[i][j])

    ax1.set_title(tlab[i])
#   ax1.text(0.01,0.9,vstr[i],ha='left',va='top',transform=ax1.transAxes)
    ax1.text(0.99,0.9,vstr[i],ha='right',va='top',transform=ax1.transAxes)
#...xticks
    xtick1  =  arange(xran[i][0],xran[i][1]+xran[i][2],xran[i][2])   # major tick location
    ax1.set_xticks (xtick1)
    if len(xran)==4:
      xtick2  =  arange(xran[i][0],xran[i][1]+xran[i][3],xran[i][3]) # minor tick location
      ax1.set_xticks (xtick2,minor=True)
    ax1.set_xlabel (xlab[i])
    if i!=len(xx)-1: ax1.set_xticklabels ([ '' for j in xtick1])
    ax1.set_xlim   (xran[i][0],xran[i][1])
    plt.setp(ax1.get_xticklabels(),fontsize=8)
    ax1.tick_params(axis='x',which='major',direction='inout',length=6) #,width=2)
    ax1.tick_params(axis='x',which='minor',direction='inout',length=6)

#...yticks
    ytick1  =  arange(yran[i][0],yran[i][1]+yran[i][2],yran[i][2])   # major tick location
    ax1.set_yticks (ytick1)
    if len(yran)==4:
      ytick2  =  arange(yran[i][0],yran[i][1]+yran[i][3],yran[i][3]) # minor tick location
      ax1.set_yticks (ytick2,minor=True)
    if len(twin)!=0 : ax1.set_ylabel (ylab[i],color=lst[i][0][0])
    else            : ax1.set_ylabel (ylab[i])
    ax1.set_ylim   (yran[i][0],yran[i][1])
    plt.setp(ax1.get_yticklabels(),fontsize=8)
    plt.setp(ax1.get_yticklabels()[-1],visible=False)
    plt.setp(ax1.get_yticklabels()[0],visible=False)
#   ax1.grid(True)
    ax1.grid(axis='x')

#...vlines
    if len(vline)!=0:
      if len(vline[i])!=0:
        loc,col=vline[i]
        for k in range(len(loc)): ax1.axvline(x=loc[k],ls='-',lw=2,c=col[k])

#...hlines
    if len(hline)!=0:
      if len(hline[i])!=0:
        loc,col=hline[i]
        for k in range(len(loc)): ax1.axhline(y=loc[k],ls='-',lw=2,c=col[k])
    if yran[i][0] <0 and yran[i][1] >0: ax1.axhline(y=0,ls=':',c='k')
#   ax1.axhline(y=0.,ls=':',lw=2,c=k)

#### share x-axis and plot yvalues
    if len(twin)!=0 :
      ax2 = ax1.twinx()
      for j in range(len(xtw[i])):
        if pstw[i][j]=='step': ax2.step(xtw[i][j],ytw[i][j],lstw[i][j])
        else                 : ax2.plot(xtw[i][j],ytw[i][j],lstw[i][j])

#... twin yticks
      ytk1  =  arange(yrtw[i][0],yrtw[i][1]+yrtw[i][2],yrtw[i][2])   # major tick location
      ytk2  =  arange(yrtw[i][0],yrtw[i][1]+yrtw[i][3],yrtw[i][3])   # minor tick location
      ax2.set_ylabel (yltw[i],color=lstw[i][j][0])
      ax2.set_yticks (ytk1)
      ax2.set_yticks (ytk2,minor=True)
      ax2.set_ylim   (yrtw[i][0],yrtw[i][1])
      plt.setp(ax2.get_yticklabels(),fontsize=8)
      plt.setp(ax2.get_yticklabels()[-1],visible=False)
      plt.setp(ax2.get_yticklabels()[0],visible=False)
      ax2.set_xlim   (xran[i][0],xran[i][1])


# plt.show()
# plt.tight_layout(h_pad=0.2)
  print("Save ",fps)
  plt.savefig(fps)

  plt.close()

  return


def easy2Dplot(nrow,ncol,fps,xran,yran,xx,yy,val,vstr,title,ftitle):
  "plot 2D"

####### draw graphs

  fig = plt.figure(figsize=(11,8))

  for i in range(len(val)):

    ax1      = fig.add_subplot(nrow,ncol,i+1,aspect='equal')
    ax1.tick_params(axis='both',which='major',labelsize=7)

    x,y      = np.meshgrid(xx,yy)
    pkg_plot = mhd_vpkg(vstr[i])


    if pkg_plot[5]==1:
      cs    = ax1.contourf(x,y,val[i],levels=pkg_plot[3], \
              cmap=pkg_plot[1],norm=LogNorm())
    else :
      cs    = ax1.contourf(x,y,val[i],levels=pkg_plot[3], \
              cmap=pkg_plot[1],extend='both')

#   cax1  = make_axes_locatable(ax1)
#   cax2  = cax1.append_axes("right",size="3%",pad="5%")
#   cb    = fig.colorbar(cs,cax=cax2,ticks=pkg_plot[4])
#   cl    = plt.getp(cb.ax, 'ymajorticklabels')
#   plt.setp(cl, fontsize=7)

####### tick infomation

    ax1.yaxis.set_major_locator(MultipleLocator(yran[2]))
    ax1.yaxis.set_minor_locator(MultipleLocator(yran[3]))
    ax1.xaxis.set_major_locator(MultipleLocator(xran[2]))
    ax1.xaxis.set_minor_locator(MultipleLocator(xran[3]))
    ax1.set_xlim(xran[0],xran[1])
    ax1.set_ylim(yran[0],yran[1])
    ax1.grid(True)

##### titles for the figures
    vmax,vmin = maxmin_ran([xran[0],xran[1]],[yran[0],yran[1]],xx,yy,val[i])
    lmax = "Max: %.2f "%vmax
    lmin = "Min: %.2f "%vmin

    ax1.text(0.0,1.0,title[i]   ,fontsize=9,ha='left' ,va='bottom' ,transform=ax1.transAxes)
    ax1.text(1.0,1.0,pkg_plot[0],fontsize=9,ha='right',va='bottom' ,transform=ax1.transAxes)
    ax1.text(0.0,0.0,lmin       ,fontsize=8,ha='left' ,va='bottom',transform=ax1.transAxes)
    ax1.text(1.0,0.0,lmax       ,fontsize=8,ha='right',va='bottom',transform=ax1.transAxes)

  plt.figtext(0.5,0.95,ftitle,fontsize=10,ha='center')
  plt.savefig(fps,orientation='landscape')
  plt.close()

  return



def magic_summ(nrow,ncol,fname,fout):
  " make a sumary plot of ps files"

  k     = -1
  name3 =' '
  for i in range(nrow) :
    name1 = ' '
    name2 = 'test%02d.'%(i+1)+fout.split('.')[-1]
    for j in range(ncol):
       k    = k+1
       name1= name1+fname[k]+' '
    cmd1='convert -trim'+name1+' +append '+name2
    print(cmd1)
    os.system(cmd1)
    name3=name3+name2+' '

  cmd2='convert '+name3+' -append '+fout
  print(cmd2)
  os.system(cmd2)

  cmd3='rm '+name3
  print(cmd3)
  os.system(cmd3)

  return
