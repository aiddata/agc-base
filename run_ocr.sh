#!/bin/bash

T="$(date +%s)"

showhelp="FALSE"
country=""
short=""

while getopts "shc:" opt; do
	case "${opt}" in
	    h)   
	    	showhelp="TRUE"     
            echo " "
            echo "	options:"
            echo "		-h 		show help"
            echo "		-c [country] 	specify the country to run the script for [required]"
            echo "		-s 		use input_short documents"         
            echo " "
			;;

	    c) country=${OPTARG} ;;

		s) short="_short" ;;

	    *) echo "  Unexpected option ${opt}"; exit ;;
  	esac
done

if [[ $showhelp == "TRUE" ]]; then
	exit 0
fi

base=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cbase="$base"/"$country"

if [[ $country == "" || ! -d "$cbase" || ! -d "$cbase"/inputs ]]; then 
	echo "  A valid country with input documents is required."
	exit 1
fi

tesseractrc=/home/usery/agc/.tesseractrc


mkdir -p "$cbase"/ocr/output"$short"_"$T"
info="$cbase"/ocr/output"$short"_"$T"/info.txt
touch $info
echo Date: $(date +"%Y-%m-%d") >> $info

types=$(find "$cbase"/inputs/input"$short"/* -type d)

for atype in $types; do
	atype="${atype##*/}"

	mkdir -p "$cbase"/ocr/output"$short"_"$T"/"$atype"

	# run in parallel
	# equivalent to: for file in "$cbase"/inputs/input"$short"/"$atype"/*; do
	parallel -q bash "$base"/file_ocr.sh "$cbase" "$atype" "$short" "$T" {} ::: "$cbase"/inputs/input"$short"/"$atype"/*

done

echo 'run_ocr : done'

T="$(($(date +%s)-T))"
runtime="Runtime: $((T/60)):$((T%60))"
echo $runtime >> $info
echo "	"$runtime
