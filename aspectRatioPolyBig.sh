#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:2
#SBATCH --partition=volta_compute --qos=long
#SBATCH --job-name=aspRatioBig
#SBATCH --output=./slurmOutputs/aspectRatioAnalysis/%x_%A_%a.out
#SBATCH --error=./slurmOutputs/aspectRatioAnalysis/%x_%A_%a.err
#SBATCH --mail-user=abdelhamid.ettahri@stud.tu-darmstadt.de --mail-type=ALL
#SBATCH --exclude=v16
#SBATCH --array=0-11


#mainPath="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
mainPath="/work/home/aettahri/simQcd/data" 
generalConfFolder="/work/conf/aettahri"
rhmcScriptFile1Gpu="${mainPath}/rhmc.sh"
rhmcScriptFile2Gpu="${mainPath}/rhmc2Gpu.sh"
rhmcScriptFile=$rhmcScriptFile2Gpu
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


create_simInput_content(){
    printf "latS=$ns\nlatT=$nt\nmassL=$ml\nmassS=$ms\nbeta=$beta\nnodeX=$nodeX\nnodeY=$nodeY\nnodeZ=$nodeZ\nnodeT=$nodeT\n"
    printf "stepSize=$stepSize\nnumStepTraj=$numStepTraj\nnumStepStrangeInt=$numStepStrangeInt\nnumStepGaugeInt=$numStepGaugeInt\n"
    printf "maxCG=$maxCG\nnewRand=$newRand #new=0 and read=1\nstartRandPath=$startRandPath\nrandPath=$randPath\nseed=$seed\n"
    printf "loadConf=$loadConf #(0=identity, 1=random, 2=getconf)\nstartGaugePath=$startGaugePath\ngaugePath=$gaugePath\n"
    printf "confNum=$confNum\nnumUpdate=$numUpdate\nwriteEvery=$writeEvery\nsimFolderName=$simFolderName\nnoSkipMetro=$noSkipMetro"

}

maxCG=20000
writeEvery=100
nodeX=1
nodeY=1
nodeZ=2
nodeT=1
beta=7.373
newRand=0
simFolderName="aspectRatioAnalysis"
seed=0
numStepTraj=19
stepSize=0.053
numStepGaugeInt=2
numStepStrangeInt=10
numUpdate=300
confNum=0


declare -a COMBOS=()
#COMBOS=("16 8" "24 8" "32 8" "16 16" "24 16")
#COMBOS=("16 8" "16 16")
lattices=("24 16" "24 8" "32 16" "32 8")
masses=("0.35 0.4" "0.25 0.3" "0.15 0.2")

for lattice in "${lattices[@]}"; do
    for massBoth in "${masses[@]}"; do
        read -r ns nt <<< "$lattice"
        
        read -r mass startMass <<< "$massBoth"
        COMBOS+=("$ns $nt $mass $startMass")
    done
done

read -r ns nt mass startMass<<< "${COMBOS[$SLURM_ARRAY_TASK_ID]}"
    

#for mIndex in "${!masses3[@]}"; do

    ml=$mass
    ms=$mass
    startRandPath="$startRandFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}" #doesnt matter 

                                      
    noSkipMetro=10
    loadConf=2
    mlPrev=$startMass
    msPrev=$startMass
    startGaugePath="$startConfigFolder/l${ns}${nt}f3b${beta}ml${mlPrev}ms${msPrev}_"$numUpdate
    

    gaugePath="$configFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"
    randPath="$randFolder/l${ns}${nt}f3b${beta}ml${ml}ms${ms}_"
    simInputFile="${simInputFolder}/ns_${ns}_nt_${nt}_ml_${ml}_ms_${ms}_"
    create_simInput_content > "$simInputFile"
    bash $rhmcScriptFile $simInputFile 

#done



