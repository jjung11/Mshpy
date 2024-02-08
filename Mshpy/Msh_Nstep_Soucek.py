import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import datetime
from scipy.spatial.transform import Rotation as R

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

R_0=15.02
lam=1.17
epsilon=6.55

def appendSpherical_np(xyz):
    ptsnew = np.hstack((xyz,np.empty(xyz.shape)))
    xy = xyz[:,0]**2 + xyz[:,1]**2
    ptsnew[:,3] = np.sqrt(xy + xyz[:,2]**2)
    #ptsnew[:,4] = np.arctan2(np.sqrt(xy), xyz[:,2]) # for elevation angle defined from Z-axis down
    ptsnew[:,4] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    ptsnew[:,5] = np.arctan2(xyz[:,1], xyz[:,0])
    return ptsnew

def mpdf(Pd,Bz,xyz):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    r0=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    alpha=(0.58-0.007*Bz)*(1+0.024*np.log(Pd))
    R = r0*(2/(1+np.cos(theta)))**alpha
    return R

def BSf_Farris(Pd,Bz,Mm,xyz):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    R_mp=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    R_bs=(1+1.1/4*(Mm**2+3)/Mm**2)*R_mp
    b=0.0223*(Pd/1.8)**(1/6)
    r_bs=(-np.cos(theta)+np.sqrt(np.cos(theta)**2+4*R_bs*b*np.sin(theta)**2))/(2*b*np.sin(theta)**2)
    return r_bs

def BSf_Farris_Jerab(Pd,N,V,B,Ma,xyz):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    D=0.937*(0.846+0.042*B)
    R_bs=91.55/(N*V**2)**(1/6)*(1+D*((5/3-1)*Ma**2+2)/((5/3+1)*(Ma**2-1)))

    b=0.0223*(Pd/1.8)**(1/6)
    r_bs=(-np.cos(theta)+np.sqrt(np.cos(theta)**2+4*R_bs*b*np.sin(theta)**2))/(2*b*np.sin(theta)**2)
    return r_bs

def bsdf_Jelinek(Pd,xyz):

    a_14=(4*R_0/lam**2*Pd**(-1/epsilon))
    a_44=(-1/4*lam**2*a_14**2)
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    cos=np.cos(theta)
    sin=np.sin(theta)
    r=np.array((-a_14*cos+np.sqrt(a_14**2*cos**2-4*a_44*sin**2))/(2*sin**2))
    r0=-a_44/a_14
    r[np.isnan(r)]=r0[np.isnan(r)]
    return r

def KF94R(Pd,Bz,N,V,B,Ma,xyz,f_msh):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    phi=np.arctan2(xyz[:,2],xyz[:,1])

    R_mp=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    D=0.937*(0.846+0.042*B)
    R_bs=91.55/(N*V**2)**(1/6)*(1+D*((5/3-1)*Ma**2+2)/((5/3+1)*(Ma**2-1)))
    b=0.0223*(Pd/1.8)**(1/6)
    b_mp=b/(1+4*b*(R_mp-R_bs))

    r_mp=(-np.cos(theta)+np.sqrt(np.cos(theta)**2+4*R_mp*b_mp*np.sin(theta)**2))/(2*b_mp*np.sin(theta)**2)
    r_bs=(-np.cos(theta)+np.sqrt(np.cos(theta)**2+4*R_bs*b*np.sin(theta)**2))/(2*b*np.sin(theta)**2)
    print('R_mp & R_bs at the first data point:',r_mp.iloc[0],r_bs.iloc[0])

    r_KF=r_mp+f_msh*(r_bs-r_mp)
    #print(r_KF)
    xyz_KF=np.array([r_KF*np.cos(theta),r_KF*np.sin(theta)*np.cos(phi),r_KF*np.sin(theta)*np.sin(phi)]).T
    return xyz_KF

