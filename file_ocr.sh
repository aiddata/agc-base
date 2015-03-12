#!/bin/bash

cbase=$1
atype=$2
short=$3
T=$4
file=$5

oname=$(basename "$file")
ext="${oname##*.}"

file_array=()

#open zip to use individual files
if [[ $ext == 'zip' ]]; then
	echo 'opening zip'
	zipdir=$(mktemp -d)
	unzip -q "$file" -d "$zipdir"

	file_array="$zipdir"/*

else
	file_array[${#array[@]}]=$file
fi

for infile in $file_array; do

	file_full=$(basename "$infile")

	file_name="${file_full%.*}" # .txt
	file_ext="${file_full##*.}"

	outtxt="$cbase"/ocr/output"$short"_"$T"/"$atype"/"$file_name"_"$file_ext".txt

	echo INFILE: $infile
	echo OUTTXT: $outtxt

	if [[ $file_ext == 'pdf' ]]; then
		echo 'processing pdf doc'

		pdf2txt=$(pdftotext "$infile" -)
		if [[ $( echo "pdf2txt" | tr '\n' ' ' | wc -w ) -lt 100 ]]; then
			tmpdir=$(mktemp -d)
			cd $tmpdir
			pdftk "$infile" burst

			rm $outtxt 2>/dev/null

			for page in *.pdf; do
				echo $page
				tmptif=$(mktemp | sed 's:$:.tif:g')
				tmpocr=$(mktemp -p .)
				rm $tmpocr
				gm convert -density 300 $page $tmptif
				tesseract $tmptif $tmpocr $tesseractrc
				echo ${tmpocr}.txt
				cat ${tmpocr}.txt >> $outtxt
			done
		else
			echo "$pdf2txt" > $outtxt
		fi

	elif [[ $file_ext == 'jpg' ]]; then
		echo 'processing jpg'
		tmpdir=$(mktemp -d)
		cd $tmpdir
		tmptif=$(mktemp)
		gm convert -density 300 "$infile" $tmptif
		tesseract $tmptif out $tesseractrc
		cd - 1>/dev/null
		mv $tmpdir/out.txt $outtxt

	elif [[ $file_ext == 'doc' || $file_ext == 'docx' ]]; then
		echo 'processing word'
		soffice --headless --convert-to txt:Text --outdir "$cbase"/ocr/output"$short"_"$T"/"$atype" $infile
	elif [[ $file_ext == 'xls' || $file_ext == 'xlsx' ]]; then
		echo 'processing spreadsheet'
		soffice --headless --convert-to csv --outdir "$cbase"/ocr/output"$short"_"$T"/"$atype" $infile
	else
		echo 'file type not recognized: '$infile
	fi

done
