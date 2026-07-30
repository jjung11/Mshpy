import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv
import datetime
import glob
import BSaMP


def OMNIread(f):

    BErr='9999.99'          # err of B field
    VErr='99999.9'          # err of Velocity
    NErr='999.99'               # err of Number density

    time,Bx,By,Bz,vx,vy,vz,n,Pd,Ma,Mm=[],[],[],[],[],[],[],[],[],[],[]
    header1,header2=[],[]
    list=glob.glob(f)
    f0=open(list[0],'r')
    for line in f0:
        line=line.strip()
        w=line.split()
        if w[4]!=BErr and w[7]!=VErr and w[8]!=NErr:
            time.append(datetime.datetime(int(w[0]),1,1)+datetime.timedelta(days=int(w[1])-1,hours=int(w[2]),minutes=int(w[3])))
            Bx.append(float(w[4]))
            By.append(float(w[5]))
            Bz.append(float(w[6]))
            vx.append(float(w[7]))
            vy.append(float(w[8]))
            vz.append(float(w[9]))
            n.append(float(w[10]))
            Pd.append(float(w[11]))
            Ma.append(float(w[12]))
            Mm.append(float(w[13]))
    Bx=np.array(Bx)
    By=np.array(By)
    Bz=np.array(Bz)
    vx=np.array(vx)
    vy=np.array(vy)
    vz=np.array(vz)
    n=np.array(n)
    Pd=np.array(Pd)
    Ma=np.array(Ma)
    Mm=np.array(Mm)
    B_sw=np.sqrt(Bx**2+By**2+Bz**2)
    V=np.sqrt(vx**2+vy**2+vz**2)
    omni=pd.DataFrame({'datetime':time,'Bx':Bx,'By':By,'Bz':Bz,'V':V,'vx':vx,'vy':vy,'vz':vz,'n':n,'Pd':Pd,'Ma':Ma,'Mm':Mm,'B':B_sw})
    return omni

def SSCread(f):
    dateparse=lambda x,y: pd.datetime.strptime(x+' '+y,'%y/%m/%d %H:%M:%S')
    sat=pd.read_csv(f,header=None,sep='\s+',names=['d','t','x','y','z'],parse_dates={'datetime':[0,1]},date_parser=dateparse)
    sat.datetime=pd.to_datetime(sat.datetime)
    return sat

f_sw='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001_Jel/omni.lst'
xyz='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001_Jel/orbit.txt'
sc='Cluster 4'
omni=OMNIread(f_sw)
xyz=SSCread(xyz)

fig,(ax9,ax10)=plt.subplots(1,2)

BSaMP.BSMPj(ax9,ax10,omni.Bz[0],omni.Pd[0],0)
BSaMP.BSMPj(ax9,ax10,omni.Bz.iloc[-1],omni.Pd.iloc[-1],1)
ax9.plot(xyz.x,xyz.y,label=sc)
ax9.plot(xyz.x[0],xyz.y[0],'o',markersize=3)
ax9.set_xticks(np.linspace(-20,20,5))
ax9.grid()
ax9.set_ylabel('$Y_{gse}[Re]$')
ax9.set_xlabel('$X_{gse}[Re]$')
#ax9.text(-0.1,1.1,'A',transform=ax9.transAxes, size=20,weight='bold')
#    leg9=ax9.legend(handlelength=0,loc='upper left',bbox_to_anchor=(0,.9),framealpha=0,fontsize=9)
#    for line,text in zip(leg9.get_lines(),leg9.get_texts()):
#        text.set_color(line.get_color())
ax9.set_aspect('equal')


ax10.plot(xyz.x,xyz.z,label=sc)
ax10.plot(xyz.x[0],xyz.z[0],'o',markersize=3)
ax10.set_xticks(np.linspace(-20,20,5))
ax10.grid()
ax10.set_xlabel('$X_{gse}[Re]$')
ax10.set_ylabel('$Z_{gse}[Re]$')
#    leg10=ax10.legend(handlelength=0,loc='upper left',bbox_to_anchor=(0,.9),framealpha=0,fontsize=9)
#    for line,text in zip(leg10.get_lines(),leg10.get_texts()):
#        text.set_color(line.get_color())
ax10.set_aspect('equal')
plt.tight_layout()

plt.savefig('2003May04_001_sc_orbit_Jel.png')