def KF94R_R(Pd,Bz,N,V,B,Ma,xyz_kf):
    #print(xyz_kf)
    yz=xyz_kf[:,1]**2+xyz_kf[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz_kf[:,0])
    phi=np.arctan2(xyz_kf[:,2],xyz_kf[:,1])
    r_kf=np.sqrt(yz+xyz_kf[:,0]**2)
    R_mp=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    alpha=(0.58-0.007*Bz)*(1+0.024*np.log(Pd))
    #print(xyz_kf,R_mp,theta,alpha)
    r_mp=R_mp*(2/(1+np.cos(theta)))**alpha
    D=0.937*(0.846+0.042*B)
    R_bs=91.55/(N*V**2)**(1/6)*(1+D*((5/3-1)*Ma**2+2)/((5/3+1)*(Ma**2-1)))
    b=0.0223*(Pd/1.8)**(1/6)
    b_mp=b/(1+4*b*(R_mp-R_bs))


    r_mp_kf=(-np.cos(theta)+np.sqrt(np.cos(theta)**2+4*R_mp*b_mp*np.sin(theta)**2))/(2*b_mp*np.sin(theta)**2)
    r_bs=(-np.cos(theta)+np.sqrt(np.cos(theta)**2+4*R_bs*b*np.sin(theta)**2))/(2*b*np.sin(theta)**2)

#    print(r_kf,r_mp_kf,r_bs)
    f_kf=(r_kf-r_mp_kf)/(r_bs-r_mp_kf)
    #print(f_kf)

    r=r_mp+f_kf*(r_bs-r_mp)
    xyz=np.array([r*np.cos(theta),r*np.sin(theta)*np.cos(phi),r*np.sin(theta)*np.sin(phi)]).T
#    print('KF and GSE',xyz_kf,xyz)
    return xyz



def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

def backtrack(Pd,Bz,N,B,Ma,v_x,v_y,v_z,xyz,f_msh):
    V=np.sqrt(v_x**2+v_y**2+v_z**2)
    R_mp=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    D=0.937*(0.846+0.042*B)
    R_bs=91.55/(N*V**2)**(1/6)*(1+D*((5/3-1)*Ma**2+2)/((5/3+1)*(Ma**2-1)))
    bl=0.0223*(Pd/1.8)**(1/6)
    df=2*R_bs-R_mp-1/(2*bl)
    R_bsl=R_bs-df
    R_mpl=R_mp-df
    xfl=R_mpl/2+df
    #R_bsl=R_bs
    #R_mpl=R_mp


    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    r_kf=np.sqrt(yz+xyz[:,0]**2)

    alpha=(0.58-0.007*Bz)*(1+0.024*np.log(Pd))
    #print(xyz_kf,R_mp,theta,alpha)
    b_mp=bl/(1+4*bl*(R_mp-R_bs))
    r_mp_kf=(-np.cos(theta)+np.sqrt(np.cos(theta)**2+4*R_mp*b_mp*np.sin(theta)**2))/(2*b_mp*np.sin(theta)**2)
    r_bs_kf=(-np.cos(theta)+np.sqrt(np.cos(theta)**2+4*R_bs*bl*np.sin(theta)**2))/(2*bl*np.sin(theta)**2)
    f_kf=(r_kf-r_mp_kf)/(r_bs_kf-r_mp_kf)
    #print('r_kf,r_mp,r_bs_kf',r_kf,r_mp,r_bs_kf)


    Cl=R_mpl/2*(2*R_bsl-R_mpl)/(R_bsl-R_mpl)
    v_fl=[]
    #xerR_mpl=R_mp-df
    check=0
    for i,vx,vy,vz,f,R_mp,R_bs,C,b,xf,R_bs_r in zip(xyz,v_x,v_y,v_z,f_msh,R_mpl,R_bsl,Cl,bl,xfl,R_bs):

#        print(i)
        x,y,z=i
        vsw=np.array([vx,vy,vz])
        d=np.sqrt((x-xf)**2+y**2+z**2)
        v0=np.array([C*(1/(2*d)-1/R_mp),C*y/(2*d*(d+x-xf)),C*z/(2*d*(d+x-xf))])
        v0=normalize(v0)
#        print(v0)
        #print(f,f_kf)
