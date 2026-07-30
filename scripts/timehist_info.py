#!/usr/bin/python
#

import sys

def timehist_info(runname,scloc):
  " set val range based on satellite location"

  if runname=='hjc-19970110-jr02' or \
     runname=='hjc-19970110-jr01' or \
     runname=='test_oldCTIM' or \
     runname=='hjc-19970110-jr15y' :

   if scloc=='SW' :
     vran=[ [-50,50],   \
            [-500,500], \
            [0,30],     \
            [0,1]       ]

   elif scloc=='MSH':
     vran=[ [-100,100], \
            [-300,300], \
            [0,50],     \
            [0,1]       ]

   elif scloc=='tail':
     vran=[ [-70,70], \
            [-400,400], \
            [0,3],     \
            [0,5]       ]

   elif scloc=='nlobe':
     vran=[ [-70,70],   \
            [-400,400], \
            [0,1],      \
            [0,1]       ]

   elif scloc=='slobe':
     vran=[ [-70,70], \
            [-400,400], \
            [0,1],     \
            [0,5]       ]

   elif scloc=='nlobe1':
     vran=[ [-70,70],   \
            [-400,400], \
            [0,1],      \
            [0,1]       ]
   elif scloc=='nlobe2':
     vran=[ [-70,70],   \
            [-400,400], \
            [0,1],      \
            [0,1]       ]

   elif scloc=='tail1':
     vran=[ [-150,150], \
            [-400,400], \
            [0,3],     \
            [0,5]       ]

   elif scloc=='tail2':
     vran=[ [-50,50], \
            [-600,600], \
            [0,3],     \
            [0,5]       ]

   elif scloc=='tail3':
     vran=[ [-50,50], \
            [-600,600], \
            [0,3],     \
            [0,5]       ]

   elif scloc=='tail4':
     vran=[ [-70,70], \
            [-600,600], \
            [0,3],     \
            [0,5]       ]



   else :
    print ("ERROR!!! No data matches with scloc:",scloc)
    print ("Add data in timehist_info !!")
    sys.exit(1)

  elif runname=='hjk2003' or runname=='hjk2015' or runname=='hjk2017' :

   if scloc=='SW' :
     vran=[ [-10,30],   \
            [-500,100], \
            [0,30],     \
            [0,1]       ]

   elif scloc=='MSH':
     vran=[ [-20,150], \
            [-300,100], \
            [0,100],     \
            [0,1]       ]

   elif scloc=='tail':
     vran=[ [-50,50], \
            [-600,600], \
            [0,25],     \
            [0,20]       ]

   elif scloc=='nlobe':
     vran=[ [-50,50],   \
            [-400,100], \
            [0,2],      \
            [0,2]       ]

   elif scloc=='slobe':
     vran=[ [-70,70], \
            [-400,400], \
            [0,10],     \
            [0,1]       ]

   elif scloc=='nlobe1':
     vran=[ [-50,50],   \
            [-400,400], \
            [0,2],      \
            [0,2]       ]

   else :
    print ("ERROR!!! No data matches with scloc:",scloc)
    print ("Add data in timehist_info !!")
    sys.exit(1)

  elif runname=='djl00503' or runname=='hjk2001' :

   if scloc=='SW' :
     vran=[ [-10,10],   \
            [-500,100], \
            [0,50],     \
            [0,1]       ]

   elif scloc=='MSH':
     vran=[ [-50,100], \
            [-500,100], \
            [0,150],     \
            [0,1]       ]

   elif scloc=='tail':
     vran=[ [-50,50], \
            [-600,600], \
            [0,25],     \
            [0,20]       ]

   elif scloc=='nlobe':
     vran=[ [-50,50],   \
            [-400,100], \
            [0,2],      \
            [0,2]       ]

   elif scloc=='nlobe1':
     vran=[ [-50,50],   \
            [-400,400], \
            [0,2],      \
            [0,2]       ]

   elif scloc=='nlobe1' or scloc=='nlobe2' or scloc=='nlobe3' or scloc=='nlobe4':
     vran=[ [-100,100],   \
            [-400,400], \
            [0,10],      \
            [0,10]       ]



   elif scloc=='slobe':
     vran=[ [-70,70], \
            [-400,400], \
            [0,10],     \
            [0,1]       ]

   else :
    print ("ERROR!!! No data matches with scloc:",scloc)
    print ("Add data in timehist_info !!")
    sys.exit(1)


  else:
    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in timehist_info !!")
    sys.exit(1)


  return vran
