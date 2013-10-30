#!/bin/sh
# tool to extract headers from ziped fb2s.
# Usage: extract_headers.sh <librusec dir> <output dir>
INDIR="/mnt/shares/ftp/pub/_Lib.rus.ec - Официальная/lib.rus.ec"
TEST="fb2-000024-030559.zip"
OUTD="/mnt/shares/tmp/librusec"
INFILE=$INDIR/$TEST
echo "Processing $TEST"
for i in `zipinfo -1 "$INFILE"`
do
    FILENAME=`basename $i .fb2`
    FULLNAME=`printf '%06d' $FILENAME`
    DIR=`echo $FULLNAME | cut -c1-3`
    OUTDIR=$OUTD/$DIR
    if [ ! -d "$OUTDIR" ]; then mkdir $OUTDIR; fi
    unzip "$INFILE" $i
    echo $i
    cat $i | dos2unix | xmlindent -i0 | ./extract_header.py > $OUTDIR/$FILENAME.xml
    rm -f $i
done
