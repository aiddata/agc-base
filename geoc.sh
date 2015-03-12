#!/bin/bash

T="$(date +%s)"
geoc=$T

showhelp="FALSE"
country=""
prep=""

while getopts "hc:f:" opt; do
	case "${opt}" in
	    h)   
	    	showhelp="TRUE"     
            echo " "
            echo "	options:"
            echo "		-h 		show help"
            echo "		-c [country] 	specify the country to run the script for [required]"
            echo "		-f [folder]	prep output folder containing strings for geocoding [required]"         
            echo " "
			;;

	    c) country=${OPTARG} ;;

		f) prep=${OPTARG} ;;

	    *) echo "  Unexpected option ${opt}"; exit ;;
  	esac
done

if [[ $showhelp == "TRUE" ]]; then
	exit 0
fi

base=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cbase="$base"/"$country"

if [[ $country == "" || $prep == "" || ! -d "$cbase"/prep/"$prep" ]]; then
	echo "	An existing prep output folder must be specified"
	exit 1
fi

mkdir -p "$cbase"/geoc/"$prep"_"$geoc"
info="$cbase"/geoc/"$prep"_"$geoc"/info.txt
touch $info
echo Date: $(date +"%Y-%m-%d") > $info

geocoded="$cbase"/geoc/"$prep"_"$geoc"/"$prep"_"$geoc"_raw.tsv
if [[ -e $geocoded ]]; then
	rm $geocoded
fi
touch $geocoded

types=$(find "$cbase"/prep/"$prep"/* -type d)

for atype in $types; do
	atype="${atype##*/}"

	parallel -q python "$base"/geoc.py "$cbase" "$country" "$prep" "$geoc" {} ::: "$cbase"/prep/"$prep"/"$atype"/*

done


echo 'geoc : done'

T="$(($(date +%s)-T))"
runtime="Runtime: $((T/60)):$((T%60))"
echo $runtime >> $info
echo "	"$runtime
