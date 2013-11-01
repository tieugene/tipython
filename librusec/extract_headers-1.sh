#!/bin/sh
# tool to extract headers from ziped fb2s.
# Usage: extract_headers.sh <librusec dir> <output dir>
# Result (~4 file/s) => ~19h for all;
INDIR="/mnt/shares/ftp/pub/_Lib.rus.ec - Официальная/lib.rus.ec"
TEST="fb2-000024-030559.zip"	# 22807 files - ~1h 20'
#TEST="fb2-203897-204340.zip"	# 293 files - 1' (4.9 files/s)
OUTD="/mnt/shares/tmp/librusec"
INFILE=$INDIR/$TEST
echo "Processing $TEST"
for i in `zipinfo -1 "$INFILE"`
do
    #echo $i
    FILENAME=`basename $i .fb2`
    FULLNAME=`printf '%06d' $FILENAME`
    OUTDIR=$OUTD/`echo $FULLNAME | cut -c1-3`
    if [ ! -d "$OUTDIR" ]; then mkdir $OUTDIR; fi
    unzip -q -c "$INFILE" $i | dos2unix | ./extract_header-1.py > $OUTDIR/$FULLNAME.xml || echo $i >&2
done
