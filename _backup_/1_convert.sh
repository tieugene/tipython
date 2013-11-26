#!/bin/sh
# tool to clean up headers
# Usage: 1_clean.sh <srcdir> <dstdir>
# Result: 262 fps

IDIR="dst/hdr"
ODIR="utf8/hdr"

for i in `ls $IDIR`
do
    echo "$i"
    if [ ! -d "$ODIR/$i" ]; then mkdir $ODIR/$i; fi
    for j in `ls $IDIR/$i`
    do
        if [ ! -f $ODIR/$i/$j ]
        then
            XMLLINT_INDENT=" " xmllint --format --encode UTF-8 --noblanks --nonet --output $ODIR/$i/$j $IDIR/$i/$j || echo "Err: $j"
        fi
    done
done
