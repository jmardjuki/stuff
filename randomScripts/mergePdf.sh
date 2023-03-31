#!/bin/bash
###############################################
# Merge PDF documents within current directory
###############################################
MERGERAPP=pdfunite
OUTTEXT=out.pdf

# TODO: Follow the readarray way to deal with spaces
# https://unix.stackexchange.com/questions/9496/looping-through-files-with-spaces-in-the-names
for FILE in $(ls | grep .pdf)
do
	if test -f "$FILE"; then
	    LISTFILES="$LISTFILES $FILE"
	fi
done

echo $LISTFILES
$MERGERAPP $LISTFILES $OUTTEXT
	

