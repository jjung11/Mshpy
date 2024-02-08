import numpy as np
#from mayavi import mlab
import matplotlib.pyplot as plt
import copy


theta, phi = np.linspace(0, np.pi, 40), np.linspace(0, 2*np.pi, 40)
THETA, PHI = np.meshgrid(theta, phi)

#mlab.clf()
x, y, z = np.mgrid[-40:40:50j, -40:40:50j, -40:40:50j]
x2=z2=np.arange(-40,40,.1)
X,Z=np.meshgrid(x2,z2)


# Jerab Bow Shock
a11=.45
a22=1
a33=.8
a12=.18
a14=46.6
a24=-2.2
a34=-.6
a44=-618
R0=11.8954

#Jelinek Bow Shock
R_0=15.02
lam=1.17
epsilon=6.55

#Jerab [2005] BS model
def bsy(ax,N,V,Ma,B,j):
    D=0.937*(0.846+0.042*B)
#    print(N,V,D,Ma)
    f=91.55/(N*V**2)**(1/6)*(1+D*(5/3-1)*(Ma**2+2)/((5/3+1)*(Ma**2-1)))/R0
#    values=a11*(x/f)**2+a22*(y/f)**2+a33*(z/f)**2+a12*(x/f)*(y/f)+a14*(x/f)+a24*(y/f)+a34*(z/f)+a44
    values2=a11*(X/f)**2+a22*(Z/f)**2+a12*(X/f)*(Z/f)+a14*(X/f)+a24*(Z/f)+a44
    if j==0: ln=ax.contour(X,Z,values2,0,colors='orange')
    else: ln=ax.contour(X,Z,values2,0,colors='orange',linestyles='dashed')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    return ln

def bsz(ax,N,V,Ma,B,j):
    D=0.937*(0.846+0.042*B)
    f=91.55/(N*V**2)**(1/6)*(1+D*(5/3-1)*(Ma**2+2)/((5/3+1)*(Ma**2-1)))/R0
#    values=a11*(x/f)**2+a22*(y/f)**2+a33*(z/f)**2+a12*(x/f)*(y/f)+a14*(x/f)+a24*(y/f)+a34*(z/f)+a44
    values2=a11*(X/f)**2+a33*(Z/f)**2+a14*(X/f)+a34*(Z/f)+a44
    if j==0: ln=ax.contour(X,Z,values2,0,colors='orange')
    else: ln=ax.contour(X,Z,values2,0,colors='orange',linestyles='dashed')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    return ln


#Jelinek [2012] BS model
def bsj(ax,Pd,j,k):
    a14=4*R_0/lam**2*Pd**(-1/epsilon)
    a44=-1/4*(lam*a14)**2
    values=Z**2+a14*X+a44
    if j==0: ln=ax.contour(X,Z,values,0,colors='orange')
    else: ln=ax.contour(X,Z,values,0,colors='orange',linestyles='dashed')
    ax.set_xlabel('X')
    if k=='y':
        ax.set_ylabel('Y')
    elif k=='z':
        ax.set_ylabel('Z')
    return ln




# Shue MP model
def mp2(ax,Pd,Bz,j):
    r0=(10.22+1.29*np.tanh(0.184*(Bz+8.14)))*Pd**(-1/6.6)
    alpha=(0.58-0.007*Bz)*(1+0.024*np.log(Pd))
    R = r0*(2/(1+np.cos(theta)))**alpha
    Z = R * np.sin(theta)
    Z2= -R*np.sin(theta)
    X = R * np.cos(theta)
    if j==0:
        ln,=ax.plot(X,Z,color='red')
        ln2,=ax.plot(X,Z2,color='red')
    else:
        ln,=ax.plot(X,Z,color='red',linestyle='dashed')
        ln2,=ax.plot(X,Z2,color='red',linestyle='dashed')
    ax.set_xlim(-25,25)
    ax.set_ylim(-25,25)
    return ln,ln2

B,Bz,V,N,Pd,Ma=4.78, -0.41, 511.3, 2.68, 1.4, 8.8
Earth=plt.Circle((0,0),1)
#Earth2=plt.Circle((0,0),1)


def BSMP(ax1,ax2,B,Bz,V,N,Pd,Ma,j):
    if j==0:
        ln1=bsy(ax1,N,V,Ma,B,0)
        ln2=mp2(ax1,Pd,Bz,0)
        ln3=ax1.add_patch(copy.copy(Earth))
        ln4=bsz(ax2,N,V,Ma,B,0)
        ln5=mp2(ax2,Pd,Bz,0)
        ln6=ax2.add_patch(copy.copy(Earth))
        #plt.tight_layout()
    else:
        ln1=bsy(ax1,N,V,Ma,B,1)
        ln2=mp2(ax1,Pd,Bz,1)
        ln3=ax1.add_patch(copy.copy(Earth))
        ln4=bsz(ax2,N,V,Ma,B,1)
        ln5=mp2(ax2,Pd,Bz,1)
        ln6=ax2.add_patch(copy.copy(Earth))
        #plt.tight_layout()
    return ln1,ln2,ln3,ln4,ln6,ln6

def BSMPj(ax1,ax2,Bz,Pd,j):
    if j==0:
        ln1=bsj(ax1,Pd,0,'y')
        ln2=mp2(ax1,Pd,Bz,0)
        ln3=ax1.add_patch(copy.copy(Earth))
        ln4=bsj(ax2,Pd,0,'z')
        ln5=mp2(ax2,Pd,Bz,0)
        ln6=ax2.add_patch(copy.copy(Earth))
        #plt.tight_layout()
    else:
        ln1=bsj(ax1,Pd,1,'y')
        ln2=mp2(ax1,Pd,Bz,1)
        ln3=ax1.add_patch(copy.copy(Earth))
        ln4=bsj(ax2,Pd,1,'z')
        ln5=mp2(ax2,Pd,Bz,1)
        ln6=ax2.add_patch(copy.copy(Earth))
        #plt.tight_layout()
    return ln1,ln2,ln3,ln4,ln6,ln6



if __name__=='__main__':
    #test(1,B,Bz,V,N,Pd,Ma,1)
    f,(ax1,ax2)=plt.subplots(1,2)
    BSMP(ax1,ax2,B,Bz,V,N,Pd,Ma,0)
