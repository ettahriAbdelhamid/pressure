import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
import os
import re
import sys

def mkdir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)

mainFolder="../../"
simFolder=f"{mainFolder}/simulations/simThermalization/"
rawDataFolder="rawData"
plotFolder="plots"
mkdir(rawDataFolder)
mkdir(plotFolder)

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
    massFolders=os.listdir(f"{simFolder}/{lattice}")
    for massFolder in massFolders:
        ml=massFolder.split("_")[3]
        print(f"Mass: {ml}")
        mdFolders=os.listdir(f"{simFolder}/{lattice}/{massFolder}")
        for mdFolder in mdFolders:
            if mdFolder == "md100":
                md=100
            elif mdFolder == "md50":
                md=50
            else:
                print("No idea how this is possible")
                exit(1)
            print(f"number of md steps: {md}")
            chi_ud_array=[]
            chi_s_array=[]
            logFile=f"{simFolder}/{lattice}/{massFolder}/{mdFolder}/doc/log.log"
            with open(logFile) as f:
                for line in f:
                    match=re.search(chi_ud_pattern, line)
                    if match:
                        chi_ud_array.append(float(match.group(1)))
                    match=re.search(chi_s_pattern, line)
                    if match:
                        chi_s_array.append(float(match.group(1)))
            df_chi_ud[lattice][f"ml{ml}_md{md}"]=pd.Series(chi_ud_array)
            df_chi_ud_binned[lattice] = df_chi_ud[lattice].groupby(df_chi_ud[lattice].index //10).mean()
            df_chi_s[lattice][f"ml{ml}_md{md}"]=pd.Series(chi_s_array)
            df_chi_s_binned[lattice] = df_chi_s[lattice].groupby(df_chi_s[lattice].index //10).mean()
    df_chi_ud[lattice].to_csv(f"{rawDataFolder}/{lattice}/chiUD.csv")
    df_chi_ud_binned[lattice].to_csv(f"{rawDataFolder}/{lattice}/chiUD_binned.csv")
    df_chi_s[lattice].to_csv(f"{rawDataFolder}/{lattice}/chiS.csv")
    df_chi_s_binned[lattice].to_csv(f"{rawDataFolder}/{lattice}/chiS_binned.csv")

    plt.figure()
    df_chi_ud[lattice].plot(title = f"Thermalization of Chi UD for lattice {lattice}")
    plt.grid()
    plt.savefig(f"{plotFolder}/{lattice}_chiUD.png")
    plt.close()

    plt.figure()
    df_chi_ud_binned[lattice].plot(title = f"Thermalization of Chi UD for lattice {lattice} Binned")
    plt.grid()
    plt.savefig(f"{plotFolder}/binned_{lattice}_chiUD.png")
    plt.close()

    plt.figure()
    df_chi_s[lattice].plot(title = f"Thermalization of Chi S for lattice {lattice}")
    plt.grid()
    plt.savefig(f"{plotFolder}/{lattice}_chiS.png")
    plt.close()

    plt.figure()
    df_chi_s_binned[lattice].plot(title = f"Thermalization of Chi S for lattice {lattice} Binned")
    plt.grid()
    plt.savefig(f"{plotFolder}/binned_{lattice}_chiS.png")
    plt.close()