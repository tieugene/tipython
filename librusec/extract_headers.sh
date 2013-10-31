#!/bin/sh
# tool to extract headers from ziped fb2s.
# Usage: extract_headers.sh <librusec dir> <output dir>
# Result (fb2-000024-030559.zip, 1651MB, 22807 files) - 10k/43' (~4 file/s) => ~19h for all;
# test: xmllint <file> || echo "Error: <file>"
# TODO: xmlindent stops on error
INDIR="/mnt/shares/ftp/pub/_Lib.rus.ec - Официальная/lib.rus.ec"
TEST="fb2-000024-030559.zip"
# 293 files - 1'52"
#TEST="fb2-203897-204340.zip"
OUTD="/mnt/shares/tmp/librusec"
INFILE=$INDIR/$TEST
echo "Processing $TEST"
for i in `zipinfo -1 "$INFILE"`
do
    echo $i
    FILENAME=`basename $i .fb2`
    FULLNAME=`printf '%06d' $FILENAME`
    DIR=`echo $FULLNAME | cut -c1-3`
    OUTDIR=$OUTD/$DIR
    if [ ! -d "$OUTDIR" ]; then mkdir $OUTDIR; fi
    unzip -q -c "$INFILE" $i | dos2unix | XMLLINT_INDENT="" xmllint --recover --nonet --format - 2>/dev/null | ./extract_header.py | xmlindent -i1 > $OUTDIR/$FULLNAME.xml
    # exit
done
