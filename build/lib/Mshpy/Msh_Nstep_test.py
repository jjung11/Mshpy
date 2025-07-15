import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv
from sympy.solvers import solve
from sympy import Symbol,nsolve
from sympy import sqrt,log,tanh
from scipy.interpolate import NearestNDInterpolator as NNDI
from scipy.interpolate import LinearNDInterpolator as LNDI
from scipy.interpolate import RegularGridInterpolator as RGI
from scipy.spatial.transform import Rotation as R
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

def appendSpherical_np(xyz):
    ptsnew = np.hstack((xyz,np.empty(xyz.shape)))
    xy = xyz[:,0]**2 + xyz[:,1]**2
    ptsnew[:,3] = np.sqrt(xy + xyz[:,2]**2)
    #ptsnew[:,4] = np.arctan2(np.sqrt(xy), xyz[:,2]) # for elevation angle defined from Z-axis down
    ptsnew[:,4] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    ptsnew[:,5] = np.arctan2(xyz[:,1], xyz[:,0])
    return ptsnew

def bsdf(N,V,Ma,B,xl,yl,zl):
    D=0.937*(0.846+0.042*B)
    f=91.55/(N*V**2)**(1/6)*(1+D*((5/3-1)*Ma**2+2)/((5/3+1)*(Ma**2-1)))/R0
    t=Symbol('t',positive="True")
    x=xl*t
    y=yl*t
    z=zl*t
    sol=solve(a11*(x/f)**2+a22*(y/f)**2+a33*(z/f)**2+a12*(x/f)*(y/f)+a14*(x/f)+a24*(y/f)+a34*(z/f)+a44,t)
    dist=np.linalg.norm([np.array((xl*sole,yl*sole,zl*sole),dtype=np.float32) for sole in sol])
    return dist

def bsdf2(N,V,Ma,B,xl,yl,zl):
    D=0.937*(0.846+0.042*B)
    f=91.55/(N*V**2)**(1/6)*(1+D*((5/3-1)*Ma**2+2)/((5/3+1)*(Ma**2-1)))/R0
    t=0
    sol0=a44
    sol=sol0
    while sol*sol0>0:
        t+=0.001
        x=xl*t
        y=yl*t
        z=zl*t
        sol=a11*(x/f)**2+a22*(y/f)**2+a33*(z/f)**2+a12*(x/f)*(y/f)+a14*(x/f)+a24*(y/f)+a34*(z/f)+a44
#        print(sol)
    dist=np.linalg.norm(np.array([xl*t,yl*t,zl*t]))
    return dist


def mpdf(Pd,Bz,xyz):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    r0=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    alpha=(0.58-0.007*Bz)*(1+0.024*np.log(Pd))
    R = r0*(2/(1+np.cos(theta)))**alpha
    return R

def OMNIreadnan(f):

    BErr='9999.99'          # err of B field
    VErr='99999.9'          # err of Velocity
    NErr='999.99'               # err of Number density

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
        else:
            time.append(datetime.datetime(int(w[0]),1,1)+datetime.timedelta(days=int(w[1])-1,hours=int(w[2]),minutes=int(w[3])))
            Bx.append(np.nan)
            By.append(np.nan)
            Bz.append(np.nan)
            V.append(np.nan)
            n.append(np.nan)
            Pd.append(np.nan)
            Ma.append(np.nan)
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

def WINDread(f):

    BErr='9999.99'          # err of B field
    VErr='99999.9'          # err of Velocity
    NErr='999.99'               # err of Number density

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
    Bx=np.array(Bx)
    By=np.array(By)
    Bz=np.array(Bz)
    V=np.array(V)
    n=np.array(n)
    Pd=2e-6*n*V**2
    B_sw=np.sqrt(Bx**2+By**2+Bz**2)
    Ma=20*B_sw/np.sqrt(n)
    omni=pd.DataFrame({'datetime':time,'Bx':Bx,'By':By,'Bz':Bz,'V':V,'n':n,'Pd':Pd,'Ma':Ma,'B':B_sw})
    return omni

def SSCread(f):
    dateparse=lambda x,y: pd.datetime.strptime(x+' '+y,'%y/%m/%d %H:%M:%S')
    sat=pd.read_csv(f,header=None,sep='\s+',names=['d','t','x','y','z'],parse_dates={'datetime':[0,1]},date_parser=dateparse)
    sat.datetime=pd.to_datetime(sat.datetime)
    return sat

