#!/bin/sh
# tool to check ziped fb2s as xml.
# Usage: chkxml.sh <librusec dir>
# Result (fb2-000024-030559.zip, 1651MB, 22807 files) - 10k/43' (~4 file/s) => ~19h for all;
INDIR="/mnt/shares/ftp/pub/_Lib.rus.ec - Официальная/lib.rus.ec"
TEST="fb2-000024-030559.zip"	# 22807 files (92'30")
#TEST="fb2-203897-204340.zip"	# 293 files - 18" (16 files/s)
INFILE=$INDIR/$TEST
echo "Processing $TEST"
for i in `zipinfo -1 "$INFILE"`
do
    #echo $i
    unzip -q -c "$INFILE" $i | xmllint --nonet --noout - 2>/dev/null || echo $i >&2
done
