#!/bin/sh
# tool to split zipped fb2 into header and images.
# Usage: split_fb2.sh <librusec_dir> <headers_dir> <images_dir>

INDIR="/mnt/shares/ftp/pub/_Lib.rus.ec - Официальная/lib.rus.ec"
HDRD="/mnt/shares/tmp/librusec/hdr"
IMGD="/mnt/shares/tmp/librusec/img"

for j in `cat librusec.lst`
do
    echo "$j"
    nice ./split_fb2.py "$INDIR/$j" $HDRD $IMGD
done
