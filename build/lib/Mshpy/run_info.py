#!/usr/bin/python
#

import os
import sys

HOME=os.getenv("HOME")
sys.path.append(HOME+"/svn/hkc-project/trunk/src/event_summary")
sys.path.append(HOME+"/svn/hkc-project/trunk/src/mhd-openggcm")

from event_info 	import event_info,mrstory_1Dinfo,mrstory_info
from paper_info		import paper_info
from timehist_info      import timehist_info


def openggcm_run(runname):
  "provide information of OpenGGCM Run"

  if runname=='djl00703a':
    STARTTIME  = "1997:01:10:07:30:0.0"
    ENDTIME    = "1997:01:10:14:30:0.0"
    DIPTIME    = "1997:01:10:11:00:0.0"

  elif runname=='2008Jun28_002':
    STARTTIME  = "2008:06:28:11:00:0.000"    # UT when the run starts
    ENDTIME    = "2008:06:28:21:00:0.000"
    DIPTIME    = "2008:06:28:10:00:0.000"

  elif runname=='2008Jun28_003':
    STARTTIME  = "2008:06:28:09:00:0.000"    # UT when the run starts
    ENDTIME    = "2008:06:28:15:00:0.000"
    DIPTIME    = "2008:06:28:09:00:0.000"

  elif runname=='2008Jun28_004':
    STARTTIME  = "2008:06:28:09:00:0.000"    # UT when the run starts
    ENDTIME    = "2008:06:28:21:00:0.000"
    DIPTIME    = "2008:06:28:09:00:0.000"

  elif runname=='2010Aug20_002':
    STARTTIME  = "2010:08:20:20:00:0.000"
    ENDTIME    = "2010:08:21:12:00:0.000"
    DIPTIME    = "2010:08:20:20:00:0.000"

  elif runname=='2009Oct14_001':
    STARTTIME  = "2009:10:14:20:00:0.000"
    ENDTIME    = "2009:10:15:06:00:0.000"
    DIPTIME    = "2009:10:14:20:00:0.000"

  elif runname=='2006Jan10_001':
    STARTTIME  = "2006:01:10:01:00:0.000"
    ENDTIME    = "2006:01:10:07:00:0.000"
    DIPTIME    = "2006:01:10:01:00:0.000"

  elif runname=='2006Jan10_003':
    STARTTIME  = "2006:01:09:23:00:0.000"
    ENDTIME    = "2006:01:10:13:00:0.000"
    DIPTIME    = "2006:01:09:23:00:0.000"

  elif runname=='2006Jan13_002':
    STARTTIME  = "2006:01:13:12:00:0.000"
    ENDTIME    = "2006:01:15:09:00:0.000"
    DIPTIME    = "2006:01:13:12:00:0.000"

  elif runname=='2009Oct14_002':
    STARTTIME  = "2009:10:14:20:00:0.000"
    ENDTIME    = "2009:10:15:12:00:0.000"
    DIPTIME    = "2009:10:14:20:00:0.000"

  elif runname=='2000Sep29_002':
    STARTTIME  = "2000:09:29:17:00:0.000"
    ENDTIME    = "2000:09:30:09:00:0.000"
    DIPTIME    = "2000:09:29:17:00:0.000"

  elif runname=='2000Sep29_003':
    STARTTIME  = "2000:09:29:13:00:0.000"
    ENDTIME    = "2000:09:30:09:00:0.000"
    DIPTIME    = "2000:09:29:13:00:0.000"

  elif runname=='2001Mar22_002':
    STARTTIME  = "2001:03:22:00:00:0.000"
    ENDTIME    = "2001:03:22:09:00:0.000"
    DIPTIME    = "2001:03:22:00:00:0.000"

  elif runname=='2001Apr26_001':
    STARTTIME  = "2001:04:26:17:00:0.000"
    ENDTIME    = "2001:04:27:07:00:0.000"
    DIPTIME    = "2001:04:26:17:00:0.000"

  elif runname=='2003Jul10_001':
    STARTTIME  = "2003:07:10:22:00:0.000"
    ENDTIME    = "2003:07:12:00:00:0.000"
    DIPTIME    = "2003:07:10:22:00:0.000"

  elif runname=='2003Jul10_003':
    STARTTIME  = "2003:07:11:04:00:0.000"
    ENDTIME    = "2003:07:12:00:00:0.000"
    DIPTIME    = "2003:07:11:04:00:0.000"

  elif runname=='2008Oct09_001':
    STARTTIME  = "2008:10:09:08:00:0.000"
    ENDTIME    = "2008:10:09:20:00:0.000"
    DIPTIME    = "2008:10:09:08:00:0.000"

  elif runname=='2008Nov12_001':
    STARTTIME  = "2008:11:11:23:00:0.000"
    ENDTIME    = "2008:11:12:14:00:0.000"
    DIPTIME    = "2008:11:11:23:00:0.000"

  elif runname=='2003Feb12_002':
    STARTTIME  = "2003:02:12:12:00:0.000"
    ENDTIME    = "2003:02:13:00:00:0.000"
    DIPTIME    = "2003:02:12:12:00:0.000"

  elif runname=='2002Apr10_001':
    STARTTIME  = "2002:04:10:06:00:0.000"
    ENDTIME    = "2002:04:11:00:00:0.000"
    DIPTIME    = "2002:04:10:06:00:0.000"

  elif runname=='2004Jan24_002':
    STARTTIME  = "2004:01:23:10:00:0.000"
    ENDTIME    = "2004:01:24:13:00:0.000"
    DIPTIME    = "2004:01:23:10:00:0.000"

  elif runname=='2015Nov04_002':
    STARTTIME  = "2015:11:04:00:00:0.000"
    ENDTIME    = "2015:11:04:06:00:0.000"
    DIPTIME    = "2004:11:04:00:00:0.000"

  elif runname=='2009Mar11_001':
    STARTTIME  = "2009:03:11:22:00:0.000"
    ENDTIME    = "2009:03:12:12:00:0.000"
    DIPTIME    = "2009:03:11:22:00:0.000"

  elif runname=='2009Mar28_002':
    STARTTIME  = "2009:03:28:00:00:0.000"
    ENDTIME    = "2009:03:28:16:00:0.000"
    DIPTIME    = "2009:03:28:00:00:0.000"

  elif runname=='2009Apr05_001':
    STARTTIME  = "2009:04:05:00:00:0.000"
    ENDTIME    = "2009:04:06:00:00:0.000"
    DIPTIME    = "2009:04:05:00:00:0.000"

  elif runname=='2009Apr13_001':
    STARTTIME  = "2009:04:13:10:00:0.000"
    ENDTIME    = "2009:04:14:10:00:0.000"
    DIPTIME    = "2009:04:13:10:00:0.000"

  elif runname=='Msh_Nstep_002':
    STARTTIME  = "1967:01:01:00:00:0.000"
    ENDTIME    = "1967:01:01:04:00:0.000"
    DIPTIME    = "1967:01:01:00:00:0.000"

  elif runname=='Msh_Nstep_n':
    STARTTIME  = "1967:01:01:00:00:0.000"
    ENDTIME    = "1967:01:01:04:00:0.000"
    DIPTIME    = "1967:01:01:00:00:0.000"

  elif runname=='Msh_Nstep':
    STARTTIME  = "1967:01:01:00:00:0.000"
    ENDTIME    = "1967:01:01:04:00:0.000"
    DIPTIME    = "1967:01:01:00:00:0.000"

  elif runname=='Msh_Nstep_model':
    STARTTIME  = "1967:01:01:00:00:0.000"
    ENDTIME    = "1967:01:01:04:00:0.000"
    DIPTIME    = "1967:01:01:00:00:0.000"

  elif runname=='2008Jun28_005' or runname=="2008Jun28_005_Jel":
    STARTTIME  = "2008:06:28:09:00:0.000"
    ENDTIME    = "2008:06:28:21:00:0.000"
    DIPTIME    = "2008:06:28:09:00:0.000"

  elif runname=='Msh_Nstep_cs_002':
    STARTTIME  = "1967:01:01:00:00:0.000"
    ENDTIME    = "1967:01:01:04:00:0.000"
    DIPTIME    = "1967:01:01:00:00:0.000"

  elif runname=="2001Apr26_002":
    STARTTIME  = "2001:04:26:17:00:0.000"
    ENDTIME    = "2001:04:27:07:00:0.000"
    DIPTIME    = "2001:04:26:17:00:0.000"

  elif runname=="2003May04_001" or runname=="2003May04_001_Jel":
    STARTTIME  = "2003:05:04:05:00:0.000"
    ENDTIME    = "2003:05:04:20:00:0.000"
    DIPTIME    = "2003:05:04:00:00:0.000"

  elif runname=="2004Feb21_001":
    STARTTIME  = "2004:02:21:12:00:0.000"
    ENDTIME    = "2004:02:22:09:00:0.000"
    DIPTIME    = "2004:02:21:12:00:0.000"

  elif runname=="2006Sep17_001":
    STARTTIME  = "2006:09:17:06:00:0.000"
    ENDTIME    = "2006:09:17:18:00:0.000"
    DIPTIME    = "2006:09:17:06:00:0.000"

  elif runname=="2009Oct19_001":
    STARTTIME  = "2009:10:19:06:00:0.000"
    ENDTIME    = "2009:10:20:00:00:0.000"
    DIPTIME    = "2009:10:19:06:00:0.000"

  elif runname=="2000Jul23_001":
    STARTTIME  = "2000:07:23:06:00:0.000"
    ENDTIME    = "2000:07:24:03:00:0.000"
    DIPTIME    = "2000:07:23:06:00:0.000"

  elif runname=="2000Dec26_001":
    STARTTIME  = "2000:12:26:12:00:0.000"
    ENDTIME    = "2000:12:27:05:00:0.000"
    DIPTIME    = "2000:12:26:12:00:0.000"

  elif runname=='cn':
    STARTTIME  = "1967:01:01:00:00:0.000"    # UT when the run starts
    ENDTIME    = "1967:01:01:00:00:0.000"
    DIPTIME    = "1967:01:01:00:00:0.000"

  elif runname=='cs':
    STARTTIME  = "1967:01:01:00:00:0.000"    # UT when the run starts
    ENDTIME    = "1967:01:01:00:00:0.000"
    DIPTIME    = "1967:01:01:00:00:0.000"

  else :
    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in run_info.openggcm_run!!")
    sys.exit(1)


  TIMES=[STARTTIME,ENDTIME,DIPTIME]

  return TIMES


