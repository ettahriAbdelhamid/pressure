#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --partition=volta_compute --qos=regular
#SBATCH --job-name=thermalizationBeta7825
#SBATCH --output=./%x_%j.out
#SBATCH --mail-user=abdelhamid.ettahri@stud.tu-darmstadt.de --mail-type=ALL
#SBATCH --exclude=v16

#ml=0.5
#ms=0.5

#mainPath="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
mainPath="/work/home/aettahri/simQcd/data" 
generalConfFolder="/work/conf/aettahri"
rhmcScriptFile="${mainPath}/rhmc.sh"
simInputFolder="${mainPath}/simInputFiles"
mkdir -p $simInputFolder

configFolder="${generalConfFolder}/configs"
randFolder="${generalConfFolder}/rand"
mkdir -p $configFolder
mkdir -p $randFolder
startConfigFolder="${generalConfFolder}/configs"
startRandFolder="${generalConfFolder}/rand"

#masses2p1_light=($ml)
#masses2p1_strange=($ms)
#masses3=()

masses2p1_light=()
masses2p1_strange=()
masses3=(1)


nsArray=(64)
ntArray=(12 24)
beta=7.825
maxCG=20000
newRand=0
seed=0
loadConf=1
confNum=0
writeEvery=50
nodeX=1
nodeY=1
nodeZ=1
nodeT=1
numUpdate=50
simFolderName="simThermalization"
noSkipMetro=10

create_simInput_content(){
    printf "latS=$ns\nlatT=$nt\nmassL=$ml\nmassS=$ms\nbeta=$beta\nnodeX=$nodeX\nnodeY=$nodeY\nnodeZ=$nodeZ\nnodeT=$nodeT\n"
    printf "stepSize=$stepSize\nnumStepTraj=$numStepTraj\nnumStepStrangeInt=$numStepStrangeInt\nnumStepGaugeInt=$numStepGaugeInt\n"
    printf "maxCG=$maxCG\nnewRand=$newRand #new=0 and read=1\nstartRandPath=$startRandPath\nrandPath=$randPath\nseed=$seed\n"
    printf "loadConf=$loadConf #(0=identity, 1=random, 2=getconf)\nstartGaugePath=$startGaugePath\ngaugePath=$gaugePath\n"
    printf "confNum=$confNum\nnumUpdate=$numUpdate\nwriteEvery=$writeEvery\nsimFolderName=$simFolderName\nnoSkipMetro=$noSkipMetro"

}
#progressFile="progress_m${ml}.txt"
#touch $progressFile

numStepArray=(50)
numStepStrangeIntArray=(1)
glueFactorArray=(10)

stepSizeArray=(0.02)

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
                startRandPath="$startRandFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"$confNum
                startGaugePath="$startConfigFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"$confNum
                gaugePath="$configFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"
                randPath="$randFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"
                simInputFile="${simInputFolder}/ns_${ns}_nt_${nt}_ml_${ml}_ms_${ms}"
                echo "$(create_simInput_content)" > $simInputFile
                bash $rhmcScriptFile $simInputFile &
            done

            for mIndex in "${!masses2p1_light[@]}"; do
                ml=${masses2p1_light[${mIndex}]}
                ms=${masses2p1_strange[${mIndex}]}
                startRandPath="$startRandFolder/l${ns}${nt}f21b${beta}ml${ml}ms${ms}_"$confNum
                startGaugePath="$startConfigFolder/l${ns}${nt}f21b${beta}ml${ml}ms${ms}_"$confNum
                gaugePath="$configFolder/l${ns}${nt}f21b${beta}ml${ml}ms${ms}_"
                randPath="$randFolder/l${ns}${nt}f21b${beta}ml${ml}ms${ms}_"
                simInputFile="${simInputFolder}/ns_${ns}_nt_${nt}_ml_${ml}_ms_${ms}"
                echo "$(create_simInput_content)" > $simInputFile
                bash $rhmcScriptFile $simInputFile &
            done
        done
    done
done
wait
