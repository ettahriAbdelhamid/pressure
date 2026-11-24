import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 
import csv



def getIntegratedAutoCorrTime(array):
    time = 0

    for i in array[1:]:
        if i < 0:
            break
        time += i

    return time + 0.5


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
        
        with open(f'{csvFolder}/{lattice}_autoCorrTime.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=','#,quotechar='|', quoting=csv.QUOTE_MINIMAL
            )
            csv_writer.writerow(["ml", "autoCorrTime", "N", "N_eff"])
            for mass in masses:    
                
                plotFile=f"{plotFolder}/{mass}_df.png"
                #data=df[mass].iloc[ignore:].dropna()
               

                #rho = np.array([
                #    data.autocorr(k)
                #    for k in range(maxLag+1)
                #])
                #print(rho[:15])
                #time=getIntegratedAutoCorrTime(rho)
                #N = len(data)
                #N_eff = N/(2*time)
                #print(f"{lattice} {mass} ignoring {ignore}: time is {time}, effective sample size: {unbinnedSize-ignore} -> {(unbinnedSize-ignore)/(2*time)}")
                #csv_writer.writerow([mass, time, unbinnedSize-ignore, (unbinnedSize-ignore)/(2*time)])
                
                data = df[mass].iloc[ignore:].dropna()
                maxLag = min(20, len(data)-1)
                N = len(data)

                maxLagUsed = min(maxLag, N-1)

                rho = np.array([
                    data.autocorr(k)
                    for k in range(maxLagUsed+1)
                ])

                time = getIntegratedAutoCorrTime(rho)

                N_eff = N/(2*time)

                print(
                    f"{lattice} {mass} ignoring {ignore}: "
                    f"tau = {time:.4f}, "
                    f"N = {N}, "
                    f"N_eff = {N_eff:.2f}"
                )

                csv_writer.writerow([mass, time, N, N_eff])
