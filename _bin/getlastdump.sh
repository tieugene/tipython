#!/bin/sh
# test to get last lansite backup
BASE="/mnt/shares/backup/lansite/"
# 1. year
Y=`ls -1 $BASE | sort | tail -n 1`
# 2. mon
M=`ls -1 $BASE/$Y | sort | tail -n 1`
# 3. day
D=`ls -1 $BASE/$Y/$M | sort | tail -n 1`
# 4. dump
F="$BASE/$Y/$M/$D/`ls -1 $BASE/$Y/$M/$D | sort | tail -n 1`"
echo "$F"
