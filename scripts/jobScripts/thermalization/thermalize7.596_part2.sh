#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --partition=volta_compute --qos=regular
#SBATCH --job-name=therm7596_part2
#SBATCH --output=./slurmOutputs/thermalization/beta7596/%x_%A_%a.out
#SBATCH --error=./slurmOutputs/thermalization/beta7596/%x_%A_%a.err
#SBATCH --mail-user=abdelhamid.ettahri@stud.tu-darmstadt.de --mail-type=ALL
#SBATCH --exclude=v16
#SBATCH --array=0-3

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


create_simInput_content(){
    printf "latS=$ns\nlatT=$nt\nmassL=$ml\nmassS=$ms\nbeta=$beta\nnodeX=$nodeX\nnodeY=$nodeY\nnodeZ=$nodeZ\nnodeT=$nodeT\n"
    printf "stepSize=$stepSize\nnumStepTraj=$numStepTraj\nnumStepStrangeInt=$numStepStrangeInt\nnumStepGaugeInt=$numStepGaugeInt\n"
    printf "maxCG=$maxCG\nnewRand=$newRand #new=0 and read=1\nstartRandPath=$startRandPath\nrandPath=$randPath\nseed=$seed\n"
    printf "loadConf=$loadConf #(0=identity, 1=random, 2=getconf)\nstartGaugePath=$startGaugePath\ngaugePath=$gaugePath\n"
    printf "confNum=$confNum\nnumUpdate=$numUpdate\nwriteEvery=$writeEvery\nsimFolderName=$simFolderName\nnoSkipMetro=$noSkipMetro"

}

masses2p1_light=()
masses2p1_strange=()

beta=7.596
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

numStepTraj=50
numStepStrangeInt=1
numStepGaugeInt=10
stepSize=0.02

masses3=(0.5 0.05)
#nsArray=(56)
ns=56
ntArray=(10 20)

declare -a COMBOS=()
                
for nt in "${ntArray[@]}"; do
    for masses in ${masses3[@]}; do
        COMBOS+=("$nt $masses")    
    done
done

read -r nt m <<< "${COMBOS[$SLURM_ARRAY_TASK_ID]}"

ml=$m
ms=$m
        
startRandPath="$startRandFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"$confNum
startGaugePath="$startConfigFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"$confNum
gaugePath="$configFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"
randPath="$randFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"
simInputFile="${simInputFolder}/ns_${ns}_nt_${nt}_ml_${ml}_ms_${ms}"
echo "$(create_simInput_content)" > $simInputFile
bash $rhmcScriptFile $simInputFile 