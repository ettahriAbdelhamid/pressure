import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def mkdirs(path):
    if(not os.path.isdir(path)):
        os.makedirs(path, exist_ok=True)

def getLogFiles(seed, lattice, massFolder):
    #need multiple logfiles, because done multiple simulations
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
    return logFiles


mainFolder="../../"
observables = ("chi_ud", "chi_ud_binned", "chi_s", "chi_s_binned", "polyakov_real", "polyakov_img", "polyakov_abs", "plaquette", "rectangle", "gauge_action")
observableTitles = ("Chi UD", "Chi UD binned", "Chi S", "Chi S binned", "Polyakov Loop real", "Polyakov Loop img", "Polyakov Loop abs", "Plaquette", "Rectangle", "Gauge Action")

#regex to extract chi condensate for light and strange seperately
chi_ud_pattern=r"CHI_UD = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";
chi_s_pattern=r"CHI_S = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";
polyakov_pattern=r"Polyakov Loop = \(([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*), ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)\)"
plaq_pattern=r"Plaquette = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";
rect_pattern=r"Rectangle = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";

m_8_0=(1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3)
m_8_7=(1, 0.9, 0.8, 0.7, 0.6)
seeds=[0, 774, 2002, 19210]
###seeds=[0]

simFolder={}
rawDataFolder={}
lattices={}
###plotFolder={}
#generate folder structure and preparing nested dataframe dictionary
for seed in seeds:
    simFolder[seed]=f"{mainFolder}/simulations/simPressureSeed{seed}/"
    lattices[seed]=os.listdir(simFolder[seed])
    rawDataFolder[seed]=f"rawData/seed{seed}"
    ###plotFolder[seed]=f"plots/chiOverMarkov/seed{seed}"
    ###mkdirs(plotFolder[seed])
    for lattice in lattices[seed]:
        mkdirs(f"{rawDataFolder[seed]}/{lattice}")

df_chi={seed: {lattice: {observable: pd.DataFrame() for observable in observables} for lattice in lattices} for seed in seeds}

#extract data from log to dataframe 
for seed in seeds:
    print(f"Seed: {seed}")
    for lattice in lattices[seed]:
        print(f"Lattice: {lattice}")
        massFolders=sorted(os.listdir(f"{simFolder[seed]}/{lattice}"),key=lambda x: float(x.split("ms_")[1]), reverse=True)
        df = df_chi[seed][lattice]
        #for every mass extract from log files all chi_ud and chi_s values. then insert into dataframe. 
        #then bin over noise vectors(10) and insert in binned dataframe
        for massFolder in massFolders:
            ml=float(massFolder.split("_")[3])
            print(ml)
            ns=int(lattice.split("_")[1])
            nt=int(lattice.split("_")[3])
            
            chi_ud_array=[]
            chi_s_array=[]
            polyakov_real=[]
            polyakov_img=[]
            polyakov_abs=[]
            rectangle=[]
            plaquette=[]
            gauge=[]

            logFiles=getLogFiles(seed, lattice, massFolder)
            for logFile in logFiles:
                with open(logFile) as f:
                    for line in f:
                        match=re.search(chi_ud_pattern, line)
                        if match:
                            chi_ud_array.append(float(match.group(1)))
                        match=re.search(chi_s_pattern, line)
                        if match:
                            chi_s_array.append(float(match.group(1)))
                        match=re.search(plaq_pattern, line)
                        if match:
                            plaquette.append(float(match.group(1)))
                        match=re.search(rect_pattern, line)
                        if match:
                            rectangle.append(float(match.group(1)))                
                        match=re.search(polyakov_pattern, line)
                        if match:
                            polyakov_real.append(float(match.group(1)))
                            polyakov_img.append(float(match.group(2)))
                    polyakov_abs=np.hypot(polyakov_real,polyakov_img)
                    gauge=9*ns**3*nt-10*np.array(plaquette)+np.array(rectangle)
            df["chi_ud"][f"ml{ml}"]=pd.Series(chi_ud_array)
            df["chi_s"][f"ml{ml}"]=pd.Series(chi_s_array)
            df["polyakov_real"][f"ml{ml}"]=pd.Series(polyakov_real)
            df["polyakov_img"][f"ml{ml}"]=pd.Series(polyakov_img)
            df["polyakov_abs"][f"ml{ml}"]=pd.Series(polyakov_abs)
            df["plaquette"][f"ml{ml}"]=pd.Series(plaquette)
            df["rectangle"][f"ml{ml}"]=pd.Series(rectangle)
            df["gauge_action"][f"ml{ml}"]=pd.Series(gauge)

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



#save as csv and plot
for ignore in (0, 50, 100, 150, 200, 250):
    for seed in seeds:
        for lattice in lattices[seed]:
            massFolders=sorted(os.listdir(f"{simFolder[seed]}/{lattice}"),key=lambda x: float(x.split("ms_")[1]), reverse=True)
            for massFolder in massFolders:
                mass=float(massFolder.split("_")[3])
                df = df_chi[seed][lattice]
                for observable, title in zip(observables, observableTitles):
                    df[observable].index.name = "measurement"
                    
                    fig, ax = plt.subplots(figsize=(8, 5))
                    df[observable][df[observable].index > ignore][f"ml{mass}"].plot(ax=ax, title=f"{title} for lattice {lattice}")
                    ax.grid(True)
                    mkdirs(f"{plotFolder[seed]}/ignore{ignore}/ml{mass}")
                    plt.savefig(f"{plotFolder[seed]}/ignore{ignore}/ml{mass}/{lattice}_{observable}.png")
                    plt.xscale('log')
                    plt.savefig(f"{plotFolder[seed]}/ignore{ignore}/ml{mass}/{lattice}_{observable}Log.png")
                    
                    plt.close(fig)