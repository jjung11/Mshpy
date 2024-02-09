import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv
from sympy.solvers import solve
from sympy import Symbol,nsolve
from sympy import sqrt,log,tanh
from scipy.interpolate import NearestNDInterpolator as NNDI
from scipy.interpolate import LinearNDInterpolator as LNDI
import glob
import datetime

#For LNDI:
#np.save('test',f)
#f2=np.load('test.npy')
#f2.item()(x)

# Bow Shock
a11=.45
a22=1
a33=.8
a12=.18
a14=46.6
a24=-2.2
a34=-.6
a44=-618
R0=11.8954

#filepath
external='easystore'
run='Msh_Nstep'

def appendSpherical_np(xyz):
    ptsnew = np.hstack((xyz,np.empty(xyz.shape)))
    xy = xyz[:,0]**2 + xyz[:,1]**2
    ptsnew[:,3] = np.sqrt(xy + xyz[:,2]**2)
    #ptsnew[:,4] = np.arctan2(np.sqrt(xy), xyz[:,2]) # for elevation angle defined from Z-axis down
    ptsnew[:,4] = 180/np.pi*np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    ptsnew[:,5] = 180/np.pi*np.arctan2(xyz[:,1], xyz[:,0])
    return ptsnew

def bsdf(N,V,Ma,B,xl,yl,zl):
    D=0.937*(0.846+0.042*B)
    f=91.55/(N*V**2)**(1/6)*(1+D*(5/3-1)*(Ma**2+2)/((5/3+1)*(Ma**2-1)))/R0
    t=Symbol('t',positive="True")
    x=xl*t
    y=yl*t
    z=zl*t
    sol=solve(a11*(x/f)**2+a22*(y/f)**2+a33*(z/f)**2+a12*(x/f)*(y/f)+a14*(x/f)+a24*(y/f)+a34*(z/f)+a44,t)
    dist=np.linalg.norm([np.array((xl*sole,yl*sole,zl*sole),dtype=np.float32) for sole in sol])
    return dist

def mpdf(Pd,Bz,xyz):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    r0=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    alpha=(0.58-0.007*Bz)*(1+0.024*np.log(Pd))
    R = r0*(2/(1+np.cos(theta)))**alpha
    return R

def genf(fun,nxyz,f):
    outl=[]
    for i,j in zip(nxyz,f):
        if i[2][2]<0 or i[2][2]>1:
            out=np.nan
        else:
            out1=fun[i[0]](i[2])[0]
            out2=fun[i[1]](i[2])[0]
            if i[0]==i[1]:
                out=out1
            else:
                out=(out1*(1-j)+out2*j)/2
        outl.append(out)
    outl=np.array(outl)
    return outl

def OMNIread(f):

    BErr='9999.99'			# err of B field
    VErr='99999.9'			# err of Velocity
    NErr='999.99'				# err of Number density

    time,Bx,By,Bz,V,n,Pd,Ma=[],[],[],[],[],[],[],[]
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
            V.append(float(w[7]))
            n.append(float(w[8]))
            Pd.append(float(w[9]))
            Ma.append(float(w[10]))
    Bx=np.array(Bx)
    By=np.array(By)
    Bz=np.array(Bz)
    V=np.array(V)
    n=np.array(n)
    Pd=np.array(Pd)
    Ma=np.array(Ma)
    B_sw=np.sqrt(Bx**2+By**2+Bz**2)
    omni=pd.DataFrame({'datetime':time,'Bx':Bx,'By':By,'Bz':Bz,'V':V,'n':n,'Pd':Pd,'Ma':Ma,'B':B_sw})
    return omni

def SSCread(f):
    dateparse=lambda x,y: pd.datetime.strptime(x+' '+y,'%y/%m/%d %H:%M:%S')
    sat=pd.read_csv(f,header=None,sep='\s+',parse_dates={'datetime':[0,1]},date_parser=dateparse)
    sat.datetime=pd.to_datetime(sat.datetime)
    return sat

def main():
#    al=[]
    Bxfl=[]
    Byfl=[]
    Bzfl=[]
    nfl=[]
    Tfl=[]
    Vxfl=[]
    Vyfl=[]
    Vzfl=[]
    for i in range(1,7):
        a=pd.read_csv('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_data_0.1.'+str(1200+1200*i).zfill(6),header=None,sep='\s+',
        names=['the','phi','m','rad','x','y','z','bx1','by1','bz1','vx1','vy1','vz1','rr1','pp1','ex1','ey1','ez1','xjx1','xjy1','xjz1','resis1']).drop_duplicates()
        a['T1']=72429*a.pp1/a.rr1/11600
        a['f']=a.m/10
        Bxf=LNDI((a.the,a.phi,a.f),a.bx1.values)
        Byf=LNDI((a.the,a.phi,a.f),a.by1.values)
        Bzf=LNDI((a.the,a.phi,a.f),a.bz1.values)
        nf=LNDI((a.the,a.phi,a.f),a.rr1.values)
        Tf=LNDI((a.the,a.phi,a.f),a.T1.values)
        Vxf=LNDI((a.the,a.phi,a.f),a.vx1.values)
        Vyf=LNDI((a.the,a.phi,a.f),a.vy1.values)
        Vzf=LNDI((a.the,a.phi,a.f),a.vz1.values)
        Bxfl.append(Bxf)
        Byfl.append(Byf)
        Bzfl.append(Bzf)
        nfl.append(nf)
        Tfl.append(Tf)
        Vxfl.append(Vxf)
        Vyfl.append(Vyf)
        Vzfl.append(Vzf)
        print(i,'/6 Constructing functions from OpenGGCM data')

    #For LNDI:
    np.save('/Volumnes/easystore/opengggcm_run/Msh_Nstep/Bxfl',Bxfl)
    np.save('/Volumnes/easystore/opengggcm_run/Msh_Nstep/Byfl',Byfl)
    np.save('/Volumnes/easystore/opengggcm_run/Msh_Nstep/Bzfl',Bzfl)
    np.save('/Volumnes/easystore/opengggcm_run/Msh_Nstep/nfl',nfl)
    np.save('/Volumnes/easystore/opengggcm_run/Msh_Nstep/Tfl',Tfl)
    np.save('/Volumnes/easystore/opengggcm_run/Msh_Nstep/Vxfl',Vxfl)
    np.save('/Volumnes/easystore/opengggcm_run/Msh_Nstep/Vyfl',Vyfl)
    np.save('/Volumnes/easystore/opengggcm_run/Msh_Nstep/Vzfl',Vzfl)
    #f2=np.load('test.npy')
    #f2[0](x)



#    return pts_df
    return


if __name__=="__main__":
    main()
