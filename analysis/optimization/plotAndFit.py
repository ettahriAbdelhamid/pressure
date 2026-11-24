import pandas as pd
import numpy as np
import libPlot as lp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os

 

timeConvert=1/(60*20)   #from seconds to minutes per update, in total 20 updates
timeLabel="Minutes per Update"
acceptanceLabel="Acceptance"
ratioLabel="Acceptance per Minute"
residueLabel="Residue of fit"
path="./dataRaw/"
plotsFolder="./plots/"
timePlotsFolder=plotsFolder+"time/"
timeResiudePlotsFolder=plotsFolder+"timeRelFitResidue/"
acceptancePlotsFolder=plotsFolder+"acceptance/"
acceptanceResiudePlotsFolder=plotsFolder+"acceptanceRelFitResidue/"
ratioPlotsFolder=plotsFolder+"acceptancePerTime/"
ratioResiudePlotsFolder=plotsFolder+"acceptancePerTimeRelFitResidue/"

fitParameterFolder="./fitParameter/"
fitDataFolder="./fitData/"

simOptiFolder="../../simulations/simOptimization"
lattices=os.listdir(simOptiFolder)
lattice_titles=[]
for lattice in lattices:
    splitted=lattice.split('_')
    lattice_titles.append(rf"${splitted[1]}^3 \times {splitted[3]}$")
foldersToCreate=[fitParameterFolder, fitDataFolder, plotsFolder,
                timePlotsFolder, timeResiudePlotsFolder,
                acceptancePlotsFolder, acceptanceResiudePlotsFolder,
                ratioPlotsFolder, ratioResiudePlotsFolder]
for folder in foldersToCreate:
    lp.mkdir(folder)
for lattice in lattices:
    lp.mkdir(f"{fitDataFolder}{lattice}")

dfs_time={}
dfs_acceptance={}
dfs_ratio={}
for lattice in lattices:
    full_df=pd.read_csv(f"{path}time_acceptance_{lattice}.csv").sort_values('ml')
    dfs_time[lattice]=lp.prepareDF(full_df, 'time')*timeConvert
    dfs_acceptance[lattice]=lp.prepareDF(full_df, 'acc')
    dfs_ratio[lattice]=lp.prepareDF(full_df, 'ratio')
   


masses=full_df['ml']#full_df is last csv file for last lattice
massRange=range(len(masses))
dfs_time_normed={}
dfs_acceptance_normed={}
dfs_ratio_normed={}

md_array= lp.latticeMassArrayDict(lattices, massRange)
sw_array= lp.latticeMassArrayDict(lattices, massRange)
step_sf_array= lp.latticeMassArrayDict(lattices, massRange)


time_array=lp.latticeMassArrayDict(lattices, massRange)
acc_array=lp.latticeMassArrayDict(lattices, massRange)
fitted_time_array=lp.latticeMassArrayDict(lattices, massRange)
fitted_acc_array=lp.latticeMassArrayDict(lattices, massRange)
label1_array=lp.latticeMassArrayDict(lattices, massRange)
label2_array=lp.latticeMassArrayDict(lattices, massRange)
A=lp.latticeArrayDict(lattices)
B=lp.latticeArrayDict(lattices)
C=lp.latticeArrayDict(lattices)
mMd=lp.latticeArrayDict(lattices)
mStepSf=lp.latticeArrayDict(lattices)
mSw=lp.latticeArrayDict(lattices)
mConst=lp.latticeArrayDict(lattices)

massIndex=0
#copy for normalization

