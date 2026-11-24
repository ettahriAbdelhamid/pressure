import scipy.optimize as optimize
import pandas as pd
import numpy as np
import os

from scipy.special import erfc


def timeFunc(X, mMd, mStepSf, mSw, mConst):
    md, stepSf, sw = X
    return md*mMd+stepSf*mStepSf+sw*mSw+mConst

def acceptanceFunc(X, A, B, C):
    md, stepSf, sw = X
    return erfc(1/2*np.sqrt(A/(md**4)+B/(stepSf**4)+C/(sw**4)))

def ratio(X, param):
    A, B, C, mMd, mStepSf, mSw, mConst=param
    time=timeFunc(X, mMd, mStepSf, mSw, mConst)
    acceptance=acceptanceFunc(X, A, B, C)
    return acceptance/time

def negRatio(X, param):
    return -ratio(X, param)

#def prepare_fit_df(df):
#    df = df.T
#    df.columns=df.iloc[0]
#    return df[1:]

fitFolder="fitParameter"
param=("A", "B", "C", "mMd", "mStepSf", "mSw", "mConst")
bounds = [
    (1e-8, None),
    (1e-8, None),
    (1e-8, None),
]
lattices=os.listdir(fitFolder)
lattices=[os.path.splitext(filename)[0] for filename in os.listdir(fitFolder)]#need this to extract the .csv file extension
fitDf={}
for lattice in lattices:
    print(lattice)
    fitDf[lattice]=pd.read_csv(f"{fitFolder}/{lattice}.csv").set_index("ml")
    #fitDf[lattice]=prepare_fit_df(fitDf[lattice])
    masses=fitDf[lattice].index.to_numpy()
    for mass in masses:
        print(f"\t{mass}", end="")
        fitData=[]
        for p in param:
            fitData.append(fitDf[lattice].loc[mass][p])
        optiParam=optimize.minimize(negRatio, x0=(10,10,10), args=(fitData,), bounds=bounds, method="Nelder-Mead")
        print(
            f"\tmd={optiParam.x[0]:.2f}, "
            f"step_sf={optiParam.x[1]:.2f}, "
            f"sw={optiParam.x[2]:.2f},"
            f"\t->{optiParam.x[0]:.0f}:{optiParam.x[1]/optiParam.x[0]:.0f}:{optiParam.x[2]/optiParam.x[1]:.0f},"
            f"max value: {-optiParam.fun:.3f}"
        )
        #print(f"f[x_,y_,z_]:=Exp[-({fitData[0]}/(x^2)+{fitData[1]}/(y^2)+{fitData[2]}/(z^2))]/({fitData[3]}*x+{fitData[4]}*y+{fitData[5]}*z+{fitData[6]})")
        








