import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def mkdirs(path):
    if(not os.path.isdir(path)):
        os.makedirs(path, exist_ok=True)

def getThermalizedDf(df, ignore, ns):
    if(ns==40):
        return df[df.index%300>ignore-1]
    else:
        return df[df.index > ignore-1]

mainFolder="../../"
simFolder=f"{mainFolder}/simulations/aspectRatioAnalysis/"
rawDataFolder=f"rawData/"
plotFolder=f"plots/overMarkov/"
mkdirs(plotFolder)

lattices=os.listdir(simFolder)
observables = ("chi_ud", "chi_ud_binned", "chi_s", "chi_s_binned", "polyakov_real", "polyakov_img", "polyakov_abs", "plaquette", "rectangle", "gauge_action")
observableTitles = ("Chi UD", "Chi UD binned", "Chi S", "Chi S binned", "Polyakov Loop real", "Polyakov Loop img", "Polyakov Loop abs", "Plaquette", "Rectangle", "Gauge Action")
ignoreArray=(0, 50, 100, 150, 200, 250)

for ignore in ignoreArray:
    mkdirs(f"{plotFolder}/ignore{ignore}/all/")

df_chi={lattice: {observable: pd.DataFrame() for observable in observables} for lattice in lattices}


#plot each observable over markov time for different lattices for all masses TOGETHER
for ignore in ignoreArray:
    
    for lattice in lattices:
        ns=int(lattice.split("_")[1])
        df = df_chi[lattice]
        for observable, title in zip(observables, observableTitles):
            fig, ax = plt.subplots(figsize=(8, 5))

            df[observable]=pd.read_csv(f"{rawDataFolder}/{lattice}/{observable}.csv")
            if(observable in ("gauge_action", "rectangle", "plaquette")):
                #ml=1.0 has huge differences in the first steps, leading to bad plotting
                df[observable]=df[observable].drop("ml1.0", axis=1)
            
            df[observable]=df[observable].drop("measurement", axis=1)
            df[observable].index.name = "measurement"
            getThermalizedDf(df[observable], ignore, ns).plot(ax=ax, title=f"{title} for lattice {lattice}")
            
            #ax.grid(True)
            plt.savefig(f"{plotFolder}/ignore{ignore}/all/{lattice}_{observable}.png")
            plt.close(fig)


#plot each observable for each lattice over markov time for each mass SEPARATELY
for ignore in ignoreArray:
    
    for lattice in lattices:
        ns=int(lattice.split("_")[1])
        massFolders=sorted(os.listdir(f"{simFolder}/{lattice}"),key=lambda x: float(x.split("ms_")[1]), reverse=True)
        for massFolder in massFolders:
            mass=float(massFolder.split("_")[3])
            mkdirs(f"{plotFolder}/ignore{ignore}/ml{mass}")
            for observable, title in zip(observables, observableTitles):
                
                plotfileName=f"{plotFolder}/ignore{ignore}/ml{mass}/{lattice}_{observable}"
                df = df_chi[lattice][observable]
                fig, ax = plt.subplots(figsize=(8, 5))

                df.index.name = "measurement"#maybe unnecessary
                if(observable in ("gauge_action", "rectangle", "plaquette") and mass==1.0):
                    continue
                getThermalizedDf(df, ignore, ns)[f"ml{mass}"].plot(ax=ax, title=f"{title} for lattice {lattice}")
                
                #ax.grid(True)
                plt.savefig(f"{plotfileName}.png")
                #plt.xscale('log')
                #plt.savefig(f"{plotfileName}Log.png")
                plt.close(fig)


#plot polyakov loop in complex plane for each mass SEPARATELY
for ignore in ignoreArray:
    for lattice in lattices:
        ns=int(lattice.split("_")[1])
        massFolders=sorted(os.listdir(f"{simFolder}/{lattice}"),key=lambda x: float(x.split("ms_")[1]), reverse=True)
        for massFolder in massFolders:
            mass=float(massFolder.split("_")[3])
            df = df_chi[lattice]
            real=getThermalizedDf(df["polyakov_real"], ignore, ns)[f"ml{mass}"]
            img=getThermalizedDf(df["polyakov_img"], ignore, ns)[f"ml{mass}"]
            maxNum=max(real.abs().max(), img.abs().max())

            plt.figure()
            plt.scatter(real, img)
            #plot real and img axis
            x1, y1 = [-maxNum, maxNum], [0, 0]
            x2, y2 = [0, 0], [-maxNum, maxNum] 
            plt.plot(x1, x2, y1, y2)
            
            plt.xlabel("Re(L)")
            plt.ylabel("Im(L)")
            plt.title(f"Polyakov Loop for {lattice} for mass {mass}")
            plt.savefig(f"{plotFolder}/ignore{ignore}/ml{mass}/{lattice}_complex.png")
            plt.close()