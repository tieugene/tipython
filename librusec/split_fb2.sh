#!/bin/sh
# tool to split zipped fb2 into header and images.
# Usage: split_fb2.sh <librusec_dir> <headers_dir> <images_dir>
# TODO:
# * err handling
# * xmllint
#TEST="fb2-000024-030559.zip"	# 22807 files - 159'24" (2.38 fps)
#TEST="fb2-203897-204340.zip"	# 293 files - 2'45" (1.77 fps)

INDIR="/mnt/shares/ftp/pub/_Lib.rus.ec - Официальная/lib.rus.ec"
HDRD="/mnt/shares/tmp/librusec/hdr"
IMGD="/mnt/shares/tmp/librusec/img"

for j in `cat librusec.lst`
do
    INFILE=$INDIR/$j
    echo "$j..."
    for i in `zipinfo -1 "$INFILE"`
    do
        #echo $i
        FILENAME=`basename $i .fb2`
        FULLNAME=`printf '%06d' $FILENAME`
        DIRNAME=`echo $FULLNAME | cut -c1-3`
        OUTHDIR=$HDRD/$DIRNAME
        OUTIDIR=$IMGD/$DIRNAME
        if [ ! -d "$OUTHDIR" ]; then mkdir $OUTHDIR; fi
        if [ ! -d "$OUTIDIR" ]; then mkdir $OUTIDIR; fi
        unzip -q -c "$INFILE" $i | ./split_fb2.py $OUTIDIR/$FULLNAME | dos2unix > $OUTHDIR/$FULLNAME.xml
    done
done
