calcTimeDiff(){
    local startTime="$1"
    local endTime="$2"
    startTime=$(date -d "$startTime" +%s) #convert in seconds since 1Jan1970
    endTime=$(date -d "$endTime" +%s)

    
    diff=$(echo "$endTime - $startTime" | bc)
    echo "$diff"
    
}
simFolder="../../simulations/simOptimizationThermalized/"

regexMl="beta_.*ml_(.*)_ms"
regexMs="beta_.*ml_.*_ms_(.*)_opti"
regexParameter="opti_(.*)_(.*)_(.*)"
regexEndTimeAndAcceptance="# \[(.*)\] INFO: Run has ended and took .* acceptance = (.*)"
regexStartTime="\[(.*)\] INFO: Running SIMULATeQCD"

dataPath="./dataRaw/"
mkdir -p $dataPath
numUpdates=20


#get lattices
simFolderPath=($simFolder*)
latticeDim=()
for lattice in ${simFolderPath[@]}; do
    latticeDim+=($(basename $lattice))
done

for latDim in ${latticeDim[@]}; do
    echo "Lattice Dimension: ${latDim}"

    beta=7.373


    timeAcceptanceFile=${dataPath}"/time_acceptance_${latDim}.csv"
    init=0
    massfolderPath=($simFolder${latDim}/*)
    massfolders=()
    for massPath in ${massfolderPath[@]}; do
        massfolders+=($(basename $massPath))
    done

    
    degenerateMasses=()
    for massFol in ${massfolders[@]}; do
        if [[ $massFol =~ $regexMl ]]; then
            degenerateMasses+=(${BASH_REMATCH[1]})
        fi
    done

    declare -A massesTmp

    for mass in "${degenerateMasses[@]}"; do massesTmp["$mass"]=1; done
    masses=${!massesTmp[@]}
    


    for mass in ${masses[@]}; do
        if [ $init -eq 0 ]; then 
            printf "ml" > "$timeAcceptanceFile"

            no_md_array=()
            no_step_sf_array=()
            no_sw_array=()

            for massfolder in "$simFolder${latDim}/beta_${beta}_ml_$mass"*; do

                name=$(basename $massfolder)
                if [[ $name =~ $regexParameter ]]; then
                    no_md_array+=(${BASH_REMATCH[1]})
                    no_step_sf_array+=(${BASH_REMATCH[2]})
                    no_sw_array+=(${BASH_REMATCH[3]})
                
                fi
            done

            for jndex in ${!no_md_array[@]}; do
                printf ",time_${no_md_array[$jndex]}_${no_step_sf_array[$jndex]}_${no_sw_array[$jndex]},acceptance_${no_md_array[$jndex]}_${no_step_sf_array[$jndex]}_${no_sw_array[$jndex]},ratio_${no_md_array[$jndex]}_${no_step_sf_array[$jndex]}_${no_sw_array[$jndex]}" >> "$timeAcceptanceFile"
            done
            echo "" >> "$timeAcceptanceFile"
            init=1
        fi

        foldersTmp=$(printf '%s\n' "$simFolder${latDim}/beta_${beta}_ml_${mass}"* | head -n 1)
        if [[ $foldersTmp =~ $regexMs ]]; then
            ms=${BASH_REMATCH[1]}
        fi
        echo "Masses: "$mass", "$ms
        
        ml=$mass
        printf "$ml" >> $timeAcceptanceFile
        for jndex in ${!no_md_array[@]}; do
            no_md=${no_md_array[$jndex]}
            no_sw=${no_sw_array[$jndex]}
            no_step_sf=${no_step_sf_array[$jndex]}
            echo "${no_md_array[$jndex]}_${no_step_sf_array[$jndex]}_${no_sw_array[$jndex]}"
            
            logFile="$simFolder${latDim}/beta_${beta}_ml_${mass}_ms_${ms}_opti_${no_md}_${no_step_sf}_${no_sw}/std/doc/log.log"
            echo "Processing Log File ${logFile}"
            if [ ! -f $logFile ]; then
                echo "actually no"
                printf ",,," >> $timeAcceptanceFile
                continue
            fi
            flag=0
            while  IFS="" read -r p || [ -n "$p" ]; do

                
                if [[ $p =~ $regexStartTime ]]; then
                    startTime=${BASH_REMATCH[1]}
                fi
            
                if [[ $p =~ $regexEndTimeAndAcceptance ]]; then
                flag=1
                    endTime=${BASH_REMATCH[1]}
                    acceptance=${BASH_REMATCH[2]}
                    acceptance=$(bc -l <<< "($acceptance * 20 - 4) / 16")
                    totalTime=$(calcTimeDiff "$startTime" "$endTime")
                    ratio=$(LC_NUMERIC=C printf "%.4f" $(LC_NUMERIC=C echo "$numUpdates * 60 * $acceptance / $totalTime" | bc -l)) #60 to go from seconds to min #Lc numeric stuff to turn comma to point
                   
                    printf ",${totalTime},${acceptance},${ratio}" >> $timeAcceptanceFile
                    echo ",${totalTime},${acceptance},${ratio}"
                fi

            done < $logFile 
            if [ $flag -eq 0 ]; then
                echo "actually no"
                printf ",,," >> $timeAcceptanceFile
            fi
        done
        echo "" >> $timeAcceptanceFile
    done
done