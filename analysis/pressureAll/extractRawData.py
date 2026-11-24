import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
import os
import re
import sys

def mkdir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)
def mkdirs(path):
    if(not os.path.isdir(path)):
        os.makedirs(path, exist_ok=True)

mainFolder="../../"


m_8_0=(1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3)
m_8_7=(1, 0.9, 0.8, 0.7, 0.6)



seeds=[0, 774, 2002, 19210]
seeds=[0]
observables = ("chi_ud", "chi_ud_binned", "chi_s", "chi_s_binned")
observableTitles = ("Chi UD", "Chi UD binned", "Chi S", "Chi S binned")

#regex to extract chi condensate for light and strange seperately
chi_ud_pattern=r"CHI_UD = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";
chi_s_pattern=r"CHI_S = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";

df_chi={}
simFolder={}
rawDataFolder={}
lattices={}
plotFolder={}
#generate folder structure and preparing nested dataframe dictionary
for seed in seeds:
    #prepare paths and create folders: rawData and plots (and subfolders) for iterated seed
    simFolder[seed]=f"{mainFolder}/simulations/simPressureSeed{seed}/"
    rawDataFolder[seed]=f"rawData/seed{seed}"
    plotFolder[seed]=f"plots/chi/seed{seed}"
    mkdirs(rawDataFolder[seed])
    mkdirs(plotFolder[seed])

    lattices[seed]=os.listdir(simFolder[seed])
    df_chi[seed]={}
    for lattice in lattices[seed]:
        mkdir(f"{rawDataFolder[seed]}/{lattice}")
        df_chi[seed][lattice]={observable: pd.DataFrame() for observable in observables}










#extract data from log to dataframe 
for seed in seeds:
    print(f"Seed: {seed}")
    for lattice in lattices[seed]:
        print(f"Lattice: {lattice}")
        massFolders=sorted(os.listdir(f"{simFolder[seed]}/{lattice}"),key=lambda x: float(x.split("ms_")[1]), reverse=True)
        #short reference
        df = df_chi[seed][lattice]
        #for every mass extract from log files all chi_ud and chi_s values. then insert into dataframe. 
        #then bin over noise vectors(10) and insert in binned dataframe
        for massFolder in massFolders:
            ml=float(massFolder.split("_")[3])
            print(ml)
            nt=int(lattice.split("_")[3])
            
            chi_ud_array=[]
            chi_s_array=[]
            logFileTemp=f"{simFolder[seed]}/{lattice}/{massFolder}/std"
            logEnd="/doc/log.log"
            
            if(nt == 16):
                if(ml in m_8_0):
                    logFiles=(f"{logFileTemp}{logEnd}", f"{logFileTemp}2{logEnd}")
                elif(ml == 0.2):
                    logFiles=(f"{logFileTemp}{logEnd}", f"{logFileTemp}3{logEnd}", f"{logFileTemp}4{logEnd}")
                   
                else:
                    logFiles=(f"{logFileTemp}3{logEnd}", f"{logFileTemp}4{logEnd}")
            else:
                if(seed==19210):
                    logFiles=(f"{logFileTemp}{logEnd}", f"{logFileTemp}3{logEnd}")
                elif(seed in (0, 2002)):
                    if(ml in m_8_0):
                        logFiles=(f"{logFileTemp}{logEnd}", f"{logFileTemp}2{logEnd}")
                    else:
                        logFiles=(f"{logFileTemp}{logEnd}", f"{logFileTemp}3{logEnd}")
                else:
                    if(ml in m_8_7):
                        logFiles=(f"{logFileTemp}{logEnd}", f"{logFileTemp}2{logEnd}")
                    else:
                        logFiles=(f"{logFileTemp}{logEnd}", f"{logFileTemp}3{logEnd}")
            for logFile in logFiles:
                with open(logFile) as f:
                    for line in f:
                        match=re.search(chi_ud_pattern, line)
                        if match:
                            chi_ud_array.append(float(match.group(1)))
                        match=re.search(chi_s_pattern, line)
                        if match:
                            chi_s_array.append(float(match.group(1)))
            df["chi_ud"][f"ml{ml}"]=pd.Series(chi_ud_array)
            df["chi_s"][f"ml{ml}"]=pd.Series(chi_s_array)

        #after finishing extraction for all masses, bin for ud and s at once
        df["chi_ud_binned"] = df["chi_ud"].groupby(df["chi_ud"].index //10).mean()
        df["chi_s_binned"] = df["chi_s"].groupby(df["chi_s"].index //10).mean()














#save as csv and plot
for seed in seeds:
    for lattice in lattices[seed]:
        df = df_chi[seed][lattice]
        for observable, title in zip(observables, observableTitles):
            df[observable].index.name = "measurement"
            print(f"The file is ....{rawDataFolder[seed]}/{lattice}/{observable}.csv")
            df[observable].to_csv(f"{rawDataFolder[seed]}/{lattice}/{observable}.csv")
            
            fig, ax = plt.subplots(figsize=(8, 5))
            df[observable].plot(ax=ax, title=f"{title} for lattice {lattice}")
            ax.grid(True)
            
            plt.savefig(f"{plotFolder[seed]}/{lattice}_{observable}.png")
            plt.close(fig)