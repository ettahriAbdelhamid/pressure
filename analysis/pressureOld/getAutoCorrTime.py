import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 
from scipy.optimize import curve_fit

def fitModel(X, A, B, C):
    return A+B*np.exp(-X/C)

#seeds=[0, 774, 2002, 19210]
seeds=[0]
maxLag=20
ignore=5

for seed in seeds:

    seedFolder=f"rawData/seed{seed}"
    lattices = os.listdir(seedFolder)
    
    for lattice in lattices:
        
        print(f"{lattice}: ")
        file=f"{seedFolder}/{lattice}/chiUD_binned.csv"
        plotFolder=f"plots/autoCorrelationFit/seed{seed}"
        plotFile=f"{plotFolder}/{lattice}.png"
        os.makedirs(plotFolder, exist_ok=True)
        
        df=pd.read_csv(file)
        masses=df.columns[1:]
        plt.figure()
        ind=0
        for mass in masses:   
            ind+=1
            if(ind<5):
                continue 
            print(f"{mass}: ", end="")

            data=df[mass].iloc[ignore:].dropna()
            data=df[mass].dropna()
            #print(data)
            


            popt, pcov= curve_fit(fitModel, np.arange(len(data)), data)
            A,B,C = popt
            print(f"A={A}, B={B}, C={C}")
            plt.plot(data, label=f"{mass}")
            plt.plot(fitModel(np.arange(len(data)), A, B, C), label=f"Fit for {mass}")
            plt.xlabel("Markov Time")
           
        plt.legend()
        plt.title(f"CHI UD Thermalization with fit for {lattice}")
        plt.savefig(plotFile)
        plt.close()
        