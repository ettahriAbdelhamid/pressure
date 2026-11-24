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

















def extractAvgAndStdBinned(df, ignore, lattice, ns, massNorm):
    df=df[df["measurement"]>=ignore]
    autoCorrDf=pd.read_csv(f"autoCorrData/ignore{ignore}/{lattice}.csv")
    #print(df)
    #[ml.split("ml")[1] for ml in df.columns[1:]]
    masses=df.columns[1:]
    avg=np.array([])
    std=np.array([])
    for mass in masses:
        if(massNorm):
            actualMass=float(mass.split("ml")[1])
        else:
            actualMass=1
        raw=df[mass]/((ns**3)*actualMass)
        autoCorrTime=autoCorrDf.loc[autoCorrDf.ml==mass,"autoCorrTime"].item()
        n_eff=autoCorrDf.loc[autoCorrDf.ml==mass,"N_eff"].item()
        n=autoCorrDf.loc[autoCorrDf.ml==mass,"N"].item()
        elemPerBin=np.ceil(n/max(np.floor(n_eff),1))
        #print(raw)
        #print(raw.groupby(raw.index //np.floor(n_eff)))
        #print(n_eff)
        #mighht cause bias if last bin smaller
        #avgTmp = raw.groupby(raw.index //elemPerBin).mean().mean()
        avgTmp = raw.mean()
        binned = raw.groupby(raw.index //elemPerBin).mean()
        stdTmp = binned.std()/np.sqrt(len(binned))
        #print(avgTmp)
        #print(avgTmp.mean())
        avg=np.append(avg, avgTmp)
        std=np.append(std, stdTmp)
        #exit(1)
    return pd.DataFrame({'ml': masses, 'mean': avg, 'std': std})















def mkdir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)
def mkdirs(path):
    if(not os.path.isdir(path)):
        os.makedirs(path, exist_ok=True)


observables = ("chi_ud", "chi_ud_binned", "chi_s", "chi_s_binned")
observableTitles = ("Chi UD", "Chi UD binned", "Chi S", "Chi S binned")
observable="chi_ud_binned"
latBArray=("ns_16_nt_16", "ns_24_nt_16", "ns_32_nt_16", "ns_40_nt_16")
latSArray=("ns_16_nt_8", "ns_24_nt_8", "ns_32_nt_8", "ns_40_nt_8")
latSpaceArray=("ns_16", "ns_24", "ns_32", "ns_40")


ignoreArray=(50, 100, 150, 200, 250)




for massNorm in (True, False):
    for ignore in ignoreArray:
        plt.figure()
        fig_vac_sub, ax_vac_sub = plt.subplots()
        fig_vac_sub_log, ax_vac_sub_log = plt.subplots()
    

        df_chi={}
        simFolder={}
        rawDataFolder={}
        lattices={}
        plotFolder={}
        #generate folder structure and preparing nested dataframe dictionary
        rawDataFolder=f"rawData"
        plotFolder=f"plots/chi/chiIgnore{ignore}"
        if(massNorm):
            plotFolder=f"plots/chiMassNorm/chiIgnore{ignore}"
        else:
            plotFolder=f"plots/chi/chiIgnore{ignore}"
        mkdirs(rawDataFolder)
        mkdirs(plotFolder)


        df_chi={}


        for latB, latS, latSpace in zip(latBArray, latSArray, latSpaceArray):
            #print(latB +" "+ latS)
            dfMasses={}
            
            for lattice in (latS, latB):
                ns=int(latS.split("_")[1])
                df_chi[lattice]=pd.read_csv(f"./rawData/{lattice}/{observable}.csv")
                #print(df_chi[lattice].index)
                #df_chi[lattice] = extractAvgAndStdBinned(df_chi[lattice], ignore, lattice, ns)
                df_chi[lattice] = extractAvgAndStdBinned(df_chi[lattice], ignore, lattice, 1, massNorm)
                dfMasses=extractMasses(df_chi[lattice]["ml"])
                #dfMasses=extractMasses(df_chi[lattice].index)
                
                
                #print("df is")
                #print(df_chi[lattice])
                #print("masses are")
                #print(dfMasses)
                #print("with index")
                #print(df_chi[lattice].index)

                plt.figure()
                plt.errorbar(dfMasses, df_chi[lattice]["mean"], df_chi[lattice]["std"], marker="o")
                plt.title(f"Chi_UD for {lattice} ignoring first {ignore}")
                plt.savefig(f"{plotFolder}/{lattice}_{observable}.png")
                plt.xscale('log')
                plt.savefig(f"{plotFolder}/{lattice}_{observable}Log.png")
                plt.close()


            vac_sub = df_chi[latS]["mean"] - df_chi[latB]["mean"]
            vac_sub_err = np.sqrt(
                df_chi[latB]["std"]**2 + df_chi[latS]["std"]**2
            )

            # Individual plots
            plt.figure()
            plt.errorbar(dfMasses, vac_sub, vac_sub_err, marker="o")
            plt.title(f"Vaccum subtracted Chi_UD for {latSpace} ignoring first {ignore}")
            plt.savefig(f"{plotFolder}/{latSpace}_vac_sub_{observable}.png")
            plt.xscale('log')
            plt.savefig(f"{plotFolder}/{latSpace}_vac_sub_{observable}Log.png")
            plt.close()

        # print(dfMasses)
        # print(df_chi[latS]["mean"]-df_chi[latB]["mean"])


            ax_vac_sub.errorbar(
                dfMasses, vac_sub, vac_sub_err,
                marker="o", label=latSpace
            )

            ax_vac_sub_log.errorbar(
                dfMasses, vac_sub, vac_sub_err,
                marker="o", label=latSpace
            )


        # Configure and save combined linear plot
        ax_vac_sub.set_xlabel("Mass")
        ax_vac_sub.set_ylabel("Chi_UD")
        ax_vac_sub.legend()
        ax_vac_sub.title.set_text(f"Vaccum subtracted Chi_UD ignoring first {ignore}")
        fig_vac_sub.savefig(f"{plotFolder}/all_vac_sub_{observable}.png")
        # Configure and save combined log plot
        ax_vac_sub_log.set_xscale("log")
        ax_vac_sub_log.set_xlabel("Mass")
        ax_vac_sub_log.set_ylabel("Chi_UD")
        ax_vac_sub_log.legend()
        ax_vac_sub_log.title.set_text(f"Chi_UD ignoring first {ignore}")
        fig_vac_sub_log.savefig(f"{plotFolder}/all_vac_sub_{observable}Log.png")

        plt.close(fig_vac_sub)
        plt.close(fig_vac_sub_log)