def genf(fun,nxyz,f,f2):
    outl=[]
    for i,j,k in zip(nxyz,f,f2):
        if i[2][2]<0.1 or i[2][2]>0.9:
            out=np.nan
        else:
            if k==-1:
                out1=fun[i[0]+6](i[2])[0]
                out2=fun[i[1]+6](i[2])[0]
                out=(out1*(1-j)+out2*j)
            elif k==2:
                out1=fun[i[0]](i[2])[0]
                out2=fun[i[1]](i[2])[0]
                out=(out1*(1-j)+out2*j)
            else:
                out1=fun[i[0]](i[2])[0]
                out2=fun[i[1]](i[2])[0]
                out=(out1*(1-j)+out2*j)
                out1=fun[i[0]+6](i[2])[0]
                out2=fun[i[1]+6](i[2])[0]
                outs=(out1*(1-j)+out2*j)
                out=k*out+(1-k)*outs
        outl.append(out)
    outl=np.array(outl)
    return outl

def genf_n(fun,nxyz,f,f2):
    outl=[]
    for i,j,k in zip(nxyz,f,f2):
        if i[2][2]<0 or i[2][2]>1:
            out=np.nan
        else:
            if k==-1:
                out1=fun[i[0]+6](i[2])[0]
                out2=fun[i[1]+6](i[2])[0]
                if (i[0]==0 & i[1]==0) or (i[0]==6 & i[1]==6):out1=0
                out=(out1*(1-j)+out2*j)
            elif k==2:
                out1=fun[i[0]](i[2])[0]
                out2=fun[i[1]](i[2])[0]
                if (i[0]==0 & i[1]==0) or (i[0]==6 & i[1]==6):out1=0
                out=(out1*(1-j)+out2*j)
            else:
                out1=fun[i[0]](i[2])[0]
                out2=fun[i[1]](i[2])[0]
                if (i[0]==0 & i[1]==0) or (i[0]==6 & i[1]==6):out1=0
                outn=(out1*(1-j)+out2*j)
                out1=fun[i[0]+6](i[2])[0]
                out2=fun[i[1]+6](i[2])[0]
                if (i[0]==0 & i[1]==0) or (i[0]==6 & i[1]==6):out1=0
                outs=(out1*(1-j)+out2*j)
                out=k*outn+(1-k)*outs
        outl.append(out)
    outl=np.array(outl)
    return outl

def genf_test(fun,nxyz,f,f2):
    outl=[]
    for i,j,k in zip(nxyz,f,f2):
        if i[2][2]<0 or i[2][2]>1:
            out=np.nan
        else:
            if k==-1:
                out1=fun[i[0]+6](i[2])[0]
                out2=fun[i[1]+6](i[2])[0]
                out=(out1*(1-j)+out2*j)
            elif k==2:
                out1=fun[i[0]](i[2])[0]
                out2=fun[i[1]](i[2])[0]
                out=(out1*(1-j)+out2*j)
            else:
                out1=fun[i[0]](i[2])[0]
                out2=fun[i[1]](i[2])[0]
                out=(out1*(1-j)+out2*j)
                print(out1,out2,j,out)
                out1=fun[i[0]+6](i[2])[0]
                out2=fun[i[1]+6](i[2])[0]
                outs=(out1*(1-j)+out2*j)
                out=k*out+(1-k)*outs
        outl.append(out)
    outl=np.array(outl)
    return outl

def main(xyz,f_sw,fout,mpdo=0,bsdo=0,offsetf=0):
    mpdo=float(mpdo)
    bsdo=float(bsdo)
    if offsetf!=0:
        with open(offsetf,'w') as file:
            #print(offsetf)
            file.write(f'{mpdo} {bsdo}')



    if type(xyz)==str:
        xyz=SSCread(xyz)
        if (xyz.x<0).any():
            print('Warning: there is at least one time at which satellite was on nightside, which isn\'t supported by current version of model.')
            #print(xyz.x.max())

    omni=OMNIread2(f_sw)
    if len(omni)==1:
        omni=pd.concat([omni]*np.shape(xyz)[0])

    if type(xyz)!=np.ndarray:
        test=xyz.merge(omni,how='outer')[['datetime','x','y','z']].sort_values(by=['datetime']).set_index('datetime').interpolate('index')
        omni=omni.set_index('datetime').join(test,how='left')
        xyz_np=omni[['x','y','z']].to_numpy()
    else:
        xyz_np=xyz

    r=R.from_euler('z',-4,degrees=True)
    xyz_np=(r.as_matrix()@xyz_np.T).T

    print('Finding MP nodes')
    mpd=np.array(mpdf(omni.Pd,omni.Bz,xyz_np))
