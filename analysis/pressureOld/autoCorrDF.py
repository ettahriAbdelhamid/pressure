import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 

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
            
            plotFile=f"{plotFolder}/{mass}_df.png"
            data=df[mass].iloc[ignore:].dropna()
            maxLag=len(data)-1
            rho = np.array([
                data.autocorr(k)
                for k in range(maxLag)
            ])
            
            plt.figure()
            plt.plot(rho)
            plt.xlabel("Lag")
            plt.title(f"Auto-Correlation of Chi UD for mass {mass}")
            plt.savefig(plotFile)
            plt.close()

#K = np.argmax(rho[1:] < 0) + 1
#            N=len(df2)
#            tau_int = 0.5 + np.sum(rho[1:K])
#
#            N_eff = N / (2 * tau_int)
#
#            print("Anzahl Messungen:             ", N)
#            print("Autokorrelationszeit tau_int:", tau_int)
#            print("Effektive Samples N_eff:     ", N_eff)
#            print("Reduktionsfaktor:             ", N / N_eff)




# num=sum([
#        data[i]*data[i+k]
#        for i in range(N-k)
#    ])
#    den =sum([
#        x**2
#        for x in data
#    ])

#df=pd.read_csv(file, index_col="measurement")