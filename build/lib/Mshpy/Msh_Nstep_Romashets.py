#Romashets Magnetic field

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.special import jv,iv,kn,jvp,ivp,kvp
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


def mpdf(Pd,Bz,xyz):
    yz=xyz[:,1]**2+xyz[:,2]**2
    theta=np.arctan2(np.sqrt(yz),xyz[:,0])
    r0=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    alpha=(0.58-0.007*Bz)*(1+0.024*np.log(Pd))
    R = r0*(2/(1+np.cos(theta)))**alpha
    return R

def P(v,k,s,t,s0):
    if v==0:
        f=iv(1,k*s)-kn(1,k*s)*ivp(1,k*s0)/ivp(1,k*s0)
    if v==1:
        f=(ivp(0,k*s)+kvp(0,k*s)*iv(1,k*s0)/kn(1,k*s0))*jv(0,k*t)
    if v==2:
        f=(iv(0,k*s)+kn(0,k*s)*iv(1,k*s0)/kn(1,k*s0))*jvp(0,k*t)
    if v==3:
        f=(ivp(1,k*s)-kvp(1,k*s)*ivp(1,k*s0)/kvp(1,k*s0))*jv(1,k*t)
    if v==4:
        f=(iv(1,k*s)-kn(1,k*s)*ivp(1,k*s0)/ivp(1,k*s0))*jvp(1,k*t)
    return f

"""
A,B=np.hsplit(np.array([
       [ 1.40701261e+03,  3.04789295e+03],
       [ 4.10907593e+00,  1.19842529e+01],
       [ 4.16965516e-01,  1.07833018e+00],
       [ 4.43112000e-02,  1.07371444e-01],
       [ 5.12188800e-03,  1.16881590e-02],
       [ 5.81770000e-04,  1.30437000e-03],
       [ 6.98000000e-05,  1.51000000e-04],
       [ 8.05000000e-06,  1.75000000e-05],
       [ 9.94000000e-07,  2.07000000e-06],
       [ 1.14000000e-07,  2.44000000e-07],
       [ 1.45000000e-08,  2.93000000e-08],
       [ 1.61000000e-09,  3.49000000e-09],
       [ 2.18000000e-10,  4.22000000e-10],
       [ 2.27000000e-11,  5.06000000e-11],
       [ 3.37000000e-12,  6.15000000e-12],
       [ 3.08000000e-13,  7.41000000e-13],
       [ 5.27000000e-14,  8.87000000e-14],
       [ 3.59000000e-15,  1.06000000e-14],
       [ 6.82000000e-16,  1.10000000e-15],
       [-6.13000000e-18,  9.94000000e-17]]),2)
A=A.flatten()
B=B.flatten()
"""

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

    rm=R.from_euler('z',-4,degrees=True)
    xyz_np=(rm.as_matrix()@xyz_np.T).T

    mpd=np.array(mpdf(omni.Pd,omni.Bz,xyz_np))
    mpd+=mpdo
#    bsd=np.array([bsdf(omni.n[i],v_sw[i],Ma[i],B_sw[i],xyz[i])for i in range(np.shape(xyz)[0])])

    if model!='jel':
        bsdfv=np.vectorize(bsdf2)
        bsd=np.array(bsdfv(omni.n,omni.V,omni.Ma,omni.B,xyz_np[:,0],xyz_np[:,1],xyz_np[:,2]))
    else:
        bsd=bsdf_Jelinek(omni.Pd,xyz_np)
    bsd+=bsdo
#    print(np.shape(mpd),np.shape(bsd))

    pts=appendSpherical_np(xyz_np)
    print('theta range',np.nanmin(pts[:,4])*180/np.pi,np.nanmax(pts[:,4])*180/np.pi)
    print('phi range',np.nanmin(pts[:,5]*180/np.pi),np.nanmax(pts[:,5])*180/np.pi)

    f_msh=(pts[:,3]-mpd)/(bsd-mpd)