for lattice in lattices:
    print(f"lattice {lattice}")
    for massIndex in massRange:
        print(f"mass: {masses[massIndex]}")
        #get data using only non NaN entries
        for colAcceptance in dfs_acceptance[lattice].columns:
            
            #only add non empty entries in the parameter tables used for fitting
            if(dfs_acceptance[lattice][colAcceptance][massIndex] == dfs_acceptance[lattice][colAcceptance][massIndex]):
                #colTime is the same as colAcceptance but switch 'acceptance' to 'time'
                colTime=f"time_{colAcceptance.split('_',1)[1]}"
                #get parameter from col_name
                splitted=colAcceptance.split('_')
                md=int(splitted[1])
                step_sf=int(splitted[2])
                sw=int(splitted[3])
                #step_sf2 and sw2 are the actual number of updates while step_sf and sw are the ratios
                step_sf2 = md*step_sf
                sw2=sw*step_sf2
                #label[1,2] contains the parameters, once as ratios and once absolute
                #if (step_sf2 <=15):
                #    continue
                label1_array[lattice][massIndex].append(f'{md}:{step_sf}:{sw}')
                label2_array[lattice][massIndex].append(f'{md}_{step_sf2}_{sw2}')

                md_array[lattice][massIndex].append(md)
                sw_array[lattice][massIndex].append(sw2)
                step_sf_array[lattice][massIndex].append(step_sf2)
                acc_array[lattice][massIndex].append(dfs_acceptance[lattice][colAcceptance][massIndex])
                time_array[lattice][massIndex].append(dfs_time[lattice][colTime][massIndex])

        #using data for fitting
        poptAcceptance, pcovAcceptance= curve_fit(lp.expQuadDecayModel2, (md_array[lattice][massIndex], step_sf_array[lattice][massIndex], sw_array[lattice][massIndex]), acc_array[lattice][massIndex] , bounds=(0,np.inf))
        A[lattice][massIndex],B[lattice][massIndex],C[lattice][massIndex] = poptAcceptance
        poptTime, pcovTime= curve_fit(lp.linearModel, (md_array[lattice][massIndex], step_sf_array[lattice][massIndex], sw_array[lattice][massIndex]), time_array[lattice][massIndex])
        mMd[lattice][massIndex], mStepSf[lattice][massIndex], mSw[lattice][massIndex], mConst[lattice][massIndex] = poptTime

        #lp.getOptiParam(A[lattice][massIndex], B[lattice][massIndex], C[lattice][massIndex], mMd[lattice][massIndex], mStepSf[lattice][massIndex], mSw[lattice][massIndex], mConst[lattice][massIndex])
        
        for colAcceptance in dfs_acceptance[lattice].columns:
            #only add non empty entries in the parameter tables used for fitting
            if(dfs_acceptance[lattice][colAcceptance][massIndex] == dfs_acceptance[lattice][colAcceptance][massIndex]):
                #colTime is the same as colAcceptance but switch 'acceptance' to 'time'
                colTime=f"time_{colAcceptance.split('_',1)[1]}"
                #get parameter from col_name
                splitted=colAcceptance.split('_')
                md=int(splitted[1])
                step_sf=int(splitted[2])
                sw=int(splitted[3])
                #step_sf2 and sw2 are the actual number of updates while step_sf and sw are the ratios
                step_sf2 = md*step_sf
                sw2=sw*step_sf2
                #if (step_sf2 <=15):
                #    continue

                fitted_acc_array[lattice][massIndex].append(lp.expQuadDecayModel2((md, step_sf2, sw2), A[lattice][massIndex], B[lattice][massIndex], C[lattice][massIndex]))
                fitted_time_array[lattice][massIndex].append(lp.linearModel((md, step_sf2, sw2), mMd[lattice][massIndex], mStepSf[lattice][massIndex], mSw[lattice][massIndex], mConst[lattice][massIndex]))
            
        df_fitData = pd.DataFrame({
            'label1': label1_array[lattice][massIndex],
            'label2': label2_array[lattice][massIndex],
            'md': md_array[lattice][massIndex],
            'step_sf': step_sf_array[lattice][massIndex],
            'sw': sw_array[lattice][massIndex],
            'time': time_array[lattice][massIndex],
            'fittedTime':fitted_time_array[lattice][massIndex],
            'acceptance': acc_array[lattice][massIndex],
            'fittedAcceptance':fitted_acc_array[lattice][massIndex],
            'ratio': np.array(acc_array[lattice][massIndex])/np.array(time_array[lattice][massIndex]),
            'fittedRatio':np.array(fitted_acc_array[lattice][massIndex])/np.array(fitted_time_array[lattice][massIndex])
        })
        df_fitData.to_csv(f"{fitDataFolder}{lattice}/{masses[massIndex]}.csv")
        
    df_fitParameter=pd.DataFrame({
        'ml': masses,
        'A': A[lattice],
        'B': B[lattice],
        'C': C[lattice],
        'mMd': mMd[lattice],
        'mStepSf': mStepSf[lattice],
        'mSw': mSw[lattice],
        'mConst':mConst[lattice]
    })
    df_fitParameter.to_csv(f"{fitParameterFolder}{lattice}.csv")


