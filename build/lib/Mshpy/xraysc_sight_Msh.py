#!/Users/jjung11/anaconda3/bin/python
# Calculate input for plot_rates.py
# Written by J.Jung


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from sympy.solvers import solve
from sympy import Symbol,nsolve
from sympy import sqrt,log,tanh
from scipy.interpolate import NearestNDInterpolator as NNDI
from scipy.interpolate import LinearNDInterpolator as LNDI
from scipy.interpolate import RegularGridInterpolator as RGI
from scipy.spatial.transform import Rotation as R
import glob
import datetime

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

def bsdf(D,f,pts):

    sol0=a44
    bsd=[]
#    print(pts[4])
    dx=0.1*np.cos(pts[:,4])*np.cos(pts[:,5])
    dy=0.1*np.cos(pts[:,4])*np.sin(pts[:,5])
    dz=0.1*np.sin(pts[:,4])

    for dxi,dyi,dzi in zip(dx,dy,dz):
        sol=sol0
#        print(sol,sol0)
        x=100*dxi
        y=100*dyi
        z=100*dzi
        while sol*sol0>0:
            x+=dxi
            y+=dyi
            z+=dzi
            sol=a11*(x/f)**2+a22*(y/f)**2+a33*(z/f)**2+a12*(x/f)*(y/f)+a14*(x/f)+a24*(y/f)+a34*(z/f)+a44
            #print(sol)
        dist=np.sqrt(x**2+y**2+z**2)
    bsd.append(dist)
    return bsd

def bsdf_Jelinek(a_14,a_44,xyz):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    cos=np.cos(theta)
    sin=np.sin(theta)
    r=(-a_14*cos+np.sqrt(a_14**2*cos**2-4*a_44*sin**2))/(2*sin**2)
    r0=-a_44/a_14
    r[np.logical_or(np.isnan(r),r<1e-10)]=r0
    return r



def mpdf(r0,alpha,xyz):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    R = r0[0]*(2/(1+np.cos(theta)))**alpha[0]
    return R

def genf(fun,n1,n2,xyz,f,f2):
    outl=[]
    for i in xyz:
        if i[2]<0.1 or i[2]>0.9:
            out=np.nan
        else:
            if f2==-1:
                out1=fun[n1+7](i)[0]
                out2=fun[n2+7](i)[0]
                out=(out1*(1-f)+out2*f)
            elif f2==2:
                out1=fun[n1](i)[0]
                out2=fun[n2](i)[0]
                out=(out1*(1-f)+out2*f)
            else:
                out1=fun[n1](i)[0]
                out2=fun[n2](i)[0]
                out=(out1*(1-f)+out2*f)
                out1=fun[n1+7](i)[0]
                out2=fun[n2+7](i)[0]
                outs=(out1*(1-f)+out2*f)
                out=f2*out+(1-f2)*outs
        outl.append(out)
    outl=np.array(outl)
    return outl

nfl=[]
Tfl=[]
Vxfl=[]
Vyfl=[]
Vzfl=[]
the=np.arange(-90,91,1)*np.pi/180
phi=np.arange(-90,91,1)*np.pi/180
af=np.arange(0,11,1)/10

def OMNIread2(f):

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

def appendSpherical_np(xyz):
    ptsnew = np.hstack((xyz,np.empty(xyz.shape)))
    xy = xyz[:,0]**2 + xyz[:,1]**2
    ptsnew[:,3] = np.sqrt(xy + xyz[:,2]**2)
    #ptsnew[:,4] = np.arctan2(np.sqrt(xy), xyz[:,2]) # for elevation angle defined from Z-axis down
    ptsnew[:,4] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    ptsnew[:,5] = np.arctan2(xyz[:,1], xyz[:,0])
    return ptsnew

path=sys.argv[2]
xsc=float(sys.argv[4])
ysc=float(sys.argv[6])
zsc=float(sys.argv[8])
xlk=float(sys.argv[10])
ylk=float(sys.argv[12])
zlk=float(sys.argv[14])
the1=float(sys.argv[16])
the2=float(sys.argv[18])
dthe=float(sys.argv[20])
phi1=float(sys.argv[22])
phi2=float(sys.argv[24])
dphi=float(sys.argv[26])
fout=sys.argv[28]
model=sys.argv[30]
print(path,xsc,ysc,zsc,xlk,ylk,zlk,the1,the2,dthe,phi1,phi2,dphi,fout)

