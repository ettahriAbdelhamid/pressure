import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 
import csv


ignoreArray=(0, 50, 100, 150, 200, 250)
unbinnedSize=300



for ignore in ignoreArray:
    break
    dataFolder=f"autoCorrData/ignore{ignore}/"
    lattices = [str.split(".csv")[0] for str in os.listdir(dataFolder)]
    fig, ax = plt.subplots()
    for lattice in lattices:
        file=f"{dataFolder}/{lattice}.csv"
        plotFolder=f"plots/autoCorrelationTime/ignore{ignore}"
        os.makedirs(plotFolder, exist_ok=True)
        plotFile=f"{plotFolder}/{lattice}.png"
        df=pd.read_csv(file)
        masses=[float(ml.split("ml")[1]) for ml in df["ml"]]
            
        plt.figure()
        plt.plot(masses, df["autoCorrTime"])
        plt.xlabel("mass")
        plt.title(f"Autocorrelation time ignoring {ignore}")
        plt.savefig(plotFile)
        plt.close()
        
        ax.plot(
            masses, df["autoCorrTime"], marker="o", label=lattice
        )

    # Configure and save combined linear plot
    ax.set_xlabel("Mass")
    ax.set_ylabel("Autocorrelation time")
    ax.legend()
    fig.savefig(f"{plotFolder}/allLattices.png")


fig={}
ax={}

for ignore in ignoreArray:
    dataFolder=f"autoCorrData/ignore{ignore}/"
    lattices = [str.split(".csv")[0] for str in os.listdir(dataFolder)]
    for lattice in lattices:
        fig[lattice], ax[lattice] = plt.subplots()

for ignore in ignoreArray:
    dataFolder=f"autoCorrData/ignore{ignore}/"
    lattices = [str.split(".csv")[0] for str in os.listdir(dataFolder)]
    for lattice in lattices:
        file=f"{dataFolder}/{lattice}.csv"
        plotFolder=f"plots/autoCorrelationTime/"
        os.makedirs(plotFolder, exist_ok=True)
        plotFile=f"{plotFolder}/{lattice}.png"
        df=pd.read_csv(file)
        masses=[float(ml.split("ml")[1]) for ml in df["ml"]]
            
        ax[lattice].plot(masses, df["autoCorrTime"] ,label=f"ignore {ignore}")


for ignore in ignoreArray:
    dataFolder=f"autoCorrData/ignore{ignore}/"
    lattices = [str.split(".csv")[0] for str in os.listdir(dataFolder)]
    
    for lattice in lattices:
        plotFolder=f"plots/autoCorrelationTime/"
        os.makedirs(plotFolder, exist_ok=True)
        plotFile=f"{plotFolder}/{lattice}.png"
        ax[lattice].set_xlabel("mass")
        ax[lattice].title.set_text(f"Autocorrelation time for lattice {lattice}")
        ax[lattice].legend()
        fig[lattice].savefig(plotFile)
        plt.close(fig[lattice])
    break