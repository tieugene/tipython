#!/bin/sh
# tool to extract headers from ziped fb2s.
# Usage: extract_headers-2.sh <librusec dir> <output dir>
# Result (~4 file/s) => ~19h for all;
INDIR="/mnt/shares/ftp/pub/_Lib.rus.ec - Официальная/lib.rus.ec"
#TEST="fb2-000024-030559.zip"	# 22807 files
#TEST="fb2-203897-204340.zip"	# 293 files
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
    unzip -q -c "$INFILE" $i | sed -e '/<body/,/<\/body>/d' | dos2unix > $OUTDIR/$FULLNAME.xml
done
