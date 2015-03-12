#!/bin/bash

T="$(date +%s)"
prep=$T

showhelp="FALSE"
country=""
ocr=""

while getopts "hc:f:" opt; do
	case "${opt}" in
	    h)   
	    	showhelp="TRUE"     
            echo " "
            echo "	options:"
            echo "		-h 		show help"
            echo "		-c [country] 	specify the country to run the script for [required]"
            echo "		-f [folder]	ocr output folder containing text for preprocessing [required]"         
            echo " "
			;;

	    c) country=${OPTARG} ;;

		f) ocr=${OPTARG} ;;

	    *) echo "  Unexpected option ${opt}"; exit ;;
  	esac
done

if [[ $showhelp == "TRUE" ]]; then
	exit 0
fi

base=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cbase="$base"/"$country"

if [[ $country == "" || $ocr == "" || ! -d "$cbase"/ocr/"$ocr" ]]; then
	echo "	An existing ocr output folder must be specified"
	exit 1
fi

mkdir -p "$cbase"/prep/"$ocr"_"$prep"

info="$cbase"/prep/"$ocr"_"$prep"/info.txt
touch $info
echo Date: $(date +"%Y-%m-%d") > $info


types=$(find "$cbase"/ocr/"$ocr"/* -type d)


for atype in $types; do
	atype="${atype##*/}"

	mkdir -p "$cbase"/prep/"$ocr"_"$prep"/"$atype"

	# run in parallel
	# equivalent to: for file in "$cbase"/ocr/"$ocr"/"$atype"/*; do

	parallel -q python "$base"/prep.py "$cbase" "$ocr" "$prep" "$atype" {} ::: "$cbase"/ocr/"$ocr"/"$atype"/*


done

echo 'prep : done'

T="$(($(date +%s)-T))"
runtime="Runtime: $((T/60)):$((T%60))"
echo $runtime >> $info
echo "	"$runtime