#    print(type(pts),type(f_msh))
    pts=np.hstack((pts,f_msh.reshape(pts.shape[0],1)))
    #print(pts)
    pts_df=pd.DataFrame(pts, columns=['x','y','z','r','theta','phi','f'])

    #Finding Ai and Bi, using mid time data
    mid_rw = int(len(omni)/2)
    x,y,z=xyz_np[mid_rw]
    Pd=omni.Pd.iloc[mid_rw]
    Bx=omni.Bx.iloc[mid_rw]
    By=omni.By.iloc[mid_rw]
    Bz=omni.Bz.iloc[mid_rw]

    xc=12.82*Pd**(-1/5.26)*(1-1/1.54**2)
    #xs=-1.91
    xs=15.02*Pd**(-1/6.55)*(1-1/1.17**2)

    #s0=3.66
    s0=np.sqrt(2*12.82)/1.54*Pd**(-1/(2*5.26))
    sig1=np.sqrt(2*15.02)/1.17*Pd**(-1/(2*6.55))
    #C=2
    C=sig1**2/(sig1**2-s0**2)
    #print(xc,xs,s0,C)

    kmax=4.5
    check=150
    while (check>35):
        kmax+=0.5
        k=np.linspace(0.01,kmax,20)
        taul=np.arange(1,11)

        F_A,G_A,F_B,G_B=[],[],[],[]

        for j in range(0,10):
            tau=taul[j]
            h1=np.sqrt(sig1**2+tau**2)
            q1=(sig1**2-tau**2)/2-xc+xs
            s1=np.sqrt(q1+np.sqrt(q1**2+sig1**2*tau**2))
            t1=np.sqrt(-q1+np.sqrt(q1**2+sig1**2*tau**2))
            dsdsig1=sig1/(2*s1)*(1+(q1+tau**2)/np.sqrt(q1**2+sig1**2*tau**2))
            dtdsig1=-sig1/(2*t1)*(1-(q1+tau**2)/np.sqrt(q1**2+sig1**2*tau**2))
        #    print(t1,dtdsig1)
            G_A_temp=sig1*(1-C)/np.sqrt(sig1**2+tau**2)+C*(1/h1*s0**2/s1*dsdsig1)
            G_A.append(G_A_temp)
            G_B_temp=tau*(1-C)/np.sqrt(sig1**2+tau**2)-C*(1/h1*s0**2/s1*(dtdsig1-t1/s1*dsdsig1))
            G_B.append(G_B_temp)

            Fl_A_temp=[]
            Fl_B_temp=[]
            for i in range(20):
                sum_sig_1=k[i]*(P(1,k[i],s1,t1,s0)*dsdsig1+P(2,k[i],s1,t1,s0)*dtdsig1)
                F_A_temp=(C*(sig1-s0**2/s1*dsdsig1)+sum_sig_1)/h1
                Fl_A_temp.append(F_A_temp)
                sum_sig_2=k[i]*(P(3,k[i],s1,t1,s0)*dsdsig1+P(4,k[i],s1,t1,s0)*dtdsig1)
                F_B_temp=(C*(tau+s0**2/s1*(dtdsig1-t1/s1*dsdsig1))+sum_sig_2)/h1
                Fl_B_temp.append(F_B_temp)
            F_A.append(Fl_A_temp)
            F_B.append(Fl_B_temp)
        G_A=np.array(G_A)
        F_A=np.array(F_A)
        G_B=np.array(G_B)
        F_B=np.array(F_B)
        #print(np.shape(G),np.shape(F),np.shape(F.T@F))
        A=(np.linalg.inv(F_A.T@F_A)@F_A.T)@G_A
        B=(np.linalg.inv(F_B.T@F_B)@F_B.T)@G_B

        #print(A,B)