#    bsd=np.array([bsdf(omni.n[i],v_sw[i],Ma[i],B_sw[i],xyz[i])for i in range(np.shape(xyz)[0])])
    mpd+=mpdo

    print('Finding BS nodes')
    bsdfv=np.vectorize(bsdf2)
    bsd=np.array(bsdfv(omni.n,omni.V,omni.Ma,omni.B,xyz_np[:,0],xyz_np[:,1],xyz_np[:,2]))
    print(np.shape(mpd),np.shape(bsd))
    bsd+=bsdo

    pts=appendSpherical_np(xyz_np)
    print('theta range',np.nanmin(pts[:,4])*180/np.pi,np.nanmax(pts[:,4])*180/np.pi)
    print('phi range',np.nanmin(pts[:,5]*180/np.pi),np.nanmax(pts[:,5])*180/np.pi)

    f_msh=(pts[:,3]-mpd)/(bsd-mpd)
#    print(type(pts),type(f_msh))
    pts=np.hstack((pts,f_msh.reshape(pts.shape[0],1)))
    #print(pts)

    pts_df=pd.DataFrame(pts, columns=['x','y','z','r','theta','phi','f'])
    input=pts_df[['theta','phi','f']].to_numpy()

#    if (omni.n>35).any(): print('Warning: there are at least one time at which solar wind density goes above 35cm^-3, in which our model was not validated')
    if (omni.n>35).any(): print('Warning: there is at least one time at which solar wind density goes above 35cm^-3, in which our model was not validated')
    if (omni.B>15).any(): print('Warning: there is at least one time at which IMF magnitude goes above 15cm^-3, in which our model shows discrepancy with THEMIS data')
    conditions=[omni.n<=5,(5<omni.n) & (omni.n<10),(10<=omni.n) & (omni.n<15),(15<=omni.n) & (omni.n<20),(20<=omni.n) & (omni.n<25),(25<=omni.n) & (omni.n<30),(30<=omni.n) & (omni.n<35)]
    choices1=[0,0,1,2,3,4,5]
    choices2=[0,1,2,3,4,5,5]
    n1=np.select(conditions,choices1)
    n2=np.select(conditions,choices2)
    f=omni.n/5-(n1+1)  #factor for fine tuning of SW density
    f[f<0]+=1
    conditions2=[omni.Bz<=-4,(-4<omni.Bz) & (omni.Bz<4), 4<omni.Bz]
    choices3=[-1,(omni.Bz+4)/8,2]
    f2=np.select(conditions2,choices3) #factor for fine tuning of IMF
    inputn=list(zip(n1,n2,input))
    #print(inputn)

