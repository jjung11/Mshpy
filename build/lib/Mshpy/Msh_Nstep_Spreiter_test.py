import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sys import argv
from sympy.solvers import solve
from sympy import Symbol,nsolve
from sympy import sqrt,log,tanh
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import RegularGridInterpolator as RGI
import glob
import datetime
from scipy.interpolate import interp2d
from astropy.io import fits
import pkg_resources

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
    Tev=72429*Pd/n/11600
    omni=pd.DataFrame({'datetime':time,'Bx':Bx,'By':By,'Bz':Bz,'V':V,'vx':vx,'vy':vy,'vz':vz,'n':n,'Pd':Pd,'Ma':Ma,'Mm':Mm,'B':B_sw,'Tev':Tev})
    return omni

def WINDread(f):

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
        if (xyz.x<0).any():
            print('Warning: there is at least one time at which satellite was on nightside, which isn\'t supported by current version of model.')

    omni=OMNIread2(f_sw)
    if len(omni)==1:
        omni=pd.concat([omni]*np.shape(xyz)[0])

    print('SW temp mean',omni.Tev.mean())

    if type(xyz)!=np.ndarray:
        test=xyz.merge(omni,how='outer')[['datetime','x','y','z']].sort_values(by=['datetime']).set_index('datetime').interpolate('index')
        omni=omni.set_index('datetime').join(test,how='left')
        xyz_np=omni[['x','y','z']].to_numpy()
    else:
        xyz_np=xyz

#    print(len(xyz_np))
#    print(len(omni))

    r=R.from_euler('z',-4,degrees=True)
    xyz_np=(r.as_matrix()@xyz_np.T).T

    print('Finding MP nodes')
    mpd=np.array(mpdf(omni.Pd,omni.Bz,xyz_np))
    mpd+=mpdo

    print('Finding BS nodes')
    if model!='jel':
        bsdfv=np.vectorize(bsdf2)
        bsd=np.array(bsdfv(omni.n,omni.V,omni.Ma,omni.B,xyz_np[:,0],xyz_np[:,1],xyz_np[:,2]))
    else:
        bsd=bsdf_Jelinek(omni.Pd,xyz_np)
    bsd+=bsdo

    pts=appendSpherical_np(xyz_np)
    print('theta range',np.nanmin(pts[:,4])*180/np.pi,np.nanmax(pts[:,4])*180/np.pi)
    print('phi range',np.nanmin(pts[:,5]*180/np.pi),np.nanmax(pts[:,5])*180/np.pi)

#    print(np.shape(pts[:,3]),mpd,bsd)
    f_msh=(pts[:,3]-mpd)/(bsd-mpd)
    pts=np.hstack((pts,f_msh.reshape(pts.shape[0],1)))

    pts_df=pd.DataFrame(pts, columns=['x','y','z','r','theta','phi','f'])
    pts_df['phi2']=np.absolute(pts_df.phi)
    input=pts_df[['phi2','f']].to_numpy()

    if (omni.n>35).any(): print('Warning: there is at least one time at which solar wind density goes above 35cm^-3, in which our model was not validated')
    if (omni.B>15).any(): print('Warning: there is at least one time at which IMF magnitude goes above 15cm^-3, in which our model shows discrepancy with THEMIS data')

    phi=np.arange(0,128)*np.pi/180
    af=np.arange(0,10)/10

    n1=np.loadtxt(pkg_resources.resource_filename('Mshpy',f'data/Spreiter/Msh_n'))
    T1=np.loadtxt(pkg_resources.resource_filename('Mshpy',f'data/Spreiter/Msh_T'))
    V1=np.loadtxt(pkg_resources.resource_filename('Mshpy',f'data/Spreiter/Msh_V'))

    nf=RGI((phi,af),n1,bounds_error=False)
    Tf=RGI((phi,af),T1,bounds_error=False)
    Vf=RGI((phi,af),V1,bounds_error=False)

    n=nf(input)*omni.n.to_numpy()
    T=Tf(input)*omni.Tev.to_numpy()
    V=Vf(input)*omni.V.to_numpy()

    out=pd.DataFrame({'time':omni.index,'f':pts_df.f,'n':n,'Tev':T,'V':V})
    out.to_csv(fout,float_format='%.3f',index=False)

    return n,T,V

if __name__=='__main__':
    f_sw='SW_cond_test.txt'
    test=open(f_sw,"w")
    test.write("2003 124 12 30    1.01   -1.65   -0.78  -414.8   -21.8     0.7   7.54  2.60  24.3  7.7\n")
    #Year DOY HR MN Bx By Bz Vx Vy Vz n Pd Ma Mm, as in OMNIweb
    test.close()

    xyz=np.array([[12,2,3],[10,2,3]])
    fout='Msh_Spreiter_test_out.txt'
    main(xyz,f_sw,fout)