def iosum_info(runname):
  "provide ylabel and yrange of ionosphere summary plot"

  vstr    =[ 'IMF Bx(blue), By(green), Bz(red) [nT]',                   \
             'SW  Vx(blue), Vy(green), Vz(red) [km/s]',                 \
             'Nsw (blue) [/cm$^3$], Pdyn_sw (green) [nPa]',             \
             'Polar Cap Area [m$^2$]',                                  \
             'CPCP [kV]',                                               \
             'Maximum Joule Heating [W/m$^2$]',                         \
             'Integrated Joule Heating [GW]'                       	]


  if runname=='hjk3001' or runname=='hjk3002' or runname=='hjk3003' :
    vran    =[ [-20,20],                \
               [-500,500],              \
#             [[0,50], [0,10]], 	\
               [0,50],          	\
               [1e13,1.6e13],           \
               [0,500],                 \
               [0,0.2],                 \
               [0,200]                  ]

  elif runname=='hjc0001':
    vran    =[ [-30,20],                  \
               [-600,100],                \
#             [[0,20], [0,10]],           \
               [0,30],                    \
               [1e13,2e13],               \
               [0,500],                   \
               [0,0.5],                   \
               [0,800]                    ]

  elif runname=='hjc0002' or runname=='2000Feb11_005' or runname=='2000Feb11_006' \
    or runname=='2000Feb11_010' or runname=='2000Feb11_011':
    vran    =[ [-30,20],                  \
               [-600,100],                \
#             [[0,20], [0,10]],           \
               [0,30],                    \
               [1e13,2e13],               \
               [0,150],                   \
               [0,0.5],                   \
               [0,800]                    ]


  elif runname=='djl00703a'         or  runname=='hjk2002' :
    vran    =[ [-20,20],                  \
               [-500,500],                \
#             [[0,20], [0,10]],           \
               [0,20],                    \
               [1e13,2e13],               \
               [0,500],                   \
               [0,0.5],                   \
               [0,500]                    ]


  elif runname=='hjc-19970110-jr01' or  runname=='hjc-19970110-jr02':
    vran    =[ [-20,20],                  \
               [-500,500],                \
#             [[0,20], [0,10]],           \
               [0,20],            	  \
               [1e13,2e13],               \
               [0,300],                   \
               [0,0.2],                   \
               [0,250]                    ]

  elif runname=='djl00503' or runname=='hjk2001' or runname =='hjk2007':
    vran    =[ [-10,10],                  \
               [-500,100],                \
#             [[0,50], [0,10]],           \
               [0,50],                    \
               [1.0e12,1.5e13],           \
               [0,150],                   \
               [0,0.05],                  \
               [0,100]                    ]

  elif runname=='hjk2003' or runname=='hjk2015' or runname=='hjk2017':
    vran    =[ [-20,20],                  \
               [-500,100],                \
#             [[0,30], [0,5]],            \
               [0,30],             	  \
               [1.0e12,1.5e13],           \
               [0,200],                   \
               [0,0.5],                   \
               [0,100]                    ]

  elif runname=='hjk2004' or runname=='hjk2006' or runname=='hjk2008' or  \
       runname=='hjk2014' or runname=='hjk2016' :
    vran    =[ [-20,40],                  \
               [-900,300],                \
#             [[0,50], [0,25]],           \
               [0,50], 	           	  \
#              [1.0e12,1.5e13],           \
#              [0,400],                   \
               [0,0.8],                   \
               [0,1500]                   ]

  elif runname=='hjc2007':
    vran    =[ [-40,40],                  \
               [-1000,300],                \
#             [[0,50], [0,25]],           \
               [0,50],                    \
               [0.6e13,2.0e13],           \
               [0,100],                   \
               [0,0.3],                   \
               [0,800]                   ]



  elif runname=='hjc1001' or runname=='hjc1002' or runname=='hjc1003' :
    vran    =[ [-40,10],                  \
               [-1100,100],               \
#             [[0,50], [0,25]],           \
               [0,10],                    \
               [1.0e12,2.0e13],           \
               [0,500],                   \
               [0,0.3],                   \
               [0,2000]                   ]

  elif runname=='hjc2006' or runname=='test_oldCTIM'  or runname=='storm-2014-AUG-05-jr12':
    vran    =[ [-50,50],                  \
               [-800,200],               \
#             [[0,50], [0,25]],           \
               [0,30],                    \
               [1.0e12,2.0e13],           \
               [0,300],                   \
               [0,1.0],                   \
               [0,1500]                   ]

  elif runname=='2005Aug24' or runname=='2005Aug24_001' or runname=='2005Aug24_002' or \
       runname=='2005Aug24_008':

    vran    =[ [-60,60],                  \
               [-800,200],               \
#             [[0,50], [0,25]],           \
               [0,60],                    \
               [1.0e12,2.0e13],           \
               [0,300],                   \
               [0,1.0],                   \
               [0,2000]                   ]

  elif runname=='hjc1004' :
    vran    =[ [-20,20],                  \
               [-500,100],               \
#             [[0,50], [0,25]],           \
               [0,10],                    \
               [0.5e12,3.0e13],           \
               [0,150],                   \
               [0,0.2],                   \
               [0,1000]                   ]

  elif runname=='2010Apr05_001' :
    vran    =[ [-20,20],                  \
               [-800,300],               \
#             [[0,50], [0,25]],           \
               [0,20],                    \
               [0.5e13,2.0e13],           \
               [0,200],                   \
               [0,0.4],                   \
               [0,1000]                   ]


  else :
    vran    =[ [-20,40],                  \
               [-900,300],                \
#             [[0,50], [0,25]],           \
               [0,50],                    \
               [1.0e12,1.5e13],           \
               [0,400],                   \
               [0,0.8],                   \
               [0,1500]                   ]


    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in iosum_info !!")
