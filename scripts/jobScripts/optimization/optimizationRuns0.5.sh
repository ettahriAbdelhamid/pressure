#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:8
#SBATCH --partition=volta_compute --qos=regular
#SBATCH --job-name=optimizationMass5
#SBATCH --output=./%x_%j.out
#SBATCH --mail-user=abdelhamid.ettahri@stud.tu-darmstadt.de --mail-type=ALL

ml=0.5
ms=0.5

#mainPath="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
mainPath="/work/home/aettahri/simQcd/data" 
generalConfFolder="/work/conf/aettahri"
rhmcScriptFile="${mainPath}/rhmc.sh"
simInputFolder="${mainPath}/simInputFiles"
mkdir -p $simInputFolder

configFolder="${generalConfFolder}/configsOpti"
randFolder="${generalConfFolder}/randOpti"
mkdir -p $configFolder
mkdir -p $randFolder
startConfigFolder="${generalConfFolder}/configs"
startRandFolder="${generalConfFolder}/rand"

#masses2p1_light=($ml)
#masses2p1_strange=($ms)
#masses3=()

masses2p1_light=()
masses2p1_strange=()
masses3=($ml)


nsArray=(40)
ntArray=(16 8)
beta=7.373
maxCG=20000
newRand=1
seed=0
loadConf=2
confNum=50
writeEvery=30
nodeX=1
nodeY=1
nodeZ=1
nodeT=1
numUpdate=20
simFolderName="simOptimization"
noSkipMetro=0

create_simInput_content(){
    printf "latS=$ns\nlatT=$nt\nmassL=$ml\nmassS=$ms\nbeta=$beta\nnodeX=$nodeX\nnodeY=$nodeY\nnodeZ=$nodeZ\nnodeT=$nodeT\n"
    printf "stepSize=$stepSize\nnumStepTraj=$numStepTraj\nnumStepStrangeInt=$numStepStrangeInt\nnumStepGaugeInt=$numStepGaugeInt\n"
    printf "maxCG=$maxCG\nnewRand=$newRand #new=0 and read=1\nstartRandPath=$startRandPath\nrandPath=$randPath\nseed=$seed\n"
    printf "loadConf=$loadConf #(0=identity, 1=random, 2=getconf)\nstartGaugePath=$startGaugePath\ngaugePath=$gaugePath\n"
    printf "confNum=$confNum\nnumUpdate=$numUpdate\nwriteEvery=$writeEvery\nsimFolderName=$simFolderName\nnoSkipMetro=$noSkipMetro"

}
#progressFile="progress_m${ml}.txt"
#touch $progressFile

#numStepArray=(22 8 22 18 6 19)
#numStepStrangeIntArray=(1 8 2 1 8 2)
#glueFactorArray=(11 7 9 22 8 10)
#stepSizeArray=(0.0455 0.125 0.0455 0.056 0.167 0.053)


numStepArray=(17 6 7 16 6)
numStepStrangeIntArray=(2 7 7 3 7)
glueFactorArray=(6 4 4 5 5)
stepSizeArray=(0.059 0.167 0.143 0.0625 0.167)


for ns in "${nsArray[@]}"; do
#printf "ns=${ns} " >> $progressFile
    for nt in "${ntArray[@]}"; do
        #echo "nt=${nt}: ">> $progressFile
        for numStepIndex in "${!numStepArray[@]}"; do
            numStepTraj=${numStepArray[$numStepIndex]}
            stepSize=${stepSizeArray[$numStepIndex]}
            numStepGaugeInt=${glueFactorArray[$numStepIndex]}
            numStepStrangeInt=${numStepStrangeIntArray[$numStepIndex]}
            #echo "md_${numStepTraj}_stepSf_${numStepStrangeInt}_sw_${numStepGaugeInt}">> $progressFile
                
            for m in "${masses3[@]}"; do
                ml=$m
                ms=$m

                
                testFolder="simulations/$simFolderName/ns_${ns}_nt_${nt}/beta_7.373_ml_${ml}_ms_${ms}_opti_${numStepTraj}_${numStepStrangeInt}_${numStepGaugeInt}"
                if [ ! -d $testFolder ] || [ "$(wc -l < "${testFolder}/std/doc/log.log")" -lt 2000 ];  then 
                    echo "${testFolder} exists NOT or probably cancelled"
                
                startRandPath="$startRandFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_md50_"$confNum
                startGaugePath="$startConfigFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_md50_"$confNum
                gaugePath="$configFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_md_${numStepTraj}_stepSf_${numStepStrangeInt}_sw_${numStepGaugeInt}_"
                randPath="$randFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_md_${numStepTraj}_stepSf_${numStepStrangeInt}_sw_${numStepGaugeInt}_"
                simInputFile="${simInputFolder}/ns_${ns}_nt_${nt}_ml_${ml}_ms_${ms}_md_${numStepTraj}_stepSf_${numStepStrangeInt}_sw_${numStepGaugeInt}"
                echo "$(create_simInput_content)" > $simInputFile
                bash $rhmcScriptFile $simInputFile &
                fi
            done

            for mIndex in "${!masses2p1_light[@]}"; do
                ml=${masses2p1_light[${mIndex}]}
                ms=${masses2p1_strange[${mIndex}]}
                
                
                testFolder="simulations/$simFolderName/ns_${ns}_nt_${nt}/beta_7.373_ml_${ml}_ms_${ms}_opti_${numStepTraj}_${numStepStrangeInt}_${numStepGaugeInt}"
                if [ ! -d $testFolder ] || [ "$(wc -l < "${testFolder}/std/doc/log.log")" -lt 2000 ];  then 
                    echo "${testFolder} exists NOT or probably cancelled"
                
                
                startRandPath="$startRandFolder/l${ns}${nt}f21b${beta}ml${ml}ms${ms}_md50_"$confNum
                startGaugePath="$startConfigFolder/l${ns}${nt}f21b${beta}ml${ml}ms${ms}_md50_"$confNum
                gaugePath="$configFolder/l${ns}${nt}f21b${beta}ml${ml}ms${ms}_md_${numStepTraj}_stepSf_${numStepStrangeInt}_sw_${numStepGaugeInt}_"
                randPath="$randFolder/l${ns}${nt}f21b${beta}ml${ml}ms${ms}_md_${numStepTraj}_stepSf_${numStepStrangeInt}_sw_${numStepGaugeInt}_"
                simInputFile="${simInputFolder}/ns_${ns}_nt_${nt}_ml_${ml}_ms_${ms}_md_${numStepTraj}_stepSf_${numStepStrangeInt}_sw_${numStepGaugeInt}"
                echo "$(create_simInput_content)" > $simInputFile
                bash $rhmcScriptFile $simInputFile &
                fi
            done
        done
    done
done
wait
