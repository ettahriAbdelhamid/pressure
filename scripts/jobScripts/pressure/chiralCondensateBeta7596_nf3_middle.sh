#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --partition=volta_compute --qos=long
#SBATCH --job-name=slurmPressure7596
#SBATCH --output=./slurmPressure7596/%x_%A_%a.out
#SBATCH --error=./slurmPressure7596/%x_%A_%a.err
#SBATCH --mail-user=abdelhamid.ettahri@stud.tu-darmstadt.de --mail-type=ALL
#SBATCH --exclude=v16
#SBATCH --array=0-7
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

masses3File="$mainPath/parameter/masses3.param"

#masses2p1_light=($ml)
#masses2p1_strange=($ms)
#masses3=()

#masses2p1_light=()
#masses2p1_strange=()
#masses3=(1)

mapfile -t masses3 < <(awk '{print $1}' "$masses3File")



maxCG=20000

loadConf=1
confNum=0
writeEvery=50
nodeX=1
nodeY=1
nodeZ=1
nodeT=1
numUpdate=200
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

numStepTraj=19
stepSize=0.053
numStepGaugeInt=2
numStepStrangeInt=10

beta=7.596
ns=56
ntArray=(20 10)
seeds=(0 2002 774 19210)

declare -a COMBOS=()
                
for nt in "${ntArray[@]}"; do
    for seed in ${seeds[@]}; do
        COMBOS+=("$nt $seed")    
    done
done

read -r nt seed <<< "${COMBOS[$SLURM_ARRAY_TASK_ID]}"



for mIndex in "${!masses3[@]}"; do

    ml=${masses3[$mIndex]}
    ms=${masses3[$mIndex]}

    newRand=0
    simFolderName="simPressureSeed${seed}"
    startRandPath="$startRandFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"$confNum #doesnt matter 


    if [ "$mIndex" -eq 0 ]; then
        startGaugePath="$startConfigFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_50"
    else                                   
        mlPrev=${masses3[(($mIndex-1))]}
        msPrev=${masses3[(($mIndex-1))]}
        startGaugePath="$startConfigFolder/l${ns}${nt}f3b${beta}ml${mlPrev}ms${msPrev}_seed${seed}_"$confNum
    fi


    gaugePath="$configFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_seed${seed}_"
    randPath="$randFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_seed${seed}_"
    simInputFile="${simInputFolder}/ns_${ns}_nt_${nt}_ml_${ml}_ms_${ms}_seed_${seed}_"
    create_simInput_content > "$simInputFile"
    bash $rhmcScriptFile $simInputFile 

done