#   sys.exit(1)

  return vstr,vran


def tick_info(runname):

  xmin=-9999
  xmax=9999
  if runname == 'djl00701' or \
     runname == 'djl00703' or \
     runname == 'djl00703a'or \
     runname == 'hjk2002'     :

    dtmaj   =  600                # major tick interval
    dtmin   =  60                 # minor tick interval
    dtlab   =  1800               # major tick label interval
    xadd    =  0		  # xadd used becuase of djl00503's weird timeline

  elif runname == '2008Jun28_002':
    dtmaj   =   3600
    dtmin   =   600
    dtlab   =   3600
    xadd    =   0

  elif runname == '2008Jun28_003':
    dtmaj   =   3600
    dtmin   =   600
    dtlab   =   3600
    xadd    =   0
    xmin    =   3600
    xmax    =   6.5*3600

  elif runname=='2008Jun28_005' or runname=="2008Jun28_005_Jel":
    dtmaj   =   3600
    dtmin   =   600
    dtlab   =   3600
    xadd    =   0
    xmin    =   4*3600
    xmax    =   12*3600

  elif runname == '2010Aug20_002':
    dtmaj   =   3600
    dtmin   =   600
    dtlab   =   7200
    xadd    =   0
    xmin    =   3*3600
    xmax    =   10*3600

  elif runname == '2009Oct14_001':
    dtmaj   = 3600
    dtmin   = 600
    dtlab   = 3600
    xadd    = 0

  elif runname == '2009Oct14_002':
    dtmaj   = 3600
    dtmin   = 600
    dtlab   = 7200
    xadd    = 0
