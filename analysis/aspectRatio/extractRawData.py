import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def mkdirs(path):
    if(not os.path.isdir(path)):
        os.makedirs(path, exist_ok=True)

mainFolder="../../"
observables = ("chi_ud", "chi_ud_binned", "chi_s", "chi_s_binned", "polyakov_real", "polyakov_img", "polyakov_abs", "plaquette", "rectangle", "gauge_action")
observableTitles = ("Chi UD", "Chi UD binned", "Chi S", "Chi S binned", "Polyakov Loop real", "Polyakov Loop img", "Polyakov Loop abs", "Plaquette", "Rectangle", "Gauge Action")

#regex to extract chi condensate for light and strange seperately
chi_ud_pattern=r"CHI_UD = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";
chi_s_pattern=r"CHI_S = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";
polyakov_pattern=r"Polyakov Loop = \(([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*), ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)\)"
plaq_pattern=r"Plaquette = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";
rect_pattern=r"Rectangle = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";

#generate folder structure and preparing nested dataframe dictionary
#prepare paths and create folders: rawData and plots (and subfolders)
simFolder=f"{mainFolder}/simulations/aspectRatioAnalysis/"
rawDataFolder=f"rawData/"

lattices=os.listdir(simFolder)
df_chi={}
for lattice in lattices:
    mkdirs(f"{rawDataFolder}/{lattice}")
    df_chi[lattice]={observable: pd.DataFrame() for observable in observables}

#extract data from log to dataframe 
for lattice in lattices:
    print(f"Lattice: {lattice}")
    massFolders=sorted(os.listdir(f"{simFolder}/{lattice}"),key=lambda x: float(x.split("ms_")[1]), reverse=True)
    df = df_chi[lattice]
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
        logFile=f"{simFolder}/{lattice}/{massFolder}/std/doc/log.log"
        if not os.path.isfile(logFile):
            continue
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

#save as csv 
for lattice in lattices:
    df = df_chi[lattice]
    for observable, title in zip(observables, observableTitles):
        df[observable].index.name = "measurement"
        print(f"Saving {rawDataFolder}/{lattice}/{observable}.csv")
        df[observable].to_csv(f"{rawDataFolder}/{lattice}/{observable}.csv")