#        if (f_kf<0) or (f_kf>1):
#            v_f=np.array([np.nan,np.nan,np.nan])
#        else:
        while(x-R_bs_r+b*(y**2+z**2))<0:
            #print(x,y,z)
            #print(x-R_bs+1/(4*R_bs)*(y**2+z**2))
            d=np.sqrt((x-xf)**2+y**2+z**2)
            v=np.array([C*(1/(2*d)-1/R_mp),C*y/(2*d*(d+x-xf)),C*z/(2*d*(d+x-xf))])
            #print(v)
            x-=0.01*v[0]
            y-=0.01*v[1]
            z-=0.01*v[2]
        theta=np.arctan2(np.sqrt(y**2+z**2),x)
        phi=np.arctan2(z,y)
        if not 'v' in locals():
            check=1
            v_f=np.array([np.nan,np.nan,np.nan])
        else:
            #print(v)
            v=normalize(v)
            #t1=np.array([0,-np.sin(phi),np.cos(phi)])
            #t2=np.array([-np.sin(theta),np.cos(phi)*(1+np.cos(theta)),np.sin(phi)*(1+np.cos(theta))])
            #t2=normalize(t2)
#            t1=normalize(np.array([-2*b*z,0,1]))
#            t2=normalize(np.array([2*b*y,-(1+4*b**2*z**2),4*b**2*y*z]))
            n=normalize(np.array([1,2*b*y,2*b*z]))
            t1=normalize(v-np.inner(n,v)*n)
#            t2=normalize(np.cross(n,t1))
            #print(x,y,z)
            #print(vsw,v,t1,t2)
            r1=np.dot(vsw,t1)/np.dot(v,t1)
#            r2=np.dot(vsw,t2)/np.dot(v,t2)
#            r=np.sqrt((r1**2+r2**2)/2)
            #r=np.min([r1,r2])
            r=r1 #Quadratic means in Soucek 2012 can lead to blow up
            #print(r)
            rho=0.8+0.2*np.tanh(4*f)
            vm0=r/rho
            #print(r1,r2,r,rho,vm0)
            v_f=vm0*v0
    #    print(v_f)
        v_fl.append(v_f)

    v_fl=np.array(v_fl)
    if check:print('Outside of BS from the start for at least one datapoint')

    return v_fl



def OMNIread2(f):

    BErr='nan'          # err of B field
    VErr='nan'          # err of Velocity
    NErr='nan'               # err of Number density

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
    dateparse = lambda x, y: pd.to_datetime(x + ' ' + y, format='%y/%m/%d %H:%M:%S')
    sat = pd.read_csv(f, header=None, sep='\s+', names=['d','t','x','y','z'])
    sat['datetime'] = pd.to_datetime(sat['d'] + ' ' + sat['t'], format='%y/%m/%d %H:%M:%S')
    sat = sat.drop(['d', 't'], axis=1)
    return sat


def main(xyz,f_sw,fout,mpdo=0,bsdo=0,model='jel'):
    mpdo=float(mpdo)
    bsdo=float(bsdo)

    if type(xyz)==str:
        xyz=SSCread(xyz)

    omni=OMNIread2(f_sw)
    if len(omni)==1:
        omni=pd.concat([omni]*np.shape(xyz)[0])

    if type(xyz)!=np.ndarray:
        test=xyz.merge(omni,how='outer')[['datetime','x','y','z']].sort_values(by=['datetime']).set_index('datetime').interpolate('index')
        omni=omni.set_index('datetime').join(test,how='left')
        xyz_np=omni[['x','y','z']].to_numpy()
    else:
        xyz_np=xyz

    xyz_np_0=xyz_np.copy()
    rm=R.from_euler('z',-4,degrees=True)
    xyz_np=(rm.as_matrix()@xyz_np.T).T

    #To calculate the flow velocity at a given point r in the magnetosheath, we proceed as follows:
    #(i) The MIPM coordinates (F ,ϑ,ϕ) are calculated using Eqs. (1) and (7) with the chosen models for the bow shock and the magnetopause, in our case Farris et al. (1991) and Shue et al. (1997).
    r=xyz_np[:,0]**2+xyz_np[:,1]**2+xyz_np[:,2]**2
    theta=np.arccos(xyz_np[:,0]/r)
    phi=np.arctan2(xyz_np[:,2],xyz_np[:,1])
    mpd=np.array(mpdf(omni.Pd,omni.Bz,xyz_np))
    mpd+=mpdo
    if model!='jer':
        bsd=bsdf_Jelinek(omni.Pd,xyz_np)
    else:
         bsd=np.array(BSf_Farris_Jerab(omni.Pd,omni.n,omni.V,omni.B,omni.Ma,xyz_np))
    bsd+=bsdo
    pts=appendSpherical_np(xyz_np)


    f_msh=(pts[:,3]-mpd)/(bsd-mpd)
    #print(mpd,bsd,f_msh)
    pts=np.hstack((pts,f_msh.reshape(pts.shape[0],1)))

    pts_df=pd.DataFrame(pts, columns=['x','y','z','r','theta','phi','f'])
    input=pts_df[['theta','phi','f']].to_numpy()

    #(ii) We calculate the corresponding KF94R point r˜ with the same MIPM coordinates, but using r˜bs and r˜mp from the KF94R model in Eq. (7).
    xyz_KF=KF94R(omni.Pd,omni.Bz,omni.n,omni.V,omni.B,omni.Ma,xyz_np,f_msh)
    #print(xyz_np,xyz_KF)


    #(iii) From r˜ is calculated the velocity vector v˜ in the KF94R reference frame using Eq. (3).
    v_t=backtrack(omni.Pd,omni.Bz,omni.n,omni.B,omni.Ma,omni.vx,omni.vy,omni.vz,xyz_KF,f_msh)