#    al=[]
    Bxfl=[]
    Byfl=[]
    Bzfl=[]
    nfl=[]
    Tfl=[]
    Vxfl=[]
    Vyfl=[]
    Vzfl=[]
    the=np.arange(-90,91,1)*np.pi/180
    phi=np.arange(-90,91,1)*np.pi/180
    af=np.arange(0,11,1)/10

    print('Mean Bz=',omni.Bz.mean())

    external='easystore'
    run='Msh_Nstep'

    for i in range(1,7):
        bx1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Bx_%d.npy'%i)
        by1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_By_%d.npy'%i)
        bz1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Bz_%d.npy'%i)
        rr1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_n_%d.npy'%i)
        pp1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_pp_%d.npy'%i)
        T1=72429*pp1/rr1/11600
        vx1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vx_%d.npy'%i)
        vy1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vy_%d.npy'%i)
        vz1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vz_%d.npy'%i)

        Bxf=RGI((the,phi,af),bx1,bounds_error=False)
        Byf=RGI((the,phi,af),by1,bounds_error=False)
        Bzf=RGI((the,phi,af),bz1,bounds_error=False)
        nf=RGI((the,phi,af),rr1,bounds_error=False)
        Tf=RGI((the,phi,af),T1,bounds_error=False)
        Vxf=RGI((the,phi,af),vx1,bounds_error=False)
        Vyf=RGI((the,phi,af),vy1,bounds_error=False)
        Vzf=RGI((the,phi,af),vz1,bounds_error=False)
        Bxfl.append(Bxf)
        Byfl.append(Byf)
        Bzfl.append(Bzf)
        nfl.append(nf)
        Tfl.append(Tf)
        Vxfl.append(Vxf)
        Vyfl.append(Vyf)
        Vzfl.append(Vzf)

    external='Elements'
    run='Msh_Nstep_cs'

    for i in range(1,7):
        bx1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Bx_%d.npy'%i)
        by1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_By_%d.npy'%i)
        bz1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Bz_%d.npy'%i)
        rr1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_n_%d.npy'%i)
        pp1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_pp_%d.npy'%i)
        T1=72429*pp1/rr1/11600
        vx1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vx_%d.npy'%i)
        vy1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vy_%d.npy'%i)
        vz1=np.load('/Volumes/'+external+'/openggcm_run/'+run+'/modeling/Msh_Vz_%d.npy'%i)

        Bxf=RGI((the,phi,af),bx1,bounds_error=False)
        Byf=RGI((the,phi,af),by1,bounds_error=False)
        Bzf=RGI((the,phi,af),bz1,bounds_error=False)
        nf=RGI((the,phi,af),rr1,bounds_error=False)
        Tf=RGI((the,phi,af),T1,bounds_error=False)
        Vxf=RGI((the,phi,af),vx1,bounds_error=False)
        Vyf=RGI((the,phi,af),vy1,bounds_error=False)
        Vzf=RGI((the,phi,af),vz1,bounds_error=False)
        Bxfl.append(Bxf)
        Byfl.append(Byf)
        Bzfl.append(Bzf)
        nfl.append(nf)
        Tfl.append(Tf)
        Vxfl.append(Vxf)
        Vyfl.append(Vyf)
        Vzfl.append(Vzf)

#        print(i,'/6 Constructing functions from OpenGGCM data')

#    test=Bxfl[0](input[0])
#    print(input[0],test)
#    np.shape(test)


    Bx=genf(Bxfl,inputn,f,f2)
    By=genf(Byfl,inputn,f,f2)
    Bz=genf(Bzfl,inputn,f,f2)
    n=genf(nfl,inputn,f,f2)
    T=genf(Tfl,inputn,f,f2)
    Vx=genf(Vxfl,inputn,f,f2)
    Vy=genf(Vyfl,inputn,f,f2)
    Vz=genf(Vzfl,inputn,f,f2)
    V_0=np.vstack([Vx,Vy,Vz]).T
    V=(r.as_matrix().T@V_0.T).T

    print(len(omni),len(f))
    out=pd.DataFrame({'time':omni.index,'Bx':Bx,'By':By,'Bz':Bz,'n':n,'Tev':T,'Vx':V[:,0],'Vy':V[:,1],'Vz':V[:,2],'f':pts_df.f})
    out.to_csv(fout,float_format='%.3f',index=False)



#    return pts_df
    return Bx,By,Bz,n,T,Vx,Vy,Vz


if __name__=="__main__":
    f_sw="SW_cond_test.txt"
    test=open(f_sw,"w")
    test.write("2003 124 12 30    1.01   -1.65   -0.78  -414.8   -21.8     0.7   7.54  2.60  24.3  7.7\n")
    #Year DOY HR MN Bx By Bz Vx Vy Vz n Pd Ma Mm, as in OMNIweb
    test.close()

    #f_sw='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/omni.lst'
    xyz=np.array([[12,2,3],[10,2,3]])
    #Orbit data from the SSWweb can be used as xyz. (filepath)
    #Data would be interpolated based on OMNI time.
    #xyz='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/cl_orbit.txt'
    fout='Msh_test_out.txt'
    #fout='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Msh_test_out.txt'
    main(xyz,f_sw,fout)
