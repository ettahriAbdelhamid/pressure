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
seeds=[0, 774, 2002, 19210]
for seed in seeds:

    simFolder=f"{mainFolder}/simulations/simPressureSeed{seed}/"
    rawDataFolder=f"rawData/seed{seed}"
    plotFolder=f"plots/chi/seed{seed}"
    mkdirs(rawDataFolder)
    mkdirs(plotFolder)

    lattices=os.listdir(simFolder)
    df_chi_ud={}
    df_chi_ud_binned={}
    df_chi_s={}
    df_chi_s_binned={}
    for lattice in lattices:
        mkdir(f"{rawDataFolder}/{lattice}")
        df_chi_ud[lattice] = pd.DataFrame()
        df_chi_ud_binned[lattice] = pd.DataFrame()
        df_chi_s[lattice] = pd.DataFrame()
        df_chi_s_binned[lattice] = pd.DataFrame()

    chi_ud_pattern=r"CHI_UD = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";
    chi_s_pattern=r"CHI_S = ([+-]?[0-9]*[.][0-9]*e*[+-]?[0-9]*)";

    for lattice in lattices:
        print(f"Lattice: {lattice}")
        massFolders=sorted(os.listdir(f"{simFolder}/{lattice}"),key=lambda x: float(x.split("ms_")[1]), reverse=True)
        
        for massFolder in massFolders:
            ml=massFolder.split("_")[3]
            print(f"Mass: {ml}")
        
            chi_ud_array=[]
            chi_s_array=[]
            logFile=f"{simFolder}/{lattice}/{massFolder}/std/doc/log.log"
            with open(logFile) as f:
                for line in f:
                    match=re.search(chi_ud_pattern, line)
                    if match:
                        chi_ud_array.append(float(match.group(1)))
                    match=re.search(chi_s_pattern, line)
                    if match:
                        chi_s_array.append(float(match.group(1)))
            df_chi_ud[lattice][f"ml{ml}"]=pd.Series(chi_ud_array)
            df_chi_ud_binned[lattice] = df_chi_ud[lattice].groupby(df_chi_ud[lattice].index //10).mean()
            df_chi_s[lattice][f"ml{ml}"]=pd.Series(chi_s_array)
            df_chi_s_binned[lattice] = df_chi_s[lattice].groupby(df_chi_s[lattice].index //10).mean()
        
        df_chi_ud[lattice].index.name = "measurement"
        df_chi_ud_binned[lattice].index.name = "measurement"
        df_chi_s[lattice].index.name = "measurement"
        df_chi_s_binned[lattice].index.name = "measurement"


        df_chi_ud[lattice].to_csv(f"{rawDataFolder}/{lattice}/chiUD.csv")
        df_chi_ud_binned[lattice].to_csv(f"{rawDataFolder}/{lattice}/chiUD_binned.csv")
        df_chi_s[lattice].to_csv(f"{rawDataFolder}/{lattice}/chiS.csv")
        df_chi_s_binned[lattice].to_csv(f"{rawDataFolder}/{lattice}/chiS_binned.csv")

        plt.figure()
        df_chi_ud[lattice].plot(title = f"Chi UD for lattice {lattice}")
        plt.grid()
        plt.savefig(f"{plotFolder}/{lattice}_chiUD.png")
        plt.close()

        plt.figure()
        df_chi_ud_binned[lattice].plot(title = f"Chi UD for lattice {lattice} Binned")
        plt.grid()
        plt.savefig(f"{plotFolder}/binned_{lattice}_chiUD.png")
        plt.close()

        plt.figure()
        df_chi_s[lattice].plot(title = f"Chi S for lattice {lattice}")
        plt.grid()
        plt.savefig(f"{plotFolder}/{lattice}_chiS.png")
        plt.close()

        plt.figure()
        df_chi_s_binned[lattice].plot(title = f"Chi S for lattice {lattice} Binned")
        plt.grid()
        plt.savefig(f"{plotFolder}/binned_{lattice}_chiS.png")
        plt.close()