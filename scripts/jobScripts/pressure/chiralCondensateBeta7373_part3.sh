#!/bin/bash
#SBATCH --time=18:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --partition=volta_compute --qos=regular
#SBATCH --job-name=presPart3
#SBATCH --output=./slurmOutputs/pressure/slurmPressure7373/%x_%A_%a.out
#SBATCH --error=./slurmOutputs/pressure/slurmPressure7373/%x_%A_%a.err
#SBATCH --mail-user=abdelhamid.ettahri@stud.tu-darmstadt.de --mail-type=ALL
#SBATCH --exclude=v16
#SBATCH --array=0-38%16
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

masses3File="$mainPath/parameter/masses3part2.param"
masses3FileSmall="$mainPath/parameter/masses3missing.param"

#masses2p1_light=($ml)
#masses2p1_strange=($ms)
#masses3=()

#masses2p1_light=()
#masses2p1_strange=()
#masses3=(1)

mapfile -t masses3 < <(awk '{print $1}' "$masses3File")
mapfile -t masses3Small < <(awk '{print $1}' "$masses3FileSmall")



maxCG=20000

newRand=1
loadConf=2
confNum=200
writeEvery=50
nodeX=1
nodeY=1
nodeZ=1
nodeT=1
numUpdate=100
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

numStepTraj=19
stepSize=0.053
numStepGaugeInt=2
numStepStrangeInt=10

beta=7.373
ns=40
ntArray=(8)

declare -a COMBOS=()
COMBOS+=("1 8 774 5")
COMBOS+=("1 8 774 6")
COMBOS+=("1 8 774 7")
for mIndex in "${!masses3[@]}"; do
    COMBOS+=("1 8 19210 $mIndex")    
done
seeds=(0 2002 774 19210)

for seed in ${seeds[@]}; do
    for mIndex in "${!masses3Small[@]}"; do
        COMBOS+=("2 8 $seed $mIndex")    
    done
done

read -r loop nt seed mIndex <<< "${COMBOS[$SLURM_ARRAY_TASK_ID]}"

if [ $loop -eq 1 ]; then
    ml=${masses3[$mIndex]}
    ms=${masses3[$mIndex]}
else
    ml=${masses3Small[$mIndex]}
    ms=${masses3Small[$mIndex]}
fi

simFolderName="simPressureSeed${seed}"
startRandPath="$startRandFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_seed${seed}_"$confNum
startGaugePath="$startConfigFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_seed${seed}_"$confNum

gaugePath="$configFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_seed${seed}_"
randPath="$randFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_seed${seed}_"
simInputFile="${simInputFolder}/ns_${ns}_nt_${nt}_ml_${ml}_ms_${ms}_seed_${seed}_"
create_simInput_content > "$simInputFile"
bash $rhmcScriptFile $simInputFile 