for i in range(0,7):
    rr1=np.load(path+'/cn/Msh_n_%d.npy'%i)
    pp1=np.load(path+'/cn/Msh_pp_%d.npy'%i)
    T1=72429*pp1/rr1/11600
    vx1=np.load(path+'/cn/Msh_Vx_%d.npy'%i)
    vy1=np.load(path+'/cn/Msh_Vy_%d.npy'%i)
    vz1=np.load(path+'/cn/Msh_Vz_%d.npy'%i)

    nf=RGI((the,phi,af),rr1,bounds_error=False)
    Tf=RGI((the,phi,af),T1,bounds_error=False)
    Vxf=RGI((the,phi,af),vx1,bounds_error=False)
    Vyf=RGI((the,phi,af),vy1,bounds_error=False)
    Vzf=RGI((the,phi,af),vz1,bounds_error=False)
    nfl.append(nf)
    Tfl.append(Tf)
    Vxfl.append(Vxf)
    Vyfl.append(Vyf)
    Vzfl.append(Vzf)

for i in range(0,7):
    rr1=np.load(path+'/cs/Msh_n_%d.npy'%i)
    pp1=np.load(path+'/cs/Msh_pp_%d.npy'%i)
    T1=72429*pp1/rr1/11600
    vx1=np.load(path+'/cs/Msh_Vx_%d.npy'%i)
    vy1=np.load(path+'/cs/Msh_Vy_%d.npy'%i)
    vz1=np.load(path+'/cs/Msh_Vz_%d.npy'%i)

    nf=RGI((the,phi,af),rr1,bounds_error=False)
    Tf=RGI((the,phi,af),T1,bounds_error=False)
    Vxf=RGI((the,phi,af),vx1,bounds_error=False)
    Vyf=RGI((the,phi,af),vy1,bounds_error=False)
    Vzf=RGI((the,phi,af),vz1,bounds_error=False)
    nfl.append(nf)
    Tfl.append(Tf)
    Vxfl.append(Vxf)
    Vyfl.append(Vyf)
    Vzfl.append(Vzf)



nh0=25
drad=0.2*6372*1e3
ri=2.1
str1=4*np.pi
crs=6e-16



distance=np.sqrt((xsc-xlk)**2+(ysc-ylk)**2+(zsc-zlk)**2)
p=np.arctan2(ysc-ylk,xsc-xlk)
t=np.arccos((zsc-zlk)/distance)
print(distance,p*180/np.pi,t*180/np.pi)

f_sw="SW_cond_test.txt"
#test=open(f_sw,"w")
#test.write("1967 1 0 00 0 0 5 -400 0 0 10 2 10 6\n")
#Year DOY HR MN Bx By Bz Vx Vy Vz n Pd Ma Mm, as in OMNIweb
#test.close()
omni=OMNIread2(f_sw)
D=0.937*(0.846+0.042*omni.B)
f=(91.55/(omni.n*omni.V**2)**(1/6)*(1+D*((5/3-1)*omni.Ma**2+2)/((5/3+1)*(omni.Ma**2-1)))/R0)[0]
r0=(10.22+1.29*np.tanh(0.184*(omni.Bz+8.14)))*omni.Pd**(-1/6.6)
alpha=(0.58-0.007*omni.Bz)*(1+0.024*np.log(omni.Pd))
mp0=mpdf(r0,alpha,np.array([[1,0,0]]))
bs0=bsdf(D,f,np.array([[0,0,0,1,0,0]]))
print('Shue/Jerab',mp0,bs0)
R_0=15.02
lam=1.17
epsilon=6.55
a_14=(4*R_0/lam**2*omni.Pd**(-1/epsilon))[0]
a_44=(-1/4*lam**2*a_14**2)
bs0_j=bsdf_Jelinek(a_14,a_44,np.array([[1,0,0]]))
print('a_14,a_44',a_14,a_44)
print('Shue/Jelinek',mp0,bs0_j)


#bsdfv=np.vectorize(bsdf)
if (omni.n>35).any():print('Warning: Solar wind density goes above 35cm^-3, in which our model was not validated.')
if (omni.B>15).any():print('Warning: IMF magnitude goes above 15cm^-3, in which our model shows discrepancy with THEMIS data.')

conditions=[omni.n<=1,(1<omni.n) & (omni.n<=5),(5<omni.n) & (omni.n<10),(10<=omni.n) & (omni.n<15),(15<=omni.n) & (omni.n<20),(20<=omni.n) & (omni.n<25),(25<=omni.n) & (omni.n<30),(30<=omni.n) & (omni.n<35)]
choices1=[0,0,1,2,3,4,5,6]
choices2=[0,1,2,3,4,5,6,6]
n1=np.select(conditions,choices1)[0]
n2=np.select(conditions,choices2)[0]
f1=np.where(n2==1,(omni.n-1)/4,omni.n/5-n1)[0]
conditions2=[omni.Bz<=-4,(-4<omni.Bz) & (omni.Bz<4), 4<=omni.Bz]
choices3=[-1,(omni.Bz+4)/8,2]
f2=np.select(conditions2,choices3)[0]
print('f1,f2',f1,f2)


