#!/usr/bin/python
# all info regarding the paper plots

import sys

def event_info(runname):
  " set ylabel & yrange of event plots"

  ylab = [ 'IMF [nT]',                          \
           'Vsw [km/s]',                        \
           'Nsw [cm$^{-3}$]',                   \
           'Psw [nPa]',                         \
           'PC area [${R_E}^2$]',                 \
           'CPCP[kV]',                          \
           'MR rates  [kV]'                     ]

  if runname=='hjc-19970110-jr02'  or \
     runname=='hjc-19970110-jr01'  or \
     runname=='hjc-19970110-jr14y' or \
     runname=='hjc-19970110-jr15y'  :

    yran = [ [-20,0],           \
             [300,500],         \
             [0,20],            \
             [0,10],             \
             [0.25,0.45],         \
             [0,250],           \
             [0,250]            ]

  elif runname=='djl00503' :

    yran = [ [-10,10],          \
             [250,450],         \
             [0,60],            \
             [0,20],            \
             [0.,0.5],          \
             [0,150],           \
             [0,150]            ]


  elif runname=='hjk2003' or runname=='hjk2015' or runname=='hjk2017' :

    yran = [ [-5,20],           \
             [300,500],         \
             [0,30],            \
             [0,20],            \
             [0.,0.5],          \
             [0,150],           \
             [0,200]            ]

  elif runname=='hjc0001':
    yran = [ [-30,20],           \
             [300,700],         \
             [0,30],            \
             [0,20],            \
             [0.2,0.6],          \
             [0,500],           \
             [0,500]            ]

  elif runname=='hjc0002':
    yran = [ [-30,20],           \
             [300,700],         \
             [0,30],            \
             [0,20],            \
             [0.2,0.6],          \
             [0,300],           \
             [0,300]            ]

  elif runname=='hjc2004':
    yran = [ [-15,15],           \
             [400,500],         \
             [0,10],            \
             [0,10],            \
             [0.,0.6],          \
             [0,500],           \
             [0,500]            ]


  elif runname=='hjc1004':
    yran = [ [-15,15],           \
             [400,500],         \
             [0,10],            \
             [0,10],            \
             [0.,0.6],          \
             [0,200],           \
             [0,200]            ]


  else:
    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in event_info !!")
    sys.exit(1)

  return ylab,yran


def mrstory_1Dinfo(runname):
  " set yrange of mrstory1D plots"

  if runname=='hjc-19970110-jr02' or runname=='hjc-19970110-jr01' :

    yran = [ [0,250],                             \
             [0,10],                              \
             [-100,100],                          \
             [-20,100],                           \
             [-20,100],                           \
             [-20,100],                           \
             [-20,100]                            ]

  elif runname=='hjk2003' or runname=='hjk2015' or runname=='hjk2017':

    yran = [ [0,250],                             \
             [0,30],                              \
             [-50,150],                          \
             [-30,40],                           \
             [-30,40],                           \
             [-30,40],                           \
             [-30,40]                            ]

  elif runname=='djl00503' :

    yran = [ [0,150],                             \
             [0,100],                              \
             [-30,70],                          \
             [-10,90],                           \
             [-10,90],                           \
             [-10,90],                           \
             [-10,90]                            ]


  elif runname=='hjc0001':
    yran = [ [0,150],                             \
             [0,100],                              \
             [-30,70],                          \
             [-10,90],                           \
             [-10,90],                           \
             [-10,90],                           \
             [-10,90]                            ]



  else :
    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in event_info !!")
    sys.exit(1)

  return yran

def mrstory_info(runname):
  " set yrange of mrstory1D plots"

  if runname=='hjc-19970110-jr01' :

    yran = [ 					\
             # Plot 1
             [ [-20,0],				\
               [300,500],                       \
               [0,20],				\
               [0,250],				\
               [-100,100] ],			\
             # Plot 2
             [ [0,250],				\
               [-20,100],                       \
               [-20,100],                       \
               [-20,100],                       \
               [-20,100] ],                     \
             # Plot 3
             [ [0,250],                         \
               [-100,400],                      \
               [-100,400],                      \
               [-100,400],                      \
               [-100,400] ]                     ]

  elif runname=='hjc-19970110-jr15y' :

    yran = [                                    \
             # Plot 1
             [ [-20,0],                         \
               [300,500],                       \
               [0,20],                          \
               [0,250],                         \
               [-100,100] ],                    \
             # Plot 2
             [ [0,250],                         \
               [-20,60],                       \
               [-20,60],                       \
               [-20,60],                       \
               [-20,60] ],                     \
             # Plot 3
             [ [0,250],                         \
               [-600,600],                      \
               [-600,600],                      \
               [-600,600],                      \
               [-600,600] ]                     ]

  elif runname=='hjc0001':
    yran = [                                    \
             # Plot 1
             [ [-20,0],                         \
               [300,500],                       \
               [0,20],                          \
               [0,250],                         \
               [-100,100] ],                    \
             # Plot 2
             [ [0,250],                         \
               [-20,60],                       \
               [-20,60],                       \
               [-20,60],                       \
               [-20,60] ],                     \
             # Plot 3
             [ [0,250],                         \
               [-600,600],                      \
               [-600,600],                      \
               [-600,600],                      \
               [-600,600] ]                     ]


  elif runname=='hjk2003' or runname=='hjk2015' or runname=='hjk2017':

    yran = [ 					\
             # Plot 1
             [ [-5,20],                         \
               [300,500],                       \
               [0,30],                          \
               [0,200],                         \
               [-50,150] ],                     \
             # Plot 2
             [ [0,200],                         \
               [-50,50],                        \
               [-50,50],                        \
               [-50,50],                        \
               [-50,50] ],                      \
             # Plot 3
             [ [0,200],                         \
               [-300,600],                      \
               [-300,600],                      \
               [-300,600],                      \
               [-300,600] ]                     ]

  elif runname=='djl00503' :

    yran = [                                    \
             # Plot 1
             [ [-10,20],                        \
               [250,450],                       \
               [0,60],                          \
               [0,150],                         \
               [-50,50] ],                      \
             # Plot 2
             [ [0,150],                         \
               [-50,50],                        \
               [-50,50],                        \
               [-50,50],                        \
               [-50,50] ],                      \
             # Plot 3
             [ [0,150],                         \
               [-600,600],                      \
               [-600,600],                      \
               [-600,600],                      \
               [-600,600] ]                     ]


  else :
    print ("ERROR!!! No data matches with runname:",runname)
    print ("Add data in event_info !!")
    sys.exit(1)

  return yran