#    xmin    = 10*3600
#    xmax    = 16*3600

  elif runname == '2006Jan13_002':
    dtmaj   = 14400
    dtmin   = 3600
    dtlab   = 14400
    xadd    = 0
    #xmax

  elif runname == '2006Jan10_002':
    dtmaj   = 14400
    dtmin   = 3600
    dtlab   = 14400
    xadd    = 0

  elif runname == '2001Mar22_002':
    dtmaj   = 7200
    dtmin   = 1800
    dtlab   = 7200
    xadd    = 0

  elif runname == '2000Sep29_003':
    dtmaj   = 3600
    dtmin   = 600
    dtlab   = 3600
    xadd    = 0
    xmin    = 3600*2
    xmax    = 3600*9

  elif runname == '2001Apr26_001':
    dtmaj   = 7200
    dtmin   = 1800
    dtlab   = 14400
    xadd    = 0

  elif runname == '2008Oct09_001':
    dtmaj   = 3600
    dtmin   = 600
    dtlab   = 3600
    xadd    = 0
    xmin    = 3600*1
    xmax    = 3600*8

  elif runname == '2008Nov12_001':
    dtmaj   = 3600
    dtmin   = 600
    dtlab   = 3600
    xadd    = 0
#    xmin    = 4.5*3600
#    xmax    = 8.1*3600

  elif runname == '2009Mar28_002':
    dtmaj   = 3600
    dtmin   = 1800
    dtlab   = 7200
    xadd    = 0
