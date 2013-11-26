#!/bin/sh

# make list of all files in all zips
# for i in `ls src`; do for j in `zipinfo -1 src/$i`; do echo "$i $j"; done; done

# convert prev into 6-decimal list
# (for i in `zcat librusec.txt.gz | gawk '{print $2}'`; do printf "%06d\n" "`basename $i .fb2`"; done)>ziplist.lst

# make same list of xmls:
