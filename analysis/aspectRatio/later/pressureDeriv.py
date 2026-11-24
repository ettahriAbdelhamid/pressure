import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def plot(masses, df, filename, title, start=0, end=0, startLog=0, endLog=0):
    
    cols = [col for col in df.columns if col.startswith('Ns') and 'err' not in col]

    def generate_plot(is_log=False):
        plt.figure()
        if (is_log):
            s=startLog
            e=endLog
        else:
            s=start
            e=end
        for col in cols:
            err = f"{col}_err"
            if(e==0):
                plt.errorbar(
                    masses[s:], 
                    df[col].iloc[s:],
                    df[err].iloc[s:],
                    label=col,
                    fmt="-o"
                )
            else:
                plt.errorbar(
                    masses[s:-e], 
                    df[col].iloc[s:-e],
                    df[err].iloc[s:-e],
                    label=col,
                    fmt="-o"
                ) 
            
        plt.legend()
        plt.xlabel("masses")
        plt.axhline(0)
        plt.axvline(0.025)
        plt.title(title)
        if (is_log):
            plt.xscale('log')
            plt.savefig(f"plots/chiPlotsLog/{filename}Log.png")
            
        else:
            plt.savefig(f"plots/chiPlots/{filename}.png")

    generate_plot(False)
    generate_plot(True)


def extractMasses(index):
    return [float(s.split("ml")[1]) for s in index]

def extractAvgAndStd(df):
    return(df.agg(['mean', 'std']).drop("measurement", axis=1).T)






def mkdir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)
def mkdirs(path):
    if(not os.path.isdir(path)):
        os.makedirs(path, exist_ok=True)

ignore=250
norm=np.sqrt(300-ignore)
seeds=[0, 774, 2002, 19210]
seeds=[0]
observables = ("chi_ud", "chi_ud_binned", "chi_s", "chi_s_binned")
observableTitles = ("Chi UD", "Chi UD binned", "Chi S", "Chi S binned")

df_chi={}
simFolder={}
rawDataFolder={}
lattices={}
plotFolder={}
#generate folder structure and preparing nested dataframe dictionary
for seed in seeds:
    #prepare paths and create folders: rawData and plots (and subfolders) for iterated seed
    
    rawDataFolder[seed]=f"rawData/seed{seed}"
    plotFolder[seed]=f"plots/pressureDerivativeIgnore{ignore}/seed{seed}"
    mkdirs(rawDataFolder[seed])
    mkdirs(plotFolder[seed])
    

df_chi={}
df_all_seeds={}

for seed in seeds:
    df_chi[seed]={}

    observable="chi_ud_binned"
    latB="ns_40_nt_16"
    latS="ns_40_nt_8"
    for lattice in (latB, latS):
        df_chi[seed][lattice]=pd.read_csv(f"./rawData/seed{seed}/{lattice}/{observable}.csv")
        df_chi[seed][lattice]=extractAvgAndStd(df_chi[seed][lattice][df_chi[seed][lattice]["measurement"] > ignore])
        dfMasses=extractMasses(df_chi[seed][lattice].index)
        plt.figure()
        plt.errorbar(dfMasses, df_chi[seed][lattice]["mean"], df_chi[seed][lattice]["std"]/norm, marker="o")
        plt.savefig(f"{plotFolder[seed]}/{lattice}_{observable}.png")
        plt.xscale('log')
        plt.savefig(f"{plotFolder[seed]}/{lattice}_{observable}Log.png")
        plt.close()


    plt.figure()
    plt.errorbar(dfMasses, df_chi[seed][latS]["mean"]-df_chi[seed][latB]["mean"], np.sqrt(df_chi[seed][latB]["std"]**2+df_chi[seed][latS]["std"]**2)/norm, marker="o")
    plt.savefig(f"{plotFolder[seed]}/vac_sub_{observable}.png")
    plt.xscale('log')
    plt.savefig(f"{plotFolder[seed]}/vac_sub_{observable}Log.png")
    plt.close()
    print( df_chi[seed][latS]["mean"]-df_chi[seed][latB]["mean"])





