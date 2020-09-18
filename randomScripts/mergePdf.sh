#!/bin/bash
###############################################
# Merge PDF documents within current directory
###############################################
MERGERAPP=pdfunite
OUTTEXT=out.pdf

for FILE in $(ls | grep .pdf)
do
	if test -f "$FILE"; then
	    LISTFILES="$LISTFILES $FILE"
	fi
done

echo $LISTFILES
$MERGERAPP $LISTFILES $OUTTEXT
	