#    xmin    = 10*3600
#    xmax    = 16*3600

  elif runname == '2009Apr05_001':
    dtmaj   = 7200
    dtmin   = 1800
    dtlab   = 14400
    xadd    = 0
#    xmin    = 4.5*3600
#    xmax    = 8.5*3600

  elif runname == '2009Mar11_001':
    dtmaj   = 7200
    dtmin   = 1800
    dtlab   = 14400
    xadd    = 0

  elif runname == '2009Apr13_001':
    dtmaj   = 7200
    dtmin   = 1800
    dtlab   = 14400
    xadd    = 0

  elif runname == '2015Nov04_002':
   dtmaj   = 1800
   dtmin   = 600
   dtlab   = 3600
   xadd    = 0

  elif runname=="2003May04_001" or runname=="2003May04_001_Jel":
   dtmaj    = 1800
   dtmin    = 600
   dtlab    = 1800
   xadd     = 0
   xmin     = 6*3600
   xmax     = 9*3600

  elif runname == '2003Feb12_002':
    dtmaj   = 7200
    dtmin   = 1800
    dtlab   = 14400
    xadd    = 0

  elif runname == '2006Sep17_001':
    dtmaj   = 3600
    dtmin   = 600
    dtlab   = 3600
    xadd    = 0

  elif runname == '2009Oct19_001':
    dtmaj   = 10800
    dtmin   = 3600
    dtlab   = 10800
    xadd    = 0

  else :
    dtmaj   =  600
    dtmin   =  60
    dtlab   =  1800
    xadd    =  0

    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in run_info.tick_info !!")
#   sys.exit(1)

  xran=[xmin,xmax]

  return  dtmaj,dtmin,dtlab,xran



