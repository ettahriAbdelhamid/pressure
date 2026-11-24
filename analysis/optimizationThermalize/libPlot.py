import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.special import erfc

def plot(masses, df, filename, folder, title, labels, colors, markers):
    
    def generate_plot(is_log=False):
        cols=df.columns

        plt.figure()
        for i, label, color in zip(range(len(cols)), labels, colors):
            col=cols[i]
            plt.plot(masses, df[col], label=label, 
                     color=color, marker=markers[i%len(markers)] #,linestyle=line_style_array[i]
                     )

        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
                
        #plt.axvline(0.5)
        plt.xlabel("masses")
        plt.title(title)
        if (is_log):
            plt.xscale('log')
            plt.savefig(f"{folder}{filename}Log.png", bbox_inches='tight')
        else:
            plt.savefig(f"{folder}{filename}.png", bbox_inches='tight')
        plt.close()
    generate_plot(False)
    generate_plot(True)


def prepareDF(df, startOfColname):
    colNameMask=df.columns.str.startswith(startOfColname)
    correctCols=df.columns[colNameMask]
    return df[correctCols]



def linearModel(X, A, B, C, D):
    x, y, z = X
    return A*x + B*y + C*z + D

def expQuadDecayModel(X, A, B, C):
    md, step_sf, sw = X 
    return np.exp(-(A/(md**2)+B/(step_sf**2)+C/(sw**2)))

def expQuadDecayModel2(X, A, B, C):
    md, step_sf, sw = X 
    return erfc(1/2*np.sqrt(A/(md**4)+B/(step_sf**4)+C/(sw**4)))

def ratioToAbs(md, step_sf, sw):
    return (md, step_sf*md, sw*step_sf*md)


def latticeMassArrayDict(lattices, massRange):
    return {lattice: {index: [] for index in massRange} for lattice in lattices}

def latticeArrayDict(lattices):
    return {lattice: {} for lattice in lattices}

def mkdir(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def getOptiParam(A, B, C, mMd, mStepSf, mSw, mConst):
   
    r=mMd/(2*A)
    s = mMd+ mStepSf * np.cbrt(B*mMd/(A*mStepSf))+ mSw * np.cbrt(C*mMd/(A*mSw))
    t=mConst

    def returnXk(k):
        x = 2*np.sqrt(s/(3*r))*np.cos(  1/3 * np.arccos(3*t/(2*s)*np.sqrt(3*r/s))   -2*k*np.pi/3)
        return x

    radicant=(mConst/(2*r))**2-(s/(3*r))**3
    if (radicant>0):
        a=mConst/(2*r)
        b=np.sqrt(radicant)
        x=np.cbrt(a+b)+np.cbrt(a-b)
        
        
    else:
        #print(f"x0={returnXk(0)}")
        #print(f"x1={returnXk(1)}")
        #print(f"x2={returnXk(2)}")
        print("first of three")
        x=returnXk(0)

    y=x*np.cbrt((B*mMd)/(A*mStepSf))
    z=x*np.cbrt((C*mMd)/(A*mSw))
    #print(f"{x:.2f}_{y:.2f}_{z:.2f}")
    #print(f"{x:.2f}:{y/x:.2f}:{z/y:.2f}")

    print(f"{x:.2f}:{y/x:.2f}:{z/y:.2f}")