#    print('v_t',v_t)

    #(iv) The velocity vector v˜ is transformed back from the KF94R magnetosheath to the original GSE reference frame. Choose a small time increment ∆t and calculating the position of an adjacent point on the same flowline r˜0 = r˜ + v˜ ∆t. The point r˜0 is then easily transformed from the KF94R reference frame to the original GSE frame in a manner analogous to steps 1 and 2 above (let r0 be the resulting advanced GSE point). The resulting flow velocity vector in GSE coordinates is obtained as v = (r0 − r)/ ∆t.
    dt=0.01
#    print(np.shape(xyz_KF)[0])
#    print(np.shape(v_t))
#    print(v_t[0])
    r_t0=v_t*dt+xyz_KF
#    print(xyz_KF,r_t0)
    r0=KF94R_R(omni.Pd,omni.Bz,omni.n,omni.V,omni.B,omni.Ma,r_t0)
#    xyz_R=KF94R_R(omni.Pd,omni.Bz,omni.n,omni.V,omni.B,omni.Ma,xyz_KF)
#    print(r0,xyz_R)
    #print(r0-xyz_np)
    v=(r0-xyz_np)/dt
    v=(rm.as_matrix().T@v.T).T
    inv=np.logical_or(pts_df.f<0.05,pts_df.f>1)
    inv2=np.logical_or(np.absolute(v[:,0])>1000,np.absolute(v[:,1])>1000,np.absolute(v[:,2])>1000)
    v[inv]=np.array([np.nan,np.nan,np.nan])
    #v[inv2]=np.array([np.nan,np.nan,np.nan])


    out=pd.DataFrame({'time':omni.index,'x':xyz_np_0[:,0],'y':xyz_np_0[:,1],'z':xyz_np_0[:,2],'f':pts_df.f,'vx':v[:,0],'vy':v[:,1],'vz':v[:,2]})
    out.to_csv(fout,float_format='%.3f',index=False)
    return

if __name__=='__main__':
    f_sw="Soucek_test.txt"
    test=open(f_sw,"w")
    test.write("2003 124 11 34    2.17   -4.01    0.58  -407.2   -47.2     5.1   4.39  1.48   9.1  6.0\n")
    #Year DOY HR MN Bx By Bz Vx Vy Vz n Pd Ma Mm, as in OMNIweb
    #time is not used in the calculation
    #One line data can be used for constant SW cond.
    test.close()
#    f_sw='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/omni.lst'
    xyz=np.array([[  7.43,-7.58,6.56]])

#    xyz='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/cl_orbit.txt'

    #Orbit data from the SSWweb can be used as xyz. (filepath)
    #Data would be interpolated based on OMNI time.
    fout='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Soucek_test.txt'
#    fout='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Soucek_out.txt'
    main(xyz,f_sw,fout)
