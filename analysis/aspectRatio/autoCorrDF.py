import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 
import csv



def getIntegratedAutoCorrTime(array):
    time=0
    skip=True
    for i in array:
        if(skip):
            skip=False
            continue
        if(i>=0):
            time+=i
        else:
            break

    return time+1/2


maxLag=20
ignoreArray=(0, 50, 100, 150, 200, 250)
unbinnedSize=300

dataFolder=f"rawData/"
lattices = os.listdir(dataFolder)

for ignore in ignoreArray:
    for lattice in lattices:
        file=f"{dataFolder}/{lattice}/chi_ud_binned.csv"
        plotFolder=f"plots/autoCorrelation/autoCorrelationDF{ignore}/{lattice}"
        os.makedirs(plotFolder, exist_ok=True)
        csvFolder=f"autoCorrData/ignore{ignore}"
        os.makedirs(csvFolder, exist_ok=True)
        df=pd.read_csv(file)
        masses=df.columns[1:]
        
        with open(f'{csvFolder}/{lattice}.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=','#,quotechar='|', quoting=csv.QUOTE_MINIMAL
            )
            csv_writer.writerow(["ml", "autoCorrTime", "N", "N_eff"])
            for mass in masses:    
                
                plotFile=f"{plotFolder}/{mass}_df.png"
                data=df[mass].iloc[ignore:].dropna()
                maxLag=len(data)-1
                rho = np.array([
                    data.autocorr(k)
                    for k in range(maxLag)
                ])
                time=getIntegratedAutoCorrTime(rho)
                print(f"{lattice} {mass} ignoring {ignore}: time is {time}, effective sample size: {unbinnedSize-ignore} -> {(unbinnedSize-ignore)/(2*time)}")
                csv_writer.writerow([mass, time, unbinnedSize-ignore, (unbinnedSize-ignore)/(2*time)])
                continue
                plt.figure()
                plt.plot(rho)
                plt.xlabel("Lag")
                plt.title(f"Auto-Correlation of Chi UD for mass {mass}")
                plt.savefig(plotFile)
                plt.close()