numGraphs=len(dfs_time[lattices[0]].columns)
#colors = matplotlib.cm.tab20(range(numGraphs))
colors = plt.cm.hsv(np.linspace(0, 1, numGraphs, endpoint=False))
markers=(".", "v", "s", "*", "d", ">", "<", "x")

for lattice, lattice_title in zip(lattices, lattice_titles):
    dfs_time_normed[lattice] = dfs_time[lattice].copy().astype(float)
    dfs_acceptance_normed[lattice] = dfs_acceptance[lattice].copy().astype(float)
    dfs_ratio_normed[lattice] = dfs_ratio[lattice].copy().astype(float)
    labels=[]
    for colAcceptance in dfs_acceptance[lattice].columns:
        colTime=f"time_{colAcceptance.split('_',1)[1]}"
        colRatio=f"ratio_{colAcceptance.split('_',1)[1]}"
        splitted=colAcceptance.split('_')
        md=int(splitted[1])
        step_sf=int(splitted[2])
        sw=int(splitted[3])
        #step_sf2 and sw2 are the actual number of updates while step_sf and sw are the ratios
        step_sf2 = md*step_sf
        sw2=sw*step_sf2
        labels += [f'{md}:{step_sf}:{sw}, {md}_{step_sf2}_{sw2}']
        for massIndex in massRange:
            acceptanceNorm=lp.expQuadDecayModel2((md, step_sf2, sw2), A[lattice][massIndex], B[lattice][massIndex], C[lattice][massIndex])
            if (acceptanceNorm==0):
                acceptanceNorm=0.001
            timeNorm=lp.linearModel((md, step_sf2, sw2), mMd[lattice][massIndex], mStepSf[lattice][massIndex], mSw[lattice][massIndex], mConst[lattice][massIndex])
            ratioNorm=acceptanceNorm/timeNorm
            #dfs_time_normed[lattice][colTime][massIndex]/=timeNorm
            #dfs_acceptance_normed[lattice][colAcceptance][massIndex]/=acceptanceNorm
            #dfs_ratio_normed[lattice][colRatio][massIndex]*=(timeNorm/acceptanceNorm)
            
            dfs_time_normed[lattice].loc[massIndex,colTime]=(dfs_time_normed[lattice][colTime][massIndex]-timeNorm)#/timeNorm
            dfs_acceptance_normed[lattice].loc[massIndex,colAcceptance]=(dfs_acceptance_normed[lattice][colAcceptance][massIndex]-acceptanceNorm)#/acceptanceNorm
            dfs_ratio_normed[lattice].loc[massIndex,colRatio]=(dfs_ratio_normed[lattice][colRatio][massIndex]-ratioNorm)#/ratioNorm

    lp.plot(
        masses, 
        dfs_time[lattice], 
        f'time_{lattice}', 
        timePlotsFolder,  
        f'{timeLabel} {lattice_title}', 
        labels, colors, markers
    )
    lp.plot(
        masses, 
        dfs_acceptance[lattice], 
        f'acceptance_{lattice}', 
        acceptancePlotsFolder, 
        f'{acceptanceLabel} {lattice_title}', 
        labels, colors, markers
    )
    lp.plot(
        masses, 
        dfs_ratio[lattice], 
        f'acceptancePerTime_{lattice}', 
        ratioPlotsFolder,  
        f'{ratioLabel} {lattice_title}', 
        labels, colors, markers
    )
    lp.plot(
        masses, 
        dfs_time_normed[lattice], 
        f'time_residue_{lattice}', 
        timeResiudePlotsFolder, 
        f'{residueLabel} {timeLabel} {lattice_title}', 
        labels, colors, markers)
    lp.plot(
        masses, 
        dfs_acceptance_normed[lattice], 
        f'acceptance_residue_{lattice}', 
        acceptanceResiudePlotsFolder,  
        f'{residueLabel} {acceptanceLabel} {lattice_title}', 
        labels, colors, markers
    )
    lp.plot(
        masses, 
        dfs_ratio_normed[lattice], 
        f'acceptancePerTime_residue_{lattice}', 
        ratioResiudePlotsFolder,  
        f'{residueLabel} {ratioLabel} {lattice_title}', 
        labels, colors, markers
    )
