import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def mkdirs(path):
    if(not os.path.isdir(path)):
        os.makedirs(path, exist_ok=True)

def getLogFiles(seed, lattice, massFolder, nt):
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


simFolder={seed: f"{mainFolder}/simulations/simPressureSeed{seed}/" for seed in seeds}

lattices=os.listdir(simFolder[seeds[0]])
rawDataFolder=f"rawData/"
massFolders=sorted(os.listdir(f"{simFolder[seeds[0]]}/{lattices[0]}"),key=lambda x: float(x.split("ms_")[1]), reverse=True)
for lattice in lattices:
    mkdirs(f"{rawDataFolder}/{lattice}")

df_chi={lattice: {observable: pd.DataFrame() for observable in observables} for lattice in lattices}
chi_ud_array={lattice: {massFolder: [] for massFolder in massFolders} for lattice in lattices}
chi_s_array={lattice: {massFolder: [] for massFolder in massFolders} for lattice in lattices}
polyakov_real={lattice: {massFolder: [] for massFolder in massFolders} for lattice in lattices}
polyakov_img={lattice: {massFolder: [] for massFolder in massFolders} for lattice in lattices}
polyakov_abs={lattice: {massFolder: [] for massFolder in massFolders} for lattice in lattices}
rectangle={lattice: {massFolder: [] for massFolder in massFolders} for lattice in lattices}
plaquette={lattice: {massFolder: [] for massFolder in massFolders} for lattice in lattices}
gauge={lattice: {massFolder: [] for massFolder in massFolders} for lattice in lattices}



#extract data from log to array
for seed in seeds:
    print(f"Seed: {seed}")
    for lattice in lattices:
        print(f"Lattice: {lattice}")
        #for every mass extract from log files all chi_ud and chi_s values. then insert into dataframe. 
        #then bin over noise vectors(10) and insert in binned dataframe
        for massFolder in massFolders:
            ml=float(massFolder.split("_")[3])
            print(ml)
            nt=int(lattice.split("_")[3]) 
            logFiles=getLogFiles(seed, lattice, massFolder, nt)
            for logFile in logFiles:
                with open(logFile) as f:
                    for line in f:
                        match=re.search(chi_ud_pattern, line)
                        if match:
                            chi_ud_array[lattice][massFolder].append(float(match.group(1)))
                        match=re.search(chi_s_pattern, line)
                        if match:
                            chi_s_array[lattice][massFolder].append(float(match.group(1)))
                        match=re.search(plaq_pattern, line)
                        if match:
                            plaquette[lattice][massFolder].append(float(match.group(1)))
                        match=re.search(rect_pattern, line)
                        if match:
                            rectangle[lattice][massFolder].append(float(match.group(1)))                
                        match=re.search(polyakov_pattern, line)
                        if match:
                            polyakov_real[lattice][massFolder].append(float(match.group(1)))
                            polyakov_img[lattice][massFolder].append(float(match.group(2)))



#save as dataframe
for lattice in lattices:
    df = df_chi[lattice]
    for massFolder in massFolders:     
        ml=float(massFolder.split("_")[3])
        print(ml)
        ns=int(lattice.split("_")[1])
        nt=int(lattice.split("_")[3]) 
        polyakov_abs[lattice][massFolder]=np.hypot(polyakov_real[lattice][massFolder],polyakov_img[lattice][massFolder])
        gauge[lattice][massFolder]=9*ns**3*nt-10*np.array(plaquette[lattice][massFolder])+np.array(rectangle[lattice][massFolder])
        df["chi_ud"][f"ml{ml}"]=pd.Series(chi_ud_array[lattice][massFolder])
        df["chi_s"][f"ml{ml}"]=pd.Series(chi_s_array[lattice][massFolder])
        df["polyakov_real"][f"ml{ml}"]=pd.Series(polyakov_real[lattice][massFolder])
        df["polyakov_img"][f"ml{ml}"]=pd.Series(polyakov_img[lattice][massFolder])
        df["polyakov_abs"][f"ml{ml}"]=pd.Series(polyakov_abs[lattice][massFolder])
        df["plaquette"][f"ml{ml}"]=pd.Series(plaquette[lattice][massFolder])
        df["rectangle"][f"ml{ml}"]=pd.Series(rectangle[lattice][massFolder])
        df["gauge_action"][f"ml{ml}"]=pd.Series(gauge[lattice][massFolder])

    #after finishing extraction for all masses, bin for ud and s at once
    df["chi_ud_binned"] = df["chi_ud"].groupby(df["chi_ud"].index //10).mean()
    df["chi_s_binned"] = df["chi_s"].groupby(df["chi_s"].index //10).mean()



#save as csv
for lattice in lattices:
    df = df_chi[lattice]
    for observable, title in zip(observables, observableTitles):
        df[observable].index.name = "measurement"
        print(f"Creating {rawDataFolder}/{lattice}/{observable}.csv")
        df[observable].to_csv(f"{rawDataFolder}/{lattice}/{observable}.csv")
            