def mrplt_info(runname):

  vstr     = [ 'IMF By (blue) and Bz (green) [nT]',         			\
               'Nsw (blue) [/cm$^3$], Pdy_sw (green) [nT]', 			\
               'CPCP (blue), Ave MR_rates (green) [kV]\n'			\
               +'Delta Pot along OCB (red)',                           	\
               'Day MR_rate (blue), Night MR_rate (green) [kV]\n' 		\
               +'Delta Pot along OCB (red)',                           	\
               'PC Area [m$^2$]',                                           	\
               'Delta OpenFlux/ Delta t  (blue) [kV]\n'+                   	\
               'Day MR_rate - Night MR_rate (green) ',                   	\
               'Delta Day_OpenFlux (blue) [T-m$^2$]\n'+                    	\
               'Deata Night_OpenFlux (green)'                               ]


  if runname == 'djl00701' 		or \
     runname == 'djl00703' 		or \
     runname == 'djl00703a'		or \
     runname == 'hjk2002'  		:
    vran     = [ [-20,0]   , 			\
                [[0,20],[0,10]],                \
                 [100,400],                     \
                 [100,400],                     \
                 [0.8e13,1.6e13],               \
                 [-150,150], 			\
                 [-1e7,1e7]                     ]

  elif runname == 'hjk0009' :
    vran     = [ [-10,10],                      \
                [[0,60],[0,10]],                \
                 [0,300] ,                      \
                 [0,300],                       \
                 [0.0e13,1.5e13],               \
                 [-50,100],                     \
                 [-1e7,1e7]                     ]

  elif runname == 'hjc0001':
    vran     = [ [-30,20],                      \
                [[0,30],[0,20]],                \
                 [0,500] ,                      \
                 [0,500],                       \
                 [0.0e13,1.5e13],               \
                 [-50,300],                     \
                 [-1e7,1e7]                     ]

  elif runname == 'hjc0002' or runname == '2000Feb11_011':
    vran     = [ [-30,20],                      \
                [[0,30],[0,20]],                \
                 [0,300] ,                      \
                 [0,300],                       \
                 [1.0e13,2.0e13],               \
                 [-50,300],                     \
                 [-1e7,1e7]                     ]


  elif runname == 'hjc-19970110-jr01'   or \
       runname == 'hjc-19970110-jr02'   or \
       runname == 'hjc-19970110-jr14y'  or \
       runname == 'hjc-19970110-jr15y'     :
    vran     = [ [-20,0]   , 			\
                [[0,20],[0,10]],                \
                 [0,300],                       \
                 [0,300],                       \
                 [1.3e13,1.9e13],               \
                 [-150,150], 			\
                 [-1e7,1e7]                     ]

  elif runname == 'djl00503' or runname == 'hjk2001' or runname =='hjk2007'     :
    vran     = [ [-10,10],			\
                [[0,60],[0,10]],                \
                 [0,150] ,                      \
                 [0,150],                       \
                 [0.0e13,1.5e13],               \
                 [-50,100], 			\
                 [-1e7,1e7]                     ]


  elif runname == 'hjk2003' or runname == 'hjk2015' or runname=='hjk2017'   :
    vran     = [ [-5,20],                       \
                [[0,30],[0,10]],                 \
                 [0,200] ,                      \
                 [0,200],                       \
                 [0.0e13,1.5e13],               \
                 [-200,200],                    \
                 [-1e7,1e7]                     ]

  elif runname == 'hjk2004' or runname == 'hjk2006' or  \
       runname == 'hjk2014' or runname == 'hjk2016':
    vran     = [ [-30,30],                      \
                [[0,50],[0,50]],                \
                 [-100,400] ,                   \
                 [-100,400],                    \
                 [0.0e13,1.5e13],               \
                 [-300,300],                    \
                 [-2e7,2e7]                     ]

  elif runname == 'hjk3001' or runname == 'hjk3003' :
    vran     = [ [-10,10], 			\
                [[0,50],[0,10]],                \
                 [100,300] ,                    \
                 [100,300],                     \
                 [1.0e13,1.6e13],               \
                 [-100,100], 			\
                 [-1e7,1e7]                     ]


  elif runname == 'hjc1004' :
    vran     = [ [-20,20],                      \
                [[0,10],[0,10]],                \
                 [0,150] ,                      \
                 [0,150],                       \
                 [0.5e12,3.0e13],               \
                 [-200,200],                    \
                 [-2e7,2e7]                     ]

  elif runname == 'hjk0001' or runname=='hjk0003' or \
       runname == 'hjk0005' or runname=='hjk0006' :
    vran     = [ [-10,10],                      \
                [[0,10],[0,10]],                \
                 [0,400] ,                      \
                 [0,400],                       \
                 [0.5e12,1.5e13],               \
                 [-200,200],                    \
                 [-1e7,1e7]                     ]

  elif runname == 'N2SIMF_hR':
    vran     = [ [-10,10],                      \
                [[0,10],[0,10]],                \
                 [0,300] ,                      \
                 [0,300],                       \
                 [0.1e13,1.5e13],               \
                 [-150,150],                    \
                 [-1e7,1e7]                     ]


  else :
    vran     = [ [-10,10],                      \
                [[0,50],[0,10]],                \
                 [100,300] ,                    \
                 [100,300],                     \
                 [1.0e13,1.6e13],               \
                 [-100,100],                    \
                 [-1e7,1e7]                     ]

    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in mrplt_info !!")
