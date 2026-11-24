import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def autoCorrFunc(rawData):
    data=data.to_numpy().copy()
    mean = data.mean()
    data-=mean
    N=len(data)
    
    autoCorr=np.correlate(data, data, "full")[N-1:]
    autoCorr/=autoCorr[0]
    return autoCorr

def autoCorrFuncNormed(data):
    data=data.to_numpy().copy()
    mean = data.mean()
    data-=mean
    N=len(data)
    
    autoCorr=np.correlate(data, data, "full")[N-1:]
    autoCorr/=autoCorr[0]
    autoCorr*=N/(N-k)
    return autoCorr
    


#seeds=[0, 774, 2002, 19210]
seeds=[0]
maxLag=20
ignore=25
for seed in seeds:

    seedFolder=f"rawData/seed{seed}"
    lattices = os.listdir(seedFolder)
    for lattice in lattices:
        file=f"{seedFolder}/{lattice}/chiUD_binned.csv"
        plotFolder=f"plots/autoCorrelation/seed{seed}/{lattice}"
        os.makedirs(plotFolder, exist_ok=True)
        
        df=pd.read_csv(file)
        masses=df.columns[1:]
        
        for mass in masses:    
            plotFile=f"{plotFolder}/{mass}_np.png"
            data=df[mass].iloc[ignore:].dropna()
            maxLag=len(data)
            rho = autoCorrFunc(data)
                
            
            plt.figure()
            plt.plot(rho)
            plt.xlabel("Lag")
            plt.title(f"Auto-Correlation of Chi UD for mass {mass}")
            plt.savefig(plotFile)
            plt.close()

            plotFile=f"{plotFolder}/{mass}_np_normed.png"
            data=df[mass].iloc[ignore:].dropna()
            maxLag=len(data)-1
            rho2 = autoCorrFuncNormed(data)
            
            plt.figure()
            plt.plot(rho2)
            plt.xlabel("Lag")
            plt.title(f"Auto-Correlation of Chi UD for mass {mass}")
            plt.savefig(plotFile)
            plt.close()