fo=open(fout,'w+')
#fout2='test.txt'
#fo2=open(fout2,'w+')
fo.write('%d %d %f %f %f %f %f %f\n' % (((phi2-phi1)/dphi+1),((the2-the1)/dthe+1),xsc,ysc,zsc,xlk,ylk,zlk))
thel=np.arange(the1,the2+dthe,dthe)
phil=np.arange(phi1,phi2+dphi,dphi)
for i,the in enumerate(thel):
    lat=90-the
    the_r=the*np.pi/180
    for j,phi in enumerate(phil):
        phi_r=phi*np.pi/180
        rate=0
        los=[]
        for r in np.arange(0,100+0.2,0.2):
            x1=r*np.sin(the_r)*np.cos(phi_r)
            y1=r*np.sin(the_r)*np.sin(phi_r)
            z1=r*np.cos(the_r)
            x2=x1*np.sin(t)*np.cos(p)-y1*np.sin(p)-z1*np.cos(t)*np.cos(p)
            y2=x1*np.sin(t)*np.sin(p)+y1*np.cos(p)-z1*np.cos(t)*np.sin(p)
            z2=x1*np.cos(t)+z1*np.sin(t)
            x=xsc+x2
            y=ysc+y2
            z=zsc+z2
            ro=np.sqrt(x**2+y**2+z**2)
            phio=np.arctan2(x,y)
            theo=np.arccos(z/np.sqrt(x**2+y**2+z**2))
#            print( ["{0:0.2f}".format(i) for i in [x,y,z]])
            if ro<ri:
                rate=9999
#                print(x,y,z)
                break
            los.append(np.array([x,y,z,ro]))
        los=np.array(los)
#        omni=pd.concat([omni]*np.shape(xyz)[0])

        rm=R.from_euler('z',-4,degrees=True)
        xyz_np=(rm.as_matrix()@los[:,:-1].T).T
#        xyz_np=los[:,:-1]

#        print('Finding MP nodes')
        mpd=np.array(mpdf(r0,alpha,xyz_np))

 #       print('Finding BS nodes')
        #print(xyz_np)
        pts=appendSpherical_np(xyz_np)
        if model!='jer':
            bsd=np.array(bsdf_Jelinek(a_14,a_44,xyz_np))
        else:
            bsd=np.array(bsdf(D,f,pts))

        f_msh=(pts[:,3]-mpd)/(bsd-mpd)
        pts=np.hstack((pts,f_msh.reshape(pts.shape[0],1)))
    #    print(f_msh)

        input=pts[:,4:]
#        print(np.shape(input))

        #print(phi,np.shape(nfl),np.shape(n1),np.shape(n2),np.shape(input),np.shape(f),np.shape(f2))
        n=genf(nfl,n1,n2,input,f1,f2)
        T=genf(Tfl,n1,n2,input,f1,f2)
        Vx=genf(Vxfl,n1,n2,input,f1,f2)
        Vy=genf(Vyfl,n1,n2,input,f1,f2)
        Vz=genf(Vzfl,n1,n2,input,f1,f2)
#        V_0=np.vstack([Vx,Vy,Vz]).T
#        V=(rm.as_matrix().T@V_0.T).T
        vth=np.sqrt(3*1.38e-23*(T*11600)/1.6727e-27)*100
        vbu=np.sqrt(Vx**2+Vy**2+Vz**2)*1e5
        vrel=np.sqrt(vth**2+vbu**2)
        nn=nh0*(10./los[:,-1])**3
        xray=n*vrel*nn*drad*100*crs #eV/cm^3/s
        rate=np.nansum(xray/str1) #cV/cm^2/s/sr
#        np.set_printoptions(precision=3,suppress=True,threshold=sys.maxsize,linewidth=150)
#        print(np.shape(xyz_np[:,1]),np.shape(n),np.shape(vrel),np.shape(nn),np.shape(xray))
        sh=np.shape(xyz_np)[0]

    #    index=~np.isnan(n)
    #    print(len(index))

    #    test=np.hstack((pts[:,0:4],f_msh.reshape(sh,1),n.reshape(sh,1),vrel.reshape(sh,1),nn.reshape(sh,1),xray.reshape(sh,1),mpd.reshape(sh,1),bsd.reshape(sh,1)))
        #print(test[index])
#        fo2.write(str(test[index]))
#        fo2.write('\n\n')
    #    np.savetxt('test.txt',test[index],fmt='%.3f')
    #    np.savetxt('test_0.txt',test,fmt='%.3f')

        fo.write('%d %d %f %f %f %e\n' % (j,i,r,phi,lat,rate))
#        print(phi,lat,rate)
    print(lat,'/',90-the2)
fo.close()
#fo2.close()
