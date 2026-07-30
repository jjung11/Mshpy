
#  Jimmy's python modules
#  2005-12-27
#  Jimmy Raeder
#  UNH Space Science Center  J.Raeder@unh.edu

import locale

def read_tseries(file,t1,t2):
  f = open(file,'r'); l = f.read().split('\n'); f.close(); ll = []; ww = []
  #...... convert to float and pick out time

  for s in l:
    w = s.split(None)
#    print('w',w)
    if len(w) == 7:
      iy = locale.atof(w[0]); mo = locale.atof(w[1]); id = locale.atof(w[2])
      ih = locale.atof(w[3]); mi = locale.atof(w[4]); se = locale.atof(w[5])
      vv = locale.atof(w[6]); tt = epo1(iy,mo,id,ih,mi,se)
      if (tt >= t1 and tt <= t2):
        w[0]=iy; w[1]=mo; w[2]=id; w[3]=ih; w[4]=mi; w[5]=se; w[6]=tt; w.append(vv)
        ll.append(w)

  #...... transpose
  if ll == [] : return 0
  else: x = [[r[col] for r in ll] for col in range(len(ll[0]))]

#  x = [[r[col] for r in ll] for col in range(len(ll[0]))]

  return x

def epo1c(c):
  w=c.split(':')
  return(epo1(locale.atoi(w[0]),
              locale.atoi(w[1]),
              locale.atoi(w[2]),
              locale.atoi(w[3]),
              locale.atoi(w[4]),
              locale.atof(w[5])))

def epo1(iy,mo,id,ih,mi,se):
  if iy < 200 : iy = 1900 + iy
  i1=367*iy
  i2=int((mo+9)/12)
  i2=(i2+iy)*7
  i2=int(i2/4)
  i3=int((275*mo)/9)
  i4=100*iy+mo
  d1=(1.0)
  if (i4-190002.5) < 0.0 : d1=(-1.0)
  rr = ( i1 - i2 + i3 + id + 1721013.5 -0.5*d1 +0.5 )*86400.0
  rr = rr + 3600.0*ih + 60.0*mi +se
  return(rr)
