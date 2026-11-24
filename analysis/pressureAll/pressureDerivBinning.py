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



def getBinned(df, k):
    return df.groupby(df.index //k).mean()
def getAvgAndStdErr(array):
    mean=array.mean()
    std=array.std()/np.sqrt(array.size)
    return mean, std


def getFolders(seed, ignore):
    rawDataFolder=f"rawData/seed{seed}"
    mkdirs(rawDataFolder)
    plotFolder=f"plots/binnedStd/ignore{ignore}"
    mkdirs(plotFolder)
    return rawDataFolder, plotFolder



#observables = ("chi_ud", "chi_ud_binned", "chi_s", "chi_s_binned")
#observableTitles = ("Chi UD", "Chi UD binned", "Chi S", "Chi S binned")

#df_chi={}
#simFolder={}
#array={}



rawDataFolder={}
plotFolder={}  

lattices=("ns_40_nt_16", "ns_40_nt_8")
masses=("ml1.0", "ml0.9", "ml0.8","ml0.7","ml0.6","ml0.5","ml0.4","ml0.3","ml0.2","ml0.1","ml0.075","ml0.05","ml0.04","ml0.03","ml0.025")
ignoreArray=(50, 100, 150, 200, 250)
seeds=[0, 774, 2002, 19210]
observable="chi_ud_binned"

'''
for k in np.arange(50):
    continue
    array[k]={}
    for seed in seeds:
        df_chi[seed]={}
        observable="chi_ud_binned"
        latB="ns_40_nt_16"
        latS="ns_40_nt_8"
        for lattice in (latB, latS):
            df_chi[seed][lattice]=pd.read_csv(f"./rawData/seed{seed}/{lattice}/{observable}.csv")[mass]
            array[lattice]=np.concatenate(getBinned(df_chi[seed][lattice]).to_numpy(), array[lattice])

            df_chi[seed][lattice]=extractAvgAndStd(df_chi[seed][lattice][df_chi[seed][lattice]["measurement"] > ignore])
            


        plt.figure()
        plt.errorbar(dfMasses, df_chi[seed][latS]["mean"]-df_chi[seed][latB]["mean"], np.sqrt(df_chi[seed][latB]["std"]**2+df_chi[seed][latS]["std"]**2)/norm, marker="o")
        plt.savefig(f"{plotFolder[seed]}/vac_sub_{observable}.png")
        plt.xscale('log')
        plt.savefig(f"{plotFolder[seed]}/vac_sub_{observable}Log.png")
        plt.close()
        print( df_chi[seed][latS]["mean"]-df_chi[seed][latB]["mean"])
'''


for ignore in ignoreArray:    
    elementsPerSeed=300-ignore
    for mass in masses:
        for lattice in lattices:
            avg=np.array([])
            stdErr=np.array([]) 
            for k in np.arange(1,elementsPerSeed+1):
                subArray=np.array([])
                for seed in seeds:
                    rawDataFolder[seed], plotFolder = getFolders(seed, ignore)
                    norm=np.sqrt(len(seeds)*elementsPerSeed)
                    df=pd.read_csv(f"./rawData/seed{seed}/{lattice}/{observable}.csv")
                    df=df[df["measurement"]>ignore][mass]
                    subArray=np.append(subArray, getBinned(df, k).to_numpy())
                    
                    
                avgTmp, stdTmp = getAvgAndStdErr(subArray)
                avg=np.append(avg, avgTmp)
                stdErr=np.append(stdErr, stdTmp)  
            plt.figure() 
            x = np.arange(1, elementsPerSeed + 1)

            ticks = x[24::25]
            number_of_bins = elementsPerSeed // ticks
            labels = [
                f"{size}\n({n})"
                for size, n in zip(ticks, number_of_bins)
            ]
            plt.xticks(ticks, labels, rotation=0)
            plt.xlabel("Bin size / Number of bins per seed",
           fontsize=12,
           labelpad=15)

            plt.plot(x, stdErr)
            plt.title(f"Standard Error wrt bin-size; {lattice}, m={mass}")
            #plt.subplots_adjust(bottom=2, top=0.88)
            plt.tight_layout()
            plt.savefig(f"{plotFolder}/{lattice}_{mass}.png")