#!/bin/sh
# tool to check ziped fb2s as xml.
# Usage: chkxml.sh <librusec dir> <output dir>
# Result (fb2-000024-030559.zip, 1651MB, 22807 files) - 10k/43' (~4 file/s) => ~19h for all;
INDIR="/mnt/shares/ftp/pub/_Lib.rus.ec - Официальная/lib.rus.ec"
TEST="fb2-000024-030559.zip"	# 22807 files
#TEST="fb2-203897-204340.zip"	# 293 files - 22"
OUTD="/mnt/shares/tmp/librusec"
INFILE=$INDIR/$TEST
echo "Processing $TEST"
for i in `zipinfo -1 "$INFILE"`
do
    echo $i
    unzip -q "$INFILE" $i
    xmllint --nonet --noout $i 2>/dev/null && rm -f $i || (FILENAME=`basename $i .fb2`; FULLNAME=`printf '%06d' $FILENAME`; OUTDIR=$OUTD/`echo $FULLNAME | cut -c1-3`; if [ ! -d "$OUTDIR" ]; then mkdir $OUTDIR; fi; mv -f $i $OUTDIR/; echo "err")
done
