#!/bin/sh
# Validate fb2s
# @param: $1:str - src folder
# Result: 64 arch, 266100 files, 18 ~file/s (=> ~4h for all)

ZC=0
FC=0
BC=0

for z in `ls $1`
do
    echo $z
    ZC=$[$ZC +1]
    for f in `zipinfo -1 $1/$z`
    do
        FC=$[$FC +1]
        nice unzip -c -q $1/$z $f | nice xmllint --nonet --noout - 2>/dev/null || (echo $z $f >&2; BC=$[$BC +1])
    done
done
echo "Zips: $ZC, Files: $FC, Bad: $BC"