#        print('A,B calculated')

        Bxl,Byl,Bzl,B_tl=[],[],[],[]
        for (xyz,Pd,B0x,B0y,B0z,f) in zip(xyz_np,omni.Pd,omni.Bx,omni.By,omni.Bz,pts_df.f):
            if (0<=f) & (f<=1):
                x,y,z=xyz
                #xc=1.55
                xc=12.82*Pd**(-1/5.26)*(1-1/1.54**2)
                #xs=-1.91
                xs=15.02*Pd**(-1/6.55)*(1-1/1.17**2)
                phi=np.arctan2(z,y)
                r_s=np.sqrt((x-xs)**2+y**2+z**2)
                r_c=np.sqrt((x-xc)**2+y**2+z**2)
                sig=np.sqrt(r_s+x-xs)
                tau=np.sqrt(r_s-x+xs)
                s=np.sqrt(r_c+x-xc)
                t=np.sqrt(r_c-x+xc)
              #  s=np.sqrt(r_c+x-xc)
              #  t=np.sqrt(r_c-x+xc)
                q=(sig**2-tau**2)/2-xc+xs
        #        s=np.sqrt(q+np.sqrt(q**2+sig**2*tau**2))
        #        t=np.sqrt(-q+np.sqrt(q**2+sig**2*tau**2))

                h=np.sqrt(sig**2+tau**2)
                h_phi=sig*tau

                #s0=3.66
                s0=np.sqrt(2*12.82)/1.54*Pd**(-1/(2*5.26))
                sig1=np.sqrt(2*15.02)/1.17*Pd**(-1/(2*6.55))
                #C=2
                C=sig1**2/(sig1**2-s0**2)
                #print(xc,xs,s0,C)

                denom=np.sqrt(q**2+sig**2*tau**2)
                dsdsig=sig/(2*s)*(1+(q+tau**2)/denom)
                dsdtau=-tau/(2*s)*(1+(q-sig**2)/denom)
                dtdsig=-sig/(2*t)*(1-(q+tau**2)/denom)
                dtdtau=tau/(2*t)*(1-(q-sig**2)/denom)
                #print(denom,dsdsig,dsdtau,dtdsig,dtdtau)

             #   k=np.linspace(0.01,5.5,20)

                sum_sig_1,sum_sig_2,sum_tau_1,sum_tau_2,sum_phi=0,0,0,0,0
                for i in range(20):
            #        print('A',i,A[i]*k[i]*(P(1,k[i],s,t,s0)*dsdsig+P(2,k[i],s,t,s0)*dtdsig))
            #        print('B',i,B[i]*k[i]*(P(3,k[i],s,t,s0)*dsdsig+P(4,k[i],s,t,s0)*dtdsig))
                    sum_sig_1+=A[i]*k[i]*(P(1,k[i],s,t,s0)*dsdsig+P(2,k[i],s,t,s0)*dtdsig)
                    sum_sig_2+=B[i]*k[i]*(P(3,k[i],s,t,s0)*dsdsig+P(4,k[i],s,t,s0)*dtdsig)
                    sum_tau_1+=A[i]*k[i]*(P(1,k[i],s,t,s0)*dsdtau+P(2,k[i],s,t,s0)*dtdtau)
                    sum_tau_2+=B[i]*k[i]*(P(3,k[i],s,t,s0)*dsdtau+P(4,k[i],s,t,s0)*dtdtau)
                    sum_phi+=B[i]*P(0,k[i],s,t,s0)*jv(1,k[i]*t)
            #    print(B0x,h,C,sig,s0,s,dtdsig,sum_sig_1,B0y,B0z,tau,dtdtau,sum_sig_2,A[i],B[i],k[i],phi)
            #    print(sum_sig_1,sum_sig_2,sum_tau_1,sum_tau_2,sum_phi)
                B_sig=(B0x*(C*(sig-s0**2/s*dsdsig)+sum_sig_1)+(B0y*np.cos(phi)+B0z*np.sin(phi))*(C*(tau+s0**2/s*(dtdsig-t/s*dsdsig))+sum_sig_2))/h
                B_tau=(B0x*(-C*(tau+s0**2/s*dsdtau)+sum_sig_1)+(B0y*np.cos(phi)+B0z*np.sin(phi))*(C*(sig+s0**2/s*(dtdtau-t/s*dsdtau))+sum_tau_2))/h
                B_phi=(-B0y*np.sin(phi)+B0z*np.cos(phi))/h_phi*(C*(sig*tau+s0**2*t/s)+sum_phi)
                #print(B_sig,B_tau,B_phi)

                Bx=(B_sig*sig-B_tau*tau)/h
                By=(B_sig*tau+B_tau*sig)/h*np.cos(phi)-B_phi*np.sin(phi)
                Bz=(B_sig*tau+B_tau*sig)/h*np.sin(phi)+B_phi*np.cos(phi)
                B_t=np.sqrt(Bx**2+By**2+Bz**2)
            else:
                Bx=np.nan
                By=np.nan
                Bz=np.nan
                B_t=np.nan
            Bxl.append(Bx)
            Byl.append(By)
            Bzl.append(Bz)
            B_tl.append(B_t)
        check=np.nanmax(B_tl)
        print(kmax,check)
    out=pd.DataFrame({'time':omni.index,'Bx':Bxl,'By':Byl,'Bz':Bzl,'B':B_tl})
    out.to_csv(fout,float_format='%.3f',index=False)
    return

if __name__=='__main__':
#    f_sw="Romashets_test.txt"
#    fout='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Romashets_test.txt'
#    xyz=np.array([[10,2,3],[8,3,1]])

    f_sw='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/omni.lst'
    xyz='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/cl_orbit.txt'

    #Orbit data from the SSWweb can be used as xyz. (filepath)
    #Data would be interpolated based on OMNI time.
#    fout='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Soucek_test.txt'
    fout='/Volumes/easystore/openggcm_run/Msh_Nstep/case_studies/2003May04_001/Romashets_out.txt'

    main(xyz,f_sw,fout)
