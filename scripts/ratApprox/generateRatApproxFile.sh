#!/bin/bash

get_precond_mass() {
    mass=$1
    awk -v m="$mass" 'BEGIN{printf "%.6f\n", sqrt(5 / (sqrt((5+m*m) / (m*m)) - 1))}'
}

m=$1
M=$2
degFA=$3
degMD=$4
precision=$5
eigenvalueLength=$6

if awk -v m="$m" -v M="$M" 'BEGIN { exit ((m + 0) == (M + 0) ? 0 : 1) }'; then
    precM=$(get_precond_mass $m)
    y1=3; y2=0; y3=3; y4=-3
else
    precM=$M
    y1=3; y2=0; y3=2; y4=-2
fi

m1=0
m2=$precM
m3=$precM
m4=$m
lowerlimit1=$(awk "BEGIN{print $precM * $precM* 0.95}")
upperlimit1=$(awk "BEGIN{print $precM * $precM + $eigenvalueLength}")
lowerlimit2=$(awk "BEGIN{print ($m*$m)* 0.95}")
upperlimit2=$(awk "BEGIN{print ($m*$m)+$eigenvalueLength}")

str1="2\n\n${y1}\n${y2}\n${m1}\n${m2}\n${degFA}\n${degMD}\n${lowerlimit1}\n${upperlimit1}\n${precision}"
str2="\n\n${y3}\n${y4}\n${m3}\n${m4}\n${degFA}\n${degMD}\n${lowerlimit2}\n${upperlimit2}\n${precision}" 
printf ${str1}${str2}