#   sys.exit(1)

  return vstr,vran



def DHmr_info(runname):

  vstr     = [ 'IMF By (blue) and Bz (green) [nT]',                             \
               'Nsw (blue) [/cm$^3$], Pdy_sw (green) [nT]',                     \
               'CPCP (blue), Ave MR_rates (green) [kV]\n'                       \
               +'Delta Pot along OCB (red)',                            	\
               'Day MR_rate (blue), Night MR_rate (green) [kV]\n'               \
               +'Delta Pot along OCB (red)',                            	\
               'Hesse Day MR_rate (blue), Night MR_rate (green) [kV]\n',         \
               'PC Area [m$^2$]',                                               \
               'Delta OpenFlux/ Delta t  (blue) [kV]\n'+                        \
               'Day MR_rate - Night MR_rate (green) ',                          \
               'Delta Day_OpenFlux (blue) [T-m$^2$]\n'+                         \
               'Deata Night_OpenFlux (green)'                               ]


  if runname == 'djl00701' 		or \
     runname == 'djl00703' 		or \
     runname == 'djl00703a'		or \
     runname == 'hjk2002'  		or \
     runname == 'hjc-19970110-jr01'     or \
     runname == 'hjc-19970110-jr15y'    :


    vran     = [ [-20,0]   ,                    \
                [[0,20],[0,10]],                \
#                [0,20],                	\
                 [100,400],                     \
                 [100,400],                    	\
                 [100,400],                    	\
                 [0.8e13,1.6e13],               \
                 [-150,150],                    \
                 [-1e7,1e7]                     ]


  elif runname == 'djl00503' or runname == 'hjk2001' or runname =='hjk2007'     :
    vran     = [ [-10,10],                      \
                [[0,60],[0,10]],                \
#                [0,60], 	                \
                 [0,150] ,                      \
                 [0,150] ,                      \
                 [0,150],                       \
                 [0.0e13,1.5e13],               \
                 [-50,100],                     \
                 [-1e7,1e7]                     ]



  elif runname == 'hjk2003' or runname == 'hjk2005'    :
    vran     = [ [-5,20],                      	\
                [[0,30],[0,5]],                	\
#                [0,30],                	\
                 [0,250] ,                      \
                 [0,250] ,                      \
                 [0,250],                    	\
                 [0.0e13,1.5e13],               \
                 [-200,200],                    \
                 [-1e7,1e7]                     ]

  elif runname == 'hjk2004' or runname == 'hjk2006'  :
    vran     = [ [-30,30],                      \
                [[0,50],[0,30]],                \
#                [0,50],                        \
                 [-50,500],                     \
                 [-50,500],                     \
                 [-50,500],                     \
                 [0.0e13,1.5e13],               \
                 [-300,300],                    \
                 [-2e7,2e7]                     ]

  elif runname == 'hjk3001' or runname == 'hjk3003' :
    vran     = [ [-10,10],                      \
                [[0,50],[0,10]],                \
#                [0,50],               	 	\
                 [100,300] ,                    \
                 [100,300],                     \
                 [0,30],                        \
                 [1.0e13,1.6e13],               \
                 [-100,100],                    \
                 [-1e7,1e7]                 	]

  else :
    vran     = [ [-10,10],                      \
                [[0,50],[0,10]],                \
#                [0,50],                        \
                 [100,300] ,                    \
                 [100,300],                     \
                 [0,30],                        \
                 [1.0e13,1.6e13],               \
                 [-100,100],                    \
                 [-1e7,1e7]                     ]

    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in DHmr_info !!")
#   sys.exit(1)

  return vstr,vran
